from constants import Text_Type
from textnode import TextNode

old_nodes = []
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == Text_Type.text:
            index_of_delimited_node = 1
            if node.text[:len(delimiter)] == delimiter:
                index_of_delimited_node = 0
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("Incorrect Markdown closing symbol not found")
            else:
                split_strings = node.text.split(delimiter)

                if split_strings[0] == '':
                    split_strings = split_strings[1:]
                if split_strings[-1] == '':
                    split_strings = split_strings[:-1]

                for i, string in enumerate(split_strings, index_of_delimited_node):
                    if i % 2 == 1:
                        new_nodes.append(TextNode(string, Text_Type.text))
                    else:
                        new_nodes.append(TextNode(string, text_type))
        else:
            new_nodes.append(node)
    return new_nodes