class TreeNode:
    def __init__(self, parentNode, value):
        self.parentNode = parentNode or None
        self.value = value
        self.children = []
    
    def addChild(self, childNode):
        if len(self.children) < 2:
            self.children.append(childNode)
    
    def removeChild(self, childNode):
        if len(self.children) > 0:
            self.children = [child for child in self.children if child is not childNode]
