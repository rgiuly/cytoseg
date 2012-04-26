# Graph class

import pygraph.classes.graph

class Graph(pygraph.classes.graph.graph):
    
    def add_node_object(self, node):
        
        self.add_node(node.name, [node])

