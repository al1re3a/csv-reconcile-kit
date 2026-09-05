<!-- readme-refresh:start -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/readme-banner.png">
    <img alt="CSV Reconcile Kit project banner" src="assets/readme-banner.png" width="100%">
  </picture>
</p>

<h1 align="center">🧾 CSV Reconcile Kit</h1>

<p align="center"><strong>Reconcile CSV exports while keeping duplicate keys and decimal tolerance visible.</strong></p>

<p align="center">
  <a href="https://github.com/al1re3a/csv-reconcile-kit/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/al1re3a/csv-reconcile-kit/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-fbbf24.svg"></a>
  <a href="https://github.com/al1re3a/csv-reconcile-kit/releases"><img alt="Release" src="https://img.shields.io/github/v/release/al1re3a/csv-reconcile-kit?display_name=tag&sort=semver"></a>
  <a href="https://github.com/al1re3a/csv-reconcile-kit/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/al1re3a/csv-reconcile-kit?style=flat&color=8b5cf6"></a>
  <a href="https://github.com/al1re3a/csv-reconcile-kit/issues"><img alt="Open issues" src="https://img.shields.io/github/issues/al1re3a/csv-reconcile-kit?style=flat&color=06b6d4"></a>
</p>

<p align="center">
  <a href="https://github.com/al1re3a/csv-reconcile-kit"><img alt="Source" src="https://img.shields.io/badge/Source-open-111827?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="#install"><img alt="Quick Start" src="https://img.shields.io/badge/Quick_Start-open-0f766e?style=for-the-badge&logo=gnubash&logoColor=white"></a>
  <a href="CONTRIBUTING.md"><img alt="Contribute" src="https://img.shields.io/badge/Contribute-open-7c3aed?style=for-the-badge&logo=github&logoColor=white"></a>
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,githubactions" alt="Python and GitHub Actions" height="42">
</p>

> [!NOTE]
> Duplicate-key handling and numeric tolerance are explicit so accounting differences are not silently collapsed.

## 📑 Contents

- [At a glance](#-at-a-glance)
- [What it does](#what-it-does)
- [Install](#install)
- [Quick start](#quick-start)
- [Scope and limitations](#scope-and-limitations)
- [Related work](#related-work)
- [Development and validation](#development-and-validation)

---

## 🔎 At a glance

| | |
|---|---|
| **Purpose** | Reconcile CSV exports without hiding duplicate keys or decimal rounding differences. |
| **Input** | Two CSV exports |
| **Output** | Reconciliation report |
| **Runtime** | Python 3.11+ |
| **CI** | ✅ Linux · macOS · Windows |
| **Status** | ✅ Maintained |

<details>
<summary><strong>🧭 How it works</strong></summary>

```mermaid
flowchart LR
    A["Two CSV exports"] --> B["Match and compare"]
    B --> C["Reconciliation report"]
```

</details>

<details>
<summary><strong>📁 Repository layout</strong></summary>

```text
csv-reconcile-kit/
├── .github/
├── tests/
├── examples/
├── pyproject.toml
├── csv_reconcile_kit.py
└── README.md
```

</details>

<details>
<summary><strong>🤝 Contributors</strong></summary>

<br>
<a href="https://github.com/al1re3a/csv-reconcile-kit/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=al1re3a/csv-reconcile-kit" alt="Contributors">
</a>

</details>
<!-- readme-refresh:end -->

Reconcile CSV exports without hiding duplicate keys or decimal rounding differences.

Small, offline-first command-line software. Version **0.1.0** implements the scope below.
No runtime dependencies beyond Python 3.11+ and its standard library.

## What it does

- Order-independent comparison with repeatable composite key columns.
- Added, removed, changed records and schema changes in deterministic JSON.
- Per-column absolute Decimal tolerances, ignored columns, strict header/row/key validation.

## Install

From a source checkout:

```console
git clone https://github.com/al1re3a/csv-reconcile-kit.git
cd csv-reconcile-kit
python -m pip install .
csv-reconcile-kit --help

# Or run without installing:
python csv_reconcile_kit.py --help
```

No PyPI, package-registry or hosted-release availability is implied by these commands.

## Quick start

Run from the repository root:

```console
python csv_reconcile_kit.py examples/before.csv examples/after.csv --key sku --key region --ignore updated --tolerance price=0.01
# Exit 1: B removed, C added; the one-cent A difference is within tolerance.
```

JSON goes to stdout; diagnostics go to stderr. Exit status: **0** successful/clean,
**1** findings (where applicable), **2** invalid input or operational error.
Use `--help` for the full CLI contract. Inputs are local files; no telemetry or network calls.

## Scope and limitations

Comma-separated UTF-8 only (BOM accepted). Snapshots and results are held in memory. Values remain strings; tolerances apply only when both changed values parse as finite decimals. Tolerances are absolute, not relative. No automatic key inference. Schema differences are reported separately; only common columns are compared per row. Output includes input record values. Precision alignment or exponent magnitude beyond 10000 digits is rejected.

## Related work

[csv-diff](https://github.com/simonw/csv-diff) and [csvdiff](https://github.com/aswinkarthik/csvdiff) offer mature snapshot comparison.

The release combines explicit duplicate-key rejection and exact decimal tolerance rules in a zero-runtime-dependency workflow. This is a focused alternative, not a claim of feature superiority or global uniqueness.
Implementation is original; no upstream code was copied.

## Development and validation

```console
python -m unittest discover -s tests -v
```

Local release verification passed **10 unit tests**, package/binary build, installed CLI help, the documented example and a missing-input error path on Windows amd64. See [VALIDATION.txt](VALIDATION.txt) for actual output. CI is configured for
Linux, macOS and Windows; a workflow file is not evidence of a successful hosted run.
Large-scale performance and production integrations have not been validated.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Small reproductions and real workflow feedback
are especially useful. See [LAUNCH.md](LAUNCH.md) for an opt-in community introduction plan.

## License and history

MIT; see [LICENSE](LICENSE). Commits use actual creation times. History is not reconstructed
or backdated. Version 0.1.0 is a small complete implementation, not a promise of future features.
