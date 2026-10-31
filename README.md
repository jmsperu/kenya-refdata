# kenya-refdata

Kenyan reference data as sourced, versioned CSV files: administrative units, post offices, banks and
branch codes, regulated institutions, mobile number prefixes, public holidays, currencies, education
levels and occupations. **Data only, no code.** Shared by the MojaEdge (CollectPoa) and Afya apps.

Current version: **0.1.0**. Composer package `xcobean/kenya-refdata` (type library, no dependencies).

## Rules

- Every dataset comes from an official public source (regulator, government, ISO, ILO). No scraped login-walled
  or licence-restricted data. The source URL and as-of date are in each manifest.
- Nothing is invented: a code the source does not publish stays blank; a list that could not be sourced is
  not here (see "Not included").
- Phone prefixes are in 254 form (no plus), the platform standard.

## Layout

- `data/<dataset>.csv`: UTF-8, header row, natural key column(s) (see `schema.json`), `active` (1/0), optional
  `effective_from` / `effective_to` (YYYY-MM-DD) and row-level `source_url`. Other columns are extra detail.
- `data/<dataset>.manifest.json`: key, name, version, source, source_url, other_sources, as_of, retrieved,
  row_count, sha256 (of the CSV), natural_key, notes (caveats, what is missing and why).
- `schema.json`: natural key and required columns per dataset. `datasets.json`: machine-readable index.
- `scripts/validate.py`: checks headers, required cells, `active`, unique keys, sha256 and row_count (CI runs it).

## Consuming

```json
"repositories": [{"type": "vcs", "url": "https://github.com/jmsperu/kenya-refdata"}],
"require": {"xcobean/kenya-refdata": "0.1.0"}
```

Then read `vendor/xcobean/kenya-refdata/data`. Upsert by the natural key; treat rows with `active = 0`, and rows
a new version no longer lists (a revoked licence, a closed branch), as inactive rather than deleting them.

## Datasets

| Dataset | Rows | As of | Source |
| --- | ---: | --- | --- |
| `counties` Counties of Kenya | 47 | 2010-08-27 | [Constitution of Kenya 2010, First Schedule (Counties) [names]; IEBC, Registered Voters per County Assembly Ward for the 2022 General Election [codes]](https://klrc.go.ke/index.php/constitution-of-kenya/163-schedules-schedules/165-first-schedule-counties/434-1-counties) |
| `sub_counties` Sub-counties of Kenya (KNBS 2019 census) | 333 | 2019-11-04 | [KNBS, 2019 Kenya Population and Housing Census Volume I: Population by County and Sub-County, Table 2.5](https://www.knbs.or.ke/wp-content/uploads/2023/09/2019-Kenya-population-and-Housing-Census-Volume-1-Population-By-County-And-Sub-County.pdf) |
| `constituencies` Constituencies of Kenya (IEBC) | 290 | 2022-06-23 | [IEBC, Registered Voters per Constituency for the 2022 General Election](https://www.iebc.or.ke/docs/rov_per_constituency.pdf) |
| `wards` County Assembly Wards of Kenya (IEBC) | 1450 | 2022-06-23 | [IEBC, Registered Voters per County Assembly Ward for the 2022 General Election](https://www.iebc.or.ke/docs/rov_per_caw.pdf) |
| `post_offices` Posta Kenya post offices and postal codes | 621 | 2026-11-01 | [Postal Corporation of Kenya, "Locate a post office" store-locator data on posta.co.ke/post-offices](https://posta.co.ke/post-offices/) |
| `banks` Kenyan banks (CBK-licensed commercial banks, mortgage finance institution, microfinance banks) with KEPSS/clearing bank code and SWIFT/BIC | 53 | 2026-07-01 | [Central Bank of Kenya: Directory of Licenced Commercial Banks, Mortgage Finance Institutions and Authorised Non-Operating Bank Holding Companies (July 2026 upload) + Directory of Licenced Microfinance Banks (Feb 2026); bank codes from Kenya Bankers Association Bank Branch Code list 2026; SWIFT from each bank's own website or CBK KEPSS Rules Schedule B](https://www.centralbank.go.ke/wp-content/uploads/2026/07/Directory-of-Licenced-Commercial-Banks-Mortgage-Finance-Institutions-and-Authorised-Non-Operating-Bank-Holding-Companies.pdf) |
| `bank_branches` Kenyan bank branches with clearing (bank + branch) codes | 1924 | 2026-09-16 | [Kenya Bankers Association: Bank Branch Code list 2026 (Branch-Code-2026.pdf, linked from kba.co.ke/bank-branch-code/)](https://www.kba.co.ke/wp-content/uploads/2026/09/Branch-Code-2026.pdf) |
| `payment_service_providers` CBK Authorised Payment Service Providers | 44 | 2026-08-10 | [Central Bank of Kenya - Directory of Authorized Payment Service Providers (PSPs) as at August 10, 2026](https://www.centralbank.go.ke/wp-content/uploads/2026/09/Directory-of-Authorized-Payment-Service-Providers-August-10-2026.pdf) |
| `money_remittance_providers` CBK Licensed Money Remittance Providers | 37 | 2026-09-30 | [Central Bank of Kenya - Directory of Licenced Money Remittance Providers (MRPs) as at September 30, 2026](https://www.centralbank.go.ke/wp-content/uploads/2026/10/Directory-of-Licenced-Money-Remittance-Providers-as-at-September-30-2026.pdf) |
| `credit_reference_bureaus` CBK Licensed Credit Reference Bureaus | 3 | 2025-12-31 | [Central Bank of Kenya - Bank Supervision Annual Report 2025, Appendix XIX Directory of Credit Reference Bureaus (cross-checked against the Directory of Licensed CRBs, November 2022)](https://www.centralbank.go.ke/uploads/banking_sector_annual_reports/1241268828_ANNUAL%20REPORT%202025.pdf) |
| `digital_credit_providers` CBK Licensed Digital Credit Providers | 281 | 2026-09-29 | [Central Bank of Kenya - Directory of Digital Credit Providers, updated on September 29, 2026](https://www.centralbank.go.ke/wp-content/uploads/2026/09/Directory-of-Digital-Credit-Providers-September-2026.pdf) |
| `forex_bureaus` CBK Licensed Foreign Exchange Bureaus | 96 | 2026-09-30 | [Central Bank of Kenya - Directory of Licenced Foreign Exchange Bureaus as at September 30, 2026](https://www.centralbank.go.ke/wp-content/uploads/2026/10/Directory-of-Licenced-Foreign-Exchange-Bureaus-as-at-September-30-2026.pdf) |
| `saccos` SASRA Licensed and Authorised SACCO Societies 2026 | 357 | 2026-02-03 | [Sacco Societies Regulatory Authority - List of Licensed and Authorised Sacco Societies in Kenya for the Financial Year ending 31st December 2026 (dated 3 February 2026)](https://www.sasra.go.ke/download/list-of-licensed-and-authorized-sacco-societies-in-kenya-for-the-financial-year-ending-31st-december-2026/?wpdmdl=1573) |
| `cma_licensees` Capital Markets Authority (Kenya) licensees, approved institutions and approved schemes | 342 | 2026-11-01 | [Capital Markets Authority Kenya - Licensees/Market Players portal (licensees.cma.or.ke), all 20 category pages](https://licensees.cma.or.ke/) |
| `statutory_bodies` Kenyan statutory bodies for HR, payroll, finance and compliance | 31 | 2026-11-01 | [Each institution's official website (verified by HTTP request on 2026-11-01); Affordable Housing Act 2024 on kenyalaw.org for the Affordable Housing Board](https://new.kenyalaw.org/akn/ke/act/2024/2) |
| `msisdn_prefixes` Kenyan mobile number prefixes (NDC allocations) | 130 | 2026-04-01 | [Communications Authority of Kenya - Telecommunication Numbering Plan for Kenya (CA/SRM/S&N/NNP/APRIL/2026), section 1.1(b)](https://www.ca.go.ke/sites/default/files/2026-04/Numbering%20Plan%20Kenya%20April%202026.pdf) |
| `public_holidays` Kenya public holidays 2026-2028 | 36 | 2024-04-26 | [Kenya Law - Public Holidays Act (Cap. 110), revised 26 April 2024 (latest version); Kenya Gazette special issues on kenyalaw.org](https://new.kenyalaw.org/akn/ke/act/1912/21/eng@2024-04-26) |
| `currencies` ISO 4217 currency codes (List One, active) | 178 | 2026-09-17 | [SIX Financial Information (ISO 4217 Maintenance Agency) - ISO 4217 List One: Currency, fund and precious metal codes](https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml) |
| `education_levels` Kenya National Qualifications Framework levels | 10 | 2025-05-30 | [Kenya Law - The Kenya National Qualifications Framework (General) Regulations, 2025 (L.N. 94 of 2025), First Schedule Part 4 (Minimum Entry Requirements table)](https://new.kenyalaw.org/akn/ke/act/ln/2025/94/eng@2025-05-30) |
| `occupations` ISCO-08 occupation classification (used because KNOCS/KeSCO is not openly published) | 619 | 2026-11-01 | [International Labour Organization - ISCO-08 Structure and definitions (English)](https://webapps.ilo.org/ilostat-files/ISCO/newdocs-08-2021/ISCO-08/ISCO-08%20EN%20Structure%20and%20definitions.xlsx) |

Notes per dataset (caveats, corrections made while transcribing, gaps) are in each manifest.

## Not included (and why)

- **Insurers / insurance brokers (IRA)**: ira.go.ke and the Kenya Law gazette copies sit behind bot checks; the 2026
  licensed-entities PDF could not be fetched. Add from the PDF downloaded by hand.
- **Court stations (Judiciary)**: only a mixed contact directory is published (no court type / county).
- **Licensed auctioneers (Auctioneers Licensing Board)**: no public register online.
- **Sub-county codes**: KNBS publishes none (names only, 2019 census).
- **KNOCS / KeSCO occupation codes (KNBS)**: not openly published; ISCO-08 (ILO) is provided instead.
- **Idd-ul-Fitr 2027 / 2028**: not yet gazetted (moon-dependent).
- **SWIFT/BIC for some banks**: only where the bank itself or CBK publishes it (see `banks` manifest).

## Updating

Edit or replace the CSV, update its manifest (as_of, source_url, notes), run
`python3 scripts/regen_manifests.py` to refresh sha256 / row_count, `python3 scripts/validate.py`, bump `version`
in the manifests, and tag the release (semver: new rows / datasets = minor, corrections = patch).
