import unittest

from textnode import TextNode, TextType, split_nodes_by_delimiter, split_nodes_image

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Node splitting test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Node splitting test done")
    
    def test_bold_splitting(self):
        boldTextSample: TextNode = TextNode("Lorem **ipsum** dolor", TextType.text)
        nodeList: list[TextNode] = [boldTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "**", TextType.bold)
        
        self.assertEqual(
            3,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Lorem ", TextType.text),
            toTest[0]
        )
        
        self.assertEqual(
            TextNode("ipsum", TextType.bold),
            toTest[1]
        )
    
    def test_italic_splitting(self):
        italicTextSample: TextNode = TextNode("Lorem *ipsum* dolor", TextType.text)
        nodeList: list[TextNode] = [italicTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "*", TextType.italic)
        
        self.assertEqual(
            3,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Lorem ", TextType.text),
            toTest[0]
        )
        
        self.assertEqual(
            TextNode("ipsum", TextType.italic),
            toTest[1]
        )
    
    def test_code_splitting(self):
        codeTextSample: TextNode = TextNode("Lorem `ipsum` dolor", TextType.text)
        nodeList: list[TextNode] = [codeTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "`", TextType.bold)
        
        self.assertEqual(
            3,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Lorem ", TextType.text),
            toTest[0]
        )
        
        self.assertEqual(
            TextNode("ipsum", TextType.bold),
            toTest[1]
        )
    
    def test_malformed_splitting(self):
        malformedType: TextNode = TextNode("Lorem **ipsum dolor sit amet", TextType.text)
        nodeList: list[TextNode] = [malformedType]
        
        with self.assertRaises(AttributeError):
            split_nodes_by_delimiter(nodeList, "**", TextType.bold)
        
    def test_ignored_splitting(self):
        
        ignoredType: TextNode = TextNode("[Lorem ipsum](https://dolor-sit-am.et)", TextType.link)
        nodeList: list[TextNode] = [ignoredType]
        toTest = split_nodes_by_delimiter(nodeList, "`", TextType.bold)
        
        self.assertEqual(
            1,
            len(toTest)
        )
        
        self.assertEqual(
            nodeList,
            toTest
        )

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
    