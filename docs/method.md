# Method guide

VentureLens follows twelve stages, numbered 0 to 11. Each stage answers one question, produces a written output, and ends with a decision that a person makes, not the AI. A stage can end the work: stopping early for a good reason is a useful result.

Work can start from a market, to discover and rank companies, or from a named company, to test it against its market and the realistic alternatives. Both routes use the same twelve stages, and a company that arrives by name does not need to be selected again.

## The twelve stages

Version V0.3 keeps the V0.2 backbone: the same twelve stages and questions, the loops between them, and a human decision at the end of each stage.

| Stage | Question it answers | What the human decides |
|---|---|---|
| 0. Fund mandate | What is investable for this fund? | Approve the fund profile and any exceptions. |
| 1. Investment search brief | What market or opportunity are we investigating? | Approve the research scope. |
| 2. Exploratory market scan and startup discovery | How does the market work, and what solutions already exist? | Refine the market boundaries, then continue or stop. |
| 3. Market and competitive analysis | Is the market structurally attractive, and how does competition work? | Accept or refine the market work and its main gaps, or stop. |
| 4. Working market thesis | Where and why could venture-scale opportunities exist? | Approve the working thesis. |
| 5. Systematic startup landscape | Which companies fit or challenge the working thesis? | Accept the landscape's coverage or ask for important additions. |
| 6. Refined market thesis | Does the company evidence support the original thesis? | Approve the thesis and the screening criteria. |
| 7. Initial company screening | Which companies appear attractive and fit the fund? | Advance to planning, Monitor, Defer or Pass. |
| 8. Company selection and diligence planning | Which companies deserve deeper work, and what must be proven? | Approve the full scope and depth of diligence. |
| 9. Detailed company diligence | Does the evidence support the company investment case? | Weigh the support, counterevidence and gaps, then move to synthesis, ask for targeted work, or stop. |
| 10. Investment synthesis | Is this an attractive investment for the fund? | Accept the judgment and decide what kind of memo it supports, such as a learning memo or one ready for a decision, or send important gaps back to earlier stages. |
| 11. IC memo | What should the investment committee decide? | Review a learning memo, or make an investment decision if the evidence is strong enough, recording who decided and on what conditions. |

The decisions are simplified from the process document (V0.3). The decisions in stage 7 are the method's general options. In the worked example, the outcome in this exercise was Monitor.

## What each stage must produce

- **0. Fund mandate.** What the fund is allowed to back, before any company is looked at: its focus, exclusions, cheque size, stage and geography, with any exceptions recorded. The demo mandate covers US$1–5 million cheques into Seed-to-Series B technology companies, mainly in Europe and MENA.
- **1. Search brief.** What exactly is being investigated, by which route, at what depth, and where the work will stop. For a named company, early checks on its funding and legal entity begin here.
- **2. Exploratory scan.** A first map of the market, its customers, value chain and solutions: a sample of companies when starting from a market, a rapid scan when starting from a company. Funding, its stated use, and public rollout or hiring plans are recorded where they apply.
- **3. Market and competition.** An agreed market boundary and the unit customers actually buy, a workbook that keeps sources, assumptions and calculations apart, and a narrative that follows it. It also covers growth and trends, a check against wider market data, and the economics of adoption where they matter. Physical assets, the serviceable market and the company's own opportunity are kept separate.
- **4. Working thesis.** A testable statement of the opportunity and why now, with segments, alternatives, possible winning models and what evidence would prove it wrong. Trends are linked to what they mean for customers.
- **5. Landscape.** One sourced landscape of companies, incumbents and substitutes, with the limits of its coverage. Both routes test the realistic alternatives.
- **6. Refined thesis.** What the company evidence changed in the thesis, and the criteria for screening companies. Parts of the market that were not sized stay visible.
- **7. Screening.** A first look at the current product, team, commercial position, finances and fit with the fund. Funding and rollout plans are compared with the company's scope, price, starting business and capacity. Unknown is kept separate from weak.
- **8. Diligence planning.** The few beliefs that would decide the case, put first while every area of diligence stays in scope, with how each will be tested, who owns it and when to stop.
- **9. Diligence.** Evidence that the current product works in operation; which customers are contracted, live, paying or renewing; price, unit and willingness to pay; delivery costs; leadership, competition, finances and security; and what the funding can achieve. Material mismatches with outside signals are worked through, and hypothetical scenarios and adapted benchmarks are labelled.
- **10. Synthesis.** One judgment that weighs the case against the countercase, with conditional outcomes and returns, terms and the conditions that would decide it. Checks on the sums are kept apart from the commercial challenge, models and cutoff dates are reconciled, and the human decision is recorded.
- **11. IC memo.** The reviewed judgment, written so a new reader can follow it, through all fifteen core sections, with sources, unknowns, risks and the decision requested. No new research or calculations happen while the memo is being drafted.

Competition is assessed twice: in stages 2 to 6 as market structure (incumbents, substitutes, crowding and gaps), and in stages 7 to 10 as whether one company can win and defend its position. Later stages can send work back: diligence can change the market analysis or the landscape.

## Evidence rules

These apply at every stage. The governing rule: never make the available evidence appear stronger than it is.

| Rule | What it changes |
|---|---|
| Trace material claims to specific sources | A bibliography alone does not support every conclusion. |
| Separate evidence type from confidence | A company claim can be accurately recorded while confidence in its wider implication remains low. |
| Preserve counterevidence | Conflicting findings stay visible instead of being averaged away or omitted. |
| Keep Unknown distinct from zero | Missing revenue or customer data does not become a zero or an automatic poor score. |
| Explain assumptions | Estimates show their rationale, units, limits and sensitivity. |
| Separate economic questions | Market opportunity, company revenue potential and customer savings have different definitions. |
| Keep the dates of changeable sources apart | A page's publication, access and review dates are recorded separately, and pages that can change or disappear are captured when first used. |
| Give every price its product, unit, scope and date | A price is tied to the exact package, what it covers, the unit it is charged by and when it applies. Current and announced prices stay separate. |
| Record who proposed each assumption | Each assumption carries its proposer where known, its support or reasoning and how it was adapted. Passing a number on or approving it does not make it evidence. |
| Keep customer states distinct | Contracted, evaluating, live, accepted, paying and renewing are different states. One is never inferred from another. |
| Keep automated checks apart from plausibility | Checks on sources, units and formulas are recorded separately from the commercial challenge. Passing tests or AI agreement cannot approve the economics. |
| Treat benchmarks as borrowed evidence | A benchmark describes other companies and needs a stated adaptation. Combining separate medians or quartiles gives constructed cases, not percentiles. |

The evidence threshold rises through the funnel: directionally credible sources are enough for exploration, major claims are checked at screening, and material claims are corroborated or explicitly left unresolved in diligence. In this repo, the rules are enforced by [`venturelens/records.py`](../venturelens/records.py) and the tests.

The evidence sample in this repo was built before the new evidence standard. Its records do not yet carry every field the standard now asks for. Bringing the data format up to the standard is planned with the evidence explorer.

## Who decides what

Automation may propose, organise, compare and flag. It must not hide source limitations, manufacture confidence or present an unowned judgment as an objective system result.

| AI helps with | Stays with the investor |
|---|---|
| Source discovery, extraction and deduplication | Defining the decision question and what matters |
| Evidence logging and freshness checks | Interpreting contradictions and management credibility |
| Flagging missing fields and unsupported claims | Classifying supportable versus structural weaknesses |
| Comparative tables and initial scorecards | Deciding whether the case survives the countercase |
| Handoffs, status, ownership and version history | Accepting valuation, ownership and risk |
| Repeated formatting and document-generation checks | Making the final recommendation |

Two review results are kept separate. Automated checks can flag arithmetic, missing data, units, unsupported claims, out-of-date versions or stale sources. A separate review of commercial plausibility considers outside signals, customer economics, price, unit and market boundary, what the funding can pay for, how benchmarks were adapted and the countercase, and an accountable person decides what to do about it. Passing checks, AI agreement or a finished file cannot approve that judgment, and an AI challenging its own work is not an independent review.

## The ten approved controls

These controls come from the Gigaton case. They were approved on 16 November 2026 as default requirements and have not yet been tested on a new case.

1. **Funding and outside signals early.** Record a named company's funding early and compare it with the model's scope, price, starting business and capacity. A material mismatch becomes a specific test, repeated after any major correction. Funding is a signal, not proof, and a model is never forced to match it.
2. **Prices and proxies.** Record the exact product, package, charging unit, sites covered and dates for every price, and prefer a vendor's own offer that matches the scope to a directory figure. A package shared across sites is split only across sites assumed to use it, and each case is shown separately, not as a range.
3. **Consistency and commercial plausibility.** Keep two records: one that checks formulas, units, sources and dates, and a commercial challenge that ends in a human decision. A correction should leave the result better supported, not just smaller.
4. **Economic scope and company forecasts.** Keep market potential, actual spending, the company's opportunity, new-customer scenarios, whole-company revenue and customer savings distinct. When a company's existing paying business is unknown, there is no whole-company forecast.
5. **Market boundary and commercial units.** Agree the boundary before sizing, and separate physical, eligible and billable units. Record what is sized, excluded and not sized; not sized is never zero.
6. **Product and customer evidence states.** Tie each result to the product version and set-up that produced it, and keep customer states, from announced to expanding, distinct.
7. **Durable sources and assumption origins.** Capture sources when first used, keep their dates separate, and record who proposed each assumption and what supports it.
8. **Benchmarks and returns.** Record what each benchmark measures and how it was adapted. Treat combined quartiles as constructed cases, test favourable cases as well as adverse ones, and keep the revenue a return would need separate from the market the evidence supports.
9. **Judgment before the memo.** Form the judgment in synthesis before the memo is written, keep one record of the current outputs and their cutoff dates, and keep review, approval and decision as separate steps.
10. **Coverage before communication.** Cover growth, trends, leadership, customer economics and funding position before the memo, or state the limit, and keep every core memo section.

## Versions

| Process version | Became the baseline | What it holds |
|---|---|---|
| V0.2 | 2 September 2026 | The twelve stages, the evidence rules and the human decisions |
| V0.3 | 16 November 2026 | The same twelve stages, the two ways in, a longer evidence standard and the ten approved controls |

This baseline was approved on 16 November 2026 for use and further testing. The Gigaton case did not test every requirement, and none of the ten new controls has been used on a new case.

## Glossary

- **Mandate:** the fund's rules for what it may back: sector, geography, company stage, cheque size and exclusions.
- **Thesis:** a testable view of where and why attractive opportunities could exist in a market, with the conditions that would prove it wrong.
- **Diligence:** detailed checking of a company's claims, market, product, team, finances and risks before a decision.
- **TAM (total addressable market):** the revenue available if every potential customer bought. Here, full adoption potential, not current spending.
- **SAM (serviceable addressable market):** the part of the TAM that a supplier of this kind could realistically serve, here after size and readiness filters.
- **Investment committee (IC) memo:** the document that sets out findings, risks, conditions and a recommendation for the group that makes the investment decision.
- **Monitor:** public evidence gave reasons to look further but could not settle the decision; the case is revisited if decisive evidence becomes available.
- **Incumbents and substitutes:** established suppliers already serving the need, and other ways a customer could meet it.
- **Value pools and exits:** where the money in a market is made, and how investors have realised returns (for example a sale or listing).
- **Whitespace:** a part of the market that no company yet serves well.
- **Bull, base and bear cases:** optimistic, central and pessimistic versions of how the company could develop.
- **Dilution:** the share of a company sold in a new funding round, which shrinks every existing investor's stake.
- **Exit multiple:** a company's sale value divided by its annual revenue. The case study calls it the sale multiple, written as "times revenue".
- **Return multiple:** what an investor gets back divided by what it put in; 10x means ten times the money invested.
