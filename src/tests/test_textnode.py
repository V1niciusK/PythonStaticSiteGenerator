import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Beggining Text Node Tests")
    
    @classmethod
    def tearDownClass(cls):
        print("Ending Text Node tests")
        print("")
    
    def test_eq_values(self):
        #Base test
        node_e1 = TextNode("This is a text node", TextType.bold)
        node_e2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node_e1, node_e2)
    
    def test_default_url(self):
        # Default URL Test        
        node_e1 = TextNode("This is a text node", TextType.bold)
        node_e3 = TextNode("This is a text node", TextType.bold, url=None)
        self.assertEqual(node_e1, node_e3)
        
    def test_eq_type(self):
        # Text Type test
        node_n1 = TextNode("This is a text node", TextType.in_code)
        node_e4 = TextNode("This is a text node", TextType.in_code)
        self.assertEqual(node_e4, node_n1)
        
    def test_dif_type(self):
        # Different Text Type test
        node_e1 = TextNode("This is a text node", TextType.bold)
        node_n1 = TextNode("This is a text node", TextType.in_code)
        self.assertNotEqual(node_e1, node_n1)
    
    def test_dif_text(self):
        # Different text test
        node_e1 = TextNode("This is a text node", TextType.bold)
        node_n2 = TextNode("This is another text node", TextType.bold)
        self.assertNotEqual(node_e1, node_n2)
        
    def test_dif_all(self):
        # Everything different test
        node_n2 = TextNode("This is another text node", TextType.bold)
        node_n3 = TextNode("This is yet another text node", TextType.image, url="https://avatars.githubusercontent.com/u/47822836?v=4")
        self.assertNotEqual(node_n2, node_n3)

if __name__ == "__main__":
    unittest.main()