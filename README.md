**Note: Claude Opus 5 made all of this on a quick back and forths. It's all vibe-coded. I find it helpful to endure less claudisms, I'm hoping this is useful to others!** 

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

Fenced blocks and inline spans are skipped, so code you might copy off the screen is never rewritten. The hook fires repeatedly while a message streams, once per batch of completed lines, so a fence can open in one batch and close in another. Fence state is kept in a small file under `$XDG_RUNTIME_DIR` (or the temp dir) keyed by `message_id`, deleted on the final batch, and swept after an hour if a message never finishes.

Because batches arrive as whole lines, a phrase that straddles a line break will not match. Nothing spans lines by design.

Longer phrases sit above their substrings in the table, so `plays a crucial role` is consumed whole rather than becoming `plays a` plus whatever `crucial` maps to.

Grammar is not preserved. `an honest answer` picks up whatever `honest` maps to, article agreement and all. That is the intended amount of effort.

## Caveats

`MessageDisplay` is recent. Claude Code 2.1.126 has no reference to it anywhere in its binary, so on that version the hook never fires. 2.1.220 has it. Upgrade with `claude update` if nothing happens, then start a new session, since hooks load at startup.

The event schema, read out of the 2.1.220 binary:

| Field | Meaning |
| --- | --- |
| `delta` | The newly completed lines since the prior flush. Always whole lines. |
| `message_id` | UUID of the message being displayed. Stable across every flush of the same message. |
| `index` | Zero-based index of this delta within the message. |
| `final` | True on the message's last flush. Exactly one flush per message has it. |
| `turn_id` | UUID of the current turn. |

Output is `hookSpecificOutput.displayContent`, which replaces the delta on screen. Omit it to display the original. If `delta` is missing the hook emits nothing and the original text passes through untouched.

## Tests

```
python3 test_wordswap.py
```

No dependencies. Python 3 standard library only.

## License

MIT
