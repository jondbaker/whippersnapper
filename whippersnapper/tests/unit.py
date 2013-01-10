#!/usr/bin/env python
import sys
sys.path.append("..")
from whippersnapper.translate import MessageParser
sys.path.remove("..")

import unittest


class BaseTestCase(unittest.TestCase):

    MESSAGE = """Hi Grandma!  459! Can't wait to CU :-).  JC if u got my thank
you card for the U2 tickets: they are SOOOO awesome! XOXO, Lola"""

    def setUp(self):
        self.parser = MessageParser(self.MESSAGE, False)


class TestBuildDictionary(BaseTestCase):

    def setUp(self):
        super(TestBuildDictionary, self).setUp()

    def test_empty_source(self):
        result = self.parser.build_dictionary(
            "./tests/fixtures/empty.txt", False)
        self.assertEqual(result, {})

    def test_first_entry(self):
        result = self.parser.build_dictionary(
            "./tests/fixtures/dictionary.txt", False)
        self.assertEqual(result["459"], "I Love You")

    def test_last_entry(self):
        result = self.parser.build_dictionary(
            "./tests/fixtures/dictionary.txt", False)
        self.assertEqual(
            result[":%I"], "Lowering glasses to see if you're serious")

    def test_promiscuous(self):
        pass


class TestParse(BaseTestCase):

    def setUp(self):
        super(TestParse, self).setUp()

    def test_expected_result(self):
        result = self.parser.parse()
        expected = "Hi Grandma! I Love You! Can't wait to See You Happy. Just Curious if You got my thank you card for the You Too tickets: they are SOOOO awesome! Hugs and Kisses, Lola"
        self.assertEqual(result, expected)


class TestEdgeOfSentenceSegment(BaseTestCase):

    def setUp(self):
        super(TestEdgeOfSentenceSegment, self).setUp()

    def test_edge_emoticon(self):
        result = self.parser.edge_of_sentence_segment(":&.")
        self.assertTrue(result)

    def test_emoticon(self):
        result = self.parser.edge_of_sentence_segment(":&")
        self.assertFalse(result)

    def test_edge_shorthand(self):
        result = self.parser.edge_of_sentence_segment("459,")
        self.assertTrue(result)

    def test_shorthand(self):
        result = self.parser.edge_of_sentence_segment("459")
        self.assertFalse(result)

    def test_edge_word(self):
        result = self.parser.edge_of_sentence_segment("Howdy!")
        self.assertTrue(result)

    def test_word(self):
        result = self.parser.edge_of_sentence_segment("Howdy")
        self.assertFalse(result)


class TestSubstitute(BaseTestCase):

    def setUp(self):
        super(TestSubstitute, self).setUp()

    def test_edge_emoticon(self):
        result = self.parser.substitute(":&.")
        self.assertEqual(result, "Tongue-tied.")

    def test_emoticon(self):
        result = self.parser.substitute(":&")
        self.assertEqual(result, "Tongue-tied")

    def test_edge_shorthand(self):
        result = self.parser.substitute("459,")
        self.assertEqual(result, "I Love You,")

    def test_shorthand(self):
        result = self.parser.substitute("459")
        self.assertEqual(result, "I Love You")

    def test_edge_word(self):
        result = self.parser.substitute("Howdy!")
        self.assertEqual(result, "Howdy!")

    def test_word(self):
        result = self.parser.substitute("Howdy")
        self.assertEqual(result, "Howdy")


if __name__ == "__main__":
    unittest.main()
