from enum import Enum
from htmlnode import ParentNode, LeafNode

class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    in_code = "inline code"
    link = "link"
    image = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def to_html_node(self):
        match self.text_type:
            case TextType.text:
                return LeafNode(None, self.text)
            case TextType.bold:
                return LeafNode("b", self.text)
            case TextType.italic:
                return LeafNode("i", self.text)
            case TextType.in_code:
                return LeafNode("code", self.text)
            case TextType.link:
                return LeafNode("a", self.text, { "href": f"{self.url}" })
            case TextType.image:
                return LeafNode("img", value="", props={ "src": f"{self.url}", "alt": f"{self.text}"})
            case _:
                raise TypeError("Text type error: please check the text type")
    
    def __eq__(self, value) -> bool:
        return (
           self.text == value.text and
           self.text_type == value.text_type and
           self.url == value.url
        )
    
    def __repr__(self) -> None:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
""" 
def __split_nodes_by_delimiter(to_split: list, delimiter: str, delimited_type: TextType):
    to_split.copy() """