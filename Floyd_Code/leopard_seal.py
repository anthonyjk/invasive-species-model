def leopard_seal(animal_dict, edges_dict):
    '''
    A function updating the number of leopard_seals in the ecosystem.
    It is used internally to update
    '''
    #Defining the current numbers of each animal
    krill = animals_dict["Krill"]
    arctic_cod = animals_dict["Arctic Cod"]
    orca = animals_dict["Orca"]

    #Updating the number of Leopard Seals
    animal_dict["Leopard Seal"] += (#Function of krill and cod - Function of orcas)

    #Taking the subtracted values for use in the Networkx graph.
    edges_dict[("Leopard Seal", "Orca")] = #Function of orcas

    #Returns updated information for the Leopard Seal
    return animal_dict, edges _dict
    
    