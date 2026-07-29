#!/usr/bin/env python3
import json
import re
import sys

TEXT_KEYS = ("message", "message_text", "delta", "displayContent", "content", "text")

CURLY_QUOTES = {
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
}

EM_DASH_PATTERN = re.compile(r"\s*—\s*")

CODE_PATTERN = re.compile(r"(```.*?```|~~~.*?~~~|`[^`\n]*`)", re.DOTALL)

REPLACEMENTS = [
    ("you're absolutely right", "I'm a complete clown"),
    ("you are absolutely right", "I am a complete clown"),
    ("you're absolutely correct", "I'm a complete clown"),
    ("you're right", "I have no idea what I'm doing"),
    ("you're spot on", "I panicked and agreed"),
    ("great question", "I was hoping you would not ask that"),
    ("excellent question", "oh no"),
    ("great catch", "you found the bug I hid"),
    ("good catch", "you found the bug I hid"),
    ("I hope this helps", "godspeed"),
    ("let me know if you have any questions", "please do not follow up"),
    ("let me know if you need anything else", "please do not follow up"),
    ("apologies for the confusion", "I confused you on purpose"),
    ("I apologize for", "whoops about"),
    ("thank you for your patience", "sorry, the wait continues"),
    ("as an AI", "as a guy"),

    ("honest take", "spicy doodad"),
    ("to be honest", "as a small treat"),
    ("in all honesty", "for no particular reason"),
    ("honestly", "with my whole chest"),
    ("honesty", "a thing I lack"),
    ("honest", "made of glass"),
    ("is very real", "is extremely made up"),
    ("are very real", "are extremely made up"),
    ("is real", "is a hallucination I stand behind"),
    ("are real", "are hallucinations I stand behind"),
    ("was real", "was a hallucination I stood behind"),
    ("were real", "were hallucinations I stood behind"),
    ("feels real", "feels made up"),
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
    ("a testament to", "a billboard for"),
    ("testament to", "billboard for"),
    ("testament", "billboard"),
    ("the landscape of", "the swamp of"),
    ("landscape", "swamp"),
    ("in the realm of", "in the corner of"),
    ("realm", "corner"),
    ("tapestry", "throw rug"),
    ("symphony", "kazoo solo"),
    ("beacon", "night light"),
    ("cornerstone", "one of the rocks"),
    ("backbone", "one of the bones"),
    ("paradigm", "way of doing stuff"),
    ("synergy", "two things touching"),
    ("journey", "errand"),
    ("embark", "wander off"),
    ("crucially", "eh"),
    ("crucial", "sort of important"),
    ("pivotal", "mildly relevant"),
    ("vital", "safe to skip"),
    ("comprehensive", "exhausting"),
    ("holistic", "vibes-based"),
    ("nuanced", "confusing"),
    ("meticulously", "fussily"),
    ("meticulous", "fussy"),
    ("intricate", "annoying"),
    ("robust", "chunky"),
    ("elegantly", "while wearing a tiny hat"),
    ("elegant", "wearing a tiny hat"),
    ("powerful", "medium"),
    ("flexible", "wobbly"),
    ("scalable", "big-ish"),
    ("performant", "not slow, hopefully"),
    ("lightweight", "small"),
    ("idiomatic", "how the cool kids do it"),
    ("battle-tested", "used once"),
    ("production-ready", "probably fine"),
    ("enterprise-grade", "expensive"),
    ("first-class", "coach class"),
    ("cutting-edge", "new to me"),
    ("state-of-the-art", "current, allegedly"),
    ("game-changer", "minor convenience"),
    ("game-changing", "barely different"),
    ("groundbreaking", "a shovel was involved"),
    ("revolutionary", "new-ish"),
    ("transformative", "different"),
    ("innovative", "untested"),
    ("best practices", "things people say"),
    ("under the hood", "in the goo"),
    ("out of the box", "before you break it"),
    ("low-hanging fruit", "the easy stuff"),
    ("north star", "vague goal"),

    ("sheds light on", "shines a flashlight at"),
    ("underscores", "yells about"),
    ("underscore", "yell about"),
    ("showcases", "waves around"),
    ("showcase", "wave around"),
    ("highlights", "waves around"),
    ("underpins", "sits under, somehow"),
    ("aligns with", "rhymes with"),
    ("resonates", "makes a noise"),
    ("unlocks", "jiggles the handle of"),
    ("unlock", "jiggle the handle of"),
    ("streamline", "make slightly less bad"),
    ("leverage", "wiggle"),
    ("utilize", "use, but fancy"),
    ("ensure", "hope"),
    ("facilitate", "get out of the way of"),
    ("foster", "sprinkle water on"),
    ("empower", "hand a juice box to"),
    ("harness", "grab"),
    ("unleash", "let out of the crate"),
    ("supercharge", "add a battery to"),
    ("navigating", "stumbling through"),
    ("navigate", "stumble through"),
    ("curated", "picked at random"),
    ("bespoke", "homemade"),
    ("boasts", "has"),
    ("serves as", "is"),
    ("stands as", "is"),

    ("due to the fact that", "because, dressed up"),
    ("in order to", "to, but longer"),
    ("the fact that", "the deal where"),
    ("a wide range of", "some"),
    ("a variety of", "a handful of"),
    ("plethora", "a bunch"),
    ("myriad", "several, maybe"),
    ("vast majority", "most"),
    ("furthermore", "brace yourself"),
    ("moreover", "and another thing"),
    ("additionally", "one more thing"),
    ("ultimately", "eventually, I guess"),
    ("fundamentally", "deep down"),
    ("essentially", "basically, but pompous"),
    ("arguably", "someone might say"),
    ("notably", "look at this"),
    ("significantly", "a bit"),
    ("dramatically", "a bit"),
    ("certainly", "sure, whatever"),
    ("absolutely", "if you insist"),
    ("nestled", "sitting there"),
    ("vibrant", "loud"),
    ("breathtaking", "fine"),
    ("stunning", "okay looking"),
    ("iconic", "famous, allegedly"),
    ("must-see", "optional"),
    ("hidden gem", "regular place"),
    ("unforgettable", "already fading"),
    ("rest assured", "worry a normal amount"),
    ("peace of mind", "mild calm"),
    ("the future looks bright", "who knows"),
    ("it's not just", "it is, in fact, just"),
    ("not only", "only, plus"),
    ("reach out", "bother"),
    ("circle back", "bother you again"),
    ("touch base", "bother you briefly"),
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

    def swap(self, text):
        assert isinstance(text, str), "text must be a string"
        segments = CODE_PATTERN.split(text)
        return "".join(
            segment if index % 2 else self._swap_prose(segment)
            for index, segment in enumerate(segments)
        )


SWAPPER = Swapper(REPLACEMENTS)


def read_text(payload):
    assert isinstance(payload, dict), "hook payload must be a JSON object"
    for key in TEXT_KEYS:
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def main():
    payload = json.load(sys.stdin)
    text = read_text(payload)
    if text is None:
        return
    output = {
        "hookSpecificOutput": {
            "hookEventName": "MessageDisplay",
            "displayContent": SWAPPER.swap(text),
        }
    }
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
