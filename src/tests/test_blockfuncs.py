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
            BlockType.h,
            toTest
        )
    
    def test_block_classification_h5(self):
        testBlock: str = "##### Test"
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.h,
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

    def test_block_classification_dashul(self):
        testBlock: str = """- item1
- item2
- item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.ul,
            toTest
        )
        
    def test_block_classification_plusul(self):
        testBlock: str = """+ item1
+ item2
+ item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.ul,
            toTest
        )
 
    def test_block_classification_starul(self):
        testBlock: str = """* item1
* item2
* item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.ul,
            toTest
        )
        
    def test_block_classification_nol(self):
        testBlock: str = """1. item1
2. item2
3. item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.nol,
            toTest
        )
    
    def test_block_classification_lol(self):
        testBlock: str = """a. item1
b. item2
c. item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.lol,
            toTest
        )
    
    def test_block_classification_rol(self):
        testBlock: str = """i. item1
ii. item2
iii. item3 
        """
        toTest: BlockType = block_to_blocktype(testBlock)
        
        self.assertEqual(
            BlockType.rol,
            toTest
        )

if __name__ == '__main__':
    unittest.main()