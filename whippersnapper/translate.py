#!/usr/bin/env python
import argparse
import re


class MessageParser(object):

    def __init__(self, message, promiscuous=False):
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

                if bits[1][-1] == "\n":
                    dictionary[bits[0]] = bits[1][:-1]  # slice newline
                else:
                    dictionary[bits[0]] = bits[1]

        return dictionary

    def parse(self):
        """Parse the message and attempt substitution."""
        result = []

        for word in self.message:
            result.append(self.substitute(word))

        return " ".join([i for i in result])

    def edge_of_sentence_segment(self, word):
        # @todo only call in promiscuous mode?
        """Check if a word ends with standard segment edge punctuation."""
        if word[-1] in ['.', ',', '!', '?', ';']:
            return True
        return False

    def substitute(self, word):
        """Return shorthand substitution or original word."""
        entry = self.dictionary.get(word, None)  # easy, explicit match

        if entry:
            return entry
        else:
            if self.edge_of_sentence_segment(word):
                punctuation = word[-1]
                entry = self.dictionary.get(word[:-1], None)
                if entry:
                    return entry + punctuation  # re-add punctuation
                else:
                    return word  # return original
            else:
                return word  # return original


def _get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Translate shorthand within a text message.")

    parser.add_argument(
        "message", type=str, help="the text message to translate")
    parser.add_argument(
        "-p", "--promiscuous", help="parse text message promiscuously",
        action="store_true")

    return parser.parse_args()


def _display_output(original, translated):
    """Format stdout."""
    print "\n" + ("#" * 31) + " ORIGINAL MESSAGE " + ("#" * 31)
    print original + "\n"
    print ("#" * 30) + " TRANSLATED MESSAGE " + ("#" * 30)
    print translated + "\n"


if __name__ == "__main__":
    args = _get_args()
    parser = MessageParser(args.message, args.promiscuous)
    result = parser.parse()
    _display_output(args.message, result)
