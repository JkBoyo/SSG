from re import match, findall

from constants import Text_Type, Block_Type
from textnode import TextNode

def markdown_to_blocks(markdown):
    block_list = markdown.split('\n\n')
    for block in block_list:
        block.strip()
        if block == '':
            block_list.remove(block)
    return block_list

def block_to_block_type(block:str):
    if match("^#{1,6} ", block):
        return Block_Type.heading
    elif block[:3] == '```' and block[-3:] == '```':
        return Block_Type.code
    elif line_start_contains(block, '>'):
        return Block_Type.quote
    elif line_start_contains(block, '*-'):
        return Block_Type.unordered_list
    elif check_for_ordered_list(block):
        return Block_Type.ordered_list
    else:
        return Block_Type.paragraph
    
    
def line_start_contains(block, chars):
    for line in block.splitlines():
        if line[0] not in chars or line[1] != ' ':
            return False
    return True
    
def check_for_ordered_list(block):
    for i, line in enumerate(block.splitlines(), start = 1):
        if line[:3] != f"{i}. ":
            return False
    return True

def text_to_textnodes(text):
    text_n = TextNode(text, Text_Type.text)
    text_n_results = split_nodes_link(
                split_nodes_image(
                split_nodes_delimiter(
                split_nodes_delimiter(
                split_nodes_delimiter(
                    [text_n], '**', Text_Type.bold
                    ), '*', Text_Type.italic
                ), '`', Text_Type.code
            )
        )
    )
    return text_n_results

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
    