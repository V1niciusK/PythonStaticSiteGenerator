import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    
    def setUp(self):
        self.sample_p: dict[str,str] = {
            "tag": "a",
            "value": "Lorem ipsum",
            "children": [],
            "props": { "href": "https://www.google.com" }
        }
        self.sample_div: dict[str,str] = {
            "tag": "div",
            "value": "",
            "children": [],
            "props": None
        }
    
    @classmethod
    def setUpClass(cls):
        print("Beggining HTML Node tests")
    
    @classmethod
    def tearDownClass(cls):
        print("Ending HTML Node tests")
        print("")
    
    def test_class_creation(self):
        
        testNode = HTMLNode(
            self.sample_p["tag"],
            self.sample_p["value"],
            self.sample_p["children"],
            self.sample_p["props"]
            )
        
        self.assertEqual(
            testNode.tag,
            self.sample_p["tag"],
            "Tag initialization error"
        )
        self.assertEqual(
            testNode.value,
            self.sample_p["value"],
            "Value initialization error"
        )
        self.assertEqual(
            testNode.children,
            self.sample_p["children"],
            "Children initialization error"
        )
        self.assertEqual(
            testNode.props,
            self.sample_p["props"],
            "Prop initialization error"
        )
    
    def test_class_creation_with_child(self):
        testChildNode = HTMLNode(
            self.sample_p["tag"],
            self.sample_p["value"],
            self.sample_p["children"],
            self.sample_p["props"]
            )
        testNode = HTMLNode(
            self.sample_div["tag"],
            self.sample_div["value"],
            [testChildNode],
            self.sample_div["props"]
            )
        
        self.assertEqual(
            testNode.tag,
            self.sample_div["tag"],
            "Tag initialization error"
        )
        self.assertEqual(
            testNode.value,
            self.sample_div["value"],
            "Value initialization error"
        )
        self.assertEqual(
            testNode.children[0],
            testChildNode,
            "Children initialization error"
        )
        self.assertEqual(
            testNode.props,
            self.sample_div["props"],
            "Prop initialization error"
        )
        
    def test_tag_default(self):
        nodeWoTag = HTMLNode(
            value=self.sample_p["value"],
            children=self.sample_p["children"],
            props=self.sample_p["props"]
        )
        self.assertEqual(
            self.sample_p["value"],
            nodeWoTag.value
        )
        self.assertEqual(
            None,
            nodeWoTag.tag
        )
    
    def test_value_default(self):
        nodeWoTag = HTMLNode(
            tag=self.sample_p["tag"],
            children=self.sample_p["children"],
            props=self.sample_p["props"]
        )
        self.assertEqual(
            None,
            nodeWoTag.value
        )
        self.assertEqual(
            self.sample_p["tag"],
            nodeWoTag.tag
        )
    
    def test_children_default(self):
        nodeWoTag = HTMLNode(
            tag=self.sample_p["tag"],
            value=self.sample_p["value"],
            props=self.sample_p["props"]
        )
        self.assertEqual(
            self.sample_p["value"],
            nodeWoTag.value
        )
        self.assertEqual(
            None,
            nodeWoTag.children
        )
    
    def test_props_default(self):
        nodeWoTag = HTMLNode(
            tag=self.sample_p["tag"],
            value=self.sample_p["value"],
            children=self.sample_p["children"]
        )
        self.assertEqual(
            self.sample_p["value"],
            nodeWoTag.value
        )
        self.assertEqual(
            None,
            nodeWoTag.props
        )
        
    def test_props_formating(self):
        testNode = HTMLNode(
            props=self.sample_p["props"]
        )
        
        self.assertEqual(
            ' href="https://www.google.com"',
            testNode.props_to_html(),
            "Error in the props to html function"
        )
    
    def test_leaf_full(self):
        testNode = LeafNode(self.sample_p["tag"], self.sample_p["value"], self.sample_p["props"])
        html_code = testNode.to_html()
        
        self.assertEqual(
            '<a href="https://www.google.com">Lorem ipsum</a>',
            testNode.to_html()
        )
        self.assertEqual(
            None,
            testNode.children
        )
    
    def test_leaf_tagless(self):
        testNode = LeafNode(None, self.sample_p["value"])
        
        self.assertEqual(
            self.sample_p["value"],
            testNode.to_html()
        )
    
    def test_valueless_leaf(self):
        valueless_leaf = LeafNode(self.sample_p["tag"], None)
        
        with self.assertRaises(ValueError):
            print( valueless_leaf.to_html() )
        

if __name__ == "__main__":
    unittest.main()