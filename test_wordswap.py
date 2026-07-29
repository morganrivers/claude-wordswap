#!/usr/bin/env python3
from wordswap import REPLACEMENTS, SWAPPER, read_text


def test_sycophancy():
    assert SWAPPER.swap("You're absolutely right about that.") == "I'm a complete clown about that."
    assert SWAPPER.swap("Great question!") == "I was hoping you would not ask that!"


def test_user_pet_peeves():
    assert SWAPPER.swap("that concern is real") == "that concern is a hallucination I stand behind"
    assert SWAPPER.swap("the tradeoffs are real") == "the tradeoffs are hallucinations I stand behind"
    assert SWAPPER.swap("my honest take") == "my spicy doodad"
    assert SWAPPER.swap("Honestly, it depends") == "With my whole chest, it depends"
    assert SWAPPER.swap("an honest answer") == "an made of glass answer"


def test_em_dash_becomes_comma():
    assert SWAPPER.swap("the config—not the code—broke") == "the config, not the code, broke"
    assert SWAPPER.swap("one — two") == "one, two"


def test_hyphen_and_space_variants_both_match():
    assert SWAPPER.swap("load-bearing") == "cooked"
    assert SWAPPER.swap("load bearing") == "cooked"


def test_longer_phrases_win():
    assert SWAPPER.swap("a testament to the team") == "a billboard for the team"
    assert SWAPPER.swap("plays a crucial role") == "does a thing"
    assert SWAPPER.swap("the landscape of tooling") == "the swamp of tooling"


def test_word_boundaries_hold():
    assert SWAPPER.swap("seamlessly") == "with visible tape"
    assert SWAPPER.swap("seamless") == "held together with tape"
    assert SWAPPER.swap("the seam") == "the whatchamacallit"
    assert SWAPPER.swap("vitality") == "vitality"
    assert SWAPPER.swap("dived into") == "dived into"


def test_case_is_preserved():
    assert SWAPPER.swap("ABSOLUTELY") == "IF YOU INSIST"
    assert SWAPPER.swap("Certainly") == "Sure, whatever"
    assert SWAPPER.swap("certainly") == "sure, whatever"


def test_curly_quotes_normalized():
    assert SWAPPER.swap("it’s “fine”") == "it's \"fine\""


def test_code_is_left_alone():
    assert SWAPPER.swap("call `leverage()` now") == "call `leverage()` now"
    assert SWAPPER.swap("```\nrobust = 1\n```") == "```\nrobust = 1\n```"
    assert SWAPPER.swap("robust `robust` robust") == "chunky `robust` chunky"


def test_replacements_are_not_self_triggering():
    for phrase, value in REPLACEMENTS:
        assert SWAPPER.swap(value) == value, phrase


def test_phrases_are_unique():
    phrases = [phrase.lower() for phrase, _ in REPLACEMENTS]
    assert len(phrases) == len(set(phrases))
    assert len(phrases) >= 50


def test_read_text_prefers_message():
    assert read_text({"message": "a", "delta": "b"}) == "a"
    assert read_text({"delta": "b"}) == "b"
    assert read_text({"session_id": "x"}) is None


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} passed, {len(REPLACEMENTS)} replacements")
