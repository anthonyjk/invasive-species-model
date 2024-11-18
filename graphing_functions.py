def set_dictionaries():
    '''
    This function is used to create the needed dictionaries for the function food_web_plot.

    Inputs: None

    Outputs: direction_dict (dictionary type object), position_dict (dictionary type object), conversion_dict (dictionary type object)
    
    direction_dict is a dictionary of node connections using labels used to initialize the networkx graph.
    postiion_dict is a dictionary of node positions indexed by animal names as strings.
    conversion_dict is a dictionary used to create the edges dictionary in the create_edges_dict function. It contains the keys to the      dictionary defined in the run function of the ecosystem library.
    '''
    #Creates a dictionary to use for the directions of edges in the Networkx Plot.
    direction_dict = {"Arctic Cod": ["Orca", "Leopard Seal"], 
                    "Orca": [], 
                    "Krill": ["Arctic Cod", "Leopard Seal", "Baleen Whale", "Penguin"], 
                    "Penguin": ["Orca"], 
                    "Baleen Whale": [], 
                    "Leopard Seal": ["Orca"]}
    
    #Creates a dictionary to use for the locations of nodes in the Networkx Plot.
    position_dict = {"Arctic Cod": (1, 5), 
                    "Orca": (7, 4), 
                    "Krill": (3.5, 5.5), 
                    "Penguin": (5.75, 6.5), 
                    "Baleen Whale": (2, 8), 
                    "Leopard Seal": (6.5, 8)}
    
    #Creates a dictionary containing the same keys as the direction_dict. Each of these contains keys to the eco_data dictionary.
    #When used together in the create_edges_dict function, they update the edges dictionary with new information for the graphing
    #function.
    conversion_dict = {"Arctic Cod": ["orca_cod_consumed", "seal_cod_consumed"], 
                    "Orca": [], 
                    "Krill": ["cod_krill_consumed", "seal_krill_consumed", "whale_krill_consumed", "penguin_krill_consumed"], 
                    "Penguin": ["orca_penguin_consumed"], 
                    "Baleen Whale": [], 
                    "Leopard Seal": ["orca_seal_consumed"]}

    #Creates a list to use in the food_web_plot function as node sizes.
    node_size_list = [4500, 2000, 2000, 3000, 8000, 8000]

    return direction_dict, position_dict, conversion_dict, node_size_list



def generate_color_list(creatures):
    '''
    This function generates a list of color values for use in the food_web_plot function.

    Inputs: creatures (dictionary type object) with keys as animal names and values of numbers of those animals.

    Outputs: A list of values for the intensity of the colors of the nodes in the Networkx graph. 
    Each value being between 0 and 1 (inclusive).
    '''
    #Author Note, Update the denominator values when some testing is done
    arctic_cod_color = creatures["cod_pop"] / (2000 * 6)
    orca_color = creatures["orca_pop"] / (20)
    krill_color = creatures["krill_pop"] / (1.8e6)
    penguin_color = creatures["penguin_pop"] / (1200)
    baleen_whale_color = creatures["whale_pop"] / (30)
    leopard_seal_color = creatures["seal_pop"] / (50 * 2)

    #Checks if invasive species has been added to the creatures dictionary and, if yes, adds a color for it to the color list.
    if "King Crab" in creatures:
        king_crab_color = creatures["crab_pop"] / (1)
        color_list = [arctic_cod_color, orca_color, krill_color, penguin_color, balleen_whale_color, leopard_seal_color, king_crab_color]

    else:
        color_list = [arctic_cod_color, orca_color, krill_color, penguin_color, baleen_whale_color, leopard_seal_color]

    for i in range(len(color_list)):
        if color_list[i] > 1:
            color_list[i] = 1

    return color_list





def create_edges_dict(creatures, direction_dict, conversion_dict):
    '''
    This function creates a dictionary to use for the edge values in the Networkx graph.

    Inputs: creatures (pandas dataframe), direction_dict (dictionary type object), conversion_dict (dictionary type object).
    The direction_dict and conversion_dict are recieved as outputs of the set_dictionaries function and can be used without alteration.
    The creatures dictionary is received from the run function in the ecosystem library. It contains the majority of all of the information that is calculated by the model. This function makes use only of certain relevant portions of this dictionary.

    Outputs: edges_dict (dictionary type object).
    The edges_dict is specifically designed to be used in the food_web_plot in the place of the parameter with the same name.
    It defines the edge values on the resulting Networkx graph.
    '''
    edges_dict = {}
    for i in direction_dict:
        for j in range(len(direction_dict[i])):
            edges_dict[(i , direction_dict[i][j])] = int(creatures[conversion_dict[i][j]])

    return edges_dict
            
    



def food_web_plot(eco_dict, direction_dict, position_dict, conversion_dict, node_size_list, file_name, step = 100):
    
    '''
    This function creates a Networkx graph.

    Inputs: direction_dict (dictionary type object), position_dict (dictionary type object), edges_dict (dictionary type object)
    These inputs are obtained from the set_dictionaries function, edges_dict is designed to be updated before use.
    node_color_array (list type object), is a list of values for the intensity of the colors of the nodes. It must be of
    the same length as the number of nodes in the Networkx graph and each value must be between 0 and 1.
    
    Optional Input of node_size_array (array type object with length == len(direction_dict). Changing this array is not recommended.

    Output: A visual of the input data graphed using Networkx. This function does not return anything, it only prints an image.
    '''
    #Plots the Networkx Graph
    import networkx as nx
    import matplotlib.pyplot as plt
    import time
    from PIL import Image
    import io
    
    images = []
    for i in range(len(eco_dict)):
        if i % step == 0 or i == (len(eco_dict)):
            fig = plt.figure(3, figsize=(12,10), animated = True)
            temp_im = io.BytesIO()
            G = nx.DiGraph(direction_dict)
            node_color_list = generate_color_list(eco_dict.iloc[i,:])
            edges_dict = create_edges_dict(eco_dict.iloc[i,:], direction_dict, conversion_dict)
            nx.draw_networkx_edge_labels(G, pos = position_dict, 
                                         edge_labels = edges_dict, 
                                         verticalalignment = "bottom") #Plots edge labels
            nx.draw_networkx(G, pos = position_dict, 
                             node_size = node_size_list, 
                             cmap = "plasma", 
                             node_color = node_color_list, 
                             vmin = 0, vmax = 1, alpha = 0.8)
            fig.savefig(temp_im, format='png')
            temp_im.seek(0)
            images.append(Image.open(temp_im))
            G.clear()
            fig.clear()
    
    images[0].save(file_name, 
                   save_all=True, 
                   append_images=images[1:], 
                   duration=600, 
                   loop=0)