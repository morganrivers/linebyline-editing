# Line-by-Line Editing Tool

This tool is designed to assist with the precise editing of text files by numbering sentences. This is especially useful for providing Large Language Models (LLMs) with specific locations of sentences, improving their ability to make targeted improvements.

## Features
- Number sentences in a text file.
- Save the numbered text for easy editing.
- Automatically detect and correct formatting errors in the edited text.
- Apply changes from the edited text back to the original text.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/morganrivers/linebyline-editing.git
    cd linebyline-editing
    ```

3. **Install dependencies:**

    The only dependency is pytest, so `pip install pytest` is simplest.

## Usage

1. **Run the script:**

    ```sh
    python numberify.py <filename>
    ```

    Replace `<filename>` with the path to the text file you want to edit.

2. **Edit the numbered text file:**

    - A numbered copy of your file will be saved in the current directory with `_numbered` appended to the original filename.
    - Edit this numbered file as needed.

3. **Apply changes:**

    - After editing, press Enter when prompted to apply the changes back to the original file.
    - The script will check for and correct any format errors in the edited file before applying changes.

## Example

1. **Original text file (`example.txt`):**

    ```
    This is a test. Does it work? Yes, it does!
    ```

2. **Numbered text file (`example_numbered.txt`):**

    ```
    1. This is a test.
    2. Does it work?
    3. Yes, it does!
    ```

3. **Edited numbered text file (`example_numbered.txt`):**

    ```
    1. This is an edited test.
    2. Does it work?
    3. Yes, it does!
    ```

4. **Resulting text file (`example.txt`):**

    ```
    This is an edited test. Does it work? Yes, it does!
    ```

## Testing

To run the tests, use the following command:

```sh
pytest test_numberify.py
