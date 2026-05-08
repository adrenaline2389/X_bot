from __future__ import annotations

import argparse
import traceback

from x_bot.features import price_report, whale_alert


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an X Bot feature.")
    parser.add_argument(
        "command",
        choices=("price-report", "whale-alert"),
        help="Feature to run.",
    )
    args = parser.parse_args(argv)

    try:
        if args.command == "price-report":
            price_report.run()
        elif args.command == "whale-alert":
            whale_alert.run()
    except Exception as exc:
        print(f"::error::x_bot {args.command} failed: {exc}")
        traceback.print_exc()
        return 1

    return 0
