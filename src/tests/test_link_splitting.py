import unittest

from textnode import TextNode, TextType, split_nodes_link

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Link splitting test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Link splitting test done")

    def test_image_splitting_None(self):
        linkMarkdown: TextNode = TextNode("Suspendisse laoreet urna dui, non aliquet massa congue a.", TextType.text)
        nodeList: list[TextNode] = [linkMarkdown]
        toTest: list[TextNode] = split_nodes_link(nodeList)
        
        self.assertEqual(
            1,
            len(toTest)
        )
        
        self.assertEqual(
            linkMarkdown,
            toTest[0]
        )

    def test_link_splitting_head(self):
        linkMarkdown: TextNode = TextNode("[dolor](sitamet) neque porro", TextType.text)
        nodeList: list[TextNode] = [linkMarkdown]
        toTest: list[TextNode] = split_nodes_link(nodeList)
        self.assertEqual(
            2,
            len(toTest)
        )
        self.assertEqual(
            TextNode("dolor", TextType.link, "sitamet"),
            toTest[0]
        )
        self.assertEqual(
            TextNode(" neque porro", TextType.text),
            toTest[1]
        )

    def test_link_splitting_tail(self):
        linkMarkdown: TextNode = TextNode("Lorem ipsum [dolor](sitamet)", TextType.text)
        nodeList: list[TextNode] = [linkMarkdown]
        toTest: list[TextNode] = split_nodes_link(nodeList)
        self.assertEqual(
            2,
            len(toTest)
        )
        self.assertEqual(
            TextNode("dolor", TextType.link, "sitamet"),
            toTest[1]
        )
        self.assertEqual(
            TextNode("Lorem ipsum ", TextType.text),
            toTest[0]
        )

    def test_link_splitting_egg(self):
        linkMarkdown: TextNode = TextNode("Lorem ipsum [dolor](sitamet) neque porro", TextType.text)
        nodeList: list[TextNode] = [linkMarkdown]
        toTest: list[TextNode] = split_nodes_link(nodeList)
        self.assertEqual(
            3,
            len(toTest)
        )
        self.assertEqual(
            TextNode("dolor", TextType.link, "sitamet"),
            toTest[1]
        )
        self.assertEqual(
            TextNode(" neque porro", TextType.text),
            toTest[2]
        )

    def test_link_splitting_multiple(self):
        linkMarkdown: TextNode = TextNode("Lorem ipsum [dolor](sitamet) neque porro [quisquam](dolorem)", TextType.text)
        nodeList: list[TextNode] = [linkMarkdown]
        toTest: list[TextNode] = split_nodes_link(nodeList)
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

    def test_link_splitting_mixed(self):
        linkMarkdown: TextNode = TextNode("Lorem ipsum [dolor](sitamet) neque porro ![quisquam](dolorem)", TextType.text)
        nodeList: list[TextNode] = [linkMarkdown]
        toTest: list[TextNode] = split_nodes_link(nodeList)
        self.assertEqual(
            3,
            len(toTest)
        )
        self.assertEqual(
            TextNode("dolor", TextType.link, "sitamet"),
            toTest[1]
        )
        self.assertEqual(
            TextNode(" neque porro ![quisquam](dolorem)", TextType.text),
            toTest[2]
        )

if __name__ == '__main__':
    unittest.main()