from re import findall, compile, search, Pattern, Match
from enum import Enum
from htmlnode import LeafNode

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

def split_nodes_by_delimiter(to_split: list[TextNode], delimiter: str, delimited_type: TextType) -> list[TextNode]:
    result = []
    for node in to_split:
        # For now nested types (e.g. bold inside an italic block) are not treated
        if node.text_type != TextType.text:
            result.append(node)
            continue
        
        original_txt = node.text
        split_text = original_txt.split(delimiter)
        
        if len(split_text) != 3:
            raise AttributeError("Text to split must contain a pair of delimiters")
        
        result.append( TextNode(split_text[0], TextType.text) )
        result.append( TextNode(split_text[1], delimited_type) )
        result.append( TextNode(split_text[2], TextType.text) )
    
    return result

def split_nodes_improved(to_split: list[TextNode], delimiter: str) -> list[TextNode]:
    result = []
    
    delimited_type: TextType = TextType.bold
    
    match delimiter:
        case "*":
            delimited_type = TextType.italic
        case "**":
            delimited_type = TextType.bold
        case "`":
            delimited_type = TextType.in_code
        case _:
            raise AttributeError(f"Unsuported delimiter: {delimiter}")
        
    
    for node in to_split:
        # For now nested types (e.g. bold inside an italic block) are not treated
        if node.text_type != TextType.text:
            result.append(node)
            continue
        
        original_txt = node.text
        split_text = original_txt.split(delimiter)
        
        if len(split_text) != 3:
            raise AttributeError("Text to split must contain a pair of delimiters")
        
        result.append( TextNode(split_text[0], TextType.text) )
        result.append( TextNode(split_text[1], delimited_type) )
        result.append( TextNode(split_text[2], TextType.text) )
    
    return result

def extract_markdown_images(toExtract: str) -> list[tuple[str, str]]:
    img_pattern: str = r"\!\[([^\]]*?)\]\(([^\)]+?)\)"
    extracted = findall(img_pattern, toExtract)
    return extracted

def extract_markdown_links(toExtract: str) -> list[tuple[str, str]]:
    lnk_pattern: str = r"\s\[([^\]]*?)\]\(([^\)]+?)\)"
    extracted = findall(lnk_pattern, toExtract)
    return extracted

def split_nodes_image(toSplit: list[TextNode]) -> list[TextNode]:
    
    img_pattern: Pattern = compile(r"\!\[[^\]]*?\]\([^\)]+?\)")
    result: list[TextNode] = []
    
    for node in toSplit:
        
        matches: Match | None = search(img_pattern, node.text)
    
        if matches == None:
            result.append(node)
            continue
        
        # Grabs alt text and link
        linkTupleList: list[tuple[str, str]] = extract_markdown_images(node.text)
        cursorPosition: int = 0
        
        for i in range(len(linkTupleList)):
            linkLabel = linkTupleList[i][0]
            linkDestination = linkTupleList[i][1]
            delimiter: str = f"![{linkLabel}]({linkDestination})"
            
            # Appends text before link
            beforeText: str = node.text[cursorPosition:].split(delimiter, 1)[0]
            cursorPosition += len(beforeText) + len(delimiter)
            
            if len(beforeText) > 0:
                nonLinkText: TextNode = TextNode(beforeText, TextType.text)
                result.append(nonLinkText)
            
            linkText: TextNode = TextNode(linkLabel, TextType.link, linkDestination)
            result.append(linkText)
        
        if len(node.text[cursorPosition:]) > 0:
            remainingText: TextNode = TextNode(node.text[cursorPosition:], TextType.text)
            result.append(remainingText)
        
        return result
        
        
        
        
        
    