# invasive-species-model-CMSE202
Compartmental model of an invasive species in an ecosystem as well as results analysis for CMSE 202

Invasive Species Model

**Group Members:** <br>
Brendan Floyd<br>
Anthony Kosinski<br>
Jake Crosby<br>
Dev Jyoti Ghosh Arnab<br>
Riley LeFevre

# The Model

The **ecosystem.py** file contains the functions for each of the native species in the arctic ecosystem, as well as functions to run the ecosystem

The **invasive_species.py** file contains the functions necessary to add the invasive species to the ecosystem

## How to run the Model

In order to run the model, you must import the **ecosystem.py** file:

```python
import ecosystem
```

Once the ecosystem has been imported, there are two functions to run the ecosystem

**Resetting the Population**
```python
ecosystem.reset_pops() # Resets the population of the ecosystem to its initial state
```
<br>It's important to run this function BEFORE running the ecosystem, so that it has a fresh start with its initial population.

**Running the Ecosystem**

Once the population has been reset, the ecosystem's run function can be called.<br>
The run function has three parameters shown below.

```python
ecosystem.run(
    invasive=False, # Whether to include the invasive king crab as part of the ecosystem simulation, by default it is set to False.
    cod_birth_rate=1.5, # The birth rate of the arctic cod in the ecosystem, by default it is set to 1.5
    cod_death_rate=0.1 # The death rate of the arctic cod in the ecosystem, by default it is set to 0.1
)
```

**Obtaining Ecosystem Data**

Now that the ecosystem has been run, you can obtain the data from the ecosystem simulation by accessing the resulting dataframe in the ecosystem file.

```python
ecosystem.eco_data # a Pandas DataFrame with information about each of the native animals' metrics each day.

ecosystem.crab_data # a Pandas DataFrame with information about the king crab's metrics each day. 
                        # If invasive is set to False, this will be an empty DataFrame.
```

## Other Files

The **analysis.ipynb** is a notebook comparing the SVM and Logistic Regression models, as well as some analysis of the resulting graphs.

The **Networkx.ipynb** and **graphing_functions.py** are files that are necessary to create the weighted graph representation of the ecosystem.

The **ProjectAndDiscussionPlanning.md** is the initial planning file for the project

# Group Accomplishments

**Brendan Floyd**

Researched possible ecosystem environments to simulate and came up with the arctic ecosystem compartmental model

Created the networkx graph representions for the ecosystem as well as an animated version of the graph

**Anthony Kosinski**

Designed the ecosystem.py file

Created the analysis.ipynb notebook to run analysis on the ecosystem data

**Jake Crosby**

Created matplotlib.pyplot visualizations with the resulting ecosystem data

Primary organizer for creating slide decks

**Dev Jyoti Ghosh Arnab**

Researched possible invasive species for the model

Primary designer of the invasive_species.py file and helped plug it in to the ecosystem

**Riley LeFevre**

Made statistical insights with the resulting ecosystem data

Organizer of writing the Abstract

# Abstract

Group 10 set out to create a simulated arctic ocean ecosystem in order to answer the question: “What effect do invasive species have on existing ecosystems?” The focus was set on an arctic ecosystem environment, and specifically focused on the effect the invasive species, the king crab, had on the arctic cod population. In this way, the question was viewed through the lens of analyzing the arctic cod population. The methods used to create the ecosystem model was creating a compartmental model through a functional programming approach. Each animal had its own function, which determined its own population growth, natural population death, and how much prey it consumed for that one time step. One time step is equal to a single day in the simulation. The ```run()``` function in the ecosystem file had parameters to enable the invasive species, which would be introduced with an initial tiny population, or change the arctic cod’s birth or death rate since it was our primary focus for analysis. The visualization libraries employed were matplotlib’s pyplot library for simple population graphs, seaborn to visualize analytical results, and networkx to display how the ecosystem functions as a system. Once the ecosystem functioned consistently, three main features were focused on for the analysis on the invasive species’ effect on the ecosystem. These three features were ```cod_birth_rate```, ```cod_death_rate```, and the presence of the invasive species: the king crab. What was sought to be predicted through these features was if the arctic cod would go extinct by seeing if at any point in a 5 year time span the arctic cod population hit zero. Two models were employed in order to analyze the effect an invasive species’ presence had on the arctic cod population. The two models were: a Support Vector Machine (SVM) from the sklearn library to linearly separate the data and predict the class (the class being 1 if the arctic cod went extinct in a given simulation, and 0 if it did not), and a Logistic Regression which had the same goal as the SVM. The results of each model found that there was a significant effect on the arctic cod population with the presence of the invasive species. The way this conclusion was reached was by running five-hundred simulations of the ecosystem with randomly assigned cod birth rates and death rates without an invasive species present, then comparing the model’s linear prediction for arctic cod extinction against the linear prediction for another five-hundred simulations with the invasive species present. The significant impact of the invasive species was shown by the linear separation of simulations where the x-intercept and slope in the simulations with an invasive species was greater in comparison to the simulations lacking an invasive species. This means even with the same possible range of cod birth rates and death rates, simulations were much more likely to end in arctic cod extinction if the king crab was present. The introduction of an invasive species does not always cause an extinction of its prey, but it does increase the possibility of extinction for its prey. This can cause ecological collapse, as the arctic cod is a central part of the arctic ecosystem- without it many of its predators would have to rely more on different food sources such as krill, which may cause general population decrease. Other factors that could change drastically in the ecosystem once an invasive species is introduced could be analyzed in the future such as the population of competing predators. The results of the ecosystem model show that an invasive species impact on an existing ecosystem depends on the abundance and reproduction rate of its primary resource. If the invasive species’ primary resource is unable to reproduce fast enough to sustain a stable population, it may go extinct within that local ecosystem, thus meaning the invasive species caused major ecological damage to the ecosystem by depriving it of one of its most important resources. However, if the primary resource of the invasive species is able to survive and maintain a stable population, it may be possible for the invasive species to be incorporated as a new part of the ecosystem.

