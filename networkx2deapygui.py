import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import dearpygui.dearpygui as dpg

def networkx2deapygui(G, layout, width, height):
    # Get node and edge information
    node_list = {}  # {"node_name": [in_id, out_id]}
    for node in G.nodes:
        node_list[node] = [-1, -1]
    edge_list = G.edges

    # Convert layout ([-1, 1] -> [0, width])
    layout_np = np.array(list(layout.values()))
    layout_min, layout_max = layout_np.min(0), layout_np.max(0)
    for pos in layout.values():
        pos *= 0.8
        pos[0] -= layout_min[0]
        pos[0] /= (layout_max[0] - layout_min[0])
        pos[1] -= layout_min[1]
        pos[1] /= (layout_max[1] - layout_min[1])
        pos[1] = 1 - pos[1]
        pos[0] *= 0.8 * width
        pos[1] *= 0.8 * height

    with dpg.window(label="Tutorial", width=width, height=height):
        with dpg.node_editor(label="Node Editor 1"):
            for node_name in node_list:
                with dpg.node(label=node_name, pos=layout[node_name]):
                    with dpg.node_attribute() as id_sub:
                        node_list[node_name][0] = id_sub
                    with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as id_pub:
                        node_list[node_name][1] = id_pub
            for edge in edge_list:
                dpg.add_node_link(node_list[edge[0]][1], node_list[edge[1]][0])


if __name__ == '__main__':
    # Create a graph
    G = nx.DiGraph()
    nx.add_path(G, [3, 5, 4, 1, 0, 2])
    nx.add_path(G, [3, 0, 4, 2, 1, 5])

    # Layout the graph and draw it using matplotlib
    layout = nx.spring_layout(G)
    nx.draw_networkx(G, layout)
    plt.show()

    # Draw the graph using Dear PyGui Node Editor
    dpg.create_context()
    networkx2deapygui(G, layout, 600, 400)
    dpg.create_viewport(title='NetworkX Graph', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
