from pulverage import main


def test_parse_git_diff():
    parsed_result = main.parse_git_diff("resources/single_file_uncontinuous_change/changes.diff")
    assert parsed_result == {
        'token_store/service/module1.py': {range(4, 16)}
    }


def test_parse_coverage():
    parse_result = main.parse_coverage({"token_store/service/module1.py"},
                                       "resources/single_file_uncontinuous_change/coverage.xml")
    assert parse_result == {
        'token_store/service/module1.py': {
            9, 12, 15
        }
    }


def test_main():
    coverage_diff = main.compute_missing_coverage("resources/single_file_uncontinuous_change/changes.diff",
                                                  "resources/single_file_uncontinuous_change/coverage.xml")
    assert coverage_diff == {
        'token_store/service/module1.py': {
            9, 15
        }
    }
