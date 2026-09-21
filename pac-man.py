from src.m1_config_parser import Parser
import sys


def main():

    if len(sys.argv) != 2:
        raise Exception("\n❌ Usage: python3 pac-man.py <config_file>.json\n")

    if not sys.argv[1].endswith('.json'):
        raise Exception(f"❌ JSON format: '{sys.argv[1]}' must be a json file")

    p = Parser(sys.argv[1])

    print(p.config_txt)


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(e)
