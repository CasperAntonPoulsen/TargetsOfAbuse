"""
Contains validators for the DAGW format.
"""
from dataclasses import dataclass, field
import datetime
import json
from pathlib import Path
import re
from typing import List, Set, Tuple


class Meta:
    """
    Models the metadata.
    """

    class Field:
        """
        Keys in the metadata object"
        """
        DOC_ID: str = "doc_id"
        YEAR_PUBLISHED: str = "year_published"
        DATE_BUILT: str = "date_built"
        LOCATION_NAME: str = "location_name"
        LOCATION_LATLONG: str = "location_latlong"
        DATE_COLLECTED: str = "date_collected"
        DATE_PUBLISHED: str = "date_published"
        URI: str = "uri"

    REQUIRED_FIELDS = {Field.DOC_ID}
    OPTIONAL_FIELDS: Set[str] = {Field.YEAR_PUBLISHED, Field.DATE_BUILT,
                                 Field.LOCATION_NAME, Field.LOCATION_LATLONG,
                                 Field.DATE_COLLECTED}
    PREFERRED_FIELDS: Set[str] = {Field.DATE_PUBLISHED, Field.URI}
    ALL_FIELDS = REQUIRED_FIELDS.union(OPTIONAL_FIELDS).union(PREFERRED_FIELDS)


@dataclass
class TestReport:
    """
    Models test reports.
    """
    test_name: str
    passed: bool = True
    fail_messages: List[str] = field(default_factory=list)

    def __iadd__(self, o):
        self.passed = self.passed and o.passed
        if not o.passed and len(o.fail_messages) > 0:
            self.fail_messages += o.fail_messages
        return self


def check_correct_prefix(p: Path) -> TestReport:
    """
    Checks that all non-auxiliary files' names start with the namespace
    :param p: path to check
    :return: a test report
    """
    namespace = p.name
    t = TestReport(test_name="Content files prefix")
    auxiliary_files, _ = get_auxiliary_files(namespace)
    for child in p.iterdir():
        if child.name not in auxiliary_files and child.is_file() and not child.name.startswith(
                namespace):
            t.passed = False
            msg = f"The name of file {child} should start with the namespace {namespace}"
            t.fail_messages.append(msg)
    return t


def get_auxiliary_files(namespace: str) -> Tuple[List[str], List[bool]]:
    """
    Returns a list of auxiliary files for a namespace.
    :param namespace:
    :return: list of expected auxiliary files
    """
    auxiliary_files = [f"{namespace}.jsonl", "LICENSE", "raw_data", "talere.json"]
    required_flag = [True, True, False, False]
    return auxiliary_files, required_flag


def check_auxiliary_files(p: Path) -> TestReport:
    """
    Checks that all required auxiliary files exist.
    :param p: path to check
    :return: test report
    """
    namespace = p.name
    t = TestReport(test_name="Auxiliary files")
    auxiliary_files, req_info = get_auxiliary_files(namespace)
    for f, r in zip(auxiliary_files, req_info):
        meta_path = p / f
        if not meta_path.exists() and r:
            t.passed = False
            msg = f"File {f} does not exist"
            t.fail_messages.append(msg)
    return t


def check_set(file_set, error_msg) -> TestReport:
    """
    Checks that the given set is empty.
    :param file_set: set to check
    :param error_msg: a template error message
    :return: a test report
    """
    t = TestReport(test_name="")
    if len(file_set) > 0:
        t.passed = False
        for f in file_set:
            t.fail_messages.append(error_msg.format(f))
    return t


def check_all_files_in_metadata(p: Path) -> TestReport:
    """
    Checks that all the files in the metadata exist.
    :param p: path to check
    :return: test report
    """
    namespace = p.name
    t = TestReport(test_name="Test files manifest")
    expected_doc_ids: Set[str] = set()
    actual_doc_ids: Set[str] = {c.name for c in p.iterdir()}
    auxiliary_files, _ = get_auxiliary_files(p.name)
    auxiliary_files = set(auxiliary_files)
    meta_file = p / f"{namespace}.jsonl"
    if meta_file.exists():
        with meta_file.open(mode="r") as in_meta:
            for line in in_meta:
                current_meta = json.loads(line)
                doc_id = current_meta[Meta.Field.DOC_ID]
                expected_doc_ids.add(doc_id)

        undeclared = actual_doc_ids - expected_doc_ids - auxiliary_files
        nonexistent = expected_doc_ids - actual_doc_ids
        shared = actual_doc_ids.intersection(expected_doc_ids)
        t.passed += len(shared)
        msg_undeclared = "File {} not declared in meta file"
        msg_nonexistent = "File {} declared in meta file, but does not exist"

        t += check_set(undeclared, msg_undeclared)
        t += check_set(nonexistent, msg_nonexistent)
    else:
        t.passed = False
        t.fail_messages.append(f"Could not find metadata file {str(meta_file)}")
    return t


matcher_Z = re.compile(r"[A-Z]{3}")  # tz name
matcher_z = re.compile(r"[+-]\d{4}")  # tz offset
matcher_year = re.compile(r"\s([\d]{4})")  # find year
msg_year = "Year {} is higher than current year {} in meta date: {}"
msg_missing_Z = "Missing timezone as string from meta date: {}"
msg_missing_z = "Missing timezone as offset from meta date: {}"
msg_missing_Y = "Missing year in meta date: {}"


def check_datetime(s: str) -> TestReport:
    """
    Checks the dates and times
    :param s: string to check
    :return: test report
    """

    # Time zone checks are done by regular expression since danish locale is
    # inconsistent across OS'es (Linux vs macOS)

    t = TestReport(test_name="")
    if s is not None:
        m = matcher_z.search(s)
        if m is None:
            t.passed = False
            t.fail_messages.append(msg_missing_z.format(s))
        m = matcher_year.search(s)
        if m is None:
            t.passed = False
            t.fail_messages.append(msg_missing_Y.format(s))
        else:
            current_year: int = int(datetime.datetime.now().strftime("%Y"))
            year = m.group(1)
            year = int(year)
            if year > current_year:
                t.passed = False
                t.fail_messages.append(msg_year.format(year, current_year, s))
    return t


def check_metadata_fields(p: Path) -> TestReport:
    """
    Checks every field in metadata
    :param p: path to check
    :return: a test report
    """
    current_year: int = int(datetime.datetime.now().strftime("%Y"))
    namespace = p.name
    t = TestReport(test_name="Fields in metadata")
    meta_file = p / f"{namespace}.jsonl"
    if meta_file.exists():
        with meta_file.open("r") as in_meta:
            for line in in_meta:
                current_meta = json.loads(line)
                doc_id = current_meta[Meta.Field.DOC_ID]
                keys = set(current_meta.keys())
                missing_required = Meta.REQUIRED_FIELDS - keys
                required_msg = "Metadata missing field {{}} for doc_id = {d}"
                t += check_set(missing_required, required_msg.format(d=doc_id))

                illegal_fields = keys - Meta.ALL_FIELDS
                illegal_msg = "Metadata contains undocumented field {{}} for doc_id = {d}"
                t += check_set(illegal_fields, illegal_msg.format(d=doc_id))

                # Check year published
                year_published = current_meta.get(Meta.Field.YEAR_PUBLISHED,
                                                  None)
                if year_published is not None:
                    year_published = int(year_published)
                    if year_published > current_year:
                        t.passed = False
                        t.fail_messages.append(
                            f"{Meta.Field.YEAR_PUBLISHED}: {year_published} is in the future!")

                # Check all dates for correct content
                date_built = current_meta.get(Meta.Field.DATE_BUILT, None)
                t += check_datetime(date_built)

                date_collected = current_meta.get(Meta.Field.DATE_COLLECTED,
                                                  None)
                t += check_datetime(date_collected)

                date_published = current_meta.get(Meta.Field.DATE_PUBLISHED,
                                                  None)
                t += check_datetime(date_published)
    else:
        t.passed = False
        t.fail_messages.append(f"Could not find metadata file {str(meta_file)}")
    return t


def check_utf8_encoding(path: Path) -> TestReport:
    t = TestReport(test_name="UTF-8 encoding")
    from chardet.universaldetector import UniversalDetector
    err_msg = "File {} is not UTF-8 encoded, but {} (confidence: {:.2f})"
    accepted_encs = {"ascii", "utf-8"}
    detector = UniversalDetector()
    max_lines = 50
    for file in path.iterdir():
        detector.reset()
        for idx, line in enumerate(file.open("rb")):
            detector.feed(line)
            if detector.done or idx > max_lines:
                break
        detector.close()
        actual_enc = detector.result["encoding"]
        if actual_enc not in accepted_encs:
            conf = detector.result["confidence"]
            t.passed = False
            name = file.name
            t.fail_messages.append(err_msg.format(name, actual_enc, conf))
    return t


tests = [check_correct_prefix, check_auxiliary_files,
         check_all_files_in_metadata, check_metadata_fields,
         check_utf8_encoding]
