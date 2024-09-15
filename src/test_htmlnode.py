import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def setUp(self):
        self.one_att_dict = {"href": "https://www.link.com"}
        self.href_html = " href=\"https://www.link.com\""
        self.target_html = " target=\"_blank\""
        

        self.two_att_dict = {"href": "https://www.link.com", "target": "_blank"}

    def test_1_prop(self):
        node = HtmlNode(props= self.one_att_dict)

        self.assertEqual(node.props_to_html(), " href=\"https://www.link.com\"")

    def test_2_props(self):
        node = HtmlNode(props= self.two_att_dict)
        
        met_html = node.props_to_html()

        self.assertIn(self.href_html, met_html)

        self.assertIn(self.target_html, met_html)
        
    def test_no_props(self):
        node = HtmlNode()

        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_if_not_value(self):
        with self.assertRaises(ValueError, msg="All Leaf Nodes must have a value"):
            LeafNode("a", None, {"href": "https://www.link.com"})
        
    def test_with_mult_attr(self):
        node = LeafNode("a", "This is a Link!", {"href": "https://www.link.com", "target": "_blank"})

        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.link.com" target="_blank">This is a Link!</a>'
            )
        
    def test_with_no_tag(self):
        node = LeafNode(None, "This is a Link!", {"href": "https://www.link.com"})

        self.assertEqual(node.to_html(), "This is a Link!")

class TestParentNode(unittest.TestCase):
    def test_one_layer_PN(self):
        node = ParentNode(
        "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_children_error(self):
        node = ParentNode("p", None,None)

        with self.assertRaises(ValueError, msg= "All ParentNode's must have children"):
            node.to_html()

    def test_no_tag_error(self):
        node = ParentNode(
        None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        with self.assertRaises(ValueError, msg="All ParentNode's must have a tag"):
            node.to_html()

    def test_multi_layer_PN(self):
        node = ParentNode(
        "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
        'a',
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            ),
                LeafNode("i", "italic text"),
                ParentNode(
        'a',
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            ),
            ],
            )
        
        self.assertEqual(node.to_html(), 
                    "<p><b>Bold text</b><a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a><i>italic text</i><a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a></p>")
        