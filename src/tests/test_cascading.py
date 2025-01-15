import unittest

from textnode import TextNode, TextType, text_to_textnodes

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Node splitting test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Node splitting test done")

    def test_splitting(self):
        textSample: str = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://imgur.com/a/r9vTtoC) and a [link](https://boot.dev)"
        toTest: list[TextNode]= text_to_textnodes(textSample)
        benchmark: list[TextNode] = [
                TextNode("This is ", TextType.text),
                TextNode("text", TextType.bold),
                TextNode(" with an ", TextType.text),
                TextNode("italic", TextType.italic),
                TextNode(" word and a ", TextType.text),
                TextNode("code block", TextType.in_code),
                TextNode(" and an ", TextType.text),
                TextNode("obi wan image", TextType.image, "https://imgur.com/a/r9vTtoC"),
                TextNode(" and a ", TextType.text),
                TextNode("link", TextType.link, "https://boot.dev"),
            ]
        
        self.assertEqual(
            toTest,
            benchmark
        )

if __name__ == '__main__':
    unittest.main()
    