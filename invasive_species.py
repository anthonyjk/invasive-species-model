import random

def king_crab(creatures, step = 1):
    # Constants
    # https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/40695827.pdf
    # https://www.wwf.org.uk/learn/fascinating-facts/antarctic-krill#:~:text=Krill%20are%20larger%20than%20you,average%20size%20(by%20weight).
    # https://www.ppsf.com/ecom_img/original-8-19-ss_kingcrab.pdf
    cod_weight = 70 #gm    
    krill_weight = 1 #gm
    crab_weight = 6803 #gm

    # Consumption
    # King Crab can eat upto 10% of their body weight. Let's consider 8% - 10%
    # Search Labs | AI Overview
    for i in range(creatures['king crab']):
        intake_max = random.uniform(0.08, 0.1) * crab_weight
        intake_max = intake_max * step
        consumed = 0

        while consumed < intake_max:
            prey_total = creatures['krill'] + creatures['arctic cod']
            krill_weight = creatures['krill'] / prey_total
            cod_weight = creatures['arctic cod'] / prey_total

            prey = random.choices(population=['krill', 'cod'], weights=[krill_weight, cod_weight])[0]

            if prey == 'krill':
                creatures['krill'] = creatures['krill'] - 1
                consumed = consumed + krill_weight

            elif prey == 'cod' and creatures['arctic cod'] > 0:
                creatures['arctic cod'] = creatures['arctic cod'] - 1
                consumed = consumed +  cod_weight



    # Reproduction
    # King Crab Reproduces once every year
    # https://www.fisheries.noaa.gov/species/red-king-crab#:~:text=Female%20red%20king%20crabs%20reproduce,settling%20on%20the%20ocean%20bottom.
    # Offspring from 50k to 500k. Since babay crabs won't be eating much so considering upper limit 100k
    # https://www.fisheries.noaa.gov/species/red-king-crab#:~:text=Female%20red%20king%20crabs%20reproduce,settling%20on%20the%20ocean%20bottom.

    reproduction_chance = step / 365.25  
    mates = creatures['king crab'] // 2

    for i in range(mates):
        offspring = random.choices(population=[0, random.randint(50000, 100000)], weights=[1 - reproduction_chance, reproduction_chance])[0]
        creatures['king crab'] = creatures['king crab'] +  offspring



    # Mortality
    # King Crabs can live upto 20 - 30 Years. Let's take the average 25 Years
    # https://www.adfg.alaska.gov/index.cfm?adfg=redkingcrab.printerfriendly#:~:text=Did%20You%20Know%3F-,Male%20red%20king%20crabs%20can%20grow%20up%20to%2024lbs%20with,up%20to%2020%2D30%20years.

    years = 20
    death_chance = step / (years * 365.25)
    for i in range(creatures['king crab']):
        death = random.choices(population=[0, 1], weights=[1 - death_chance, death_chance])[0]
        creatures['king crab'] = creatures['king crab'] - death

    return creatures
