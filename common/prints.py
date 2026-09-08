"""Color printing utility supporting 7 rainbow colors:
Red, Orange, Yellow, Green, Cyan, Blue, Purple.
"""

import builtins
import sys
from typing import Any


class Prints:
    """Enhanced print utility with 7-color ANSI output support.
    Can be used as a class (Prints.print) or instance (prints.print / prints()).
    """

    RESET = "\033[0m"
    BOLD = "\033[1m"

    # 7-color ANSI codes
    COLOR_MAP = {
        "red": "\033[91m",
        "orange": "\033[38;5;208m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "cyan": "\033[96m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "magenta": "\033[95m",
    }

    # Color constants
    RED = COLOR_MAP["red"]
    ORANGE = COLOR_MAP["orange"]
    YELLOW = COLOR_MAP["yellow"]
    GREEN = COLOR_MAP["green"]
    CYAN = COLOR_MAP["cyan"]
    BLUE = COLOR_MAP["blue"]
    PURPLE = COLOR_MAP["purple"]

    @classmethod
    def get_color_code(cls, color: str | None) -> str:
        """Get ANSI color code by name."""
        if not color:
            return ""
        return cls.COLOR_MAP.get(str(color).lower(), "")

    @classmethod
    def format(cls, *args: Any, color: str | None = None, sep: str = " ") -> str:
        """Format arguments into a colored string without printing."""
        text = sep.join(str(arg) for arg in args)
        color_code = cls.get_color_code(color)
        if color_code:
            return f"{color_code}{text}{cls.RESET}"
        return text

    @classmethod
    def print(
        cls,
        *args: Any,
        color: str | None = None,
        sep: str = " ",
        end: str = "\n",
        file: Any = None,
        flush: bool = False,
    ) -> None:
        """Overloaded print method supporting color formatting.

        Args:
            *args: Values to print.
            color: One of 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'.
            sep: String inserted between values, default space.
            end: String appended after the last value, default newline.
            file: A file-like object (stream); defaults to current sys.stdout.
            flush: Whether to forcibly flush the stream.
        """
        output = cls.format(*args, color=color, sep=sep)
        target_file = file if file is not None else sys.stdout
        builtins.print(output, end=end, file=target_file, flush=flush)

    # Callable support: prints("message", color="red")
    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.print(*args, **kwargs)

    # Dedicated color methods
    @classmethod
    def red(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Red."""
        cls.print(*args, color="red", **kwargs)

    @classmethod
    def orange(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Orange."""
        cls.print(*args, color="orange", **kwargs)

    @classmethod
    def yellow(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Yellow."""
        cls.print(*args, color="yellow", **kwargs)

    @classmethod
    def green(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Green."""
        cls.print(*args, color="green", **kwargs)

    @classmethod
    def cyan(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Cyan."""
        cls.print(*args, color="cyan", **kwargs)

    @classmethod
    def blue(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Blue."""
        cls.print(*args, color="blue", **kwargs)

    @classmethod
    def purple(cls, *args: Any, **kwargs: Any) -> None:
        """Print in Purple."""
        cls.print(*args, color="purple", **kwargs)


# Alias for convenience
Color = Prints
prints = Prints()


# ==========================================
# Standalone functions for direct importing
# ==========================================

def print_red(*args: Any, **kwargs: Any) -> None:
    """Print message in Red."""
    Prints.red(*args, **kwargs)


def print_orange(*args: Any, **kwargs: Any) -> None:
    """Print message in Orange."""
    Prints.orange(*args, **kwargs)


def print_yellow(*args: Any, **kwargs: Any) -> None:
    """Print message in Yellow."""
    Prints.yellow(*args, **kwargs)


def print_green(*args: Any, **kwargs: Any) -> None:
    """Print message in Green."""
    Prints.green(*args, **kwargs)


def print_cyan(*args: Any, **kwargs: Any) -> None:
    """Print message in Cyan."""
    Prints.cyan(*args, **kwargs)


def print_blue(*args: Any, **kwargs: Any) -> None:
    """Print message in Blue."""
    Prints.blue(*args, **kwargs)


def print_purple(*args: Any, **kwargs: Any) -> None:
    """Print message in Purple."""
    Prints.purple(*args, **kwargs)


def print_color(*args: Any, color: str | None = None, **kwargs: Any) -> None:
    """Print message in specified color."""
    Prints.print(*args, color=color, **kwargs)


__all__ = [
    "Prints",
    "prints",
    "Color",
    "print_red",
    "print_orange",
    "print_yellow",
    "print_green",
    "print_cyan",
    "print_blue",
    "print_purple",
    "print_color",
]


if __name__ == "__main__":
    builtins.print("=== Direct Function Calls ===")
    print_red("Red: print_red('...')")
    print_orange("Orange: print_orange('...')")
    print_yellow("Yellow: print_yellow('...')")
    print_green("Green: print_green('...')")
    print_cyan("Cyan: print_cyan('...')")
    print_blue("Blue: print_blue('...')")
    print_purple("Purple: print_purple('...')")
