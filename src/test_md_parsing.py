import unittest

from constants import Text_Type
from mdtotextnode import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks
    )
from textnode import TextNode


class Test_MD_Parsing(unittest.TestCase):
    def setup_test_nodes(self):
        test_nodes = [
            TextNode("this **word** is delimited", Text_Type.text),
            TextNode("*word* delimited this is", Text_Type.text), 
            TextNode("no words are delimited", Text_Type.text),
            TextNode("there are `two` delimited *words*", Text_Type.text),
            TextNode("there is an **incorrect** delimiter in this node", Text_Type.text),
            TextNode("all of this is bold", Text_Type.bold)
        ]

        result_nodes = [
            TextNode("this ", Text_Type.text),
            TextNode("word", Text_Type.bold),
            TextNode(" is delimited", Text_Type.text),
            TextNode("word", Text_Type.italic),
            TextNode(" delimited this is", Text_Type.text),
            TextNode("no words are delimited", Text_Type.text),
            TextNode("there are ", Text_Type.text),
            TextNode("two", Text_Type.code),
            TextNode(" delimited ", Text_Type.text),
            TextNode("words", Text_Type.italic),
            TextNode("there is an ", Text_Type.text),
            TextNode("incorrect", Text_Type.bold),
            TextNode(" delimiter in this node", Text_Type.text),
            TextNode("all of this is bold", Text_Type.bold)
        ]
        return test_nodes, result_nodes
    
    def test_split_nodes_delimiter(self):
        self.maxDiff = None

        test_list, result_list =  self.setup_test_nodes()

        nodes_bolded = split_nodes_delimiter(test_list, '**', Text_Type.bold)

        nodes_italicized = split_nodes_delimiter(nodes_bolded, '*', Text_Type.italic)

        finished_nodes = split_nodes_delimiter(nodes_italicized, '`', Text_Type.code)

        self.assertEqual(finished_nodes, result_list)


    def test_single_delimiter(self):
        test_single_delimiter_list = [
        TextNode("only one **delimiter", Text_Type.text)
        ]
        with self.assertRaises(Exception, msg= "Incorrect Markdown closing symbol not found"):
            split_nodes_delimiter(test_single_delimiter_list, '**', Text_Type.bold)

    def test_extract_md_img(self):
        test_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        for link_tuple in extract_markdown_images(test_string):
            self.assertIn(link_tuple, result)

    def test_extract_md_link(self):
        test_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        for link_tuple in extract_markdown_links(test_string):
            self.assertIn(link_tuple, result)

    def test_split_nodes_links(self):
        test_nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                     Text_Type.text)
        ]

        result_nodes = [
            TextNode("This is text with a link ", Text_Type.text),
            TextNode("to boot dev", Text_Type.link, "https://www.boot.dev"),
            TextNode(" and ", Text_Type.text),
            TextNode(
                "to youtube", Text_Type.link, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertEqual(split_nodes_link(test_nodes), result_nodes)
    def test_split_nodes_imgs(self):
        test_nodes = [
            TextNode(
                "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                     Text_Type.text)
        ]

        result_nodes = [
            TextNode("This is text with a image ", Text_Type.text),
            TextNode("to boot dev", Text_Type.image, "https://www.boot.dev"),
            TextNode(" and ", Text_Type.text),
            TextNode(
                "to youtube", Text_Type.image, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_image(test_nodes), result_nodes)

    def test_split_nodes_img_and_link(self):
        test_nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and an img ![to youtube](https://www.youtube.com/@bootdotdev)",
                     Text_Type.text)
        ]

        result_nodes_img = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and an img ", Text_Type.text),
            TextNode(
                "to youtube", Text_Type.image, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        result_nodes_link = [
            TextNode("This is text with a link ", Text_Type.text),
            TextNode("to boot dev", Text_Type.link, "https://www.boot.dev"),
            TextNode(
                " and an img ![to youtube](https://www.youtube.com/@bootdotdev)", Text_Type.text),
        ]

        result_nodes_both = [
            TextNode("This is text with a link ", Text_Type.text),
            TextNode("to boot dev", Text_Type.link, "https://www.boot.dev"),
            TextNode(" and an img ", Text_Type.text),
            TextNode(
                "to youtube", Text_Type.image, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertEqual(split_nodes_image(test_nodes), result_nodes_img)

        self.assertEqual(split_nodes_link(test_nodes), result_nodes_link)

        self.assertEqual(split_nodes_image(split_nodes_link(test_nodes)), result_nodes_both)
    
    def test_text_to_textnodes(self):
        test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result_nodes = [
                TextNode("This is ", Text_Type.text),
                TextNode("text", Text_Type.bold),
                TextNode(" with an ", Text_Type.text),
                TextNode("italic", Text_Type.italic),
                TextNode(" word and a ", Text_Type.text),
                TextNode("code block", Text_Type.code),
                TextNode(" and an ", Text_Type.text),
                TextNode("obi wan image", Text_Type.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", Text_Type.text),
                TextNode("link", Text_Type.link, "https://boot.dev"),
            ]   
        self.assertEqual(text_to_textnodes(test_text), result_nodes)

    def test_markdown_to_blocks(self):
        test_md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        result_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        ]
        self.assertEqual(markdown_to_blocks(test_md), result_blocks)