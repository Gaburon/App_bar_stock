from cx_Freeze import setup, Executable

base = None

executables = [Executable("App.py", base=base)]

setup(
    name="App Stoc",
    version="1.0",
    description="App de control de stock",
    executables=executables,
)