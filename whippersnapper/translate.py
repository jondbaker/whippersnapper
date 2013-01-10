#!/usr/bin/env python
import argparse


def _get_args():
    parser = argparse.ArgumentParser(
        description="Translate shorthand within a text message.")

    parser.add_argument(
        "message", type=str, help="the text message to translate",
        nargs=argparse.REMAINDER)
    parser.add_argument(
        "-p", "--promiscuous", help="parse text message promiscuously",
        action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()
