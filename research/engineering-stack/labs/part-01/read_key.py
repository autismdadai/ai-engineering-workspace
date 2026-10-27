"""Read an API key without ever printing it.

No lab in this series needs a key. This script is for practicing the habit:
a key lives in an environment variable or in a .env file that Git ignores,
never in code, and a program refuses to run without one instead of guessing.

    python read_key.py

It looks for EXAMPLE_API_KEY in the environment first, then in a .env file in
the current folder. Exit code 0 means a usable key was found; 2 means it wasn't.
"""
import os
import sys

NAME = "EXAMPLE_API_KEY"
PLACEHOLDER = "replace-me"


def from_dotenv(path=".env"):
    """A minimal .env reader: NAME=value lines, # comments, optional quotes."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() == NAME:
                    return value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


def main():
    value, source = os.environ.get(NAME), "the environment"
    if not value:
        value, source = from_dotenv(), "the .env file"
    if not value:
        print(f"No {NAME} found. Set it in the environment or in a .env file "
              "(copy .env.example to .env).")
        return 2
    if value == PLACEHOLDER:
        print(f"{NAME} in {source} is still the placeholder; replace it in .env.")
        return 2
    print(f"{NAME} found in {source} ({len(value)} characters). Its value is not shown.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
