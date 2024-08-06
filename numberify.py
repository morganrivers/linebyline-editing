import re
import sys
import os


def get_filename_without_extension(file_path):
    """
    Extract the filename without its extension.

    Args:
        file_path (str): The full path of the file.

    Returns:
        str: The filename without its extension.
    """

    basename = os.path.basename(file_path)  # Get the filename with extension
    filename_without_extension, _ = os.path.splitext(basename)  # Split the extension
    return filename_without_extension


def number_sentences(text):
    """
    Split the text into sentences, number them, and store their positions.

    Args:
        text (str): The input text to be split into sentences.

    Returns:
        tuple: A tuple containing a list of numbered sentences and a list of their positions.
    """
    regex_match = r"(\n|\. |\? |\! )"
    # Using a capturing group to keep delimiters in the output
    parts = re.split(regex_match, text)

    numbered = []
    reconstructor = []
    start = 0

    # Process parts to form numbered sentences
    for i in range(
        0, len(parts), 2
    ):  # Step by 2 to handle sentence followed by delimiter
        sentence = parts[i]
        if i == len(parts) - 1:
            delimiter = ""
            len_delimiter = 0
            delimiter_is_punctuation = False
        else:
            delimiter = parts[i + 1]
            len_delimiter = len(delimiter)
            if "." in delimiter:
                sentence = sentence + "."
                delimiter_is_punctuation = True
            elif "?" in delimiter:
                sentence = sentence + "?"
                delimiter_is_punctuation = True
            elif "!" in delimiter:
                sentence = sentence + "!"
                delimiter_is_punctuation = True
            else:
                delimiter_is_punctuation = False

        length = len(sentence)

        numbering = f"{i//2 + 1}. "
        length_numbering = len(numbering)
        numbered.append(f"{numbering}{sentence}")
        reconstructor.append(
            {
                "start_position": start,
                "line_number": i // 2,
                "length": length,
                "length_numbering": length_numbering,
                "delimiter_is_punctuation": delimiter_is_punctuation,
            }
        )
        start += (
            length + len_delimiter
        )  # +1 for the fact that split always removes one character

    return numbered, reconstructor


def preprocess_edited_text(filename, n_lines):
    """
    Preprocess the edited text to check for format errors and autocorrect them if possible.

    Args:
        filename (str): The name of the file to preprocess.
        n_lines (int): The expected number of lines in the file.

    Returns:
        tuple: A tuple containing a boolean indicating if there were errors, and the new number of lines in the file.
    """

    with open(filename, "r") as file:
        lines = file.readlines()
    original_text = "".join(lines)

    processed_lines = []
    expected_line_number = 1
    ask_user_to_correct_errors = False
    current_line_number = 0  # Initialize to zero
    error_messages = []
    for index, line in enumerate(
        lines, start=1
    ):  # Start counting from 1 for user-friendly line numbers
        # remove the newline after each line for processing.
        line = line.rstrip("\n")

        # Strip whitespace to check for empty lines
        stripped_line = line.strip()
        if not stripped_line:
            continue  # Skip empty lines

        # Check if the line starts correctly with "number. "
        if not line.split(". ")[0].isdigit() or not line.startswith(
            line.split(". ")[0] + ". "
        ):
            error_messages.append(
                f"Error on line {index}: Line format is incorrect -> '{line}'. Expected format: '<number>. <text>'.",
            )
            error_messages.append("\t -> The space after the first '.' is required.")
            ask_user_to_correct_errors = True  # Skip lines with incorrect format
            expected_line_number += 1
            continue  # the rest of the loop is just for throwing errors

        # Extract the line number from the beginning of the line
        current_line_number = int(line.split(". ")[0])

        # exit the loop if we somehow have a next line lower than the current line...
        if current_line_number < expected_line_number:
            error_messages.append(f"Error on line {index}:  -> '{line}':")
            error_messages.append(
                "\t -> The line numbers cannot decrease! Please correct the file."
            )
            ask_user_to_correct_errors = True
            continue  # the rest of the loop is just for throwing errors

        # Check if the current line number skips any numbers
        while expected_line_number < current_line_number:
            # Add a placeholder for the missing line
            processed_lines.append(f"{expected_line_number}. ")
            expected_line_number += 1

        # Add the current line to the processed list
        processed_lines.append(line)  # Add newline for formatting
        expected_line_number += 1
    end_error_messages = []

    # Update current_line_number to the last expected line number after processing all lines
    new_number_of_lines_of_file = expected_line_number - 1

    if new_number_of_lines_of_file > n_lines:
        end_error_messages.append(
            f"Error: The total number of lines in the numbered file was increased. Please correct the file."
        )
        ask_user_to_correct_errors = True

    if ask_user_to_correct_errors:
        for error in (
            list(reversed(error_messages)) + end_error_messages
        ):  # Print errors in reverse order
            print(error)
        return True, -999

    autoformatted_file = "\n".join(processed_lines)
    original_text = "".join(lines)
    if autoformatted_file != original_text:
        with open(filename, "w") as file:
            file.write(autoformatted_file)
            print("Some changes were made to autocorrect format of numbered text file.")

    return False, new_number_of_lines_of_file


def apply_changes(original_text, edited_text, reconstructor, new_n_lines):
    """
    Apply changes from the edited text back to the original text.

    Args:
        original_text (str): The original text.
        edited_text (list): The edited text split into lines.
        reconstructor (list): List of dictionaries containing sentence information.
        new_n_lines (int): The new number of lines in the edited text.

    Returns:
        str: The modified text with applied changes.
    """

    result = original_text
    offset = 0  # To track changes in string length after each modification

    for sentence_info in reconstructor:
        start_position = sentence_info["start_position"] + offset
        line_number = sentence_info["line_number"]
        length = sentence_info["length"]
        length_numbering = sentence_info["length_numbering"]
        delimiter_is_punctuation = sentence_info["delimiter_is_punctuation"]
        if delimiter_is_punctuation:
            extra_length_to_remove_punctuation = 1
        else:
            extra_length_to_remove_punctuation = 0

        # Extract the substring from edited_text
        if line_number >= len(edited_text):  # Break if the line number is out of range
            replacement_text = ""
        else:
            replacement_text = edited_text[line_number][length_numbering:]

        # Modify the result string
        result = (
            result[:start_position]
            + replacement_text
            + result[start_position + length :]
        )

        # Update the offset to account for the change in string length
        offset += len(replacement_text) - length - extra_length_to_remove_punctuation
    return result


def main(args):
    """
    Main function to orchestrate the editing and applying changes process.

    Args:
        args (list): List of command-line arguments.
    """

    if len(args) < 2:
        print("Usage: python script.py <filename>")
        return
    original_filename = args[1]
    # Read the original file
    with open(original_filename, "r") as f:
        original_text = f.read()

    # Create numbered version
    numbered_text, positions = number_sentences(original_text)

    # Save a copy in the current directory for editing
    numbered_filename = (
        get_filename_without_extension(original_filename) + "_numbered.txt"
    )
    with open(numbered_filename, "w") as f:
        f.write("\n".join(numbered_text))

    print(
        f"A copy has been saved as '{numbered_filename}' in the current directory for editing."
    )
    input("Press Enter when you've finished editing...")
    n_lines = len(numbered_text)

    # Correct any things that alter the numbered file
    while True:
        there_were_errors, new_n_lines = preprocess_edited_text(
            numbered_filename, n_lines
        )
        if not there_were_errors:
            break
        print(
            "ERROR: There was an issue. Please correct the edited numbered file and hit enter to try again."
        )
        input()
    print("Numbered text was formatted correctly.")

    # Read the edited file
    with open(numbered_filename, "r") as f:
        edited_text = f.read().split(
            "\n"
        )  # Assume the edited text was saved line by line

    # Apply changes
    result = apply_changes(original_text, edited_text, positions, new_n_lines)

    if new_n_lines != n_lines:
        print(f"File shortened by {n_lines-new_n_lines} lines.")
    # Save the result
    if result != original_text:
        with open(original_filename, "w") as file:
            file.write(result)
            print(
                f"All edits to the _numbered file have been saved back to {original_filename}"
            )
    else:
        print("No edits to original file detected.")


if __name__ == "__main__":
    main(sys.argv)
