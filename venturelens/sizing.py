"""Market sizing and the return test.

The original calculations live in private spreadsheets. This module repeats
the same arithmetic in code, reading its inputs from data/sizing_inputs.csv.
Each input row names the evidence record that describes it and gives its
status: "sourced", "benchmark-informed assumption" or "assumption".

Three parts:

- Package-use cases. Total and serviceable markets at a supplier's listed
  package price, current and announced, shared across two sites or used at
  one. Four separate dated cases, not a price range.
- The return test. The annual revenue a funding round would need for a given
  return, under benchmark ownership and sale multiples. Illustrative: the
  inputs are benchmarks and assumptions, not the investors' actual terms or
  targets.
- Model history. The earlier directory-price market and the two
  company-opportunity models, kept to show how the case was challenged. The
  models count new customers only, in one scenario; they are not estimates of
  the company's revenue.

Decimal arithmetic keeps the results exact, so they match the workbooks to
the cent. Run it directly to print the figures:

    uv run python -m venturelens.sizing
"""

import csv
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SIZING_CSV = REPO_ROOT / "data" / "sizing_inputs.csv"

YEARS = 3
MONTHS_PER_YEAR = 12

# label, price input, package-use input
PACKAGE_CASES = [
    ("Current price, package shared across 2 sites", "package_price_current", "package_use_current_2_sites"),
    ("Current price, one site", "package_price_current", "package_use_current_1_site"),
    ("Price from 1 March 2027, shared across 2 sites", "package_price_from_2027_03_01", "package_use_2027_2_sites"),
    ("Price from 1 March 2027, one site", "package_price_from_2027_03_01", "package_use_2027_1_site"),
]

LATER_ROUNDS = ["series_b", "series_c", "series_d"]


def load_inputs(path: Path = SIZING_CSV) -> dict[str, Decimal]:
    """Read the inputs as exact decimals, keyed by name."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["name"]: Decimal(row["value"]) for row in csv.DictReader(f)}


def cents(value: Decimal) -> Decimal:
    """Round to the cent, halves up, as the workbooks display it."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def annual_fee(inputs: dict[str, Decimal]) -> Decimal:
    """The listed monthly price × 12. Using it as this market's fee is an assumption."""
    return inputs["listed_monthly_fee"] * MONTHS_PER_YEAR


def market_size(inputs: dict[str, Decimal]) -> dict[str, Decimal]:
    """Model history: TAM and SAM in USD a year at the earlier directory-price proxy.

    TAM (total addressable market): every operating site × subscriptions per
    site × annual fee.

    SAM (serviceable addressable market): sites known to be at least 1 Mtpa,
    plus an assumed share of sites of unknown size, × an assumed readiness
    share × subscriptions per site × annual fee.
    """
    fee = annual_fee(inputs)
    per_site = inputs["subscriptions_per_site"]

    tam = inputs["operating_sites"] * per_site * fee
    sam = serviceable_sites(inputs) * per_site * fee

    return {"tam": tam, "sam": sam}


def serviceable_sites(inputs: dict[str, Decimal]) -> Decimal:
    """Serviceable site-equivalents: the SAM filters applied to the site counts."""
    size_qualified = (
        inputs["sites_at_least_1mtpa"]
        + inputs["sites_unknown_capacity"] * inputs["unknown_capacity_share_qualifying"]
    )
    return size_qualified * inputs["readiness_share"]


def kilns_per_site(inputs: dict[str, Decimal]) -> Decimal:
    """Physical kilns ÷ operating sites. Physical kilns are not billable units."""
    return inputs["physical_kilns"] / inputs["operating_sites"]


def package_use_cases(inputs: dict[str, Decimal]) -> list[dict]:
    """Fee per site, TAM and SAM for each package-use case.

    Fee per site = package price ÷ sites using the package. A customer with one
    site pays for the whole package. Site counts and filters are held fixed,
    so the cases isolate the effect of price and package use.
    """
    cases = []
    for label, price, use in PACKAGE_CASES:
        sites_using = inputs[use]
        if sites_using > inputs["package_max_sites"]:
            raise ValueError(f"{use}: the package covers at most {inputs['package_max_sites']} sites")
        fee = inputs[price] / sites_using
        cases.append({
            "label": label,
            "fee_per_site": fee,
            "tam": inputs["operating_sites"] * fee,
            "sam": serviceable_sites(inputs) * fee,
        })
    return cases


def return_market(inputs: dict[str, Decimal]) -> Decimal:
    """The serviceable market the return test compares against: the largest case."""
    return max(case["sam"] for case in package_use_cases(inputs))


def share_kept(dilutions: list[Decimal]) -> Decimal:
    """Share of a stake kept after later rounds, each selling the given share."""
    kept = Decimal(1)
    for dilution in dilutions:
        kept *= 1 - dilution
    return kept


def ownership_at_exit(stake: Decimal, dilutions: list[Decimal]) -> Decimal:
    """The round's stake after later rounds."""
    return stake * share_kept(dilutions)


def revenue_needed(
    round_size: Decimal, return_multiple: Decimal, ownership: Decimal, sale_multiple: Decimal
) -> Decimal:
    """Annual revenue at exit for the round to make the given return.

    Revenue needed = round × return multiple ÷ ownership at exit ÷ sale
    multiple. Assumes no debt, no sale costs and no further investment by the
    same investors.
    """
    return round_size * return_multiple / ownership / sale_multiple


def share_of_market(revenue: Decimal, market: Decimal) -> Decimal:
    """Revenue as a share of a market."""
    return revenue / market


def ownership_cases(inputs: dict[str, Decimal]) -> dict[str, Decimal]:
    """Ownership at exit in the reference case and three constructed cases.

    The favourable and unfavourable cases combine separately reported
    quartiles for each round. They are constructed cases, not percentiles of
    ownership at exit.
    """
    def later(stat, rounds=LATER_ROUNDS):
        return [inputs[f"dilution_{r}_{stat}"] for r in rounds]

    return {
        "reference": ownership_at_exit(inputs["stake_series_a_median"], later("median")),
        "favourable": ownership_at_exit(inputs["stake_series_a_p75"], later("p25")),
        "unfavourable": ownership_at_exit(inputs["stake_series_a_p25"], later("p75")),
        "two_rounds": ownership_at_exit(inputs["stake_series_a_median"], later("median", LATER_ROUNDS[:2])),
    }


# Model history. The earlier fee proxy and the two models below are kept to
# show how the case was challenged. The models count new customers only, in
# one scenario. They are not estimates of the company's revenue.


def first_model(inputs: dict[str, Decimal]) -> dict:
    """Model history. Company opportunity, first model: three years of new customers only.

    Each year, sites are qualified from a finite pool, 40% of them go live
    (rounded down to whole sites, and capped by delivery slots), and the
    cohort is carried forward at the retention rate.
    """
    pool = inputs["first_reachable_pool"]
    retention = inputs["first_retention"]
    closing = Decimal(0)
    path = []
    for year in range(1, YEARS + 1):
        qualified = min(inputs[f"first_qualified_year{year}"], pool)
        pool -= qualified
        wins = int(qualified * inputs["first_win_rate"])  # whole sites, rounded down
        new_live = min(Decimal(wins), inputs[f"first_slots_year{year}"])
        closing = closing * retention + new_live
        path.append({"qualified": qualified, "new_live": new_live, "closing": closing})
    return {"years": path, "annual_opportunity": closing * annual_fee(inputs)}


def corrected_model(inputs: dict[str, Decimal]) -> dict:
    """Model history. Company opportunity, corrected model: benchmark-informed assumptions.

    Each year, a fixed number of proposals is made, 40% are signed, 80% of
    those go live within the year (capped by delivery capacity), and the
    cohort is carried forward at the retention rate. Results are expected
    values, so they can be fractional.
    """
    pool = inputs["corrected_engagement_pool"]
    retention = inputs["corrected_retention"]
    closing = Decimal(0)
    path = []
    for _ in range(YEARS):
        proposals = min(inputs["corrected_proposals_per_year"], pool)
        pool -= proposals
        signed = proposals * inputs["corrected_win_rate"]
        new_live = min(signed * inputs["corrected_live_share"], inputs["corrected_capacity"])
        closing = closing * retention + new_live
        path.append({"proposals": proposals, "signed": signed, "new_live": new_live, "closing": closing})
    return {"years": path, "annual_opportunity": closing * annual_fee(inputs)}


def main() -> None:
    inputs = load_inputs()

    print("Package-use cases (USD a year; separate dated cases, not a price range)")
    print(f"  Serviceable site-equivalents: {serviceable_sites(inputs)}")
    for case in package_use_cases(inputs):
        print(f"  {case['label']:<48} fee per site {cents(case['fee_per_site']):>13,}"
              f"  TAM {cents(case['tam']):>17,}  SAM {cents(case['sam']):>17,}")

    round_size = inputs["funding_round"]
    market = return_market(inputs)
    owned = ownership_cases(inputs)
    low, high = inputs["sale_multiple_low"], inputs["sale_multiple_high"]
    ten, three = inputs["return_multiple_high"], inputs["return_multiple_low"]
    reference = owned["reference"]

    def line(label, revenue):
        print(f"  {label:<62} USD {cents(revenue):>17,}  ({share_of_market(revenue, market):.2%} of SAM)")

    print()
    print("Return test (illustrative: benchmarks and assumptions, not the investors' terms or targets)")
    print(f"  Round USD {round_size:,}; compared with SAM USD {cents(market):,}")
    print(f"  Share kept after rounds B, C and D: {share_kept([inputs[f'dilution_{r}_median'] for r in LATER_ROUNDS])}")
    print(f"  Ownership at exit, reference: {reference}")
    print(f"  Sale value needed for 10x: USD {cents(round_size * ten / reference):,}")
    line("Reference, 10x, at 10 times revenue", revenue_needed(round_size, ten, reference, high))
    line("Reference, 10x, at 4 times revenue", revenue_needed(round_size, ten, reference, low))
    line("Reference, 3x, at 10 times revenue", revenue_needed(round_size, three, reference, high))
    line("Reference, 3x, at 4 times revenue", revenue_needed(round_size, three, reference, low))
    line("Favourable constructed case, 10x, at 10 times revenue", revenue_needed(round_size, ten, owned["favourable"], high))
    line("Unfavourable constructed case, 10x, at 10 times revenue", revenue_needed(round_size, ten, owned["unfavourable"], high))
    line("Unfavourable constructed case, 10x, at 4 times revenue", revenue_needed(round_size, ten, owned["unfavourable"], low))
    line("Two later rounds only (B and C), 10x, at 10 times revenue", revenue_needed(round_size, ten, owned["two_rounds"], high))
    line("Separate premium case, 10x, at 15 times revenue",
         revenue_needed(round_size, ten, reference, inputs["sale_multiple_premium"]))
    smallest = revenue_needed(round_size, ten, reference, high) / inputs["market_share_high"]
    largest = revenue_needed(round_size, ten, reference, low) / inputs["market_share_low"]
    print(f"  Serviceable market needed for 10x at a 30% and a 20% share: USD {cents(smallest):,} to {cents(largest):,}")

    market_history = market_size(inputs)
    print()
    print("Model history (earlier directory-price proxy; models count new customers only, in one scenario)")
    figures = [
        ("Total market (TAM), earlier proxy", market_history["tam"]),
        ("Serviceable market (SAM), earlier proxy", market_history["sam"]),
        ("First model", first_model(inputs)["annual_opportunity"]),
        ("Corrected model", corrected_model(inputs)["annual_opportunity"]),
    ]
    for label, value in figures:
        print(f"  {label:<40} USD {cents(value):,} a year")


if __name__ == "__main__":
    main()
