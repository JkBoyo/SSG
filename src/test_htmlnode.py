import unittest

from htmlnode import HtmlNode


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

        
        
    

        