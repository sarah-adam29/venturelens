> [!IMPORTANT]
> This is a personal learning project built from public information only. It has not been reviewed by investors, the company or industry experts, and it is not investment advice. The Gigaton case reflects evidence read up to 16 November 2026 and says nothing about the company today. If you can correct or add to anything here, please open an issue.

# VentureLens

**An AI-assisted workflow for venture investment research. It combines market analysis, company screening, diligence and investment synthesis, with explicit evidence standards and human decision gates.**

VentureLens starts with a practical question: **what would we need to believe, and verify, to justify spending more time on this opportunity?**

## Why I built this

I built VentureLens to learn two things:

1. **How venture investors evaluate a company.** I designed a 12-stage process, from the fund's mandate (its rules for what it may back) to the investment committee memo, and tested it on public information.
2. **How to build an AI-assisted workflow.** That means structured records, clear rules for what AI may and may not do, and automatic checks on its output.

The aim is to make the reasoning inspectable: what supports a conclusion, what challenges it, and what remains unknown.

## Start with the worked example

[Read the Gigaton case study](docs/case-study-gigaton.md): a public-information assessment of industrial AI for cement-process optimisation.

In this exercise, the outcome was **Monitor**: public evidence gave reasons to look further but could not settle the decision. Historical operating evidence gave reasons for interest, while current-product performance, repeatable paid demand, delivery economics and transaction information remained unresolved.

The case does not estimate the company's revenue. Instead, it compares the cement market sized here with the USD 26 million funding round announced in June 2026. This return test is illustrative: its inputs are benchmarks and assumptions, not the investors' actual terms or targets.

> Under the reference assumptions, a 10x return needs more annual revenue than the entire serviceable cement market sized here. Under the most favourable case within the tested 4–10x exit range, it needs about four-fifths of that market. Either way, it needs far more than the 20–30% market-share sensitivities.

Only cement kilns were sized. The company's wider cement offering, steel and glass were not sized, which is not the same as having no value.

Company evidence was reviewed through **2 November 2026**; funding, pricing and return evidence through **16 November 2026**. This is a dated learning exercise, not a current view of the company.

## How the workflow works

The [method guide](docs/method.md) sets out all twelve stages. In short:

1. **Frame the decision:** define the mandate, research question, market boundary and stopping point.
2. **Understand the market:** investigate customers, economics, competitors and realistic alternatives; develop and challenge a working thesis.
3. **Screen the opportunity:** assess fit and decide whether deeper work is justified.
4. **Plan and conduct diligence:** prioritise decisive questions while keeping coverage of product, customers, team, operations, finances and risks.
5. **Form a judgment:** weigh support, counterevidence, assumptions and missing information.
6. **Communicate and learn:** prepare a memo, record the human decision and identify improvements to the method.

An evidence register runs across every stage, with rules such as "keep Unknown distinct from zero" and "separate evidence type from confidence". A justified early stop is a useful outcome; completing every stage is not the objective.

## How AI was used

- I designed the workflow and tested it over three rounds between August and November 2026.
- I used ChatGPT to develop the method and run the company cases.
- I used Codex to process documents, organise sources and package the working records.
- I set the scope, approved each stage and challenged the assumptions. For example, I required clearer market boundaries and better-supported modelling assumptions rather than accepting labelled guesses.
- This repo was assembled with Claude Code, including the evidence checks and the sizing code.
- Between 13 and 15 November 2026 I used Claude to recalculate the four figures the case then used from my workbooks and to re-open the cited source pages. I checked the listed price and the retention benchmark myself. The case study lists which pages were checked.
- On 15 November 2026 I questioned the result against the company's funding round. All the checks had passed by then, and none of the AI tools had raised the mismatch.
- On 15 and 16 November I used ChatGPT to reassess the market, the fee evidence and the return test.
- Claude recalculated the new figures and found the benchmarks. I confirmed the listed price, the job advert, the Carta chart, the UKRI grant record and the AspenTech results myself.

AI outputs needed review: a plausible explanation or a cited benchmark does not by itself validate a claim or its applicability. This repo does not show that I hand-coded every component, verified every external claim, or carried out professional investment diligence.

## What is in the repo

| Path | What it holds |
|---|---|
| [`docs/case-study-gigaton.md`](docs/case-study-gigaton.md) | The worked example, with a claim-and-source table |
| [`docs/method.md`](docs/method.md) | The twelve stages, the two ways in, evidence rules, who decides what, the ten approved controls and a glossary |
| [`docs/lessons.md`](docs/lessons.md) | What the exercise taught, about investing and about the workflow |
| [`data/evidence_sample.csv`](data/evidence_sample.csv) | 29 of the 113 evidence records, each with a source, dates, type, confidence and limits |
| [`data/sizing_inputs.csv`](data/sizing_inputs.csv) | Every input to the sizing, with its evidence record and whether it is sourced or assumed |
| [`venturelens/records.py`](venturelens/records.py) | Loads the evidence records and reports any that break a rule |
| [`venturelens/sizing.py`](venturelens/sizing.py) | The package-use cases, the return test and the model history |
| [`tests/`](tests/) | Checks on the records, the sums and the documents |

### Run the checks

You need [uv](https://docs.astral.sh/uv/). Then:

```
uv run pytest
```

To print the package-use cases, the return test and the model history, or list any broken evidence record:

```
uv run python -m venturelens.sizing
uv run python -m venturelens.records
```

The same tests run on every push and pull request.

## Current status and what comes next

VentureLens is a documented research workflow tested through public-information exercises. Two earlier cases were run before Gigaton; one stopped early at the screening stage. The baseline was approved on 16 November 2026 and includes ten controls from this case, not yet tested on a new case.

The worked example exposed gaps in growth analysis, leadership assessment and customer-economic context. These remain limits of this case.

The next release is a small **evidence explorer**: select a claim and inspect its sources, confidence, counterevidence and open questions, with checks for incomplete records. It is not built yet.

## About this project

VentureLens is part of my [portfolio](https://sarah-adam29.github.io/), alongside [Solar Project Finance](https://github.com/sarah-adam29/solar-project-finance) and an [AI plant-care project](https://github.com/sarah-adam29/plant-care).

It is personal learning work using public information. It does not represent client work, an investment fund, a company endorsement or professional advice. Source organisations keep their rights in their material; linking to a source does not imply endorsement or permission to redistribute it.

To correct or add to anything, please open an issue. Code is released under the [MIT licence](LICENSE).
