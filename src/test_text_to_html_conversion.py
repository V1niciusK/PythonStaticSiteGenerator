import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType

class TestConversion(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Starting conversion test")
    
    @classmethod
    def tearDownClass(cls):
        print("Finished conversion tests")
    
    def test_text_conversion(self):
        textLeaf = LeafNode(None, "Lorem ipsum")
        
        testNode = TextNode("Lorem ipsum", TextType.text)
        
        self.assertEqual(
            textLeaf,
            testNode.to_html_node()
        )
    
    def test_bold_conversion(self):
        textLeaf = LeafNode("b", "Lorem ipsum")
        
        testNode = TextNode("Lorem ipsum", TextType.bold)
        
        self.assertEqual(
            textLeaf,
            testNode.to_html_node()
        )
    
    def test_italic_conversion(self):
        textLeaf = LeafNode("i", "Lorem ipsum")
        
        testNode = TextNode("Lorem ipsum", TextType.italic)
        
        self.assertEqual(
            textLeaf,
            testNode.to_html_node()
        )
    
    def test_text_inline_code_conversion(self):
        textLeaf = LeafNode("code", "Lorem ipsum")
        
        testNode = TextNode("Lorem ipsum", TextType.in_code)
        
        self.assertEqual(
            textLeaf,
            testNode.to_html_node()
        )
    
    def test_anchor_conversion(self):
        textLeaf = LeafNode("a", "Lorem ipsum", { "href": "https://www.google.com" })
        
        testNode = TextNode("Lorem ipsum", TextType.link, "https://www.google.com")
        
        self.assertEqual(
            textLeaf,
            testNode.to_html_node()
        )
    
    def test_image_conversion(self):
        textLeaf = LeafNode("img", "", { "src": "https://www.google.com", "alt": "Lorem ipsum" })
        
        testNode = TextNode("Lorem ipsum", TextType.image, "https://www.google.com")
        
        self.assertEqual(
            textLeaf,
            testNode.to_html_node()
        )

if __name__ == "__main__":
    unittest.main()
    
    
        
        
        