from collections import defaultdict

from lxml import etree
from lxml.etree import _Element

from pulverage.diff_parser import parse_git_diff


def parse_coverage(
    files_to_get_coverage: set[str], coverage_file_path: str
) -> dict[str, set[int]]:
    parse_result = defaultdict(set)
    with open(coverage_file_path, encoding="utf-8") as coverage_file:
        tree = etree.parse(coverage_file)
        root = tree.getroot()
        for file in files_to_get_coverage:
            lines_element = root.xpath(
                f'//*[name()="class" and @filename="{file}"]/lines'
            )
            if lines_element and isinstance(lines_element, list):
                for line in lines_element[0]:
                    if isinstance(line, _Element) and not int(line.attrib["hits"]):
                        # adds not covered lines to the set
                        parse_result[file].add(int(line.attrib["number"]))

    return parse_result


def compare_coverage(
    parsed_diff: dict[str, set[int]], parsed_coverage: dict[str, set[int]]
) -> dict[str, set[int]]:
    not_covered_lines_in_diff = {}
    for filename, changed_lines in parsed_diff.items():
        if filename in parsed_coverage:
            not_covered_lines = parsed_coverage[filename]
            not_covered_lines_in_diff[filename] = changed_lines & not_covered_lines
    return not_covered_lines_in_diff


def compute_missing_coverage(
    path_to_diff: str, path_to_coverage: str
) -> dict[str, set[int]]:
    parsed_diff = parse_git_diff(path_to_diff)
    parsed_coverage = parse_coverage(set(parsed_diff.keys()), path_to_coverage)
    coverage_diff = compare_coverage(parsed_diff, parsed_coverage)
    return coverage_diff
