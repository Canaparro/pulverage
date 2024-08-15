import os

from pulverage import main

current_folder = os.path.dirname(os.path.abspath(__file__))


def test_parse_git_diff():
    diff_path = os.path.join(
        current_folder, "resources/single_file_two_hunks_changes/changes.diff"
    )
    parsed_result = main.parse_git_diff(diff_path)
    assert parsed_result == {"src/module1.py": {*range(1, 18), *range(32, 52)}}


def test_parse_coverage():
    coverage_path = os.path.join(
        current_folder, "resources/single_file_two_hunks_changes/coverage.xml"
    )
    parse_result = main.parse_coverage({"src/module1.py"}, coverage_path)
    assert parse_result == {"src/module1.py": {6, 11, 16, 25, 28, 31, 36, 41, 46, 51}}


def test_main():
    diff_path = os.path.join(
        current_folder, "resources/single_file_two_hunks_changes/changes.diff"
    )
    coverage_path = os.path.join(
        current_folder, "resources/single_file_two_hunks_changes/coverage.xml"
    )
    coverage_diff = main.compute_missing_coverage(diff_path, coverage_path)
    assert coverage_diff == {"src/module1.py": {6, 11, 16, 36, 41, 46, 51}}
