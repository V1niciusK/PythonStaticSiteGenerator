from textnode import TextNode, TextType


def main():
    test_text_node = TextNode( "Lorem ipsum dolor sit amet", TextType.bold , "https://www.boot.dev"  )
    print( test_text_node )



if __name__ == "__main__":
    main()