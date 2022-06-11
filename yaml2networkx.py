import networkx as nx
import matplotlib.pyplot as plt
import yaml

def yaml2networkx(filename):
    topic_pub_dict = {
        # "/topic_0": ["/node_0"],
    }

    topic_sub_dict = {
        # "/topic_0": ["/node_1"],
    }

    with open(filename) as file:
        yml = yaml.safe_load(file)
        nodes = yml['nodes']
        for node in nodes:
            node_name = node['node_name']
            if 'publishes' in node:
                publishes = node['publishes']
                for publish in publishes:
                    if publish['topic_name'] in topic_pub_dict:
                        topic_pub_dict[publish['topic_name']].append(node_name)
                    else:
                        topic_pub_dict[publish['topic_name']] = [node_name]
            if 'subscribes' in node:
                subscribes = node['subscribes']
                for subscribe in subscribes:
                    if subscribe['topic_name'] in topic_sub_dict:
                        topic_sub_dict[subscribe['topic_name']].append(node_name)
                    else:
                        topic_sub_dict[subscribe['topic_name']] = [node_name]

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

    return G

if __name__ == '__main__':
    G = yaml2networkx('sample_0.yaml')
    pos = nx.spring_layout(G)
    # pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos)
    plt.show()