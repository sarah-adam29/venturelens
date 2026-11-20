"""Load the evidence records and report any record that breaks a rule.

Every claim in this repo is an evidence record with a source. This module
reads data/evidence_sample.csv and checks each record against the rules
below. Run it directly to print any problems:

    uv run python -m venturelens.records
"""

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_CSV = REPO_ROOT / "data" / "evidence_sample.csv"

COLUMNS = [
    "id",
    "question",
    "finding",
    "source_title",
    "source_url",
    "licence_url",
    "source_date",
    "accessed",
    "evidence_type",
    "evidence_note",
    "confidence",
    "limits",
    "next_test",
]

REQUIRED = ["id", "finding", "evidence_type", "confidence", "limits"]

# "company-reported" is kept for Gigaton's own material. Other companies'
# own material is a "third-party company document".
EVIDENCE_TYPES = {
    "public record",
    "company-reported",
    "investor-associated",
    "partner-reported",
    "third-party company document",
    "third-party dataset",
    "third-party benchmark",
    "third-party listing",
    "analyst calculation",
}

ID_PATTERN = re.compile(r"^E-\d{3}$")
# Evidence (E-) and open-question (I-) ids mentioned anywhere inside a record.
CITED_ID = re.compile(r"\b[EI]-\d{3}\b")
SOURCE_SEPARATOR = " | "


def split_sources(value: str) -> list[str]:
    """Split a source_url field into its sources, which are separated by ' | '."""
    return [part.strip() for part in value.split(SOURCE_SEPARATOR) if part.strip()]


def is_web_link(source: str) -> bool:
    return source.startswith(("https://", "http://"))


def load(path: Path = EVIDENCE_CSV) -> list[dict]:
    """Read the evidence CSV. Each record gets a `sources` list as well as the raw columns."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise ValueError(f"{path.name}: expected columns {COLUMNS}, found {reader.fieldnames}")
        records = list(reader)
    for record in records:
        record["sources"] = split_sources(record["source_url"])
    return records


def cited_ids(record: dict) -> set[str]:
    """Ids mentioned in a record's text, other than its own id."""
    text = " ".join(record.get(column, "") for column in COLUMNS if column != "id")
    return set(CITED_ID.findall(text)) - {record.get("id")}


def problems(records: list[dict], repo_root: Path = REPO_ROOT) -> list[str]:
    """Return one line per rule broken. An empty list means every record passes."""
    found = []
    seen = set()
    sample_ids = {record.get("id") for record in records}
    for n, record in enumerate(records, start=1):
        label = record.get("id") or f"row {n}"

        for column in REQUIRED:
            if not record.get(column, "").strip():
                found.append(f"{label}: {column} is empty")

        record_id = record.get("id", "")
        if record_id and not ID_PATTERN.match(record_id):
            found.append(f"{label}: id is not shaped like E-000")
        if record_id in seen:
            found.append(f"{label}: id is used more than once")
        seen.add(record_id)

        if record.get("evidence_type") and record["evidence_type"] not in EVIDENCE_TYPES:
            found.append(f"{label}: evidence type '{record['evidence_type']}' is not in the fixed list")

        sources = record.get("sources", split_sources(record.get("source_url", "")))
        if not sources:
            found.append(f"{label}: no source URL or repo file")
        for source in sources:
            if not is_web_link(source) and not (repo_root / source).is_file():
                found.append(f"{label}: source '{source}' is neither a web link nor a file in this repo")

        licence = record.get("licence_url", "").strip()
        if licence and not is_web_link(licence):
            found.append(f"{label}: licence_url '{licence}' is not a web link")

        for cited in sorted(cited_ids(record) - sample_ids):
            found.append(f"{label}: cites {cited}, which is not in the sample")

    return found


def main() -> int:
    found = problems(load())
    for line in found:
        print(line)
    if not found:
        print("All evidence records pass.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
