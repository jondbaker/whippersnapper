#!/usr/bin/env python
import argparse
import re


class MessageParser(object):
    """
    A message parser that can perform emoticon and shorthand substitutions.
    """
    def __init__(self, message, promiscuous=False):
        """Initialize instance variables."""
        self.promiscuous = promiscuous
        self.dictionary = self.build_dictionary("./dictionary.txt")
        # remove extra whitespaces then split words
        self.message = " ".join(message.split()).split(" ")

    def build_dictionary(self, source):
        """Build the shorthand dictionary."""
        dictionary = {}
        pattern = re.compile(r'^(.+)\s=\s(.+)$')

        with open(source, "r") as f:
            for line in f:
                match = re.match(pattern, line.replace("\n", ""))
                if match:
                    if self.promiscuous:
                        dictionary[match.group(1).lower()] = match.group(2)
                    else:
                        dictionary[match.group(1)] = match.group(2)
                # @todo how to handle no match?

        # @todo raise exception if empty?
        return dictionary

    def parse(self):
        """Parse the message and attempt substitution."""
        result = []

        for word in self.message:
            result.append(self.substitute(word))

        return " ".join([i for i in result])

    def edge_of_sentence_segment(self, word):
        """Check if a word ends with standard segment edge punctuation."""
        if word[-1] in ['.', ',', '!', '?', ';']:
            return True
        return False

    def substitute(self, word):
        """Return shorthand substitution or original word."""
        if self.promiscuous:
            word = word.lower()

        entry = self.dictionary.get(word, None)  # exact match

        if entry:
            return entry
        elif self.edge_of_sentence_segment(word):
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
        description="Translate a message containing emoticon and shorthand text.")

    parser.add_argument(
        "message", type=str, help="the message to translate")
    parser.add_argument(
        "-p", "--promiscuous", help="perform substitutions promiscuously",
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
