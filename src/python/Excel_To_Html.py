from pathlib import Path
import argparse
import pandas as pd
import re
import json
from openpyxl import load_workbook
from urllib.parse import urlparse, urlunparse


ROOT = Path(__file__).resolve().parents[2]
EXCEL_DIRECTORY = ROOT / "src/excel"
OUTPUT_PATH = ROOT / "src/property"
LINKS_FILE = Path(__file__).resolve().parent / "links.json"
PROPERTY_COLUMNS = [
    "Property label",
    "Definition",
    "Property URI",
    "Range",
    "Cardinality",
    "Usage note",
    "Controlled vocabulary (if applicable)"
]


def select_workbook(excel_path=None):
    """Resolve explicit paths from the repository root, or select by mtime."""
    if excel_path is not None:
        workbook = Path(excel_path)
        if not workbook.is_absolute():
            workbook = ROOT / workbook
        workbook = workbook.resolve()

        if not workbook.exists():
            raise ValueError(f"Workbook does not exist: {workbook}")
        if workbook.is_dir():
            raise ValueError(f"Workbook path points to a directory: {workbook}")
        if not workbook.is_file():
            raise ValueError(f"Workbook path is not a regular file: {workbook}")
        return workbook

    candidates = [
        (path, path.stat().st_mtime_ns)
        for path in EXCEL_DIRECTORY.iterdir()
        if path.is_file()
        and path.suffix.lower() == ".xlsx"
        and not path.name.startswith("~$")
    ]
    if not candidates:
        raise ValueError(
            f"No eligible .xlsx workbooks found in {EXCEL_DIRECTORY}. "
            "Use --excel PATH to select a workbook explicitly."
        )

    latest_mtime = max(mtime for _, mtime in candidates)
    latest = [path for path, mtime in candidates if mtime == latest_mtime]
    if len(latest) > 1:
        names = ", ".join(sorted(path.name for path in latest))
        raise ValueError(
            f"Workbooks share the most recent modification timestamp: {names}. "
            "Use --excel PATH to select a workbook explicitly."
        )
    return latest[0].resolve()


def normalize_headers(headers, sheet_name, required_columns):
    """Normalise whitespace only; required headings must occur exactly once."""
    headers = [
        " ".join(header.split()) if isinstance(header, str) else header
        for header in headers
    ]
    errors = []
    for required in required_columns:
        count = headers.count(required)
        if count == 0:
            errors.append(f"Required column {required!r} was not found.")
        elif count > 1:
            errors.append(
                f"Required column {required!r} occurs {count} times after "
                "whitespace normalisation."
            )
    if errors:
        available = "\n".join(f"- {header}" for header in headers)
        raise ValueError(
            f"Error processing {sheet_name}:\n" + "\n".join(errors)
            + f"\nAvailable columns:\n{available}"
        )
    return headers


def read_worksheet(excel_file_path, sheet_name, required_columns):
    # Inspect the raw first row before pandas can rename duplicate headings.
    header_row = pd.read_excel(
        excel_file_path, sheet_name=sheet_name, header=None, nrows=1
    )
    headers = [] if header_row.empty else header_row.iloc[0].tolist()
    normalize_headers(headers, sheet_name, required_columns)

    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    df.columns = normalize_headers(df.columns, sheet_name, required_columns)
    return df


# ========================
# URL HELPERS
# ========================

def extract_urls(text):
    if not isinstance(text, str):
        return []
    return re.findall(r'https?://[^\s\]\),]+', text)


def strip_urls(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r'https?://[^\s\]\),]+', '', text)


def make_clickable(url):
    return f'<a href="{url}">{url}</a>'


def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse((
        "",
        parsed.netloc,
        parsed.path.rstrip("/"),
        "", "", ""
    ))


def select_canonical_urls(urls):
    groups = {}

    for url in urls:
        if not url:
            continue

        base = normalize_url(url)
        groups.setdefault(base, []).append(url)

    final = []

    for variants in groups.values():
        fragments = [u for u in variants if "#" in u]
        if fragments:
            final.append(fragments[0])
        else:
            https = [u for u in variants if u.startswith("https")]
            final.append(https[0] if https else variants[0])

    return final


# ========================
# LABEL → URL MAPPING
# ========================

def resolve_vocab_labels(text, mapping):
    if not isinstance(text, str):
        return []

    return [
        url for label, url in mapping.items()
        if label.lower() in text.lower()
    ]


# ========================
# REQUIREMENT DETECTION (fallback only)
# ========================

def detect_requirement(text):
    if not isinstance(text, str):
        return "MAY"

    t = text.lower()

    if re.search(r"at\s+least", t):
        return "AT_LEAST_1"

    # ✅ tightening this prevents false MUST
    if "must " in t:
        return "MUST"

    return "MAY"


# ========================
# EXCEL URL EXTRACTION
# ========================

def extract_urls_per_property(sheet_name, excel_file_path):
    wb = load_workbook(excel_file_path)
    ws = wb[sheet_name]

    headers = normalize_headers(
        [c.value for c in ws[1]], sheet_name, PROPERTY_COLUMNS
    )
    vocab_idx = headers.index("Controlled vocabulary (if applicable)") + 1
    uri_idx = headers.index("Property URI") + 1

    url_map = {}

    for row_idx in range(2, ws.max_row + 1):
        uri = ws.cell(row=row_idx, column=uri_idx).value
        cell = ws.cell(row=row_idx, column=vocab_idx)

        if not uri:
            continue

        urls = []

        if cell.value:
            urls += extract_urls(str(cell.value))

        if cell.hyperlink:
            urls.append(cell.hyperlink.target)

        url_map[uri] = urls

    return url_map


# ========================
# MERGE MULTI-ROW VOCAB
# ========================

def merge_vocab_rows(df):
    merged = []
    current = None

    for _, row in df.iterrows():
        vocab = row["Controlled vocabulary (if applicable)"]

        is_cont = (
            pd.notna(vocab)
            and all(
                pd.isna(v) or str(v).strip() == ""
                for col, v in row.items()
                if col != "Controlled vocabulary (if applicable)"
            )
        )

        if is_cont and current is not None:
            existing = current["Controlled vocabulary (if applicable)"]
            current["Controlled vocabulary (if applicable)"] = (
                str(existing) + "\n" + str(vocab)
                if pd.notna(existing)
                else str(vocab)
            )
        else:
            if current is not None:
                merged.append(current)
            current = row.copy()

    if current is not None:
        merged.append(current)

    return pd.DataFrame(merged).reindex(columns=df.columns)


# ========================
# TABLE TEXT NORMALIZATION
# ========================

def normalize_table_text(value):
    """
    Convert line breaks in Excel/table cell text to spaces before
    pandas serializes the DataFrame to HTML.

    pandas.to_html() can serialize newline characters in a way that
    results in the literal characters "\\n" appearing in the generated
    HTML. Bikeshed then displays those characters instead of treating
    them as whitespace.

    This handles:
      - Windows line breaks: \\r\\n
      - Unix line breaks: \\n
      - Old Mac line breaks: \\r
      - Literal escaped sequences: \\\\n
    """
    if not isinstance(value, str):
        return value

    return re.sub(r"(?:\r\n|\r|\n|\\n)+", " ", value)


# ========================
# FINAL USAGE NOTE
# ========================

def build_usage_note(row, sheet_name, url_map, links):

    base = row["Usage note"]
    if not isinstance(base, str) or not base.strip():
        base = "N.A."

    vocab = row["Controlled vocabulary (if applicable)"]
    prop = row["Property URI"]

    if not isinstance(vocab, str) or not vocab.strip():
        return base

    key_exact = f"{prop}|{sheet_name}"
    key_lower = f"{prop}|{sheet_name.lower()}"

    prop_key_norm = prop.strip().lower()

    # FINAL FIXED LOOKUP
    vocab_type = (
        links["vocabRequirements"].get(key_exact)
        or links["vocabRequirements"].get(key_lower)
        or next(
            (
                v
                for k, v in links["vocabRequirements"].items()
                if k.split("|")[0].strip().lower() == prop_key_norm
            ),
            None
        )
        or detect_requirement(vocab)
    )

    vocab_text = links["vocabTexts"].get(vocab_type, "")

    # URLs
    text_urls = extract_urls(vocab)
    excel_urls = url_map.get(prop, [])
    mapped_urls = resolve_vocab_labels(
        vocab,
        links["vocabLabelMapping"]
    )

    urls = select_canonical_urls(
        text_urls + excel_urls + mapped_urls
    )

    # Clean vocab text
    mapping_labels = [
        k.lower()
        for k in links["vocabLabelMapping"].keys()
    ]

    clean_lines = []

    for line in strip_urls(vocab).split("\n"):
        l = line.strip()

        if not l:
            continue

        lower = l.lower()

        if any(label in lower for label in mapping_labels):
            continue

        if len(l.split()) <= 6:
            continue

        if not re.search(
            r"\b(is|are|must|should|may|use|used|provides|represents)\b",
            lower
        ):
            continue

        clean_lines.append(l)

    clean_text = "<br>".join(clean_lines)

    parts = []

    if vocab_text:
        parts.append(vocab_text)

    if clean_text:
        parts.append(clean_text)

    if urls:
        parts.append("")
        parts.extend([
            make_clickable(u)
            for u in urls
        ])
        parts.append("")

    vocab_block = "<br>".join(parts)

    return (
        base
        + "<br><br><strong>Controlled vocabulary</strong><br>"
        + vocab_block
    )


# ========================
# MAIN
# ========================

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate HTML property tables from an Excel workbook."
    )
    parser.add_argument(
        "--excel",
        metavar="PATH",
        help=(
            "Workbook path (absolute or relative to the repository root). "
            "Defaults to the most recently modified .xlsx file in src/excel/."
        )
    )
    args = parser.parse_args(argv)

    try:
        excel_file_path = select_workbook(args.excel)
    except (OSError, ValueError) as exc:
        parser.error(f"Cannot select Excel workbook: {exc}")

    mode = "Explicit" if args.excel is not None else "Automatic (most recently modified)"
    print(f"Excel input mode: {mode}")
    print(f"Selected workbook: {excel_file_path}")

    try:
        classes_df = read_worksheet(
            excel_file_path,
            "classes",
            ["sheet_name"]
        )
    except Exception as exc:
        parser.error(
            f"Cannot read workbook {excel_file_path} (worksheet 'classes'): {exc}"
        )

    OUTPUT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        LINKS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        links = json.load(f)

    for _, class_row in classes_df.iterrows():

        sheet_name = class_row["sheet_name"]

        try:
            df = read_worksheet(excel_file_path, sheet_name, PROPERTY_COLUMNS)
        except ValueError as exc:
            parser.error(str(exc))

        df = df[PROPERTY_COLUMNS]

        if df.replace(r"^\s*$", pd.NA, regex=True).dropna(how="all").empty:
            print(f"Skipped {sheet_name}: no properties to document")
            continue

        df = merge_vocab_rows(df)

        url_map = extract_urls_per_property(
            sheet_name,
            excel_file_path
        )

        df["Usage note"] = df.apply(
            lambda r: build_usage_note(
                r,
                sheet_name,
                url_map,
                links
            ),
            axis=1
        )

        df = df.drop(
            columns=[
                "Controlled vocabulary (if applicable)"
            ]
        )

        # ============================================================
        # IMPORTANT:
        # Normalize all table cell text BEFORE pandas generates HTML.
        #
        # This prevents literal "\\n" from appearing in the generated
        # HTML and therefore being displayed by Bikeshed.
        # ============================================================

        df = df.map(normalize_table_text)

        output_file = (
            OUTPUT_PATH
            / f"properties-{sheet_name.lower()}.html"
        )

        df.to_html(
            output_file,
            index=False,
            escape=False
        )

        print(
            f"Generated {output_file}"
        )


if __name__ == "__main__":
    main()
