import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentHTMLNode(unittest.TestCase):
    
    def setUp(self):
        self.t_tag = "div"
        self.t_props = {
            "class": "paragraph-center",
            "nounce": "123"
        }
        self.testChildNodeA = LeafNode("a", "Lorem ipsum",{"href": "https://www.google.com"})
        self.testChildNodeB = LeafNode("b", "Foo bar baz", {"class": "bold-mild"})
        self.testChildNodeC = LeafNode(None, "Dolor sit amet")
        
        
    
    @classmethod
    def setUpClass(cls):
        print("Beginning Parent Node test")
    
    @classmethod
    def tearDownClass(cls):
        print("Ended Parent Node tests")
    
    def test_mandatory_params(self):
        testNode = ParentNode("footer",[self.testChildNodeC])
        
        self.assertEqual(
            testNode.tag,
            "footer"
        )
        self.assertEqual(
            testNode.children[0].to_html(),
            self.testChildNodeC.to_html()
        )
    
    def test_parent_to_html_single_child(self):
        
        html_result = f'<div>{self.testChildNodeA.to_html()}</div>'
        
        testNode = ParentNode("div", [self.testChildNodeA])
        
        self.assertEqual(
            html_result,
            testNode.to_html()
        )
    
    def test_parent_to_html_multi_leaf_child(self):
        html_result = f'<div>{self.testChildNodeA.to_html()}{self.testChildNodeB.to_html()}</div>'
        
        testNode = ParentNode("div", [self.testChildNodeA, self.testChildNodeB])
        
        self.assertEqual(
            html_result,
            testNode.to_html()
        )
    
    def test_parent_with_props(self):
        html_result = f'<div class="paragraph-center" nounce="123">{self.testChildNodeA.to_html()}</div>'
        
        testNode = ParentNode("div", [self.testChildNodeA], self.t_props)
        
        self.assertEqual(
            html_result,
            testNode.to_html()
        )
    
    def test_multi_parent_chain(self):
        html_result = f'<div><div>{self.testChildNodeC.to_html()}</div></div>'
        
        testInnerNode = ParentNode("div", [self.testChildNodeC])
        testOuterNode = ParentNode("div", [testInnerNode])
        
        self.assertEqual(
            html_result,
            testOuterNode.to_html()
        )

if __name__ == "__main__":
    unittest.main()