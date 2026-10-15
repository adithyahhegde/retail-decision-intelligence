"""Run a synthetic fixture report without downloads, secrets or paid services."""

import json
import argparse
from pathlib import Path
from .analytics import categories, connect, load, skus
from .intake import MAX_BYTES, IntakeError, import_csv
from .fixtures import history


def _read_bounded(path: str) -> bytes:
    with Path(path).open("rb") as stream:
        payload = stream.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise IntakeError("CSV file exceeds 2 MiB")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--products", help="Products CSV path; pair with --lines")
    parser.add_argument("--lines", help="Order lines CSV path; pair with --products")
    parser.add_argument("--history", action="store_true", help="Use 90-day synthetic history")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start")
    parser.add_argument("--end")
    args = parser.parse_args()
    if bool(args.products) != bool(args.lines) or (args.history and args.products):
        parser.error("Pair --products and --lines; do not combine files with --history")
    if args.products and (not args.start or not args.end):
        parser.error("CSV reports require explicit --start and --end")
    start = args.start or ("2026-01-01" if args.history else "2026-09-01")
    end = args.end or ("2026-03-31" if args.history else "2026-09-30")
    with connect() as connection:
        provenance = None
        if args.products or args.history:
            try:
                payloads = history(args.seed) if args.history else (
                    _read_bounded(args.products), _read_bounded(args.lines))
                provenance = import_csv(connection, *payloads)
            except (ValueError, OSError) as exc:
                parser.error(str(exc))
        else:
            load(connection, [("TEA", "Beverages"), ("SOAP", "Personal care")], [
                ("L1", "2026-09-01", "TEA", 10, 2, 10000, 10000, 5000, 3000),
                ("L2", "2026-09-02", "SOAP", 5, 0, 20000, 0, 12000, 5000),
            ])
        try:
            category_rows = categories(connection, start, end)
            sku_rows = skus(connection, start, end)
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps({
            "data_kind": "user_supplied_unverified" if args.products else "synthetic_fixture",
            "currency": "INR", "money_unit": "paise",
            "start": start, "end": end, "provenance": provenance,
            "seed": args.seed if args.history else None,
            "categories": category_rows, "skus": sku_rows,
        }, indent=2))


if __name__ == "__main__":
    main()
