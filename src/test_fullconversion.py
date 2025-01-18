import unittest

from textnode import BlockType, markdown_to_hml_node, block_to_header, block_to_list
from htmlnode import LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Full conversion test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Full conversion test done")
    
    def test_header_conversion(self):
        testBlock: str = "# Lorem ipsum"
        toTest: LeafNode = block_to_header(testBlock)
        
        self.assertEqual(
            toTest,
            LeafNode("h1", "Lorem ipsum")
        )
    
    def test_header_conversion_link(self):
        testBlock: str = "###### [Lorem](http://ipsum.dol)"
        toTest: str = block_to_header(testBlock).to_html()
        
        self.assertEqual(
            toTest,
            '<h6><a href="http://ipsum.dol">Lorem</a></h6>'
        )
    
    def test_conversion_mixed_nol(self):
        testBlock: str = '''1. Lorem Ipsum
2. [Dolor](sit)
3. Amet consectetur
'''
        toTest: ParentNode = block_to_list(testBlock, BlockType.nol).to_html()
        
        self.assertEqual(
            toTest,
            '<ol type="1"><li>Lorem Ipsum</li><li><a href="sit">Dolor</a></li><li>Amet consectetur</li></ol>'
        )
    
    def test_conversion_mixed_ul(self):
        testBlock: str = '''* Lorem Ipsum
* [Dolor](sit)
* Amet consectetur
'''
        toTest: ParentNode = block_to_list(testBlock, BlockType.ul).to_html()
        
        self.assertEqual(
            toTest,
            '<ul style="list-style-type:disc;"><li>Lorem Ipsum</li><li><a href="sit">Dolor</a></li><li>Amet consectetur</li></ul>'
        )

# Currently broken:
# Code block: code is displayed before and outside pre and code blocks as paragraphs, except for the line breaks, those are fine.
# Ordered lists: the first item is the only one inside the list, the rest comes before as a paragraph
  
    def test_block_conversion(self):
        testBlock: str = '''### Full conversion

> Lorem ipsum dolor sit amet
> consectetur adipiscing elit.
> Aliquam tempor augue urna, ut efficitur quam porta vitae.

Ut eget molestie **lorem**. Donec `neque nisl`, lacinia ut laoreet vulputate, cursus at eros. Nulla vitae sodales ligula, eget lobortis lacus. Integer convallis pretium purus, quis finibus dolor pretium faucibus. Nam venenatis lacinia ipsum, a placerat nunc iaculis sit amet.

```
print(f"Nullam rhoncus velit vel augue finibus")
print("non efficitur tellus sagittis")
```

1. Test
2. [test2](linkhere)

a. Other test ![image](uri)
b. Other **test** here
c. another test

+ unordered 1
+ unordered 2
+ *unordered* 3
+ unordered 4

#CheckYourBearTraps In finibus porttitor molestie.
        '''
        toTest: ParentNode = markdown_to_hml_node(testBlock)

        print(f"{toTest.to_html() = }")
        
        '''

        
        self.assertEqual(
            toTest.children[0].children[0],
            LeafNode("p", "Lorem ipsum dolor sit amet")
        )
        
        '''

if __name__ == '__main__':
    unittest.main()