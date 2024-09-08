class TextNode():
    def __init__(self, text = None, text_type = None, url= None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, comp_TN) -> bool:
        if (self.text_type == comp_TN.text_type) and (self.text == comp_TN.text) and (self.url == comp_TN.url):
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"