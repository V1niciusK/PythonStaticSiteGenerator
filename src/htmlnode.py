
class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict[str,str] = None
        ):
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        
        prop_list = map( 
            lambda key: f'{key}="{self.props[key]}"',
            self.props
            )
        
        prop_string = " ".join(prop_list)
        
        return f" {prop_string}"
    
    def __eq__(self, comparable):
        return (
            self.tag == comparable.tag and
            self.value == comparable.value and
            self.children == comparable.children and
            self.props == comparable.props
        )

    def __repr__(self) -> str:
        return f"""
    {self.tag = }
    {self.value = }
    {self.children = }
    {self.props = }
    """

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value:str, props: dict[str,str] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("All leafNodes should have a value")

        if self.tag == None:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict[str,str] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        # Guard clauses
        if self.tag == None:
            raise ValueError(f"Parent nodes need the tag value set")
        
        if (self.children == None ) or ( len(self.children) == 0 ):
            raise ValueError(f"Parent nodes need the children value set")
        
        # Recursion begins here
        #accumulator
        children_value_chain: str = ""
        
        for child in self.children:
            children_value_chain = f"{children_value_chain}{child.to_html()}"
        
        return f"<{self.tag}{self.props_to_html()}>{children_value_chain}</{self.tag}>"

#