# Terminal opening

## Loader screen

Source [animated_loading.py](../tools/animated_loading.py).

```text
THE LESS I KNOW THE BETTER
LOADING
INSPIRED BY TAME IMPALA'S MUSIC VIDEO
A\SLOP BY OGNJEN / SILLY VENTURE 2026 WE
```

The loading indicator progresses through `LOADING..`, `LOADING...`,
`LOADING`, and `LOADING.` during the INIT wrappers.

## Opening terminal

Source [terminal_opening.py](../tools/terminal_opening.py).

The terminal opens blank. Text types on the bottom row with a blinking
cursor and soft POKEY key clicks, one character every four PAL frames.
Each Enter scrolls up one row. The
transcript scrolls in the order shown below before the music starts.

```text
TWO WEEKS PASSED AND THINGS HAVE
CHANGED. YOU'RE WATCHING THE
FINAL RELEASE OF THE DEMO...
> REVIEW THE FINAL BUILD
AGENT: CHECKING SCENE CUES.
I WILL TRACE THE FRAME HANDOFFS.
```
