import unittest

from textnode import TextNode, TextType, split_nodes_by_delimiter

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Node splitting test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Node splitting test done")

    def test_bold_splitting_head(self):
        boldTextSample: TextNode = TextNode("**Lorem** ipsum dolor", TextType.text)
        nodeList: list[TextNode] = [boldTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "**")
        
        self.assertEqual(
            2,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Lorem", TextType.bold),
            toTest[0]
        )
        
        self.assertEqual(
            TextNode(" ipsum dolor", TextType.text),
            toTest[1]
        )

    def test_bold_splitting_egg(self):
        boldTextSample: TextNode = TextNode("Lorem **ipsum** dolor", TextType.text)
        nodeList: list[TextNode] = [boldTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "**")
        
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

    def test_bold_splitting_tail(self):
        boldTextSample: TextNode = TextNode("Lorem ipsum **dolor**", TextType.text)
        nodeList: list[TextNode] = [boldTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "**")
        
        self.assertEqual(
            2,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Lorem ipsum ", TextType.text),
            toTest[0]
        )
        
        self.assertEqual(
            TextNode("dolor", TextType.bold),
            toTest[1]
        )

    def test_italic_splitting(self):
        italicTextSample: TextNode = TextNode("Lorem *ipsum* dolor", TextType.text)
        nodeList: list[TextNode] = [italicTextSample]
        toTest = split_nodes_by_delimiter(nodeList, "*")
        
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
        toTest = split_nodes_by_delimiter(nodeList, "`")
        
        self.assertEqual(
            3,
            len(toTest)
        )
        self.assertEqual(
            TextNode("Lorem ", TextType.text),
            toTest[0]
        )
        
        self.assertEqual(
            TextNode("ipsum", TextType.in_code),
            toTest[1]
        )
    
    def test_malformed_splitting(self):
        malformedType: TextNode = TextNode("Lorem **ipsum dolor sit amet", TextType.text)
        nodeList: list[TextNode] = [malformedType]
        toTest: list[TextNode] = split_nodes_by_delimiter(nodeList, "**")
        
        self.assertEqual(
            nodeList,
            toTest
        )
        
        
    def test_ignored_type(self):
        
        ignoredType: TextNode = TextNode("[Lorem ipsum](https://dolor-sit-am.et)", TextType.link)
        nodeList: list[TextNode] = [ignoredType]
        toTest = split_nodes_by_delimiter(nodeList, "*")
        
        self.assertEqual(
            1,
            len(toTest)
        )
        
        self.assertEqual(
            nodeList,
            toTest
        )

    def test_ignored_text(self):
        
        noDelimiter: TextNode = TextNode("Lorem ipsum dolo", TextType.text)
        nodeList: list[TextNode] = [noDelimiter]
        toTest = split_nodes_by_delimiter(nodeList, "`")
        
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
    