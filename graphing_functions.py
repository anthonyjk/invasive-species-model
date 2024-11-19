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

    return direction_dict, position_dict, conversion_dict, node_size_list #Returns the above dictionaries.



def generate_color_list(creatures):
    '''
    This function generates a list of color values for use in the food_web_plot function.

    Inputs: creatures (dictionary type object) with keys as animal names and values of numbers of those animals.

    Outputs: A list of values for the intensity of the colors of the nodes in the Networkx graph. 
    Each value being between 0 and 1 (inclusive).
    '''
    #Reduces the population of each species to a ratio of ~1, based on some roughly maximally attained values based on testing.
    arctic_cod_color = creatures["cod_pop"] / (2000 * 6)
    orca_color = creatures["orca_pop"] / (20)
    krill_color = creatures["krill_pop"] / (1.8e6)
    penguin_color = creatures["penguin_pop"] / (1200)
    baleen_whale_color = creatures["whale_pop"] / (30)
    leopard_seal_color = creatures["seal_pop"] / (50 * 2)

    #Checks if invasive species has been added to the creatures dictionary and, if yes, adds a color for it to the color list.
    if "crab_pop" in creatures:
        king_crab_color = creatures["crab_pop"] / (1000)
        color_list = [arctic_cod_color, orca_color, krill_color, penguin_color, baleen_whale_color, leopard_seal_color, king_crab_color]

    #If invasive species hasn't been added then defines the color list to not include it.
    else:
        color_list = [arctic_cod_color, orca_color, krill_color, penguin_color, baleen_whale_color, leopard_seal_color]

    #Checks if any of the values in color list are greater than 1 and reduces them to 1 if they are
    for i in range(len(color_list)):
        if color_list[i] > 1:
            color_list[i] = 1

    return color_list #returns the color list





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
    edges_dict = {} #Creates an empty dictionary
    for i in direction_dict: #loops over all of the nodes contained in the direction dictionary
        for j in range(len(direction_dict[i])): #Loops over the nodes the node defined by i connects to
            edges_dict[(i , direction_dict[i][j])] = int(creatures[conversion_dict[i][j]])
            #The conversion_dict stores the node names as keys. Using the name of the node stored by i, we access a list.
            #This list contains the strings used in the dataframe output by the ecosystem run function.
            #So, conversion_dict[i][j] outputs a column title for the dataframe held by the creatures variable.
            #The right side of this equation then as a whole outputs the value associated with that key as an integer.
            #Each key accesses the number of an animal eaten by another and then stores it as the edge value in the dicitonary.

    return edges_dict #Returns the dictionary of edge values.
            
    



def food_web_plot(eco_dict, direction_dict, position_dict, conversion_dict, node_size_list, file_name, step = 100):
    
    '''
    This function creates a Networkx graph.

    Inputs: eco_dict (dictionary type object), direction_dict (dictionary type object), position_dict (dictionary type object), conversion_dict (dictionary type object), node_size_list (list type object), file_name (string type object), step (integer type object).
    The dictionary type object inputs are obtained from the set_dictionaries function. This function makes use of the create_edges_dict function internally using the input dictionaries.
    node_size_list (list type object), is a list of values for the size of the nodes in the networkx graph. It must be the same length as the number of nodes in the graph.
    file_name (string type object) is the name for the gif that will be generated using the networkx graphs.
    Optional Input of step (integer type object). This value tells the model how often to update the networkx graph. The default value is every 100 days. Regardless of step size, the model will always update the graph after the last day.

    Output: A visual of the input data graphed using Networkx in the form of a gif. This function does not return anything, it only save a gif type file.
    '''
    #importing libraries
    import networkx as nx
    import matplotlib.pyplot as plt
    import time
    from PIL import Image
    import io
    
    images = [] #defines a list to store the frames of the gif in
    for i in range(len(eco_dict)): #Loops over all of the data generated by the model
        if i % step == 0 or i == (len(eco_dict)): #Generates a frame for the gif only for the defined steps
            fig = plt.figure(3, figsize=(12,10), animated = True) #Defines the figure size
            temp_im = io.BytesIO() #Creates a temporary image variable using the io library
            G = nx.DiGraph(direction_dict) #Creates a directional Networkx graph
            node_color_list = generate_color_list(eco_dict.iloc[i,:]) #Updates the node_color_list
            edges_dict = create_edges_dict(eco_dict.iloc[i,:], direction_dict, conversion_dict) #Updates the edges dictionary
            nx.draw_networkx_edge_labels(G, pos = position_dict, 
                                         edge_labels = edges_dict, 
                                         verticalalignment = "bottom") #Plots the edge labels
            nx.draw_networkx(G, pos = position_dict, 
                             node_size = node_size_list, 
                             cmap = "plasma", 
                             node_color = node_color_list, 
                             vmin = 0, vmax = 1, alpha = 0.8) #Draws the networkx graph in a matplot figure
            fig.savefig(temp_im, format='png') #Saves the networkx graph as a png over the temp_im variable
            temp_im.seek(0)
            images.append(Image.open(temp_im)) #Adds the image to the images list
            G.clear() #clears the plot
            fig.clear() #clears the figure
    
    images[0].save(file_name, 
                   save_all=True, 
                   append_images=images[1:], 
                   duration=600, 
                   loop=0) #saves the list of images as a gif file.