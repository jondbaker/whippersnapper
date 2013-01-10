#!/usr/bin/env python
import argparse


class MessageParser(object):

    def __init__(self, message, promiscuous):
        """Initialize instance variables."""
        self.dictionary = self.build_dictionary(
            "./dictionary.txt", promiscuous)
        # remove extra whitespaces then split words
        self.message = " ".join(message.split()).split(" ")

    def build_dictionary(self, source, promiscuous):
        """Build the shorthand dictionary."""
        dictionary = {}

        with open(source, "r") as f:
            for line in f:
                bits = line.replace(" ", "").split("=")
                dictionary[bits[0]] = bits[1][:-1]  # slice newline

        return dictionary

    def parse(self):
        """Parse the message and translate as necessary."""
        result = []

        for word in self.message:
            word = self.translate(word)
            result.append(word)

        return " ".join([i for i in result])

    def edge_of_sentence_segment(self, word):
        # @todo only call in promiscuous mode?
        """Check if a word ends with standard sentence-end punctuation."""
        if word[-1] in ['.', ',', '!', '?']:
            return True
        return False

    def translate(self, word):
        """Return dictionary match or original word."""
        match = self.dictionary.get(word, None)  # easy, explicit match

        if match:
            return match
        else:
            if self.edge_of_sentence_segment(word):
                # @todo add punctuation back
                return self.dictionary.get(word[:-1], word)
            else:
                return word


def _get_args():
    parser = argparse.ArgumentParser(
        description="Translate shorthand within a text message.")

    parser.add_argument(
        "message", type=str, help="the text message to translate")
    parser.add_argument(
        "-p", "--promiscuous", help="parse text message promiscuously",
        action="store_true")

    return parser.parse_args()


def _display_output(original, translated):
    print "\n" + ("#" * 31) + " ORIGINAL MESSAGE " + ("#" * 31)
    print original + "\n"
    print ("#" * 30) + " TRANSLATED MESSAGE " + ("#" * 30)
    print translated + "\n"


if __name__ == "__main__":
    args = _get_args()
    parser = TextMessageParser(args.message, args.promiscuous)
    result = parser.parse()
    _display_output(args.message, result)
