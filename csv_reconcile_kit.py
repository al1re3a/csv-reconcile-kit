"""Reconcile UTF-8 CSV snapshots with composite keys and decimal tolerances."""
import argparse
import csv
import json
import sys
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path

def load(path, keys):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.reader(handle, strict=True)
        header = next(reader, None)
        if not header or any(not h for h in header) or len(set(header)) != len(header):
            raise ValueError('CSV requires unique nonempty column names')
        if not keys or len(set(keys)) != len(keys) or set(keys) - set(header):
            raise ValueError('key columns must be unique and present in both files')
        records = {}
        for row in reader:
            if len(row) != len(header):
                raise ValueError(f'row width differs at line {reader.line_num}')
            record = dict(zip(header, row))
            key = tuple(record[k] for k in keys)
            if any(not value for value in key):
                raise ValueError(f'empty key at line {reader.line_num}')
            if key in records:
                raise ValueError(f'duplicate key at line {reader.line_num}')
            records[key] = record
        return header, records

def close_enough(left, right, tolerance):
    try:
        a, b = Decimal(left), Decimal(right)
        if not a.is_finite() or not b.is_finite():
            return False
        if any(abs(n.as_tuple().exponent) > 10000 or abs(n.adjusted()) > 10000 for n in (a, b)):
            raise ValueError('numeric exponent exceeds supported 10000-digit range')
        # Precision includes alignment between exponents, avoiding binary-float rounding.
        precision = max(len(a.as_tuple().digits), len(b.as_tuple().digits)) + abs(a.as_tuple().exponent - b.as_tuple().exponent) + 2
        if precision > 10000:
            raise ValueError('numeric precision exceeds 10000 digits')
        with localcontext() as ctx:
            ctx.prec = max(28, precision)
            return abs(a - b) <= tolerance
    except InvalidOperation:
        return False

def reconcile(before, after, keys, ignore=(), tolerances=None):
    tolerances = tolerances or {}
    left_cols, left = load(before, keys)
    right_cols, right = load(after, keys)
    all_cols = set(left_cols) | set(right_cols)
    if (set(ignore) | set(tolerances)) - all_cols:
        raise ValueError('ignore/tolerance references an unknown column')
    if set(keys) & (set(ignore) | set(tolerances)):
        raise ValueError('key columns cannot be ignored or given a tolerance')
    for value in tolerances.values():
        if not value.is_finite() or value < 0:
            raise ValueError('tolerances must be finite and nonnegative')
    changes = []
    columns = sorted((set(left_cols) & set(right_cols)) - set(keys) - set(ignore))
    for key in sorted(left.keys() & right.keys()):
        fields = {}
        for column in columns:
            a, b = left[key][column], right[key][column]
            if a != b and not (column in tolerances and close_enough(a, b, tolerances[column])):
                fields[column] = {'before': a, 'after': b}
        if fields:
            changes.append({'key': list(key), 'fields': fields})
    return {
        'added': [right[k] for k in sorted(right.keys() - left.keys())],
        'removed': [left[k] for k in sorted(left.keys() - right.keys())],
        'changed': changes,
        'columns_added': sorted(set(right_cols) - set(left_cols) - set(ignore)),
        'columns_removed': sorted(set(left_cols) - set(right_cols) - set(ignore)),
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before')
    parser.add_argument('after')
    parser.add_argument('--key', action='append', required=True, help='repeat for composite keys')
    parser.add_argument('--ignore', action='append', default=[])
    parser.add_argument('--tolerance', action='append', default=[], metavar='COLUMN=DECIMAL')
    args = parser.parse_args(argv)
    try:
        tolerances = {}
        for item in args.tolerance:
            col, sep, value = item.partition('=')
            if not sep or not col or col in tolerances:
                raise ValueError('expected a unique COLUMN=DECIMAL tolerance')
            tolerances[col] = Decimal(value)
        report = reconcile(args.before, args.after, args.key, args.ignore, tolerances)
        print(json.dumps(report, ensure_ascii=True, indent=2))
        return int(any(report.values()))
    except (OSError, UnicodeError, ValueError, csv.Error, InvalidOperation) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
