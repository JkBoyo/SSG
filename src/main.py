from constants import Text_Type
from htmlnode import HtmlNode, LeafNode, ParentNode
from textnode import TextNode


def main():
    TN = TextNode("I am a string", "string", "http://string.com")
    
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
          

main()
