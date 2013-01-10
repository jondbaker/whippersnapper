#!/usr/bin/env python
import argparse


class TextMessageParser(object):

    def __init__(self, message, promiscuous):
        self.dictionary = self.build_dictionary(
            "./dictionary.txt", promiscuous)
        # remove extra whitespaces then split words
        self.message = " ".join(message.split()).split(" ")

    def build_dictionary(self, source, promiscuous):
        dictionary = {}

        with open(source, "r") as f:
            for line in f:
                bits = line.replace(" ", "").split("=")
                dictionary[bits[0]] = bits[1][:-1]  # slice newline

        return dictionary

    def parse(self):
        result = []

        for word in self.message:
            result.append(self.dictionary.get(word, word))

        return " ".join([i for i in result])


def _get_args():
    parser = argparse.ArgumentParser(
        description="Translate shorthand within a text message.")

    parser.add_argument(
        "message", type=str, help="the text message to translate")
    parser.add_argument(
        "-p", "--promiscuous", help="parse text message promiscuously",
        action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()
    parser = TextMessageParser(args.message, args.promiscuous)
    result = parser.parse()
    print result
