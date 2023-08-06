import calligraphy_scripting
import argparse

def run(stud_file: dict, options: argparse.Namespace) -> None:
    if not 'cmd' in stud_file[options.command].keys():
        raise KeyError(f"Command {options.command} does not contain a 'cmd' block")
    cmd = stud_file[options.command]['cmd']

    for key in vars(options):
        if key != 'command':
            val = getattr(options, key)
            cmd = f'{key} = {repr(val)}\n' + cmd
    calligraphy_scripting.runner.execute(cmd)
