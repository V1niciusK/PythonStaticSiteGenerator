import unittest

from textnode import TextNode, TextType, split_nodes_by_delimiter

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


        
if __name__ == '__main__':
    unittest.main()
    