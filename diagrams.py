# from graphviz import Digraph

# # Create Control Flow Diagram
# def create_control_flow_diagram(output_path):
#     control_flow = Digraph("ControlFlowDiagram", format="png")
#     control_flow.attr(rankdir="LR")

#     # Nodes
#     control_flow.node("Start", "Start")
#     control_flow.node("Menu", "Display Menu")
#     control_flow.node("ListBooks", "List Books")
#     control_flow.node("BorrowBook", "Borrow Book")
#     control_flow.node("ReturnBook", "Return Book")
#     control_flow.node("Exit", "Exit")

#     # Edges
#     control_flow.edges([
#         ("Start", "Menu"),
#         ("Menu", "ListBooks"),
#         ("Menu", "BorrowBook"),
#         ("Menu", "ReturnBook"),
#         ("Menu", "Exit"),
#         ("ListBooks", "Menu"),
#         ("BorrowBook", "Menu"),
#         ("ReturnBook", "Menu")
#     ])

#     control_flow.render(output_path + "/ControlFlowDiagram")

# # Create Data Flow Diagram
# def create_data_flow_diagram(output_path):
#     data_flow = Digraph("DataFlowDiagram", format="png")
#     data_flow.attr(rankdir="LR")

#     # Nodes
#     data_flow.node("User", "User", shape="ellipse")
#     data_flow.node("Library", "Library System", shape="box")
#     data_flow.node("Inventory", "Books Inventory", shape="cylinder")

#     # Edges
#     data_flow.edge("User", "Library", label="Inputs (Menu Choice)")
#     data_flow.edge("Library", "Inventory", label="Fetch/Update Book Data")
#     data_flow.edge("Inventory", "Library", label="Book Data")
#     data_flow.edge("Library", "User", label="Outputs (Messages)")

#     data_flow.render(output_path + "/DataFlowDiagram")

# # Create Call Graph
# def create_call_graph(output_path):
#     call_graph = Digraph("CallGraph", format="png")

#     # Nodes
#     call_graph.node("main", "main()")
#     call_graph.node("init", "Library.__init__()")
#     call_graph.node("list_books", "Library.list_books()")
#     call_graph.node("borrow_book", "Library.borrow_book()")
#     call_graph.node("return_book", "Library.return_book()")

#     # Edges
#     call_graph.edges([
#         ("main", "init"),
#         ("main", "list_books"),
#         ("main", "borrow_book"),
#         ("main", "return_book")
#     ])

#     call_graph.render(output_path + "/CallGraph")

# if __name__ == "__main__":
#     output_path = "."  # Output diagrams in the current directory
#     create_control_flow_diagram(output_path)
#     create_data_flow_diagram(output_path)
#     create_call_graph(output_path)
#     print("Diagrams generated successfully!")

import os
import ast
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("Agg")


# --- CFG Generation ---
def generate_cfg(file_path, output_path="cfg.png"):
    """
    Generate Control Flow Graph (CFG) from a Python file and save as PNG.
    """
    try:
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
        
        cfg = nx.DiGraph()

        class CFGNodeVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_node = None

            def generic_visit(self, node):
                if isinstance(node, ast.stmt):
                    cfg.add_node(id(node), label=type(node).__name__)
                    if self.current_node:
                        cfg.add_edge(self.current_node, id(node))
                    self.current_node = id(node)
                super().generic_visit(node)

        visitor = CFGNodeVisitor()
        visitor.visit(tree)

        # Draw and save CFG
        pos = nx.spring_layout(cfg)
        nx.draw(cfg, pos, with_labels=True, node_color="lightblue", node_size=1500, font_size=8)
        labels = nx.get_node_attributes(cfg, "label")
        nx.draw_networkx_labels(cfg, pos, labels)
        plt.savefig(output_path)
        plt.close()
        print(f"CFG saved to {output_path}")

    except Exception as e:
        print(f"Error generating CFG: {e}")


# --- Call Graph Generation ---
def generate_call_graph(entry_file, output_path="callgraph.png"):
    """
    Generate Call Graph using static analysis and save as PNG.
    """
    try:
        call_graph = nx.DiGraph()

        class CallGraphVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_function = None

            def visit_FunctionDef(self, node):
                self.current_function = node.name
                call_graph.add_node(node.name, label="Function")
                self.generic_visit(node)
                self.current_function = None

            def visit_Call(self, node):
                if self.current_function and isinstance(node.func, ast.Name):
                    call_graph.add_edge(self.current_function, node.func.id)
                self.generic_visit(node)

        with open(entry_file, "r") as source:
            tree = ast.parse(source.read())
            visitor = CallGraphVisitor()
            visitor.visit(tree)

        # Draw and save Call Graph
        pos = nx.spring_layout(call_graph)
        nx.draw(call_graph, pos, with_labels=True, node_color="lightgreen", node_size=1500, font_size=8)
        plt.savefig(output_path)
        plt.close()
        print(f"Call graph saved to {output_path}")

    except Exception as e:
        print(f"Error generating Call Graph: {e}")


# --- DFD Generation ---
def generate_dfd(processes, data_stores, external_entities, output_path="dfd.png"):
    """
    Generate a Data Flow Diagram (DFD) and save as PNG using Matplotlib.
    """
    try:
        dfd = nx.DiGraph()

        # Add external entities
        for entity in external_entities:
            dfd.add_node(entity, shape="rectangle", color="lightblue")

        # Add data stores
        for store in data_stores:
            dfd.add_node(store, shape="cylinder", color="lightgreen")

        # Add processes and connections
        for process, connections in processes.items():
            dfd.add_node(process, shape="ellipse", color="yellow")
            for target in connections:
                dfd.add_edge(process, target)

        # Draw and save DFD
        pos = nx.spring_layout(dfd)
        nx.draw(dfd, pos, with_labels=True, node_color="lightyellow", node_size=1500, font_size=8)
        plt.savefig(output_path)
        plt.close()
        print(f"DFD saved to {output_path}")

    except Exception as e:
        print(f"Error generating DFD: {e}")

def main():
    project_files = ["simple library management/main.py"]  # Ensure this path is correct
    output_dir = "analysis_output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate CFG for each file
    for file in project_files:
        try:
            output_path = os.path.join(output_dir, f"cfg_{os.path.basename(file).split('.')[0]}.png")
            print(f"Generating CFG for {file}...")
            generate_cfg(file, output_path)
        except Exception as e:
            print(f"Failed to generate CFG for {file}: {e}")

    # Generate Call Graph
    try:
        print("Generating Call Graph...")
        generate_call_graph("simple library management/main.py", os.path.join(output_dir, "callgraph.png"))
    except Exception as e:
        print(f"Failed to generate Call Graph: {e}")

    # Generate DFD
    try:
        print("Generating DFD...")
        processes = {
            "main": ["list_books", "borrow_book", "return_book"],
            "list_books": ["log"],
            "borrow_book": ["log"],
            "return_book": ["log"],
        }
        data_stores = ["log.txt"]
        external_entities = ["user"]
        generate_dfd(processes, data_stores, external_entities, os.path.join(output_dir, "dfd.png"))
    except Exception as e:
        print(f"Failed to generate DFD: {e}")

    print(f"Analysis complete. Results saved in '{output_dir}'.")
