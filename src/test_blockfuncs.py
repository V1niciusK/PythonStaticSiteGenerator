import unittest

from textnode import BlockType, markdown_to_blocks, block_to_blocktype

class TestTextNode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Block splitting test start")
    
    @classmethod
    def tearDownClass(cls):
        print("Block splitting test done")

    def test_block_splitting(self):
        textWall: str = """# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        toTest: list[str] = markdown_to_blocks(textWall)
        
        self.assertEqual(
            len(toTest),
            3
        )
        
        self.assertEqual(
            toTest[0],
            "# This is a heading"
        )
        
        self.assertEqual(
            toTest[1],
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        )

    def test_block_classification_h1(self):
        testBlock: str = "# Test"
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.h1,
            toTest
        )
    
    def test_block_classification_h5(self):
        testBlock: str = "##### Test"
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.h5,
            toTest
        )
    
    def test_block_classification_code(self):
        testBlock: str = """```
print("hello world")
```
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.code,
            toTest
        )

    def test_block_classification_ul(self):
        testBlock: str = """- item1
- item2
- item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.ul,
            toTest
        )
        
    def test_block_classification_ul(self):
        testBlock: str = """+ item1
+ item2
+ item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.ul,
            toTest
        )
 
    def test_block_classification_ul(self):
        testBlock: str = """* item1
* item2
* item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.ul,
            toTest
        )

   
if __name__ == '__main__':
    unittest.main()