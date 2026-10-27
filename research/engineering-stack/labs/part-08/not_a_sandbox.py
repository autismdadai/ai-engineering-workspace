"""Why exec() with empty builtins is not a sandbox (Python's own docs say so).

Python's docs: overriding __builtins__ "is **not** a security mechanism: the
executed code can still access all builtins." This script shows it, harmlessly:
code run with no builtins at all still reaches the os module, by walking from an
empty tuple to Python's own classes. It only reads os.getcwd(); it changes
nothing. Run: python not_a_sandbox.py
"""

ESCAPE = """
for cls in ().__class__.__base__.__subclasses__():
    if cls.__name__ == "BuiltinImporter":
        found = cls.load_module("os").getcwd()
        break
"""


def escaped():
    namespace = {"__builtins__": {}}   # "no builtins": the naive sandbox
    try:
        exec(ESCAPE, namespace)
    except Exception as error:
        return False, f"blocked by {type(error).__name__}"
    return "found" in namespace, namespace.get("found")


if __name__ == "__main__":
    reached, detail = escaped()
    print(f"code with no builtins reached the os module: {reached}")
    print(f"it could read the working folder: {detail}")
    print("A real boundary is a separate process with OS-level limits: a container, gVisor or a VM.")
