import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pygraphviz as pgv

topic_pub_dict = {
    "/topic_0": ["/node0"],
    "/topic_1": ["/node1"],
    "/topic_2": ["/node2"],
    "/topic_3": ["/node3"],
    "/topic_5": ["/node3"],
}

topic_sub_dict = {
    "/topic_0": ["/node1"],
    "/topic_1": ["/node2", "/node3"],
    "/topic_2": ["/node4"],
    "/topic_3": ["/node5"],
    "/topic_2": ["/node5"],
}

G = nx.DiGraph()

for topic, node_pub_list in topic_pub_dict.items():
    if topic in topic_sub_dict:
        node_sub_list = topic_sub_dict[topic]
    else:
        # node_sub_list = ["none:" + topic]
        continue
    for node_pub in node_pub_list:
        for node_sub in node_sub_list:
            # print(topic, node_pub, node_sub)
            G.add_edge(node_pub, node_sub, label=topic)


pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
plt.show()

H = nx.nx_agraph.to_agraph(G)
H.layout(prog='circo')
nx.draw_networkx(nx.nx_agraph.from_agraph(H))
plt.show()

nx.nx_agraph.to_agraph(G).draw('graph.png', prog='circo')
img = mpimg.imread('graph.png')
imgplot = plt.imshow(img)
plt.show()
