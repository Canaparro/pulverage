from pulverage import main


def test_parse_git_diff():
    parsed_result = main.parse_git_diff(
        "resources/multiple_files_single_hunk_changes/changes.diff"
    )
    assert parsed_result == {
        "src/module1.py": {10, 11, 12, 13, 14},
    }


def test_parse_coverage():
    parse_result = main.parse_coverage(
        {"src/module1.py"},
        "resources/multiple_files_single_hunk_changes/coverage.xml",
    )
    assert parse_result == {"src/module1.py": {9, 13, 17, 20}}


def test_main():
    coverage_diff = main.compute_missing_coverage(
        "resources/multiple_files_single_hunk_changes/changes.diff",
        "resources/multiple_files_single_hunk_changes/coverage.xml",
    )
    assert coverage_diff == {"src/module1.py": {13}}
