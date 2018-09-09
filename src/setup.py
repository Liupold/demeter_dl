from cx_Freeze import setup, Executable

base = None

executables = [Executable("cli.py", base=base, icon='icon.ico')]

packages = ["idna", "dl_engine", "smart_thread",
            "req_fn", "requests", "main_dl_fn", "os", "queue", "time", "tqdm", "colorama", "urllib"]
options = {
    'build_exe': {
        'packages': packages,
    },
}
setup(

    name="frist_build",
    options=options,
    version="0.1.3",
    description='<any description>',
    executables=executables
)
