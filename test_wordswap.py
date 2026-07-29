#!/usr/bin/env python3
from wordswap import REPLACEMENTS, SWAPPER, read_text

VALUES = {phrase.lower(): value for phrase, value in REPLACEMENTS}


def value_for(phrase):
    assert phrase.lower() in VALUES, phrase
    return VALUES[phrase.lower()]


def capitalized(phrase):
    value = value_for(phrase)
    return value[:1].upper() + value[1:]


def test_sycophancy():
    assert SWAPPER.swap("You're absolutely right about that.") == capitalized("you're absolutely right") + " about that."
    assert SWAPPER.swap("Great question!") == capitalized("great question") + "!"


def test_user_pet_peeves():
    assert SWAPPER.swap("that concern is real") == "that concern " + value_for("is real")
    assert SWAPPER.swap("the tradeoffs are real") == "the tradeoffs " + value_for("are real")
    assert SWAPPER.swap("my honest take") == "my " + value_for("honest take")
    assert SWAPPER.swap("Honestly, it depends") == capitalized("honestly") + ", it depends"
    assert SWAPPER.swap("an honest answer") == "an " + value_for("honest") + " answer"


def test_em_dash_becomes_comma():
    assert SWAPPER.swap("the config—not the code—broke") == "the config, not the code, broke"
    assert SWAPPER.swap("one — two") == "one, two"


def test_hyphen_and_space_variants_both_match():
    assert SWAPPER.swap("load-bearing") == value_for("load-bearing")
    assert SWAPPER.swap("load bearing") == value_for("load-bearing")


def test_longer_phrases_win():
    assert SWAPPER.swap("a testament to the team") == value_for("a testament to") + " the team"
    assert value_for("a testament to") != value_for("testament")
    assert SWAPPER.swap("plays a crucial role") == value_for("plays a crucial role")
    assert SWAPPER.swap("the landscape of tooling") == value_for("the landscape of") + " tooling"


def test_word_boundaries_hold():
    assert SWAPPER.swap("seamlessly") == value_for("seamlessly")
    assert SWAPPER.swap("seamless") == value_for("seamless")
    assert SWAPPER.swap("the seam") == "the " + value_for("seam")
    assert SWAPPER.swap("realms") == "realms"
    assert SWAPPER.swap("dived into") == "dived into"


def test_case_is_preserved():
    assert SWAPPER.swap("certainly") == value_for("certainly")
    assert SWAPPER.swap("Certainly") == capitalized("certainly")
    assert SWAPPER.swap("ABSOLUTELY") == value_for("absolutely").upper()


def test_curly_quotes_normalized():
    assert SWAPPER.swap("it’s “fine”") == "it's \"fine\""


def test_code_is_left_alone():
    assert SWAPPER.swap("call `leverage()` now") == "call `leverage()` now"
    assert SWAPPER.swap("```\nrobust = 1\n```") == "```\nrobust = 1\n```"
    assert SWAPPER.swap("robust `robust` robust") == f"{value_for('robust')} `robust` {value_for('robust')}"


def test_replacements_are_not_self_triggering():
    for phrase, value in REPLACEMENTS:
        assert SWAPPER.swap(value) == value, phrase


def test_phrases_are_unique():
    phrases = [phrase.lower() for phrase, _ in REPLACEMENTS]
    assert len(phrases) == len(set(phrases))
    assert len(phrases) >= 50


def test_read_text_uses_delta():
    assert read_text({"delta": "b"}) == "b"
    assert read_text({"message": "a"}) is None
    assert read_text({"session_id": "x"}) is None


def test_fence_state_carries_across_deltas():
    opened, inside = SWAPPER.swap_delta("prose is robust\n```python", False)
    assert inside is True
    assert opened == f"prose is {value_for('robust')}\n```python"

    middle, inside = SWAPPER.swap_delta("robust = 1", inside)
    assert inside is True
    assert middle == "robust = 1"

    closed, inside = SWAPPER.swap_delta("```\nrobust again", inside)
    assert inside is False
    assert closed == f"```\n{value_for('robust')} again"


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} passed, {len(REPLACEMENTS)} replacements")
