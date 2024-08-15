from collections import defaultdict

PYTHON_FILE_TOKEN = ".py\n"

HUNK_HEADER_TOKEN = "@@"

NEW_FILE_TOKEN = "+++ b/"


def parse_git_diff(diff_file_path: str) -> dict[str, set[int]]:
    with open(diff_file_path, encoding="utf-8") as diff_file:
        parsed_result: dict[str, set[int]] = defaultdict(set)
        current_file = None
        current_line_number = -1
        end_line = None
        for line in diff_file:
            if not current_file:
                if line.startswith(NEW_FILE_TOKEN) and line.endswith(PYTHON_FILE_TOKEN):
                    current_file = line[6:].strip()
            elif line.startswith(HUNK_HEADER_TOKEN):
                current_line_number, end_line = parse_hunk_start_and_end(line)
            elif current_line_number > -1:
                current_line_number = evaluate_diff_line(
                    parsed_result[current_file], current_line_number, line
                )
                if current_line_number == end_line + 1:
                    current_line_number = -1
                    current_file = None
                    end_line = None

        return parsed_result


def parse_hunk_start_and_end(line: str) -> tuple[int, int]:
    """
    Extracts the start and end line of a hunk from a diff line.
    Hunks look like this: @@ -1,6 +1,7 @@ where the first tuple
    corresponds to the original file and the second to the new file.
    The first and second integers in a tuple correspond to the start
    and the number of lines in the hunk.

    :param line:
    :return a tuple with the start and end line of the hunk:
    """
    line_changes_coordinates = line.split()[2]
    start_line, line_count = map(int, line_changes_coordinates[1:].split(","))
    end_line = start_line + line_count
    return start_line, end_line


def evaluate_diff_line(
    current_file_line_set: set[int], current_line_number: int, line: str
) -> int:
    if line.startswith("+"):
        current_file_line_set.add(current_line_number)
    elif line.startswith("-"):
        current_line_number -= 1
    return current_line_number + 1
