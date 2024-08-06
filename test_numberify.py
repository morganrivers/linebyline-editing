from numberify import (
    number_sentences,
    apply_changes,
)  # Assuming your main script is named numberify.py and it's in the same directory or properly referenced


# Define the tests
def test_run_from_test_file():
    test_txt = "This is a test. Does it work? Yes, it does!"
    expected_result = test_txt  # Since you expect the original text to be unchanged

    # Create numbered version
    numbered_text, positions = number_sentences(test_txt)

    assert test_txt == expected_result


def test_text_alteration():
    test_txt = "This is a test. Does it work? Yes, it does!"
    what_numbered_should_be = [
        "1. This is a test.",
        "2. Does it work?",
        "3. Yes, it does!",
    ]
    altered_numbered = [
        "1. This is an altered test.",
        "2. Does it work?",
        "3. Yes, it does!",
    ]
    what_result_should_be = "This is an altered test. Does it work? Yes, it does!"

    # Create numbered version
    numbered_text, positions = number_sentences(test_txt)
    result = apply_changes(test_txt, altered_numbered, positions, len(altered_numbered))

    assert numbered_text == what_numbered_should_be
    assert result == what_result_should_be


def test_multiline_punctuation():
    test_txt = "First line.\nSecond line? Third line! Fourth line."
    expected_numbered = [
        "1. First line.",
        "2. Second line?",
        "3. Third line!",
        "4. Fourth line.",
    ]
    expected_result = test_txt  # Assuming no alteration, should match original

    # Create numbered version
    numbered_text, positions = number_sentences(test_txt)
    result = apply_changes(test_txt, expected_numbered, positions, len(expected_numbered))

    assert numbered_text == expected_numbered
    assert result == expected_result


def test_no_punctuation():
    test_txt = "This is a single line without any punctuation"
    expected_numbered = ["1. This is a single line without any punctuation"]
    expected_result = test_txt  # Assuming no alteration, should match original

    # Create numbered version
    numbered_text, positions = number_sentences(test_txt)
    result = apply_changes(test_txt, expected_numbered, positions, len(expected_numbered))

    assert numbered_text == expected_numbered
    assert result == expected_result


def test_text_with_special_characters_and_dates():
    test_txt = "Hello! What's up? It's 2022, and we're coding."
    expected_numbered = [
        "1. Hello!",
        "2. What's up?",
        "3. It's 2022, and we're coding.",
    ]
    expected_result = test_txt  # Assuming no alteration, should match original

    # Create numbered version
    numbered_text, positions = number_sentences(test_txt)
    result = apply_changes(test_txt, expected_numbered, positions, len(expected_numbered))

    assert numbered_text == expected_numbered
    assert result == expected_result


def test_special_characters():
    test_txt = "Hello! What's up? It's 2022, and we're coding."
    what_numbered_should_be = [
        "1. Hello!",
        "2. What's up?",
        "3. It's 2022, and we're coding.",
    ]
    expected_result = test_txt

    numbered_text, positions = number_sentences(test_txt)
    result = apply_changes(test_txt, what_numbered_should_be, positions, len(what_numbered_should_be))

    assert numbered_text == what_numbered_should_be
    assert result == expected_result


def test_carriage_return_new_line():
    test_txt = "Line one.\r\nLine two?\rLine three!"
    what_numbered_should_be = ["1. Line one.\r", "2. Line two?\rLine three!"]

    numbered_text, positions = number_sentences(test_txt)
    result = apply_changes(test_txt, what_numbered_should_be, positions, len(what_numbered_should_be))

    assert numbered_text == what_numbered_should_be
    assert result == test_txt
