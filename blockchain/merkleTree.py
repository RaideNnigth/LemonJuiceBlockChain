# This class will implement a Merkle Tree for the blockchain, storing the transactions
# in the leaves of the tree and the hashes of the transactions in the nodes of the tree.

from utils import calculate_hash
import math
from node import Node
from lemonBlock import LemonBlock

class merkleTree:
    def __init__(self, values: list[str]):
        self.values = values
        self.root = self.build_merkle_tree(self.values)
    
    def build_merkle_tree(self, values: list[str]) -> Node:
        complete_set = self.fill_set(values)
        old_set_of_nodes = [Node(value) for value in complete_set]
        tree_depth = self.compute_tree_depth(len(old_set_of_nodes))

        new_set_of_nodes = []   # This will be the new set of nodes, creating here soo we never have it empty at return
        for i in range(tree_depth):
            num_nodes = 2**(tree_depth - i)
            new_set_of_nodes = []
            for j in range(0, num_nodes, 2):
                child_node_0 = old_set_of_nodes[j]
                child_node_1 = old_set_of_nodes[j + 1]
                new_node = Node(
                    value = calculate_hash(child_node_0.value + child_node_1.value),
                    left_child = child_node_0,
                    right_child = child_node_1
                    )
                new_set_of_nodes.append(new_node)
            old_set_of_nodes = new_set_of_nodes
        return new_set_of_nodes[0]
        
    def compute_tree_depth(self, num_leaves):
        return math.ceil(math.log(num_leaves, 2))
    
    def is_power_of_two(self, number_of_leaves: int) -> bool:
        return math.log(number_of_leaves, 2).is_integer()
    
    def fill_set(self, nodes: list):
        if self.is_power_of_two(len(nodes)):
            return nodes
        else:
            new_nodes = nodes
            while not self.is_power_of_two(len(new_nodes)):
                new_nodes.append(new_nodes[-1])
            return new_nodes
    def print_tree(self, node, depth=0):
        if node is None:
            return
        print(f"{'  ' * depth}{node.value}")
        self.print_tree(node.left, depth + 1)
        self.print_tree(node.right, depth + 1)
    
        
# Examples --- Create the nodes


# Dont forget that if you wanna test it here you would need to create a timestamp for each block
import datetime
timestamp = datetime.datetime.now().strftime("%m%d%Y%H%M%S")


t1 = "John sends 2 LC to Mike"
t2 = "Mike sends 2.5 LC to John"
t3 = "John sends 1 LC to Mike"
t4 = "Mike sends 0.5 LC to John"
t5 = "John sends 3 LC to Mike"
t6 = "Mike sends 1 LC to John"

# Initial block creation
initial_block = LemonBlock("Initial String", timestamp,[t1, t2])

# Second block creation
second_block = LemonBlock(initial_block.cryptografic_hash(), timestamp,[t3, t4])

# Third block creation
third_block = LemonBlock(second_block.cryptografic_hash(), timestamp,[t5, t6])

# Create the merkle tree
merkle_tree = merkleTree([t1, t2, t3, t4, t5, t6])

# Print tree
merkle_tree.print_tree(merkle_tree.root)
