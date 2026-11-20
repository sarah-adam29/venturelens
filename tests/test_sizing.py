"""Checks on the sizing arithmetic.

The model-history values were recalculated from the private workbooks on
13 November 2026; the package-use and return-test values from the current
workbook on 16 November 2026. They are fixed: if a test fails, fix the code
or the inputs, never the expected value.
"""

import csv
from decimal import Decimal

import pytest

from venturelens import records, sizing

INPUTS = sizing.load_inputs()

# model history: the earlier proxy market and the two company-opportunity models
TAM = Decimal("211764000")
SAM = Decimal("99842400")
FIRST_MODEL = Decimal("1777440")
CORRECTED_MODEL = Decimal("582758.40")

# label, fee per site, TAM, SAM (USD a year)
PACKAGE_CASES = [
    ("Current price, package shared across 2 sites", "33765.24", "85122170.04", "40133364.26"),
    ("Current price, one site", "67530.48", "170244340.08", "80266728.53"),
    ("Price from 1 March 2027, shared across 2 sites", "77500.00", "195377500.00", "92116500.00"),
    ("Price from 1 March 2027, one site", "155000.00", "390755000.00", "184233000.00"),
]

RETURN_MARKET = Decimal("184233000")
SHARE_KEPT = Decimal("0.72946544")
REFERENCE_OWNERSHIP = Decimal("0.1313037792")
SALE_VALUE_FOR_10X = Decimal("1980141025.52")

ROUND = INPUTS["funding_round"]
TEN = INPUTS["return_multiple_high"]
THREE = INPUTS["return_multiple_low"]
AT_10 = INPUTS["sale_multiple_high"]
AT_4 = INPUTS["sale_multiple_low"]
OWNED = sizing.ownership_cases(INPUTS)


def share(value):
    """A share to one hundredth of a percentage point."""
    return value.quantize(Decimal("0.0001"))


def test_tam():
    assert sizing.market_size(INPUTS)["tam"] == TAM


def test_sam():
    assert sizing.market_size(INPUTS)["sam"] == SAM


def test_first_model():
    assert sizing.first_model(INPUTS)["annual_opportunity"] == FIRST_MODEL


def test_corrected_model():
    assert sizing.corrected_model(INPUTS)["annual_opportunity"] == CORRECTED_MODEL


def test_annual_fee_is_listed_price_times_twelve():
    assert sizing.annual_fee(INPUTS) == Decimal("84000")


def test_serviceable_sites():
    assert sizing.serviceable_sites(INPUTS) == Decimal("1188.6")


def test_kilns_add_about_47_percent():
    assert share(sizing.kilns_per_site(INPUTS) - 1) == Decimal("0.4665")


@pytest.mark.parametrize("case", PACKAGE_CASES, ids=lambda c: c[0])
def test_package_use_case(case):
    label, fee, tam, sam = case
    found = {c["label"]: c for c in sizing.package_use_cases(INPUTS)}[label]
    assert sizing.cents(found["fee_per_site"]) == Decimal(fee)
    assert sizing.cents(found["tam"]) == Decimal(tam)
    assert sizing.cents(found["sam"]) == Decimal(sam)


def test_package_cannot_be_shared_across_more_sites_than_it_covers():
    with pytest.raises(ValueError):
        sizing.package_use_cases(dict(INPUTS, package_use_current_2_sites=Decimal(3)))


def test_return_market_is_the_2027_one_site_sam():
    assert sizing.return_market(INPUTS) == RETURN_MARKET


def test_share_kept_after_rounds_b_c_d():
    dilutions = [INPUTS[f"dilution_{r}_median"] for r in sizing.LATER_ROUNDS]
    assert sizing.share_kept(dilutions) == SHARE_KEPT


def test_reference_ownership_at_exit():
    assert OWNED["reference"] == REFERENCE_OWNERSHIP


def test_sale_value_needed_for_10x():
    assert sizing.cents(ROUND * TEN / OWNED["reference"]) == SALE_VALUE_FOR_10X


def test_revenue_for_10x_at_10_and_4_times():
    assert sizing.cents(sizing.revenue_needed(ROUND, TEN, OWNED["reference"], AT_10)) == Decimal("198014102.55")
    assert sizing.cents(sizing.revenue_needed(ROUND, TEN, OWNED["reference"], AT_4)) == Decimal("495035256.38")


def test_revenue_for_3x_at_10_and_4_times():
    assert sizing.cents(sizing.revenue_needed(ROUND, THREE, OWNED["reference"], AT_10)) == Decimal("59404230.77")
    assert sizing.cents(sizing.revenue_needed(ROUND, THREE, OWNED["reference"], AT_4)) == Decimal("148510576.91")


def test_favourable_case():
    revenue = sizing.revenue_needed(ROUND, TEN, OWNED["favourable"], AT_10)
    assert sizing.cents(revenue) == Decimal("149318107.03")
    assert share(sizing.share_of_market(revenue, RETURN_MARKET)) == Decimal("0.8105")


def test_unfavourable_case():
    assert sizing.cents(sizing.revenue_needed(ROUND, TEN, OWNED["unfavourable"], AT_10)) == Decimal("377126347.13")
    assert sizing.cents(sizing.revenue_needed(ROUND, TEN, OWNED["unfavourable"], AT_4)) == Decimal("942815867.83")


def test_two_later_rounds_only():
    revenue = sizing.revenue_needed(ROUND, TEN, OWNED["two_rounds"], AT_10)
    assert sizing.cents(revenue) == Decimal("181974960.25")
    assert share(sizing.share_of_market(revenue, RETURN_MARKET)) == Decimal("0.9877")


def test_serviceable_market_needed_at_30_and_20_percent_share():
    smallest = sizing.revenue_needed(ROUND, TEN, OWNED["reference"], AT_10) / INPUTS["market_share_high"]
    largest = sizing.revenue_needed(ROUND, TEN, OWNED["reference"], AT_4) / INPUTS["market_share_low"]
    assert sizing.cents(smallest) == Decimal("660047008.51")
    assert sizing.cents(largest) == Decimal("2475176281.90")


def test_premium_case_at_15_times():
    revenue = sizing.revenue_needed(ROUND, TEN, OWNED["reference"], INPUTS["sale_multiple_premium"])
    assert sizing.cents(revenue) == Decimal("132009401.70")
    assert share(sizing.share_of_market(revenue, RETURN_MARKET)) == Decimal("0.7165")


@pytest.mark.parametrize("sale_multiple", [AT_4, AT_10])
def test_favourable_needs_less_and_unfavourable_more_than_reference(sale_multiple):
    def needed(case):
        return sizing.revenue_needed(ROUND, TEN, OWNED[case], sale_multiple)

    assert needed("favourable") < needed("reference") < needed("unfavourable")


def test_first_model_path():
    years = sizing.first_model(INPUTS)["years"]
    assert [y["qualified"] for y in years] == [12, 24, 24]
    assert [y["new_live"] for y in years] == [4, 9, 9]
    assert [y["closing"] for y in years] == [Decimal("4"), Decimal("12.8"), Decimal("21.16")]


def test_corrected_model_path():
    years = sizing.corrected_model(INPUTS)["years"]
    assert [y["signed"] for y in years] == [Decimal("3.2")] * 3
    assert [y["new_live"] for y in years] == [Decimal("2.56")] * 3
    assert [y["closing"] for y in years] == [Decimal("2.56"), Decimal("4.864"), Decimal("6.9376")]


@pytest.mark.parametrize("readiness", ["0", "0.5", "0.7", "1"])
@pytest.mark.parametrize("unknown_share", ["0", "0.5", "1"])
def test_sam_is_never_larger_than_tam(readiness, unknown_share):
    inputs = dict(INPUTS, readiness_share=Decimal(readiness), unknown_capacity_share_qualifying=Decimal(unknown_share))
    market = sizing.market_size(inputs)
    assert market["sam"] <= market["tam"]


def read_input_rows():
    with open(sizing.SIZING_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


BASES = {"sourced", "benchmark-informed assumption", "assumption"}
BENCHMARK_TYPES = {"third-party benchmark", "third-party company document"}
EVIDENCE_TYPE = {r["id"]: r["evidence_type"] for r in records.load()}


@pytest.mark.parametrize("row", read_input_rows(), ids=lambda r: r["name"])
def test_input_row_has_evidence_and_basis(row):
    assert row["evidence_id"] in EVIDENCE_TYPE
    assert row["basis"] in BASES
    assert row["note"].strip()


@pytest.mark.parametrize(
    "row",
    [r for r in read_input_rows() if r["basis"] == "benchmark-informed assumption"],
    ids=lambda r: r["name"],
)
def test_benchmark_informed_input_cites_a_benchmark(row):
    assert EVIDENCE_TYPE[row["evidence_id"]] in BENCHMARK_TYPES


def test_benchmark_informed_inputs():
    informed = {r["name"] for r in read_input_rows() if r["basis"] == "benchmark-informed assumption"}
    carta = {f"stake_series_a_{s}" for s in ("median", "p25", "p75")} | {
        f"dilution_{r}_{s}" for r in sizing.LATER_ROUNDS for s in ("median", "p25", "p75")
    }
    package_use = {use for _, _, use in sizing.PACKAGE_CASES}
    assert informed == (
        {"corrected_win_rate", "corrected_retention", "sale_multiple_low", "sale_multiple_premium"}
        | carta
        | package_use
    )


def test_sourced_inputs():
    sourced = {r["name"] for r in read_input_rows() if r["basis"] == "sourced"}
    assert sourced == {
        "operating_sites",
        "sites_at_least_1mtpa",
        "sites_unknown_capacity",
        "physical_kilns",
        "listed_monthly_fee",
        "package_price_current",
        "package_price_from_2027_03_01",
        "package_max_sites",
        "package_max_units",
        "funding_round",
    }
