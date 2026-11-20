# CLAUDE.md

Rules for every session working in this repo. They come from the project owner and override convenience. If a task seems to need breaking one, stop and ask.

## Private material

Private working material is never copied into this repo. The list of what is excluded is kept outside the repo.

## How to write about the company

- Say what a source states, who published it and when. Keep company-reported claims labelled as company-reported.
- "Unknown" means not public. Never write it as a weakness.
- The outcome is Monitor: public evidence gave reasons to look further and could not settle the decision. No "invest" or "pass" language in any statement about a real company. This rule does not cover the method's general decision options, such as those in the stage table in `docs/method.md`, which stay word for word.
- Company evidence was reviewed through 2 November 2026; funding, pricing and return evidence through 16 November 2026. Never describe the company in the present tense as if current.
- Use "in this exercise" when stating a result.
- The case does not estimate the company's revenue or value. USD 1.78 million and USD 0.58 million appear only as model history, each time labelled as new customers only, in one scenario.
- The return test is illustrative. Always say the inputs are benchmarks and assumptions, not the investors' actual terms or targets.
- Never write that cement "cannot support" the round. State the finding in these words:

  > Under the reference assumptions, a 10x return needs more annual revenue than the entire serviceable cement market sized here. Under the most favourable case within the tested 4–10x exit range, it needs about four-fifths of that market. Either way, it needs far more than the 20–30% market-share sensitivities.

- The best and worst ownership cases are constructed cases. Never call them percentiles or a statistical range.
- The four package-use cases are separate dated cases. Never call them a price range or average them.
- "Not sized" is never written as zero or as worthless.
- The method's ten new controls are approved requirements. Never describe them as validated, tested, automated or proven to save time. They have not yet been used on a new case.

## Numbers

These figures were recalculated from the owner's current workbook on 16 November 2026. Tests compare them to the cent. Never change them, and never change a test's expected value to make it pass.

### Market: fee evidence and package-use cases

Site counts: 2,521 operating sites; 1,188.6 serviceable site-equivalents. The listed package costs USD 67,530.48 a year now and USD 155,000 a year from 1 March 2027. It covers up to 10 optimisation units across up to 2 sites.

| Case | Fee per site a year | Total market (TAM) | Serviceable market (SAM) |
|---|---|---|---|
| Current price, package shared across 2 sites | 33,765.24 | 85,122,170.04 | 40,133,364.26 |
| Current price, one site | 67,530.48 | 170,244,340.08 | 80,266,728.53 |
| Price from 1 March 2027, shared across 2 sites | 77,500.00 | 195,377,500.00 | 92,116,500.00 |
| Price from 1 March 2027, one site | 155,000.00 | 390,755,000.00 | 184,233,000.00 |
| Earlier proxy (history) | 84,000.00 | 211,764,000.00 | 99,842,400.00 |

### Return test

| Input | Value | Kind |
|---|---|---|
| Funding round | USD 26,000,000 | sourced (E-002) |
| Stake sold at Series A | 18% median; 11% and 21% quartiles | benchmark (E-110) |
| Stake sold in later rounds, medians | 12% (B), 9.8% (C), 8.1% (D) | benchmark (E-110) |
| Later rounds, quartiles | B 8.6% and 16.4%; C 5.6% and 15.0%; D 3.9% and 11.8% | benchmark (E-110) |
| Sale value as a multiple of annual revenue | 4 (benchmark median, E-111) to 10 (assumption) | mixed |
| Return multiple tested | 3 and 10 | assumption, with context (E-112) |
| Share of the serviceable market won | 20% and 30% | assumption, no benchmark |

| Result | Exact value |
|---|---|
| Share kept after rounds B, C and D (0.88 × 0.902 × 0.919) | 0.72946544 |
| Ownership at exit, reference (0.18 × 0.72946544) | 0.1313037792 |
| Sale value needed for 10x | 1,980,141,025.52 |
| Annual revenue needed for 10x, at 10 and 4 times revenue | 198,014,102.55 and 495,035,256.38 |
| Annual revenue needed for 3x, at 10 and 4 times revenue | 59,404,230.77 and 148,510,576.91 |
| Favourable case (21% stake; later rounds at 8.6%, 5.6%, 3.9%): revenue for 10x at 10 times | 149,318,107.03, which is 81.05% of 184,233,000 |
| Unfavourable case (11% stake; later rounds at 16.4%, 15.0%, 11.8%): revenue for 10x at 10 and 4 times | 377,126,347.13 and 942,815,867.83 |
| Two later rounds only (B and C): revenue for 10x at 10 times | 181,974,960.25, which is 98.77% of 184,233,000 |
| Serviceable market needed for 10x at a 30% and a 20% share | 660,047,008.51 to 2,475,176,281.90 |
| Separate premium case, 15 times revenue (E-113) | 132,009,401.70, which is 71.65% of 184,233,000 |

Revenue needed = round × return multiple ÷ ownership at exit ÷ sale multiple. It assumes no debt, no sale costs and no further investment by the same investors.

### Model history

First model USD 1,777,440; corrected model USD 582,758.40. Both count new customers only, in one scenario.

### Rounding in prose

USD 34,000 to 155,000 a site; serviceable market of about USD 40, 80, 92 and 184 million; revenue of about USD 198 to 495 million; about USD 149 million and 81%; a serviceable market of about USD 660 million to 2.5 billion. Model history: about USD 1.78 million and about USD 0.58 million.

## Style

- British spelling. First person is allowed in the README, in `docs/lessons.md`, and in the case study only where it describes a decision the owner made at a human gate (for example "At the review gate, I challenged those inputs"). No first person anywhere else in `docs/`. Plain words; explain each investing term the first time it appears.
- No emoji. No "building in public". Titles do not include the owner's name.
- This disclaimer goes at the top of the README and the case study, word for word:

```
> [!IMPORTANT]
> This is a personal learning project built from public information only. It has not been reviewed by investors, the company or industry experts, and it is not investment advice. The Gigaton case reflects evidence read up to 16 November 2026 and says nothing about the company today. If you can correct or add to anything here, please open an issue.
```

## Checks

Run `uv run pytest` before every commit.
