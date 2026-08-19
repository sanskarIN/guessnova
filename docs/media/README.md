# Release Media

This directory is reserved for terminal screenshots and short demo recordings captured from a signed-off GuessNova release candidate.

## Authenticity rule

Do not commit mock screenshots, reconstructed terminal images, or recordings from an unknown build. Every published media asset must identify the exact commit or tag used to capture it.

## Capture checklist

1. Complete the release accessibility evidence checklist.
2. Confirm the working tree is at the intended release commit/tag.
3. Install the package from that checkout/build artifact.
4. Use deterministic gameplay where practical, for example `guessnova play --seed 20260819 --no-save`.
5. Capture at least:
   - normal Rich CLI gameplay;
   - `--plain --compact` output;
   - Textual TUI input, hint, and completed-round states;
   - Hindi CLI output after `guessnova settings --locale hi`.
6. Remove usernames, home-directory paths, unrelated terminal history, tokens, or other private data from the capture environment before recording.
7. Record the source commit/tag in the media filename or companion metadata file.

## Recommended filenames

- `cli-classic-vX.Y.Z.png`
- `cli-plain-compact-vX.Y.Z.png`
- `tui-gameplay-vX.Y.Z.png`
- `demo-vX.Y.Z.webm`
- `media-vX.Y.Z.md` for capture metadata

Real release media is intentionally not fabricated by automated repository work. It should be added only after manual capture from the exact build being signed off.
