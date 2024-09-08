class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attributes = ""
        if not self.props:
            return attributes
        for key, value in self.props.items():
            attributes += f" {key.strip("\"")}=\"{value}\""
        return attributes
    
    def __repr__(self):
        print(f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})")