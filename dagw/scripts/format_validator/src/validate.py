import argparse
import logging
from pathlib import Path
import sys
from typing import List

from validators import TestReport, check_utf8_encoding, tests


class ParserWithUsage(argparse.ArgumentParser):
    """ A custom parser that writes error messages followed by command line usage documentation."""

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO,
                        datefmt='%m/%d/%Y %H:%M:%S')
    parser = ParserWithUsage()
    parser.description = "Validates a specific section of DKGW"
    parser.add_argument("input",
                        help="Path to directory containing the section")
    parser.add_argument("--check_enc", action="store_true", default=False,
                        help="Check that files are UTF-8 encoded (slow).")

    args = parser.parse_args()
    logging.info("STARTED")
    path: Path = Path(args.input)
    check_enc = args.check_enc
    logging.info("Validating section " + path.name)
    raw_data = path / "raw_data"
    metadata_file = path / f"{path.name}.jsonl"
    if raw_data.exists() and raw_data.is_dir() and not metadata_file.exists():
        logging.info(
            "The section appears to have a \"raw_data\" directory whose content has not been "
            "expanded. Stopping validation until the section is expanded.")
    else:
        validators = tests
        if not check_enc:
            logging.info("Skipping encoding validation")
            validators.remove(check_utf8_encoding)

        results: List[TestReport] = [func(path) for func in tests]

        tests_passed: List[TestReport] = [t for t in results if t.passed is True]
        tests_failed: List[TestReport] = [t for t in results if t.passed is False]
        total_tests: int = len(tests_failed) + len(tests_passed)
        logging.info(
            f"Passed {len(tests_passed)} of {total_tests} tests: {[t.test_name for t in tests_passed]}")
        logging.info(
            f"Failed {len(tests_failed)} of {total_tests} tests: {[t.test_name for t in tests_failed]}")

        for t in results:
            for m in t.fail_messages:
                logging.error(m)

        if len(tests_failed):
            exit(1)

    logging.info("DONE")


if __name__ == "__main__":
    main()
