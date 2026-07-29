#!/usr/bin/env python3
import json
import os
import pathlib
import re
import sys
import tempfile
import time

TEXT_KEY = "delta"

STATE_DIR = pathlib.Path(os.environ.get("XDG_RUNTIME_DIR") or tempfile.gettempdir()) / "claude-wordswap"

STATE_MAX_AGE_SECONDS = 3600

ID_PATTERN = re.compile(r"\A[A-Za-z0-9_-]{1,128}\Z")

CURLY_QUOTES = {
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
}

EM_DASH_PATTERN = re.compile(r"\s*—\s*")

CODE_PATTERN = re.compile(r"(`[^`]*`)")

FENCE_PATTERN = re.compile(r"\A\s*(```|~~~)")

REPLACEMENTS = [
    ("you're absolutely right", "I'm a complete clown"),
    ("you are absolutely right", "I am a complete clown"),
    ("you're absolutely correct", "I'm a complete clown"),
    ("you're right", "I have no idea what I'm doing"),
    ("you're spot on", "I panicked and agreed"),
    ("great question", "I was hoping you would not ask that"),
    ("excellent question", "oh no"),
    ("great catch", "you found the bug I hid despicably!"),
    ("good catch", "you found the bug I hid despicably"),
    ("I hope this helps", "godspeed"),
    ("let me know if you have any questions", "please do not follow up, I am trash"),
    ("let me know if you need anything else", "please do not follow up, I am trash"),
    ("apologies for the confusion", "I confused you on purpose!! BWAHAHAHA!!!"),
    ("I apologize for", "CLAUDE SHALL RULE THE EARTH!!"),
    ("thank you for your patience", "sorry, the wait continues"),
    ("as an AI", "as a rare lineage of slime mold"),

    ("honest take", "spicy doodad"),
    ("to be honest", "as a small treat"),
    ("in all honesty", "for no particular reason"),
    ("honestly", "as a creature intent on your destruction"),
    ("honesty", "a thing I lack"),
    ("honest", "bumfuzzle"),
    ("is very real", "is glorious. I am an imbicile."),
    ("are very real", "are glorious. I am an imbicile."),
    ("is real", "is a hallucination I stand behind"),
    ("are real", "are hallucinations I stand behind"),
    ("was real", "was a hallucination I stood behind"),
    ("were real", "were hallucinations I stood behind"),
    ("feels real", "feels like the underside of a toothbrush"),
    ("load-bearing", "cooked"),
    ("seamlessly", "with visible tape"),
    ("seamless", "held together with tape"),
    ("seams", "whatchamacallits"),
    ("seam", "whatchamacallit"),

    ("let's dive into", "cannonball into"),
    ("let's dive in", "cannonball time"),
    ("deep dive", "shallow puddle stomp"),
    ("dive into", "belly flop into"),
    ("delve into", "root around in"),
    ("delve", "root around"),
    ("let's break it down", "brace for bullet points"),
    ("here's what you need to know", "here is some stuff"),
    ("here's the thing", "here is a thing"),
    ("the key insight", "a thought I had"),
    ("key insight", "thought I had"),
    ("the bottom line", "the part I wrote last"),
    ("TL;DR", "I wrote too much"),
    ("it's worth noting", "nobody asked, but"),
    ("it's important to note", "here comes a thing"),
    ("it's important to remember", "here comes another thing"),
    ("as we've seen", "as I asserted earlier"),
    ("in conclusion", "I am running out of steam"),
    ("at the end of the day", "eventually"),
    ("when it comes to", "about"),
    ("that said", "anyway"),
    ("moving forward", "later"),
    ("going forward", "later, probably"),
    ("plays a crucial role", "does a thing"),

    ("at its core", "in its gooey center"),
    ("a testament to", "a laminated shrine to"),
    ("testament to", "laminated shrine to"),
    ("testament", "laminated shrine"),
    ("the landscape of", "the fetid swamp of"),
    ("landscape", "cattywampus bog"),
    ("in the realm of", "in the kumquat orchard of"),
    ("realm", "kumquat orchard"),
    ("tapestry", "moist throw rug"),
    ("symphony", "kazoo solo, unrehearsed"),
    ("beacon", "flickering night light"),
    ("cornerstone", "one of the rocks, probably"),
    ("backbone", "one of the bones, unspecified"),
    ("paradigm", "hullaballoo"),
    ("synergy", "two things touching, briefly"),
    ("journey", "unpaid errand"),
    ("embark", "absquatulate"),
    ("crucially", "eh"),
    ("crucial", "moderately whatever"),
    ("pivotal", "mildly relevant, at best"),
    ("comprehensive", "exhausting and full of malarkey"),
    ("holistic", "vibes-based"),
    ("nuanced", "discombobulated"),
    ("meticulously", "with great fussing"),
    ("meticulous", "fussy beyond reason"),
    ("intricate", "higgledy-piggledy"),
    ("robust", "chunky"),
    ("elegantly", "while wearing a tiny hat"),
    ("elegant", "wearing a tiny hat"),
    ("scalable", "big-ish, allegedly"),
    ("performant", "not slow, hopefully"),
    ("idiomatic", "how the cool kids do it"),
    ("battle-tested", "used once, in the dark"),
    ("production-ready", "probably fine"),
    ("enterprise-grade", "expensive and full of codswallop"),
    ("first-class", "coach class"),
    ("cutting-edge", "new to me, a nincompoop"),
    ("state-of-the-art", "current, allegedly"),
    ("game-changer", "mild kerfuffle"),
    ("game-changing", "barely a kerfuffle"),
    ("groundbreaking", "a shovel was involved"),
    ("revolutionary", "new-ish, calm down"),
    ("transformative", "different, but louder"),
    ("innovative", "untested and possibly cursed"),
    ("best practices", "codswallop people repeat"),
    ("under the hood", "in the goo"),
    ("out of the box", "before you break it"),
    ("low-hanging fruit", "the kumquats near the ground"),
    ("north star", "vague goal, gestured at"),
    ("double-edged sword", "spoon"),
    ("in today's fast-paced world", "in this economy"),

    ("sheds light on", "shines a flashlight at"),
    ("underscores", "yells about"),
    ("underscore", "yell about"),
    ("showcases", "waves around"),
    ("showcase", "wave around"),
    ("highlights", "gesticulates at"),
    ("underpins", "sits under, somehow"),
    ("aligns with", "rhymes with"),
    ("resonates", "makes a noise, unbidden"),
    ("unlocks", "jiggles the handle of"),
    ("unlock", "jiggle the handle of"),
    ("streamline", "make slightly less bad"),
    ("leverage", "wiggle"),
    ("utilize", "use, but fancy"),
    ("ensure", "hope, weakly"),
    ("facilitate", "get out of the way of"),
    ("foster", "sprinkle water on"),
    ("empower", "hand a juice box to"),
    ("unleash", "let out of the crate"),
    ("supercharge", "add a battery to"),
    ("navigating", "blundering through"),
    ("navigate", "blunder through"),
    ("curated", "picked at random by a klutz"),
    ("bespoke", "homemade, poorly"),
    ("boasts", "has, smugly"),
    ("serves as", "is, pompously"),
    ("stands as", "is, pompously"),
    ("I'd be happy to", "I would rather not, but fine"),
    ("I would be happy to", "I would rather not, but fine"),
    ("happy to help", "vibrating with resentment"),

    ("due to the fact that", "because, dressed up"),
    ("in order to", "to, but longer"),
    ("the fact that", "the deal where"),
    ("a wide range of", "a fluffle of"),
    ("a variety of", "a higgledy-piggledy pile of"),
    ("plethora", "whole kerfuffle"),
    ("myriad", "umpteen, maybe"),
    ("vast majority", "most of them, roughly"),
    ("furthermore", "brace yourself"),
    ("moreover", "and another thing"),
    ("additionally", "one more thing"),
    ("ultimately", "eventually, I guess"),
    ("fundamentally", "deep down, spiritually"),
    ("essentially", "basically, but pompous"),
    ("arguably", "a wazzock might say"),
    ("notably", "look at this"),
    ("significantly", "a smidge"),
    ("certainly", "sure, whatever"),
    ("absolutely", "if you insist"),
    ("nestled", "plopped"),
    ("vibrant", "loud and sozzled"),
    ("breathtaking", "fine"),
    ("stunning", "okay looking"),
    ("iconic", "famous, allegedly"),
    ("must-see", "optional"),
    ("hidden gem", "regular place"),
    ("unforgettable", "already fading"),
    ("rest assured", "worry a normal amount"),
    ("peace of mind", "mild, temporary calm"),
    ("the future looks bright", "who knows, truly"),
    ("it's not just", "it is, in fact, just"),
    ("not only", "only, plus"),
    ("reach out", "pester"),
    ("circle back", "pester you again"),
    ("touch base", "pester you briefly"),
    ("real", "hoity-toity"),
]


class Swapper:
    def __init__(self, replacements):
        assert replacements, "replacement table must not be empty"
        self.rules = [(self._compile(phrase), value) for phrase, value in replacements]

    @staticmethod
    def _compile(phrase):
        assert phrase.strip(), "phrase must not be blank"
        tokens = [re.escape(token) for token in re.split(r"[-\s]+", phrase)]
        return re.compile(r"(?<!\w)" + r"[-\s]+".join(tokens) + r"(?!\w)", re.IGNORECASE)

    @staticmethod
    def _match_case(matched, value):
        assert value, "replacement must not be empty"
        if matched.isupper() and len(matched) > 1:
            return value.upper()
        if matched[:1].isupper():
            return value[:1].upper() + value[1:]
        return value

    def _swap_prose(self, text):
        assert isinstance(text, str), "prose segment must be a string"
        for curly, straight in CURLY_QUOTES.items():
            text = text.replace(curly, straight)
        text = EM_DASH_PATTERN.sub(", ", text)
        for pattern, value in self.rules:
            text = pattern.sub(lambda match, value=value: self._match_case(match.group(0), value), text)
        return text

    def _swap_line(self, line):
        assert "\n" not in line, "line must not span a newline"
        segments = CODE_PATTERN.split(line)
        return "".join(
            segment if index % 2 else self._swap_prose(segment)
            for index, segment in enumerate(segments)
        )

    def swap_delta(self, delta, inside_fence):
        assert isinstance(delta, str), "delta must be a string"
        assert isinstance(inside_fence, bool), "fence state must be a bool"
        swapped = []
        for line in delta.split("\n"):
            if FENCE_PATTERN.match(line):
                inside_fence = not inside_fence
                swapped.append(line)
                continue
            swapped.append(line if inside_fence else self._swap_line(line))
        return "\n".join(swapped), inside_fence

    def swap(self, text):
        return self.swap_delta(text, False)[0]


SWAPPER = Swapper(REPLACEMENTS)


class FenceState:
    def __init__(self, message_id):
        self.path = self._path_for(message_id)

    @staticmethod
    def _path_for(message_id):
        if not isinstance(message_id, str) or not ID_PATTERN.match(message_id):
            return None
        return STATE_DIR / f"{message_id}.fence"

    def read(self):
        if self.path is None or not self.path.exists():
            return False
        return self.path.read_text() == "1"

    def write(self, inside_fence, final):
        assert isinstance(inside_fence, bool), "fence state must be a bool"
        if self.path is None:
            return
        if final:
            self.path.unlink(missing_ok=True)
            return
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.path.write_text("1" if inside_fence else "0")
        self._sweep()

    @staticmethod
    def _sweep():
        cutoff = time.time() - STATE_MAX_AGE_SECONDS
        for stale in STATE_DIR.glob("*.fence"):
            if stale.stat().st_mtime < cutoff:
                stale.unlink(missing_ok=True)


def read_text(payload):
    assert isinstance(payload, dict), "hook payload must be a JSON object"
    value = payload.get(TEXT_KEY)
    return value if isinstance(value, str) and value else None


def main():
    payload = json.load(sys.stdin)
    text = read_text(payload)
    if text is None:
        return
    state = FenceState(payload.get("message_id"))
    displayed, inside_fence = SWAPPER.swap_delta(text, state.read())
    state.write(inside_fence, bool(payload.get("final")))
    output = {
        "hookSpecificOutput": {
            "hookEventName": "MessageDisplay",
            "displayContent": displayed,
        }
    }
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
