class GenealogyNode:
    def __init__(
        self, user_id, parent_nodes=None, spouse_node=None, children_nodes=None
    ):
        self.user_id = user_id
        self.parent_nodes = parent_nodes or []
        self.spouse_node = spouse_node or None
        self.children_nodes = children_nodes or []

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "parent_nodes": [p.to_dict() for p in self.parent_nodes],
            "spouse_nodes": self.spouse_node.to_dict() if self.spouse_node else None,
            "children_nodes": [c.to_dict() for c in self.children_nodes],
        }
