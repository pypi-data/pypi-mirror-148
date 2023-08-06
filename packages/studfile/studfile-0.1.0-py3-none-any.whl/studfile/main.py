import os
import sys
import yaml
from studfile import parser
from studfile import runner

def main(args: list = sys.argv[1:]):
    file_path = f"{os.getcwd()}/studfile.yaml"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Studfile not found at {file_path}")

    with open(file_path, 'r', encoding='utf-8') as fi:
        stud_file = yaml.load(fi, yaml.FullLoader)

    argument_parser = parser.build_parser(stud_file)

    options = argument_parser.parse_args(args)

    runner.run(stud_file, options)

if __name__ == "__main__":
    sys.exit(main() or 0)
