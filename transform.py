import os
import re

def parse_adjacency_list(file_path):
    with open(file_path, 'r') as file:
        # Read the number of nodes and edges
        num_nodes, num_edges = map(int, file.readline().strip().split())
        
        # Initialize adjacency list
        adjacency_list = []
        
        # Read the adjacency list
        for i in range(num_nodes):
            connected_nodes = list(map(int, file.readline().strip().split()))
            for node in connected_nodes:
                if (node + 1, i + 1) not in adjacency_list:
                    adjacency_list.append((node + 1, i + 1))
                    
    return num_nodes, num_edges, adjacency_list

def create_dataset_files(adjacency_lists, num_nodes, output_dir):
    # Prepare data for the dataset
    graph_indicator = []
    graph_labels = []
    node_labels = []
    current_node_id = 1
    
    # Initialize graph ID
    graph_id = 1

    # Combine data from all adjacency lists
    for adjacency_list in adjacency_lists:
        for edge in adjacency_list:
            # Adjust node IDs for the combined dataset
            adjusted_edge = (edge[0] + current_node_id - 1, edge[1] + current_node_id - 1)
            graph_indicator.extend([graph_id] * (edge[0] + 1 - len(graph_indicator)))
            graph_indicator.extend([graph_id] * (edge[1] + 1 - len(graph_indicator)))
            node_labels.extend([1] * (max(adjusted_edge) + 1 - len(node_labels)))
        
        current_node_id += len(graph_indicator) - len(node_labels)
        graph_labels.append(1)
        graph_id += 1
    
    # Write DS_A.txt
    with open(os.path.join(output_dir, 'Moore_A.txt'), 'w') as file:
        for adjacency_list in adjacency_lists:
            for edge in adjacency_list:
                adjusted_edge = (edge[0] + current_node_id - 1, edge[1] + current_node_id - 1)
                file.write(f'{adjusted_edge[0]},{adjusted_edge[1]}\n')
                
    # Write DS_graph_indicator.txt
    with open(os.path.join(output_dir, 'Moore_graph_indicator.txt'), 'w') as file:
        for indicator in graph_indicator:
            file.write(f'{indicator}\n')
    
    # Write DS_graph_labels.txt
    with open(os.path.join(output_dir, 'Moore_graph_labels.txt'), 'w') as file:
        for label in graph_labels:
            file.write(f'{label}\n')
    
    # Write DS_node_labels.txt
    with open(os.path.join(output_dir, 'Moore_node_labels.txt'), 'w') as file:
        for label in node_labels:
            file.write(f'{label}\n')
    
def main():
    input_dir = 'polarfly/topologies/data/PolarStars'
    output_dir = 'dataset'
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Helper function to extract the numeric part from the filename
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')
    
    # Get and sort all adjacency list files in the input directory
    filenames = sorted([f for f in os.listdir(input_dir) if f.endswith('.adj.txt')],
                       key=extract_number)
    
    # Parse all adjacency list files in the input directory
    adjacency_lists = []
    total_nodes = 0
    total_edges = 0
    
    for filename in filenames:
        if filename.endswith('.adj.txt'):
            file_path = os.path.join(input_dir, filename)
            num_nodes, num_edges, adjacency_list = parse_adjacency_list(file_path)
            adjacency_lists.append(adjacency_list)
            total_nodes += num_nodes
            total_edges += num_edges
    
    # Create dataset files
    create_dataset_files(adjacency_lists, total_nodes, output_dir)
    
    print(f'Dataset files created in directory: {output_dir}')

if __name__ == '__main__':
    main()
