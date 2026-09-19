"""Validate the checked-in vehicle catalog."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow the script to be run directly from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from catalog import CatalogError, load_catalog


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a vehicle catalog")
    parser.add_argument("path", nargs="?", type=Path, help="catalog JSON path")
    args = parser.parse_args(argv)
    try:
        catalog = load_catalog(args.path)
    except CatalogError as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(f"Valid catalog: {len(catalog['vehicles'])} vehicles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
