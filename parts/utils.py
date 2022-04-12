import numpy as np
import random
from typing import *
import uuid
import matplotlib.pyplot as plt
import pandas as pd

# Initialization
def new_agent(age: int=0) -> dict:
    deposit_days = 0
    opened_position = False
    agent = {'ready_to_open': True,
             'deposit_days': deposit_days,
             'opened_position': opened_position,
             'tokens_income': 0,
             'investment_amount': 100,
             'age':age}
    return agent


def generate_agents(n_agents: int) -> Dict[str, dict]:  
    initial_agents = {}
    for agent in range(n_agents):
        created_agent = new_agent()
        #initial_agents[uuid.uuid4()] = created_agent
        initial_agents[f"Agent # {agent}"] = created_agent
    print("initial_agents", initial_agents)
    return initial_agents


# Environment
print('ffffffffffffffffff')
def new_pool() -> dict:
    pool_rate = 101
    print('1')
    total_agents = 0
    print('2')
    invested_tokens = 0
    print('3')
    pool = {'pool_rate': pool_rate,
            'total_agents': total_agents,
            'invested_tokens': invested_tokens}
    print(pool)
    return pool

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