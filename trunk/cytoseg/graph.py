
import pygraph

class Graph(pygraph.graph):
    
    def add_node_object(self, node):
        
        self.add_node(node.name, [node])

