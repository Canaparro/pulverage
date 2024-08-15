from collections import defaultdict

from lxml import etree
from lxml.etree import _Element


def parse_coverage(
    files_to_get_coverage: set[str], coverage_file_path: str
) -> dict[str, set[int]]:
    """
    Parses a coverage xml file and extracts the uncovered lines of code
    for a set of files.

    :param files_to_get_coverage:
    :param coverage_file_path:
    :return: a dictionary with the uncovered lines of code for each file
    """
    with open(coverage_file_path, encoding="utf-8") as coverage_file:
        parse_result: dict[str, set[int]] = defaultdict(set)
        tree = etree.parse(coverage_file)
        root = tree.getroot()
        for filename in files_to_get_coverage:
            parse_result[filename] = get_uncovered_lines(filename, root)

        return parse_result


def get_uncovered_lines(filename: str, root: _Element) -> set[int]:
    """
    Locates and extracts line numbers for uncovered lines of code
    from a coverage xml root element.
    :param filename:
    :param root:
    :return: a set of line numbers for uncovered lines of code
    """
    lines_element = root.find(f".//class[@filename='{filename}']/lines")
    uncovered_lines: set[int] = set()
    if lines_element:
        for line in lines_element:
            if not int(line.attrib["hits"]):
                uncovered_lines.add(int(line.attrib["number"]))
    return uncovered_lines
