x, k, p, c, s, o, w = [], [], [], [], [], [], []
def run():
    global x, k, p, c, s, o, w
    x, k, p, c, s, o, w = [], [], [], [], [], [], []
    for i in range(365*4):
        if i > 365:
            x.append(i)
            k.append(creatures['krill'])
            p.append(creatures['penguin'])
            c.append(creatures['arctic cod'])
            s.append(creatures['leopard seal'])
            o.append(creatures['orca'])
            w.append(creatures['baleen whale'])
        cycle(day=i)

    if i % 20 == 0 or i == 365*4:
        #food_web_plot(direction_dict, position_dict, edges_dict, node_color_list, 
                  #node_size_list = node_sizes):