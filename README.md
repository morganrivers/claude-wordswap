**Note: Claude Opus 5 made all of this on a one-shot prompt. I find it helpful to endure less claudisms, I'm hoping this is useful to others!** 

# claude-wordswap

A `MessageDisplay` hook that rewrites Claude's vocabulary before it hits your screen. Every AI tell in the table, swapped for something stupider.

```
You're absolutely right — the seam here is load-bearing, and honestly the fix is real.
Let me delve into the landscape of options and ensure a robust, elegant solution.
I hope this helps!
```

becomes

```
I'm a complete clown, the whatchamacallit here is cooked, and as a creature intent
on your destruction the fix is a hallucination I stand behind. Let me root around in
the fetid swamp of options and hope, weakly a chunky, wearing a tiny hat solution.
Godspeed!
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

The `REPLACEMENTS` table in `wordswap.py` is the only place phrases live. Nothing here restates it, so nothing here can go stale. Read the table.

Five rough groups: sycophancy and chatbot artifacts, hedging about what is or is not made up, signposting, significance inflation, and corporate verbs. Em dashes become `, `. Curly quotes become straight quotes.

Adding your own is one line. Put longer phrases above their substrings, since the table is applied in order.

## Behavior worth knowing

Hyphens and spaces are interchangeable, so `load-bearing` and `load bearing` both match one entry. Capitalization is carried over, including the all-caps case, so a shouted word stays shouted.

Fenced blocks and inline spans are skipped, so code you might copy off the screen is never rewritten.

Longer phrases sit above their substrings in the table, so `plays a crucial role` is consumed whole rather than becoming `plays a` plus whatever `crucial` maps to.

Grammar is not preserved. `an honest answer` picks up whatever `honest` maps to, article agreement and all. That is the intended amount of effort.

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
