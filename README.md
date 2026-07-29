**Note: Claude Opus 5 made all of this on a one-shot prompt. I find it helpful to endure less claudisms, I'm hoping this is useful to others!** 

# claude-wordswap

A `MessageDisplay` hook that rewrites Claude's vocabulary before it hits your screen. 175 phrases, swapped for something stupider.

```
You're absolutely right — the seam here is load-bearing, and honestly the fix is real.
```

becomes

```
I'm a complete clown, the whatchamacallit here is cooked, and with my whole chest the fix is a hallucination I stand behind.
```

Display only. The transcript and what Claude sees keep the original text, so this changes nothing about the model's behavior. It only changes whether you have to read the word "delve" today.

## Install

```
mkdir -p ~/.claude/hooks
curl -o ~/.claude/hooks/wordswap.py https://raw.githubusercontent.com/morganrivers/claude-wordswap/main/wordswap.py
chmod +x ~/.claude/hooks/wordswap.py
```

Then merge `settings.example.json` into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "MessageDisplay": [
      { "hooks": [ { "type": "command", "command": "$HOME/.claude/hooks/wordswap.py" } ] }
    ]
  }
}
```

Hooks load at startup. Start a new session.

## What it swaps

The `REPLACEMENTS` table in `wordswap.py` is the single source of truth. Edit it and the tests, the docs, and the hook all move together. A sample:

| Phrase | Becomes |
| --- | --- |
| you're absolutely right | I'm a complete clown |
| load-bearing | cooked |
| seam | whatchamacallit |
| honest take | spicy doodad |
| honestly | with my whole chest |
| is real / are real | is a hallucination I stand behind |
| delve into | root around in |
| let's dive in | cannonball time |
| at its core | in its gooey center |
| testament to | billboard for |
| tapestry | throw rug |
| leverage | wiggle |
| robust | chunky |
| elegant | wearing a tiny hat |
| comprehensive | exhausting |
| production-ready | probably fine |
| great question | I was hoping you would not ask that |
| I hope this helps | godspeed |

Em dashes become `, `. Curly quotes become straight quotes.

## Behavior worth knowing

Hyphens and spaces are interchangeable, so `load-bearing` and `load bearing` both match. Capitalization is carried over: `Certainly` becomes `Sure, whatever`, `ABSOLUTELY` becomes `IF YOU INSIST`.

Fenced blocks and inline spans are skipped, so code you might copy off the screen is never rewritten. Longer phrases are listed before their substrings, which is why `plays a crucial role` becomes `does a thing` rather than `plays a sort of important role`.

Grammar is not preserved. `an honest answer` becomes `an made of glass answer`. That is the intended amount of effort.

## Caveats

`MessageDisplay` is recent. Claude Code 2.1.126 has no reference to it anywhere in the binary, so on that version the hook will not fire at all. Upgrade if nothing happens.

The input field carrying the message text is not pinned down in the published schema, and three sources name three different keys. `read_text` therefore accepts the first non-empty string among `message`, `message_text`, `delta`, `displayContent`, `content`, `text`. If none match, the hook emits nothing and the original text passes through untouched. If you confirm the correct key on a current version, open an issue and the list can collapse to one entry.

## Tests

```
python3 test_wordswap.py
```

No dependencies. Python 3 standard library only.

## License

MIT
