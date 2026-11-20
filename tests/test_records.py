"""Checks on data/evidence_sample.csv: every claim is a record with a source."""

import pytest

from venturelens import records

RECORDS = records.load()


def ids(record):
    return record["id"] or "missing id"


def test_sample_is_not_empty():
    assert RECORDS


@pytest.mark.parametrize("record", RECORDS, ids=ids)
@pytest.mark.parametrize("column", records.REQUIRED)
def test_required_fields_are_filled(record, column):
    assert record[column].strip(), f"{record['id']} has no {column}"


def test_ids_are_unique():
    all_ids = [r["id"] for r in RECORDS]
    duplicates = {i for i in all_ids if all_ids.count(i) > 1}
    assert not duplicates


@pytest.mark.parametrize("record", RECORDS, ids=ids)
def test_id_is_shaped_like_e000(record):
    assert records.ID_PATTERN.match(record["id"])


@pytest.mark.parametrize("record", RECORDS, ids=ids)
def test_has_a_source_url_or_repo_file(record):
    assert record["sources"], f"{record['id']} has no source"
    for source in record["sources"]:
        assert records.is_web_link(source) or (records.REPO_ROOT / source).is_file(), source


@pytest.mark.parametrize("record", RECORDS, ids=ids)
def test_evidence_type_is_in_fixed_list(record):
    assert record["evidence_type"] in records.EVIDENCE_TYPES


@pytest.mark.parametrize("record", RECORDS, ids=ids)
def test_cited_ids_exist_in_sample(record):
    sample_ids = {r["id"] for r in RECORDS}
    assert records.cited_ids(record) <= sample_ids, records.cited_ids(record) - sample_ids


def test_loader_splits_two_sources():
    assert records.split_sources("https://a.example | data/x.csv") == ["https://a.example", "data/x.csv"]


def test_checker_reports_a_bad_record():
    bad = {
        "id": "E-1",
        "finding": "",
        "evidence_type": "rumour",
        "confidence": "Low",
        "limits": "",
        "source_url": "no/such/file.md",
        "licence_url": "CC BY",
        "next_test": "See E-999 and I-001.",
    }
    found = records.problems([bad, dict(bad)])
    assert any("finding is empty" in p for p in found)
    assert any("limits is empty" in p for p in found)
    assert any("not shaped like E-000" in p for p in found)
    assert any("more than once" in p for p in found)
    assert any("not in the fixed list" in p for p in found)
    assert any("neither a web link nor a file" in p for p in found)
    assert any("licence_url 'CC BY' is not a web link" in p for p in found)
    assert any("cites E-999" in p for p in found)
    assert any("cites I-001" in p for p in found)


def test_whole_sample_passes():
    assert records.problems(RECORDS) == []
