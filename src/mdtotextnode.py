from re import findall

from constants import Text_Type
from textnode import TextNode

old_nodes = []
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == Text_Type.text:
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("Incorrect Markdown closing symbol not found")
            else:                
                index_of_delimited_node = 1
                if node.text[:len(delimiter)] == delimiter:
                    index_of_delimited_node = 0
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

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    image_tuple = findall(pattern, text)
    return image_tuple

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    link_tuples = findall(pattern, text)
    return link_tuples    


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
        else:
            split_nodes = []
            remaining_text = node.text
            for image in images:
                alt_text, image_url = image
                split_strings = remaining_text.split(f"![{alt_text}]({image_url})", 1)
                if len(split_strings) == 2:
                    split_nodes.extend([
                        TextNode(split_strings[0], Text_Type.text),
                        TextNode(alt_text, Text_Type.image, image_url)
                    ])
                    remaining_text = split_strings[1]
                else:
                    break
            if remaining_text:
                split_nodes.append(TextNode(remaining_text, Text_Type.text))
            for split_node in split_nodes:
                if split_node.text == '':
                    pass
                else:
                    new_nodes.append(split_node)
            
    return new_nodes
            

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
        else:
            split_nodes = []
            remaining_text = node.text
            for link in links:
                alt_text, link_url = link
                split_strings = remaining_text.split(f"[{alt_text}]({link_url})", 1)
                if len(split_strings) == 2:
                    split_nodes.extend([
                        TextNode(split_strings[0], Text_Type.text),
                        TextNode(alt_text, Text_Type.link, link_url)
                    ])
                    remaining_text = split_strings[1]
                else:
                    break
            if remaining_text:
                split_nodes.append(TextNode(remaining_text, Text_Type.text))
            for split_node in split_nodes:
                if split_node.text == '':
                    pass
                else:
                    new_nodes.append(split_node)
            
    return new_nodes
    