import unittest

from constants import Text_Type
from mdtotextnode import split_nodes_delimiter
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