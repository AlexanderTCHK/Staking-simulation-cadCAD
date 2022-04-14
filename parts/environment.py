import numpy as np
from .utils import *
from sys_params import pool_params
import random

# Behaviors
def define_pool_rate(params, substep, state_history, prev_state):
    """
    Increases the food supply in all sites, subject to an maximum.
    """
    print("---------------------------------Behavior define_pool_rate---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    # Get value of poll token reward 
    pool_tokens_reward = pool_params['pool_tokens_reward']
    invested_tokens = prev_state['pool']['invested_tokens']
    try:
        pool_rate = round(pool_tokens_reward / invested_tokens * 100 * 365 , 2)
    except ZeroDivisionError:
        pool_rate = 101
    #pool_rate = random.randint(0, 10)   
    return {'pool_rate': pool_rate}


# Mechanisms
def update_pool_rate(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_pool_rate---------------------------------")
    print("policy_input:", "\n", policy_input)
    pool_rate = policy_input['pool_rate']
    updated_pool = prev_state['pool'].copy()
    updated_pool['pool_rate'] = pool_rate
    print("updated_pool:", "\n", updated_pool, "\n")
    return ('pool', updated_pool)

