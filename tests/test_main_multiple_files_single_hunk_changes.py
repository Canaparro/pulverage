import os

from pulverage import main

current_folder = os.path.dirname(os.path.abspath(__file__))


def test_parse_git_diff():
    diff_path = os.path.join(
        current_folder, "resources/multiple_files_single_hunk_changes/changes.diff"
    )
    parsed_result = main.parse_git_diff(diff_path)
    assert parsed_result == {
        "src/module1.py": {10, 11, 12, 13, 14},
    }


def test_parse_coverage():
    coverage_path = os.path.join(
        current_folder, "resources/multiple_files_single_hunk_changes/coverage.xml"
    )
    parse_result = main.parse_coverage({"src/module1.py"}, coverage_path)
    assert parse_result == {"src/module1.py": {9, 13, 17, 20}}


def test_main():
    diff_path = os.path.join(
        current_folder, "resources/multiple_files_single_hunk_changes/changes.diff"
    )
    coverage_path = os.path.join(
        current_folder, "resources/multiple_files_single_hunk_changes/coverage.xml"
    )
    coverage_diff = main.compute_missing_coverage(diff_path, coverage_path)
    assert coverage_diff == {"src/module1.py": {13}}
