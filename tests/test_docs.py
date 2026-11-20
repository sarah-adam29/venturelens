"""Checks that the documents stay tied to the evidence records."""

import re
import subprocess

import pytest

from venturelens import records

DOCS = sorted((records.REPO_ROOT / "docs").glob("*.md"))
CASE_STUDY = records.REPO_ROOT / "docs" / "case-study-gigaton.md"
SAMPLE = records.load()

WEB_LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
SECTION_LINK = re.compile(r"\]\(([^)\s#]*)#([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)

# terms that must not appear in this repo
TERMS = [
    "Divi" + "Gas",
    "Open Access" + " Energy",
    "liqui" + "dation",
    "HS" + "BC",
    "@" + "gmail",
    "[MY" + " DECISION]",
    "[YOUR" + " SUGGESTION]",
    "[UN" + "CERTAIN]",
    "[CH" + "ECK]",
    "post" + "-money",
    "pre" + "-money",
    "pay" + "roll",
    "head" + "count",
    "run" + "way",
]


def repo_files():
    """Every file git tracks, plus untracked files that git does not ignore."""
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=records.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    for name in sorted(set(listed)):
        path = records.REPO_ROOT / name
        if path.is_file():
            yield path


@pytest.mark.parametrize("doc", DOCS, ids=lambda p: p.name)
def test_every_cited_id_exists_in_evidence_csv(doc):
    sample_ids = {r["id"] for r in SAMPLE}
    cited = set(re.findall(r"\bE-\d{3}\b", doc.read_text(encoding="utf-8")))
    assert cited <= sample_ids, cited - sample_ids


def test_case_study_web_links_are_in_evidence_csv():
    csv_links = {source for r in SAMPLE for source in r["sources"] if records.is_web_link(source)}
    csv_links |= {r["licence_url"] for r in SAMPLE if r["licence_url"]}
    links = set(WEB_LINK.findall(CASE_STUDY.read_text(encoding="utf-8")))
    assert links, "case study has no web links"
    assert links <= csv_links, links - csv_links


def anchors(path):
    """Section anchors as GitHub makes them from a page's headings."""
    headings = HEADING.findall(path.read_text(encoding="utf-8"))
    return {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}


@pytest.mark.parametrize("page", [records.REPO_ROOT / "README.md", *DOCS], ids=lambda p: p.name)
def test_section_links_point_to_existing_headings(page):
    broken = []
    for target, anchor in SECTION_LINK.findall(page.read_text(encoding="utf-8")):
        if target.startswith("http"):
            continue
        linked = (page.parent / target).resolve() if target else page
        if linked.parent == CASE_STUDY.parent and anchor not in anchors(linked):
            broken.append(f"{target}#{anchor}")
    assert not broken


@pytest.mark.parametrize("path", list(repo_files()), ids=lambda p: str(p.relative_to(records.REPO_ROOT)))
def test_no_excluded_terms(path):
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    found = [term for term in TERMS if term.lower() in text]
    assert not found
