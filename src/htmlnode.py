class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        attributes = ""
        if not self.props:
            return attributes
        for key, value in self.props.items():
            attributes += f" {key.strip("\"")}=\"{value}\""
        return attributes
    
    def __repr__(self):
       return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("All Leaf Nodes must have a value")
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return NotImplemented
        return self.tag == other.tag and self.value == other.value and self.props == other.props
        
    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HtmlNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return NotImplemented
        return self.tag == other.tag and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNode's must have a tag")
        
        if self.children is None:
            raise ValueError("All ParentNode's must have children")

        children_html = ""
        
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
