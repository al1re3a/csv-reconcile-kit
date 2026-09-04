# csv-reconcile-kit

[![CI](https://github.com/al1re3a/csv-reconcile-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/al1re3a/csv-reconcile-kit/actions/workflows/ci.yml)

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
