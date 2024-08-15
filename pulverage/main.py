from lxml import etree


def parse_git_diff(diff_file_path):
    parsed_result = {}
    with open(diff_file_path) as diff_file:
        current_file = None
        current_line_number = -1
        end_line = None
        for line in diff_file:
            if current_line_number > -1:
                current_line_number += 1
                if current_line_number == end_line:
                    current_line_number = None
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
                parsed_result[current_file] = set()
                continue
            if line.startswith("@@"):
                line_changes_coordinates = line.split()[2]
                start_line, line_count = map(int, line_changes_coordinates[1:].split(","))
                end_line = start_line + line_count
                current_line_number = start_line - 1
                continue
            if current_line_number > -1 and line.startswith("+"):
                parsed_result[current_file].add(current_line_number)
                continue



    return parsed_result


def parse_coverage(files_to_get_coverage: set[str], coverage_file_path: str):
    parse_result = {}
    with open(coverage_file_path) as coverage_file:
        tree = etree.parse(coverage_file)
        root = tree.getroot()
        for file in files_to_get_coverage:
            parse_result[file] = set()
            for line in root.xpath(f'//*[name()="class" and @filename="{file}"]/lines')[0]:
                if int(line.attrib["hits"]) == 0:
                    # adds uncovered lines to the set
                    parse_result[file].add(int(line.attrib["number"]))

    return parse_result


def compare_coverage(parsed_diff, parsed_coverage):
    uncovered_lines_in_diff = {}
    for filename, changed_lines in parsed_diff.items():
        if filename in parsed_coverage:
            uncovered_lines = parsed_coverage[filename]
            uncovered_lines_in_diff[filename] = changed_lines & uncovered_lines
    return uncovered_lines_in_diff


def compute_missing_coverage(path_to_diff, path_to_coverage):
    parsed_diff = parse_git_diff(path_to_diff)
    parsed_coverage = parse_coverage(set(parsed_diff.keys()), path_to_coverage)
    coverage_diff = compare_coverage(parsed_diff, parsed_coverage)
    return coverage_diff
