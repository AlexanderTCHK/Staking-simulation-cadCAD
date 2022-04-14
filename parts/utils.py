from multiprocessing import pool
import numpy as np
import random
from typing import *
import matplotlib.pyplot as plt
import pandas as pd
import itertools

# Generate log-normal distribution value
def get_agent_invest_value():
    value = round(float(np.random.lognormal(10, .5, 1)))
    #value = random.randint(18000, 20000)
    return value

# Creating a generator
class with_current(object):

    def __init__(self, generator):
        self.__gen = generator()

    def __iter__(self):
        return self

    def __next__(self):
        self.current = next(self.__gen)
        return self.current

    def __call__(self):
        return self


def countup_gen():
    for i in itertools.count(1):
        yield i

countup_generator = countup_gen()     

# Initialization
def new_agent(age: int=0) -> dict:
    get_agent_investment_amount = get_agent_invest_value()
    agent = {'ready_to_open': False,
             'deposit_days': 0,
             'opened_position': False,
             'tokens_income': 0,
             'investment_amount': get_agent_investment_amount}
    return agent


def generate_agents(n_agents: int) -> Dict[str, dict]:  
    initial_agents = {}
    for agent in range(n_agents):
        created_agent = new_agent()
        #initial_agents[uuid.uuid4()] = created_agent
        initial_agents[f"Agent # {next(countup_generator)}"] = created_agent
    print("initial_agents", initial_agents)
    return initial_agents

# Shuffle agents 
def shuffle_agents_ordering(agents: dict):
    lst = list(agents.items())
    random.shuffle(lst)
    agents_dict = dict(lst)
    return agents_dict

# Environment
def new_pool() -> dict:
    pool_rate = 101
    total_agents = 0
    invested_tokens = 0
    pool = {'pool_rate': pool_rate,
            'total_agents': total_agents,
            'invested_tokens': invested_tokens}
    return pool

# Agents
def get_max_agents(pool_rate: int) -> int:
    if pool_rate < 5:
        max_agents = 0
    elif pool_rate < 20:
        max_agents = 1
    elif pool_rate < 50:
        max_agents = 3
    elif pool_rate < 100:
        max_agents = 6
    else:
        max_agents = 10
    return max_agents

# plotting
def aggregate_runs(df,aggregate_dimension):
    '''
    Function to aggregate the monte carlo runs along a single dimension.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.

    Example run:
    mean_df,median_df,std_df,min_df = aggregate_runs(df,'timestep')
    '''

    mean_df = df.groupby(aggregate_dimension).mean().reset_index()
    median_df = df.groupby(aggregate_dimension).median().reset_index()
    std_df = df.groupby(aggregate_dimension).std().reset_index()
    min_df = df.groupby(aggregate_dimension).min().reset_index()

    return mean_df,median_df,std_df,min_df

def monte_carlo_plot(df,aggregate_dimension,x,y,runs):
    '''
    A function that generates timeseries plot of Monte Carlo runs.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.
    x = x axis variable for plotting
    y = y axis variable for plotting
    run_count = the number of monte carlo simulations

    Example run:
    monte_carlo_plot(df,'timestep','timestep','revenue',run_count=100)
    '''
    mean_df,median_df,std_df,min_df = aggregate_runs(df,aggregate_dimension)
    plt.figure(figsize=(10,6))
    for r in range(1,runs+1):
        legend_name = 'Run ' + str(r)
        plt.plot(df[df.run==r].timestep, df[df.run==r][y], label = legend_name )
    plt.plot(mean_df[x], mean_df[y], label = 'Mean', color = 'black')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(x)
    plt.ylabel(y)
    title_text = 'Performance of ' + y + ' over ' + str(runs) + ' Monte Carlo Runs'
    plt.title(title_text)