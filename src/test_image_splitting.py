import unittest

from textnode import TextNode, TextType, split_nodes_image

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Image splitting test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Image splitting test done")

    def test_image_splitting_even(self):
        imageMarkdownEven: TextNode = TextNode("Lorem ipsum ![dolor](sitamet) neque porro ![quisquam](dolorem)", TextType.text)
        nodeList: list[TextNode] = [imageMarkdownEven]
        toTest: list[TextNode] = split_nodes_image(nodeList)
        self.assertEqual(
            4,
            len(toTest)
        )
        self.assertEqual(
            TextNode("dolor", TextType.link, "sitamet"),
            toTest[1]
        )
        self.assertEqual(
            TextNode(" neque porro ", TextType.text),
            toTest[2]
        )
        
    def test_image_splitting_Odd(self):
        imageMarkdownOdd: TextNode = TextNode("Consectetur, adipisci velit ![Proin volutpat](tempus) accumsan, ![nibh](augue) luctus lacus", TextType.text)
        nodeList: list[TextNode] = [imageMarkdownOdd]
        toTest: list[TextNode] = split_nodes_image(nodeList)
        self.assertEqual(
            5,
            len(toTest)
        )
        self.assertEqual(
            TextNode(" luctus lacus", TextType.text),
            toTest[4]
        )
        
    def test_image_splitting_Heads(self):
        imageMarkdownHeads: TextNode = TextNode("![Vestibulum](fringilla) maximus sollicitudin", TextType.text)
        nodeList: list[TextNode] = [imageMarkdownHeads]
        toTest: list[TextNode] = split_nodes_image(nodeList)
        self.assertEqual(
            2,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Vestibulum", TextType.link, "fringilla"),
            toTest[0]
        )
        
    def test_image_splitting_None(self):
        imageMarkdownNone: TextNode = TextNode("Suspendisse laoreet urna dui, non aliquet massa congue a.", TextType.text)
        nodeList: list[TextNode] = [imageMarkdownNone]
        toTest: list[TextNode] = split_nodes_image(nodeList)
        
        self.assertEqual(
            1,
            len(toTest)
        )
        
        self.assertEqual(
            imageMarkdownNone,
            toTest[0]
        )

if __name__ == '__main__':
    unittest.main()
    