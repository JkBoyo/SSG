import unittest

from constants import Text_Type, Block_Type
from htmlnode import LeafNode, ParentNode
from conversion import (text_node_to_html_node, 
                        check_for_ordered_list, 
                        line_start_contains, 
                        markdown_to_blocks, 
                        text_to_htmlnode,
                        text_to_html_list_nodes,
                        block_to_html_node,
                        block_to_block_type) 
from textnode import TextNode


class TestTNConversion(unittest.TestCase):
    def test_conversion_by_text_type(self):
        test_cases = [
            (TextNode("this is a test", Text_Type.text, None), 
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

        for text_node_ex, expected_result, message in test_cases:
            self.assertEqual(text_node_to_html_node(text_node_ex), expected_result, message)

    def test_invalid_text_type(self):
        node = TextNode("this is a test", 'incorrect', None)
        with self.assertRaises(ValueError, msg= "Unknown text type"):
            text_node_to_html_node(node)

    def test_check_for_ordered_list(self):
        test_lists = [
                "1. first el\n2. second el\n3. third el\n4. 4th el",
                "2. second el\n1. first el\n3. third el"
        ]
        expected_results = [
            True,
            False
        ]
        self.assertEqual([check_for_ordered_list(test_list) for test_list in test_lists], expected_results)

    def test_line_start_contains(self):
        test_strings = [
            "* one\n- two\n> three",
            "( one\n- two\n> three"
        ]
        expected_results = [
            True,
            False
        ]
        self.assertEqual([line_start_contains(test_string, '*->') for test_string in test_strings], expected_results)
    
    def test_markdown_to_blocks(self):
        test_markdown = [
            "this is a paragraph block\n\n1. list block\n2. with multiple elements",
            "\n\nparagraph block\n\n* unordered list\n- block"
        ]
        result_lists = [
            [
                "this is a paragraph block",
                "1. list block\n2. with multiple elements"
            ],
            [
                "paragraph block",
                "* unordered list\n- block"
            ]
        ]
        self.assertEqual([markdown_to_blocks(markdown) for markdown in test_markdown], result_lists)
        test_md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        result_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        ]
        self.assertEqual(markdown_to_blocks(test_md), result_blocks)
    def test_text_to_html_list_nodes(self):
        example_text_list = [
            ("1. first el\n2. second el\n3. third el", 'ol'),
            ("- first el\n- second el\n- third el", 'ul')
        ]
        result_nodes = [
            [
            ParentNode('li', [LeafNode(None, "first el", None)], None), 
            ParentNode('li', [LeafNode(None, "second el", None)], None), 
            ParentNode('li', [LeafNode(None, "third el", None)], None),
            ],
            [
            ParentNode('li', [LeafNode(None, "first el", None)], None),
            ParentNode('li', [LeafNode(None, "second el", None)], None),
            ParentNode('li', [LeafNode(None, "third el", None)], None)
            ]
        ]
        self.assertEqual([text_to_html_list_nodes(text, list_t) for text, list_t in example_text_list],
                         result_nodes)
        
    def test_block_to_html_node(self):
        test_blocks = [
            ("# heading 1",Block_Type.heading) , ("## heading 2", Block_Type.heading), ("### heading 3", Block_Type.heading), ("#### heading 4", Block_Type.heading), 
            ("##### heading 5", Block_Type.heading), ("###### heading 6", Block_Type.heading) ,
            ("```\nthis is a code block\n```", Block_Type.code),
            ("> these lines\n> should all be in a quote block\n> correctly laid out", Block_Type.quote),
            ("* 1st el\n- 2nd el\n* 3rd el",Block_Type.unordered_list),
            ("1. 1st el\n2. 2nd el\n3. 3rd el", Block_Type.ordered_list),
            ("this should just be a paragraph", Block_Type.paragraph)
        ]
        self.maxDiff = None
        expected_htmlnode = [
            ParentNode('h1', text_to_htmlnode("heading 1")),     
            ParentNode('h2', text_to_htmlnode("heading 2")),     
            ParentNode('h3', text_to_htmlnode("heading 3")),     
            ParentNode('h4', text_to_htmlnode("heading 4")),     
            ParentNode('h5', text_to_htmlnode("heading 5")),     
            ParentNode('h6', text_to_htmlnode("heading 6")),     
            ParentNode('pre',ParentNode('code', text_to_htmlnode("this is a code block"))),     
            ParentNode('blockquote', text_to_htmlnode("these lines\nshould all be in a quote block\ncorrectly laid out")),     
            ParentNode('ul', text_to_html_list_nodes("* 1st el\n- 2nd el\n* 3rd el", 'ul')),     
            ParentNode('ol', text_to_html_list_nodes("1. 1st el\n2. 2nd el\n3. 3rd el", 'ol')),     
            ParentNode('p', text_to_htmlnode("this should just be a paragraph")),     
        ]
        self.assertEqual([block_to_html_node(block, block_type) for block, block_type in test_blocks], expected_htmlnode)
    
    def test_Blocks_to_block_type(self):
        test_block_list = ["###### This is a heading",
                           "####### this is not a heading",
                            "```\nprint('this is a code block')\n```",
                            "```\nprint('this code block is missing a backtick')\n``",
                            "> this block is a quote block\n> with three separate lines of quoted text\n> Ain't that neat",
                            ">this block forgot the space after the line start",
                            "* this is an undordered list\n- with hyphens\n* and stars",
                            "* this unordered list has a wrong char\n$ on the second element",
                            "1. first element\n2. second element\n3. third element",
                            "1. the second element\n3. wrong spot\n2. is in"]
        test_block_results = [Block_Type.heading,
                              Block_Type.paragraph,
                              Block_Type.code,
                              Block_Type.paragraph,
                              Block_Type.quote,
                              Block_Type.paragraph,
                              Block_Type.unordered_list,
                              Block_Type.paragraph,
                              Block_Type.ordered_list,
                              Block_Type.paragraph]
        self.assertEqual([block_to_block_type(block) for block in test_block_list] , test_block_results)