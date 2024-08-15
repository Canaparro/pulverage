from collections import defaultdict

from lxml import etree
from lxml.etree import _Element


def parse_git_diff(diff_file_path: str) -> dict[str, set[int]]:
    parsed_result = defaultdict(set)
    with open(diff_file_path, encoding="utf-8") as diff_file:
        current_file = None
        current_line_number = -1
        end_line = None
        for line in diff_file:
            if current_line_number > -1:
                current_line_number += 1
                if current_line_number == end_line:
                    current_line_number = -1
                    current_file = None
                    end_line = None
            if line.startswith("+++ b/") and line.endswith(".py\n"):
                current_file = line[6:].strip()
                continue
            if not current_file:
                continue
            if line.startswith("@@"):
                line_changes_coordinates = line.split()[2]
                start_line, line_count = map(
                    int, line_changes_coordinates[1:].split(",")
                )
                end_line = start_line + line_count
                current_line_number = start_line - 1
                continue
            if current_line_number > -1 and line.startswith("+"):
                parsed_result[current_file].add(current_line_number)
                continue
            if current_line_number > -1 and line.startswith("-"):
                current_line_number -= 1
                continue
            if current_line_number > -1 and line == "\\ No newline at end of file\n":
                current_line_number -= 1

    return parsed_result


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
