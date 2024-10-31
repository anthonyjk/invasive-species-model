# Ecosystem model
import numpy as np

creatures = {"baleen whale":25,
             "krill":1000000,
             "leopard seal": 25,
             "arctic cod": 10000,
             "penguin": 750,
             "orca":10,
             "plankton": np.inf # Infinite Plankton
}

def krill():
    # https://marinesanctuary.org/blog/krill-behavior-diet-lifecycle/
    pass
    # increase pop number by random amount from source

def arctic_cod():
    #
    pass
    # increase pop number by random amount
    # decrease krill pop by related number
    # ex: growth of 25, kills 10,000 krill

def leopard_seal():
    pass

def penguin():
    pass

def orca():
    pass

def baleen_whale():
    pass
