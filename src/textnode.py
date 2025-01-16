from re import findall, compile, search, Pattern, Match
from enum import Enum
from htmlnode import LeafNode

"""
This is a V0.1 beta of this library.
To do:
[x] Improve Split nodes by delimiter (multi delimiters, can begin with delimiter)
[X] Update Split nodes by delimiter in case of unordered list using asterisk ()
[ ] Rewrite using Functional programing (simpler and shorter file)
[x] Write docstrings
"""


class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    in_code = "inline code"
    link = "link"
    image = "image"

class BlockType(Enum):
    paragraph = "paragraph"
    code = "code"
    quote = "quote"
    ul = "unordered list"
    nol = "number ordered list"
    lol = "letter ordered list"
    rol = "roman ordered list"
    h1 = "heading 1"
    h2 = "heading 2"
    h3 = "heading 3"
    h4 = "heading 4"
    h5 = "heading 5"
    h6 = "heading 6"

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

#=======#
# Utils #
#=======#
def flipFlopTextType(iterator: int, parity: bool, alternator: TextType) -> TextType:
    """Alternates between TextType.text and alternator. When parity is True, when iterator is 0 it returns TextType.text.

    Args:
        iterator (int): linear counter
        parity (bool): inverts results (first is "text" if True, first is alternator if False)
        alternator (TextType): the value to alternate

    Returns:
        TextType: TextType.text | alternator
    """
    differentiator = 0
    if not parity:
        differentiator = 1
    
    if iterator % 2 == differentiator:
        return TextType.text
    else:
        return alternator

def getHeaderLevel(header: str, currentlevel: int) -> int:
    """Dumbest way possible: recursion, but I wanted to train it here. Takes a string and returns the markdown level of the header (counts # in the beginning the line) as a int, or -1 if not a valid header (more than 6 #).

    Args:
        header (str): potential header string
        currentlevel (int): current suspected level

    Returns:
        int: returns a number from 1 to 6 if a valid markdown header. 0 or -1 if not a valid header
    """
    # Base case
    if header.startswith(" "):
        return currentlevel
    
    # Weird edge case
    if ( header.startswith("#") ) and ( currentlevel == 6 ):
        return -1
    
    return getHeaderLevel(header[1:], currentlevel + 1 )

def headerMapper(level: int) -> BlockType:
    
    # Guard clause
    if (level < 1) or (level > 6):
        return BlockType.paragraph
    
    match level:
        case 1:
            return BlockType.h1
        case 2:
            return BlockType.h2
        case 3:
            return BlockType.h3
        case 4:
            return BlockType.h4
        case 5:
            return BlockType.h5
        case 6:
            return BlockType.h6

#==================#
# Inline Functions #
#==================#
'''
# Keeping the old function bc the new one does not fully comply with the boot.dev exercises
def split_nodes_by_delimiter(toSplit: list[TextNode], delimiter: str, delimited_type: TextType) -> list[TextNode]:
    """Takes a list of TextNodes, a delimiter (e.g.: `**`) and the delimited_type (e.g.: TextType.bold). Does not work with markdown links and images.

    Args:
        toSplit (list[TextNode]): the list of TextNodes to be processed
        delimiter (str): the markdown delimiter, can be: `**` for bold; `*` for italic; ` for inline code
        delimited_type (TextType): the corresponding TextType Enum for the delimiter

    Raises:
        AttributeError: In case of a lack of delimiters

    Returns:
        list[TextNode]: List of processed TextNode, with text before the first delimiter and after the second is set as TextType.text, and text inside the delimiter is set as the demilited_type.
    """
    result = []
    for node in toSplit:
        # For now nested types (e.g. bold inside an italic block) are not treated
        if node.text_type != TextType.text:
            result.append(node)
            continue
        
        original_txt = node.text
        split_text: list[str] = original_txt.split(delimiter)
        
        if len(split_text) != 3:
            raise AttributeError("Text to split must contain a pair of delimiters")
        
        result.append( TextNode(split_text[0], TextType.text) )
        result.append( TextNode(split_text[1], delimited_type) )
        result.append( TextNode(split_text[2], TextType.text) )
    
    return result
'''

def split_nodes_by_delimiter(toSplit: list[TextNode], delimiter: str) -> list[TextNode]:
    """Takes a list of TextNodes, and a Markdown delimiter (e.g.: `**`). Works with multiple delimited pairs. Does not work with markdown links and images.

    Args:
        toSplit (list[TextNode]): the list of TextNodes to be processed
        delimiter (str): the markdown delimiter, can be either: `**` for bold; `*` for italic; or ` for inline code

    Raises:
        AttributeError: In case of an unsupported delimiter

    Returns:
        list[TextNode]: List of processed TextNode, with text before the text outside the delimiter set as TextType.text, and text inside the delimiter is set as an inferred delimited type according to the delimiter provided ( `**` for bold, `*` for italic or ` for inline code).
    """
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
    
    for node in toSplit:
        # For now nested types (e.g. bold inside an italic block) are not treated
        if node.text_type != TextType.text:
            result.append(node)
            continue
        
        original_txt = node.text
        split_text = original_txt.split(delimiter)
        iterations = len(split_text)
              
        # In case of odd number of delimiters or no delimiters found.
        # Catches case of unordered list using asterisk being confounded with malformed italicised text.
        # Also taking into consideration the human factor, a person might actually want to write for some gosh darn reason ** in the middle of a sentence.
        if iterations < 3:
            result.append(node)
            continue
        
        parity=True
        if len(split_text[0]) == 0: # Means the nodeText begins with a delimiter
            parity=False # For the flipflop, makes sure the first element in the list is the alternator, meaning the delimited_type
            del split_text[0] # Erases the empty string to avoid TextNodes that are empty
            iterations -= 1 # Corrects the split text length
        
        if len(split_text[-1]) == 0: # This is in the case there is a delimited elemented in the end of the text
            del split_text[-1]
            iterations -= 1
        
        for i in range(iterations):
            newNodeText: str = split_text[i]
            newNodeType: TextType = flipFlopTextType(i, parity, delimited_type)
            
            result.append( TextNode(newNodeText, newNodeType) )
    
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
        nodeText: str = node.text
        #Case node has no pattern        
        matches: Match | None = search(img_pattern, nodeText)

        if matches == None:
            result.append(node)
            continue
        
        # Grabs alt text and link from the pattern
        linkTupleList: list[tuple[str, str]] = extract_markdown_images(nodeText)
        cursorPosition: int = 0
        
        for i in range(len(linkTupleList)):
            linkLabel = linkTupleList[i][0]
            linkDestination = linkTupleList[i][1]
            delimiter: str = f"![{linkLabel}]({linkDestination})" # change for image or link
            
            # Appends text before link
            beforeText: str = nodeText[cursorPosition:].split(delimiter, 1)[0]
            cursorPosition += len(beforeText) + len(delimiter)
            
            if len(beforeText) > 0:
                nonLinkText: TextNode = TextNode(beforeText, TextType.text)
                result.append(nonLinkText)
            
            linkText: TextNode = TextNode(linkLabel, TextType.image, linkDestination)
            result.append(linkText)
        
        if len(nodeText[cursorPosition:]) > 0:
            remainingText: TextNode = TextNode(nodeText[cursorPosition:], TextType.text)
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
        nodeText: str = node.text
        #Case node has no pattern, should've been a guard clause
        matches: Match | None = search(link_pattern, nodeText)

        if matches == None:
            result.append(node)
            continue
        
        # Grabs alt-text and link from the pattern
        linkTupleList: list[tuple[str, str]] = extract_markdown_links(nodeText) #Change for image or link
        cursorPosition: int = 0
        
        # This walks through the (alt-text, link) tuple in order to split current node's text into into smaller nodes
        for i in range(len(linkTupleList)):
            linkLabel = linkTupleList[i][0]
            linkDestination = linkTupleList[i][1]
            delimiter: str = f"[{linkLabel}]({linkDestination})"
            
            # Shrinks remaining text of current node to be processed, and grabs part in front of delimiter
            beforeText: str = nodeText[cursorPosition:].split(delimiter, 1)[0]
            cursorPosition += len(beforeText) + len(delimiter) # We're walking in here
            
            # Appends the text that appears before the link node, if it exists
            if len(beforeText) > 0:
                nonLinkText: TextNode = TextNode(beforeText, TextType.text)
                result.append(nonLinkText)
            
            # Appends link to list
            linkText: TextNode = TextNode(linkLabel, TextType.link, linkDestination)
            result.append(linkText)
        
        # After last link append remaining text if it exists
        if len(nodeText[cursorPosition:]) > 0:
            remainingText: TextNode = TextNode(nodeText[cursorPosition:], TextType.text)
            result.append(remainingText)

    return result

def text_to_textnodes(toConvert: str) -> list[TextNode]:
    """Converts the input markdown string into a list of TextNodes of the appropriate type

    Args:
        toConvert (str): markdown text that will be converted to a list of TextNodes

    Returns:
        list[TextNode]: list of TextNodes that can be of TextType text, bold, italic, inline code, links and images, according to the input provided, in the order provided
    """
    
    stage0_unprocessed: list[TextNode] = [ TextNode(toConvert, TextType.text) ]
    
    stage1_splitImage: list[TextNode] = split_nodes_image(stage0_unprocessed)
    
    stage2_splitLink: list[TextNode] = split_nodes_link(stage1_splitImage)
    
    stage3_splitBold: list[TextNode] = split_nodes_by_delimiter(stage2_splitLink, "**")
    
    stage4_splitItalic: list[TextNode] = split_nodes_by_delimiter(stage3_splitBold, "*")

    stage5_splitInline: list[TextNode] = split_nodes_by_delimiter(stage4_splitItalic, "`")

    return stage5_splitInline

#=================#
# Block Functions #
#=================#

# To break into smaller functions
def markdown_to_blocks(markdownTxt: str) -> list[str]:
    result: list[str] = []

    splitMarkdown: list[str] = markdownTxt.splitlines()
    trimmedMarkdown: list[str] = list(map(lambda t: t.strip(),splitMarkdown))
    
    """ # Fast but wrong way of doing it
    filteredMarkdown: list[str] = list(filter(lambda t: len(t) > 0, trimmedMarkdown))
    """
    
    acc = ""
    
    for line in trimmedMarkdown:
        if len(line) == 0:
            if len(acc) > 0:
                result.append(acc)
                acc.clear()
            continue
        
        if line.startswith(( "* ", "- ", "+ ", "1. ", "a. ", "i. ", "```", "> ")):
            acc += f"{line}\n"
            continue
        
        result.append(line)
    
    if len(acc) > 0:
        result.append(acc)

    
    return result

def block_to_blocktype(block: str) -> BlockType:
    #Guard clause, non obvious types:
    if not block.startswith(( "* ", "- ", "+ ", "1. ", "a. ", "i. ", "```", "> ", "# ", "##")):
        return BlockType.paragraph
    
    identifier: str = block[:2]
    
    match identifier:
        case r"# ":
            return BlockType.h1
        case r"##":
            headerLevel: int = getHeaderLevel(block[2:], 2)
            return headerMapper(headerLevel)        
        case "``":
            return BlockType.code
        case "> ":
            return BlockType.quote
        case "* ":
            return BlockType.ul
        case "- ":
            return BlockType.ul
        case "+ ":
            return BlockType.ul
    
    # To update in case of numbered list (uses 3 starting characters)
    identifier: str = block[:3]
    match identifier:
        case "1. ":
            return BlockType.nol
        case "a. ":
            return BlockType.lol
        case "i. ":
            return BlockType.rol
    
    # In case a block begins with 1.* or a.* or i.*
    return BlockType.paragraph

#