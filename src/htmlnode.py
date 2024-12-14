
class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict[str,str] = None):
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
        
        return f"<{self.tag}{HTMLNode.props_to_html(self)}>{self.value}</{self.tag}>"