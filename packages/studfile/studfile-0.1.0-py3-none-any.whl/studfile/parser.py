import argparse

def build_parser(stud_file: dict) -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='Studfile build tool')
    subparsers = parser.add_subparsers(help='Commands', dest='command')

    # options = parser.parse_args(args)

    for key in stud_file:
        help = ''
        if 'help' in stud_file[key]:
            help = stud_file[key]['help']
        temp_parser = subparsers.add_parser(key, help=help)
        if 'options' in stud_file[key].keys():
            for opt in stud_file[key]['options']:
                build_arguments(opt, temp_parser)

    return parser
        

def build_arguments(data: dict, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    required_keys = [
        'name'
    ]
    for k in required_keys:
        if not k in data.keys():
            raise KeyError(f"Key {k} does not exist in arg block")

    flags = data['name'].split(',')
    kwargs = parse_kwargs(data)

    if len(flags) > 1:
        short = flags[0].strip()
        long = flags[1].strip()
        parser.add_argument(short, long, **kwargs)
    else:
        name = flags[0].strip()
        parser.add_argument(name, **kwargs)

def parse_kwargs(data: dict) -> dict:
    kwargs = {}
    keys = ['default', 'nargs', 'required']
    for key in keys:
        if key in data.keys():
            kwargs[key] = data[key]
    return kwargs
