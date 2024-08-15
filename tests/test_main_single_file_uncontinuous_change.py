import os

from pulverage import main

current_folder = os.path.dirname(os.path.abspath(__file__))


def test_parse_git_diff():
    diff_path = os.path.join(
        current_folder, "resources/single_file_uncontinuous_change/changes.diff"
    )
    parsed_result = main.parse_git_diff(diff_path)
    assert parsed_result == {"token_store/service/module1.py": {7, 8, 9, 13, 14, 15}}


def test_parse_coverage():
    coverage_path = os.path.join(
        current_folder, "resources/single_file_uncontinuous_change/coverage.xml"
    )
    parse_result = main.parse_coverage(
        {"token_store/service/module1.py"}, coverage_path
    )
    assert parse_result == {"token_store/service/module1.py": {9, 12, 15}}


def test_main():
    diff_path = os.path.join(
        current_folder, "resources/single_file_uncontinuous_change/changes.diff"
    )
    coverage_path = os.path.join(
        current_folder, "resources/single_file_uncontinuous_change/coverage.xml"
    )
    coverage_diff = main.compute_missing_coverage(diff_path, coverage_path)
    assert coverage_diff == {"token_store/service/module1.py": {9, 15}}
