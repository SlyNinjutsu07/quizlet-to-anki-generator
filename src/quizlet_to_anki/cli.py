"""Command-line entry point: runs the scraper, then the converter."""
import argparse

def run_generation(next_data_json):
    
    ...

def main() -> None:
    parser = argparse.ArgumentParser(prog="qta")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("test-wiring", help="tests scraper + converter capability and returns True if an apkg was generated from sample data")
    args = parser.parse_args()

    if args.command == 'test-wiring':


if __name__ == "__main__":
    main()
