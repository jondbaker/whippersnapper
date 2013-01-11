#!/usr/bin/env python
import argparse


def main(key, value):
    with open("./dictionary.txt", "a") as f:
        f.write("{} = {}".format(key, value))
    print "Successfully added {} = {}".format(key, value)


def _get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Add emoticon and shorthand dictionary entries.")

    parser.add_argument("-k", "--key", type=str, help="The entry key")
    parser.add_argument("-v", "--value", type=str, help="The entry value")

    return parser.parse_args()

if __name__ == "__main__":
    args = _get_args()
    main(args.key, args.value)
