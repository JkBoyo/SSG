import unittest

from constants import Text_Type
from htmlnode import LeafNode
from main import text_node_to_html_node
from textnode import TextNode


class TestTNConversion(unittest.TestCase):
    def test_conversion_by_text_type(self):
        test_cases = [
            (TextNode("this is a test", Text_Type.test, None), 
            LeafNode(None, "this is a test", None),
            "text test"), 
            (TextNode("this is a test", Text_Type.bold, None), 
            LeafNode('b', "this is a test", None),
            "bold test"),
            (TextNode("this is a test", Text_Type.italic, None), 
            LeafNode('i', "this is a test", None),
            "italic test"),
            (TextNode("this is a test", Text_Type.code, None), 
            LeafNode('code', "this is a test", None), 
            "code test"),
            (TextNode("this is a test", Text_Type.link, "https://www.test.com"), 
            LeafNode('a', "this is a test", {"href": "https://www.test.com"}),
            "link test"),
            (TextNode("this is a test", Text_Type.image, "https://www.test-image.com"), 
            LeafNode('img', "", {'src': "https://www.test-image.com", 'alt': "this is a test"},),
            "image test")
        ]

        for text_node_ex, expected_result in test_cases:
            self.assertEqual(text_node_to_html_node(text_node_ex), expected_result)

    def test_invalid_text_type(self):
        node = TextNode("this is a test", 'incorrect', None)
        with self.assertRaises(ValueError, msg= "Unknown text type"):
            text_node_to_html_node(node)