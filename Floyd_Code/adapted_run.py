def run():
    global eco_data
    step = []
    krill_pop, krill_growth = [], []
    penguin_pop, penguin_growth, penguin_death, penguin_krill_consumed = [], [], [], []
    cod_pop, cod_growth, cod_death, cod_krill_consumed = [],[],[],[]
    seal_pop, seal_growth, seal_death, seal_krill_consumed, seal_cod_consumed = [],[],[],[],[]
    orca_pop, orca_growth, orca_death, orca_cod_consumed, orca_penguin_consumed, orca_seal_consumed = [], [], [], [], [], []
    whale_pop, whale_growth, whale_death, whale_krill_consumed = [],[],[],[]
    for day in range(365 * 10): # 10 Years
        step.append(day)
        # Population Tracking
        krill_pop.append(creatures['krill'])
        penguin_pop.append(creatures['penguin'])
        cod_pop.append(creatures['arctic cod'])
        seal_pop.append(creatures['leopard seal'])
        orca_pop.append(creatures['orca'])
        whale_pop.append(creatures['baleen whale'])
        # Other Variables
        # Krill
        krill_growth.append(krill(day))

        # Penguin
        g, d, kc = penguin(day)
        penguin_growth.append(g)
        penguin_death.append(d)
        penguin_krill_consumed.append(kc)

        # Arctic Cod
        g, d, kc = cod(day)
        cod_growth.append(g)
        cod_death.append(d)
        cod_krill_consumed.append(kc)

        # Leopard Seal
        g, d, kc, cc = seal(day)
        seal_growth.append(g)
        seal_death.append(d)
        seal_krill_consumed.append(kc)
        seal_cod_consumed.append(cc)

        # Orca
        g, d, cc, pc, sc = orca(day)
        orca_growth.append(g)
        orca_death.append(d)
        orca_cod_consumed.append(cc)
        orca_penguin_consumed.append(pc)
        orca_seal_consumed.append(sc)

        # Whale
        g, d, kc = whale(day)
        whale_growth.append(g)
        whale_death.append(d)
        whale_krill_consumed.append(kc)

    eco_data = pd.DataFrame({
    'step': step,
    'krill_pop': krill_pop,
    'krill_growth': krill_growth,
    'penguin_pop': penguin_pop,
    'penguin_growth': penguin_growth,
    'penguin_death': penguin_death,
    'penguin_krill_consumed': penguin_krill_consumed,
    'cod_pop': cod_pop,
    'cod_growth': cod_growth,
    'cod_death': cod_death,
    'cod_krill_consumed': cod_krill_consumed,
    'seal_pop': seal_pop,
    'seal_growth': seal_growth,
    'seal_death': seal_death,
    'seal_krill_consumed': seal_krill_consumed,
    'seal_cod_consumed': seal_cod_consumed,
    'orca_pop': orca_pop,
    'orca_growth': orca_growth,
    'orca_death': orca_death,
    'orca_cod_consumed': orca_cod_consumed,
    'orca_penguin_consumed': orca_penguin_consumed,
    'orca_seal_consumed': orca_seal_consumed,
    'whale_pop': whale_pop,
    'whale_growth': whale_growth,
    'whale_death': whale_death,
    'whale_krill_consumed': whale_krill_consumed
    })

    if day % 20 == 0 or day == 365*10:
        edges_dict = create_edges_dict(eco_data, direction_dict, conversion_dict)
        node_color_list = generate_color_list(eco_data)
        food_web_plot(direction_dict, position_dict, edges_dict, node_color_list, node_size)