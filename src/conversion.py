from htmlnode import ParentNode, LeafNode
from constants import Block_Type, Text_Type
from mdtotextnode import text_to_textnodes
from re import match

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    html_node_list = []
    for block in block_list:
        block_type = block_to_block_type(block)
        html_node_list.append(block_to_html_node(block, block_type))
    return ParentNode('div',html_node_list)

def block_to_html_node(block, block_type):
    match(block_type):
        case Block_Type.heading:
            header, text = block.split(maxsplit=1)
            heading_size = header.count('#')
            return ParentNode(f"h{heading_size}", 
                              text_to_htmlnode(text))
        case Block_Type.code:
            #cut off the backticks
            text = block[3:-4].strip()
            return ParentNode('pre',
                ParentNode('code',
                              text_to_htmlnode(text))
                              )
        case Block_Type.quote:
            text = block.replace('> ', "")
            return ParentNode('blockquote',
                              text_to_htmlnode(text))
        case Block_Type.unordered_list:
            return ParentNode('ul',
                              text_to_html_list_nodes(block, 'ul'))
        case Block_Type.ordered_list:
            return ParentNode('ol',
                              text_to_html_list_nodes(block, 'ol'))
        case Block_Type.paragraph:
            return ParentNode('p',
                              text_to_htmlnode(block))
        
def text_node_to_html_node(textnode):
    match textnode.text_type:
        case Text_Type.text:
            return LeafNode(None, textnode.text, None)
        case Text_Type.bold:
            return LeafNode('b', textnode.text, None)
        case Text_Type.italic:
            return LeafNode('i', textnode.text, None)
        case Text_Type.code:
            return LeafNode('code', textnode.text, None)
        case Text_Type.link:
            return LeafNode('a', textnode.text, {'href': textnode.url})
        case Text_Type.image:
            return LeafNode('img', "", {'src': textnode.url, 'alt': textnode.text})
        case _:
            raise ValueError("Unknown text type")

def text_to_htmlnode(text):
    children = text_to_textnodes(text)
    return [text_node_to_html_node(child) for child in children]

def text_to_html_list_nodes(text, list_type):
    nodes = text.splitlines()
    html_nodes = []
    if list_type == 'ul':
        strip_length = 2
    if list_type == 'ol':
        strip_length = 3
    for node in nodes:
        html_nodes.append(ParentNode('li', text_to_htmlnode(node[strip_length:])))
    return html_nodes

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