# Implement the node for merkle tree here
from lemonBlock import LemonBlock
class Node:
    def __init__(self, value: str, left_child=None, right_child=None) -> None:
        self.left = left_child
        self.right = right_child
        self.value = value

"""
# Examples --- Create the nodes
head_node = Node("3")
node_1 = Node("2")
node_2 = Node("1")
node_3 = Node("4")
node_4 = Node("5")
"""
