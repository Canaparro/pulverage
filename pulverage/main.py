from pulverage.coverage_parser import parse_coverage
from pulverage.diff_parser import parse_git_diff


def compare_coverage(
    parsed_diff: dict[str, set[int]], parsed_coverage: dict[str, set[int]]
) -> dict[str, set[int]]:
    """
    Compares the parsed diff and coverage information to find the lines
    that were changed but were not covered by tests.

    :param parsed_diff:
    :param parsed_coverage:
    :return: a dictionary with the lines that were changed but not covered for each file
    """
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
