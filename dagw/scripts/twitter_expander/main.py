"""
Turns tweets from a hydrated jsonl file into a DAGW section.
"""
import argparse
import json
import logging
from pathlib import Path
import shutil
import sys

import arrow

import meta
from meta import get_meta_object


class ParserWithUsage(argparse.ArgumentParser):
    """ A custom parser that writes error messages followed by command line usage documentation."""

    def error(self, message) -> None:
        """
        Prints error message and help.
        :param message: error message to print
        """
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    """
    Main method
    """
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        datefmt='%m/%d/%Y %H:%M:%S')
    parser = ParserWithUsage()
    parser.description = "Turns tweets from a hydrated jsonl file into a DAGW section"
    parser.add_argument("--input", help="Input file", required=True, type=Path)
    parser.add_argument("--section_name", help="Name of resulting section", required=True, type=str)
    parser.add_argument("--output", help="Output directory", required=True, type=Path)

    args = parser.parse_args()
    input_file = args.input
    output_dir = args.output
    logging.info("STARTED")
    logging.info(f"Will read tweets from JSONL file: {input_file}")
    namespace: str = args.section_name

    if output_dir.exists():
        shutil.rmtree(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=False)

    metadata = []
    date_format = "%c %Z %z"

    license_file = output_dir / "LICENSE"
    with license_file.open(mode="w", encoding="utf8") as o:
        o.write(
            "The use of this section is described in the Twitter Terms of Service and Twitter "
            "Developer Agreement.")

    with input_file.open(mode="r") as in_file:
        doc_id = f"{namespace}_0"
        meta_object = get_meta_object()
        meta_object[meta.KEY_URI] = "https://twitter.com"
        meta_object[meta.KEY_DOC_ID] = doc_id
        meta_object[meta.KEY_DATE_BUILT] = arrow.now().replace(
            tzinfo="Europe/Copenhagen").strftime(date_format)
        metadata.append(meta_object)
        out_file = output_dir / doc_id
        with out_file.open(mode="w", encoding="utf8") as o:
            for idx, line in enumerate(in_file):
                if idx % 1_000 == 0:
                    logging.info(f"Processing tweet: {idx}")
                doc = json.loads(line)
                text_content = doc["full_text"]
                text_content = text_content.rstrip()
                text_content = text_content.replace("\n", " ")
                if len(text_content) > 0:
                    o.write(text_content)
                    o.write("\n")

    output_path_meta = output_dir / f"{namespace}.jsonl"
    with output_path_meta.open("w", encoding="utf8") as out_meta:
        for m in metadata:
            line = json.dumps(m)
            out_meta.write(line)
            out_meta.write("\n")

    logging.info("DONE")


if __name__ == "__main__":
    main()
