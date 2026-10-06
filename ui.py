"""Terminal presentation helpers for AI-Lab.

Everything here is TTY-aware: when stdout is not a real terminal (for
example, under pytest's ``capsys``) all styling, wrapping and animation is
disabled so output stays plain and deterministic.
"""

import itertools
import shutil
import sys
import textwrap
import threading

DEFAULT_WIDTH = 80

_RESET = "\033[0m"
_CODES = {
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "gray": "\033[90m",
}


def _tty(stream=None):
    stream = stream if stream is not None else sys.stdout
    return getattr(stream, "isatty", lambda: False)()


def style(text, *names):
    if not _tty():
        return text
    codes = "".join(_CODES[n] for n in names if n in _CODES)
    return f"{codes}{text}{_RESET}"


def width():
    try:
        cols = shutil.get_terminal_size((DEFAULT_WIDTH, 24)).columns
    except (ValueError, OSError):
        cols = DEFAULT_WIDTH
    return max(cols, 20)


def rule(char="─"):
    print(char * width())


def wrap_text(text, indent="", subindent=None):
    """Wrap long text for readability. Plain passthrough when not a TTY."""
    if not _tty():
        return text
    sub = subindent if subindent is not None else indent
    return textwrap.fill(text, width=width(), initial_indent=indent, subsequent_indent=sub)


def print_wrap(text, indent="", subindent=None):
    print(wrap_text(text, indent, subindent))


class Spinner:
    """Minimal threaded loading indicator written to stderr (TTY only)."""

    _FRAMES = "|/-\\"

    def __init__(self, message="Thinking", stream=None):
        self.message = message
        self.stream = stream if stream is not None else sys.stderr
        self._stop = threading.Event()
        self._thread = None

    def __enter__(self):
        if getattr(self.stream, "isatty", lambda: False)():
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        return self

    def _run(self):
        frames = itertools.cycle(self._FRAMES)
        while not self._stop.is_set():
            frame = next(frames)
            self.stream.write(f"\r{style(frame, 'cyan')} {self.message}...")
            self.stream.flush()
            self._stop.wait(0.08)

    def __exit__(self, *exc):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=0.3)
        if getattr(self.stream, "isatty", lambda: False)():
            blank = " " * (len(self.message) + 6)
            self.stream.write(f"\r{blank}\r")
            self.stream.flush()


def print_header(provider="Gemini → OpenRouter (auto-fallback)", model="—"):
    rule("═")
    print(style("  AI-LAB", "bold", "cyan"))
    print(style(f"  provider: {provider}  ·  model: {model}", "dim"))
    rule("═")
    print()


def render_user(content):
    print(style("👤 You", "cyan") + f": {wrap_text(content)}")


def render_assistant(content, model):
    print(style("🤖 AI", "magenta") + f": {wrap_text(content, subindent='  ')}")
    print(style(f"· model: {model}", "dim"))


def render_error(message):
    print(style("✖ error:", "red") + f" {message}")
    print()
