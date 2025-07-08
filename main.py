import argparse
import const
from polling import start


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--file', type=str, help=const.file_help)
    parser.add_argument('--where', type=str, help=const.where_help)
    parser.add_argument('--aggregate', type=str, help=const.aggregate_help)

    parse_args = parser.parse_args()

    if parse_args.file is None: return parser.print_help()

    start(parse_args)

if __name__ == "__main__":
    main()