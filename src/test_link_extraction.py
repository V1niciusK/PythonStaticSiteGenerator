import unittest

from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Image and link conversion functions test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Image and link conversion functions test done")
    
    def test_img_extraction(self) -> None:
        imageSample: str = f"Lorem ipsum ![dolor](https://test.co.uk/favicon.png)"
        toTest: list[tuple[str,str]] = extract_markdown_images(imageSample)
        
        self.assertEqual(
            [("dolor", "https://test.co.uk/favicon.png")],
            toTest
        )
    
    def test_link_extraction(self) -> None:
        linkSample: str = f"Lorem ipsum [dolor](https://test.co.uk) sit amet"
        toTest: list[tuple[str,str]] = extract_markdown_links(linkSample)
        
        self.assertEqual(
            [("dolor","https://test.co.uk")],
            toTest
        )
    