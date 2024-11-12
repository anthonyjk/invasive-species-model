import random
import math 
from ecosystem.py import creatures
from ecosystem.py import seasonal_adjustment

def king_crab(day, creatures, step = 1):
    # Define Constants
    # https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/40695827.pdf
    # https://www.wwf.org.uk/learn/fascinating-facts/antarctic-krill#:~:text=Krill%20are%20larger%20than%20you,average%20size%20(by%20weight).
    # https://www.ppsf.com/ecom_img/original-8-19-ss_kingcrab.pdf

    cod_weight = 70 #gm    
    krill_weight = 1 #gm
    crab_weight = 6803 #gm
    seasonal_factor = seasonal_adjustment(day)  

    # Consumption
    # King Crab can eat upto 10% of their body weight. Let's consider 8% - 10%
    # Search Labs | AI Overview
    # Total food intake of a king crab
    total_food_intake = creatures["king crab"] * random.uniform(0.80, 0.1) * crab_weight * seasonal_factor * step
    # Total animal intake
    total_prey = creatures["krill"] + creatures["arctic cod"]

    # Reduce number of Arctic cod and krill from the total after getting eaten by the invasive species
    if total_prey > 0:
        consumed_krill = (creatures["krill"]/total_prey) * total_food_intake/krill_weight
        consumed_cod = (creatures["arctic cod"]/total_prey) * total_food_intake/cod_weight

        creatures["krill"] = creatures["krill"] - int(consumed_krill)
        creatures["arctic cod"] = creatures["aractic cod"] - int(consumed_cod)



    # Reproduction
    # King Crab Reproduces once every year
    # https://www.fisheries.noaa.gov/species/red-king-crab#:~:text=Female%20red%20king%20crabs%20reproduce,settling%20on%20the%20ocean%20bottom.
    # Offspring from 50k to 500k. Since babay crabs won't be eating much so considering upper limit 100k
    # https://www.fisheries.noaa.gov/species/red-king-crab#:~:text=Female%20red%20king%20crabs%20reproduce,settling%20on%20the%20ocean%20bottom.

    reproduction_chance = step / 365.25  
    mates = creatures['king crab'] // 2

    # Increase number of king crab as they reproduce
    offspring = int(mates * reproduction_chance * random.randint(50000, 100000))
    creatures["king crab"] = creatures["king crab"] + offspring


    # Mortality
    # King Crabs can live upto 20 - 30 Years. Let's take the average 25 Years
    # https://www.adfg.alaska.gov/index.cfm?adfg=redkingcrab.printerfriendly#:~:text=Did%20You%20Know%3F-,Male%20red%20king%20crabs%20can%20grow%20up%20to%2024lbs%20with,up%20to%2020%2D30%20years.

    # Decrease number of king crab as they die
    years = 25
    death_chance = step / (years * 365.25)
    deaths = int(creatures["king crab"] * death_chance)
    creatures["king crab"] = creatures["king crab"] - deaths

    return creatures


