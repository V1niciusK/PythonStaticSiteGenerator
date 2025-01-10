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
    """This is an intermediary class for translating Markdown into HTML.
    
    Params:
        text: (optional) (str) the text to be put inside an html tag
        text_type: (mandatory) (Enum TextType) the type of information,
        url: (optional) (str) the url to be used in a tag props'
    
    Methods:
        to_html_node() -> LeafNode: converts the TextNode object into a LeafNode class
            takes no params
    """
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
    """Takes a list of TextNodes, a delimiter (e.g.: `**`) and the delimited_type (e.g.: TextType.bold). Does not work with markdown links and images.

    Args:
        to_split (list[TextNode]): the list of TextNodes to be processed
        delimiter (str): the markdown delimiter, can be: `**` for bold; `*` for italic; ` for inline code
        delimited_type (TextType): the corresponding TextType Enum for the delimiter

    Raises:
        AttributeError: In case of a lack of delimiters

    Returns:
        list[TextNode]: List of processed TextNode, with text before the first delimiter and after the second is set as TextType.text, and text inside the delimiter is set as the demilited_type.
    """
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

# WIP: 
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
    """Parses string and returns alt-text and URIs for images defined in markdown format `![alt-text](uri)`. Must contain at least one markdown image

    Args:
        toExtract (str): string to be parsed. Must contain at least one markdown image

    Returns:
        list[tuple[str, str]]: List of tuples found on string, each item of list contains (alt-text, uri) in this order."""
    #            pattern: ! [    gp1   ] (    gp2   )
    img_pattern: str = r"\!\[([^\]]*?)\]\(([^\)]+?)\)"
    extracted = findall(img_pattern, toExtract)
    return extracted

def extract_markdown_links(toExtract: str) -> list[tuple[str, str]]:
    """Parses string and returns anchors and links defined in markdown format `[anchor](link)`. Must contain at least one markdown link

    Args:
        toExtract (str): string to be parsed. Must contain at least one markdown link

    Returns:
        list[tuple[str, str]]: List of tuples found on string, each item of list contains (anchor, link) in this order.
    """
    lnk_pattern: str = r"(?:^| )[^\!]?\[([^\]]*?)\]\(([^\)]+?)\)"
    # For an explanation of this ^ mad pattern, check split nodes link
    
    extracted = findall(lnk_pattern, toExtract)
    return extracted

def split_nodes_image(toSplit: list[TextNode]) -> list[TextNode]:
    """Returns a list of processed TextNodes, breaking any TextNode containing Markdown's tipical image structure `![alt-text](uri)` into text and image type TextNodes. If a given node does not contain an image structure, it just ignores processing.

    Args:
        toSplit (list[TextNode]): List of nodes to be processed, if a node does not have any image, it is returned unprocessed

    Returns:
        list[TextNode]: List of processed TextNodes of type TextType.text and TextType.image if there were any in the list.
    """
    #                        pattern: ! [   *    ] (   *    )
    img_pattern: Pattern = compile(r"\!\[[^\]]*?\]\([^\)]+?\)") # change for image or link
    result: list[TextNode] = []
    
    for node in toSplit:

        #Case node has no pattern        
        matches: Match | None = search(img_pattern, node.text)

        if matches == None:
            result.append(node)
            continue
        
        # Grabs alt text and link from the pattern
        linkTupleList: list[tuple[str, str]] = extract_markdown_images(node.text)
        cursorPosition: int = 0
        
        for i in range(len(linkTupleList)):
            linkLabel = linkTupleList[i][0]
            linkDestination = linkTupleList[i][1]
            delimiter: str = f"![{linkLabel}]({linkDestination})" # change for image or link
            
            # Appends text before link
            beforeText: str = node.text[cursorPosition:].split(delimiter, 1)[0]
            cursorPosition += len(beforeText) + len(delimiter)
            
            if len(beforeText) > 0:
                nonLinkText: TextNode = TextNode(beforeText, TextType.text)
                result.append(nonLinkText)
            
            linkText: TextNode = TextNode(linkLabel, TextType.image, linkDestination)
            result.append(linkText)
        
        if len(node.text[cursorPosition:]) > 0:
            remainingText: TextNode = TextNode(node.text[cursorPosition:], TextType.text)
            result.append(remainingText)

    return result

def split_nodes_link(toSplit: list[TextNode]) -> list[TextNode]:
    """Returns a list of processed TextNodes, breaking any TextNode containing Markdown's tipical link structure `[anchor](url)` into text and link type TextNodes. If a given node does not contain a link structure, it just ignores processing.

    Args:
        toSplit (list[TextNode]): List of nodes to be processed, if a node does not have any link, it is returned unprocessed

    Returns:
        list[TextNode]: List of processed TextNodes of type TextType.text and TextType.link if there were any in the list.
    """
    #                        pattern:               [   *    ] (   *    )
    link_pattern: Pattern = compile(r"(?:^| )[^\!]?\[[^\]]*?\]\([^\)]+?\)") # change for image or link
    '''
    Let me describe the madness that is the regex above, because I know I will forget about it:
    First there is a non-capturing group (?: ) that can contain either the beginning of a line ^ or a space. (?:^| )
        The capturing group is to assure that the edge case of a beginning link is also capture, while maintaining the match cases where a space might precede the link.
        The reason I didn't pick \s is because for some reason it was matching newline characters
        The reason why space is there is to avoid matching
    Then there is a requirement of no exclamation marks before the real pattern. That is the [^\!]? in the pattern
    Then there is the real link pattern, which is somewhat simple:
        First is open brackets \[
        Then there is a group of zero or more characters that are not the close brackets \]
        Then there is a close bracket \]
        Next is a open parenthesis \(
        Followed by one or more characters (bc there must be an url) different from close parenthesis \)
        Finally a close parenthesis \)
    '''
    result: list[TextNode] = []
    
    for node in toSplit:

        #Case node has no pattern, should've been a guard clause
        matches: Match | None = search(link_pattern, node.text)

        if matches == None:
            result.append(node)
            continue
        
        # Grabs alt-text and link from the pattern
        linkTupleList: list[tuple[str, str]] = extract_markdown_links(node.text) #Change for image or link
        cursorPosition: int = 0
        
        # This walks through the (alt-text, link) tuple in order to split current node's text into into smaller nodes
        for i in range(len(linkTupleList)):
            linkLabel = linkTupleList[i][0]
            linkDestination = linkTupleList[i][1]
            delimiter: str = f"[{linkLabel}]({linkDestination})"
            
            # Shrinks remaining text of current node to be processed, and grabs part in front of delimiter
            beforeText: str = node.text[cursorPosition:].split(delimiter, 1)[0]
            cursorPosition += len(beforeText) + len(delimiter) # We're walking in here
            
            # Appends text before creating link node, if it exists
            if len(beforeText) > 0:
                nonLinkText: TextNode = TextNode(beforeText, TextType.text)
                result.append(nonLinkText)
            
            # Appends link after the text
            linkText: TextNode = TextNode(linkLabel, TextType.link, linkDestination)
            result.append(linkText)
        
        # After last link append remaining text if it exists
        if len(node.text[cursorPosition:]) > 0:
            remainingText: TextNode = TextNode(node.text[cursorPosition:], TextType.text)
            result.append(remainingText)

    return result