from re import U
from .utils import *
import random
from uuid import uuid4
from sys_params import pool_params, agent_params

# Behaviors


def define_deposit_days(params, substep, state_history, prev_state):
    """
    Countdows deposit days for 1 per day, and add token income to agent
    """
    print("---------------------------------Behavior define_deposit_days---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    agents = prev_state['agents']

    delta_deposit_days = {}

    for agent, properties in agents.items():
        if properties['deposit_days'] > 0:
            delta_deposit_days[agent] = -1
    return {'delta_deposit_days': delta_deposit_days}


def closing_expired_position(params, substep, state_history, prev_state):
    """
    Sets agent's opene_position to False if it has expired
    """
    print("---------------------------------Behavior closing_expired_position---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    # Pool
    pool = prev_state['pool']
    pool_active_agents = 0
    pool_invested_tokens = 0

    # Agents
    opened_position = {}
    tokens_income = {}
    investment_amount = {}

    agents = prev_state['agents']
    for agent, properties in agents.items():
        opened_position_bool = properties['opened_position']
        deposit_days = properties['deposit_days']
        total_tokens_income = properties['tokens_income']
        if opened_position_bool == True and deposit_days == 0:
            # Pool
            pool_active_agents += 1
            pool_invested_tokens += properties['investment_amount']
            # Agents
            opened_position[agent] = False
            investment_amount[agent] = total_tokens_income
            #tokens_income[agent] = 0

    return {'pool_active_agents': pool_active_agents,
            'pool_invested_tokens': pool_invested_tokens,
            'opened_position': opened_position,
            'tokens_income': tokens_income,
            'investment_amount': investment_amount}


def reproduce_agents(params, substep, state_history, prev_state):
    """
    Generates an new agent through an nearby agent pair, subject to rules.
    """
    print("---------------------------------Behavior reproduce_agents---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    # Check required amount of agents
    agents = prev_state['agents']
    free_agents = 0

    for property in agents.values():
        if property['opened_position'] == False:
            free_agents += 1
        if free_agents == 10:
            break

    print("free_agents", free_agents)
    lack_of_agents = 10 - free_agents
    print("lack_of_agents", lack_of_agents)
    new_agents = {}
    for agent in range(lack_of_agents):
        get_agent_investment_amount = get_agent_invest_value()
        new_agent_properties = {'ready_to_open': False,
                                'deposit_days': 0,
                                'opened_position': False,
                                'tokens_income': 0,
                                'investment_amount': get_agent_investment_amount}
        new_agents[f"Agent # {next(countup_generator)}"] = new_agent_properties
    print("new_agents", new_agents)
    return {'agent_create': new_agents,
            'created_agents_counter': lack_of_agents}


def define_ready_to_open_status(params, substep, state_history, prev_state):
    """
    Defines agent open_status depending on the conditions: 
    - if the agent has already opened a position 
    - pool rate > N 
    - entry quota (maximum agent/s per day) < K
    """
    print("---------------------------------Behavior define_ready_to_open_status---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    # Pool
    pool = prev_state['pool']
    pool_rate = pool['pool_rate']

    # Agent
    agents = prev_state['agents']
    # Shuffle agents
    agents = shuffle_agents_ordering(agents)
    ready_to_open = {}

    if pool_rate > agent_params['min_pool_rate_for_opening_position']:
        max_agents = get_max_agents(pool_rate)
        added_agents = 0
        for agent, properties in agents.items():
            opened_position = properties['opened_position']
            added_agents_bool = added_agents < max_agents
            if not opened_position and added_agents_bool:
                ready_to_open[agent] = True
                added_agents += 1
            else:
                ready_to_open[agent] = False
    else:
        for agent, properties in agents.items():
            ready_to_open[agent] = False
    return {'ready_to_open': ready_to_open}


def opening_position(params, substep, state_history, prev_state):
    """
    Sets agent's opene_position to True if agent is ready to open a position
    """
    print("---------------------------------Behavior opening_position---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    # Pool
    pool = prev_state['pool']
    pool_active_agents = 0
    pool_invested_tokens = 0

    # Agents
    opened_position = {}
    deposit_days = {}

    agents = prev_state['agents']
    for agent, properties in agents.items():
        ready_to_open_bool = properties['ready_to_open']
        if ready_to_open_bool == True:
            # Pool
            pool_active_agents += 1
            pool_invested_tokens += properties['investment_amount']
            # Agents
            opened_position[agent] = True
            deposit_days[agent] = agent_params['deposit_days']
    return {'pool_active_agents': pool_active_agents,
            'pool_invested_tokens': pool_invested_tokens,
            'opened_position': opened_position,
            'deposit_days': deposit_days}


def define_agent_tokens_income(params, substep, state_history, prev_state):
    """
    Add token income to agent if he has opened position
    """
    print("---------------------------------Behavior define_agent_tokens_income---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    agents = prev_state['agents']
    invested_tokens = prev_state['pool']['invested_tokens']
    pool_tokens_reward = pool_params['pool_tokens_reward']

    try:
        token_per_invested_token = pool_tokens_reward / invested_tokens
    except ZeroDivisionError:
        token_per_invested_token = 0

    agent_tokens_income = {}

    for agent, properties in agents.items():
        if properties['opened_position'] == True:
            agent_tokens_income[agent] = token_per_invested_token * \
                properties['investment_amount']
    return {'agent_tokens_income': agent_tokens_income}

# Mechanisms
def update_deposit_days(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_deposit_days---------------------------------")
    print("policy_input:", "\n", policy_input)
    updated_agents = prev_state['agents'].copy()
    for agent, value in policy_input['delta_deposit_days'].items():
        updated_agents[agent]['deposit_days'] += value
    print("updated_pool:", "\n", updated_agents, "\n")
    return ('agents', updated_agents)


def update_agent_closing_expired_position(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_agent_closing_expired_position---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    for label, value in policy_input['opened_position'].items():
        updated_agents[label]['opened_position'] = value
    for label, value in policy_input['tokens_income'].items():
        updated_agents[label]['tokens_income'] = value
    for label, value in policy_input['investment_amount'].items():
        updated_agents[label]['investment_amount'] += value
    print("updated_agents:", "\n", updated_agents, "\n")
    return ('agents', updated_agents)


def update_pool_closing_expired_position(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_pool_closing_expired_position---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_pool = prev_state['pool'].copy()
    updated_pool['pool_active_agents'] -= policy_input['pool_active_agents']
    updated_pool['invested_tokens'] -= policy_input['pool_invested_tokens']
    print("updated_pool:", "\n", updated_pool, "\n")
    return ('pool', updated_pool)


def agent_create(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism agent_create---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()

    for label, properties in policy_input['agent_create'].items():
        updated_agents[label] = properties
    print("updated_pool:", "\n", updated_agents, "\n")
    return ('agents', updated_agents)

def update_created_agents_value(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_created_agents_value---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_val = prev_state['created_agents']
    updated_val += policy_input['created_agents_counter']
    print("updated_val:", "\n", updated_val, "\n")
    return ('created_agents', updated_val)

def update_ready_to_open_status(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_ready_to_open_status---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    for label, value in policy_input['ready_to_open'].items():
        updated_agents[label]['ready_to_open'] = value
    print("updated_pool:", "\n", updated_agents, "\n")
    return ('agents', updated_agents)


def update_agent_opening_position(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_agent_opening_position---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    for label, value in policy_input['opened_position'].items():
        updated_agents[label]['opened_position'] = value
    for label, value in policy_input['deposit_days'].items():
        updated_agents[label]['deposit_days'] = value
    print("updated_agents:", "\n", updated_agents, "\n")
    return ('agents', updated_agents)


def update_pool_opening_position(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_pool_opening_position---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_pool = prev_state['pool'].copy()
    updated_pool['pool_active_agents'] += policy_input['pool_active_agents']
    updated_pool['invested_tokens'] += policy_input['pool_invested_tokens']
    print("updated_pool:", "\n", updated_pool, "\n")
    return ('pool', updated_pool)


def update_agent_tokens_income(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism update_agent_tokens_income---------------------------------")
    print("policy_input:", "\n", policy_input)
    updated_agents = prev_state['agents'].copy()
    for agent, value in policy_input['agent_tokens_income'].items():
        updated_agents[agent]['tokens_income'] += value
    print("updated_pool:", "\n", updated_agents, "\n")
    return ('agents', updated_agents)
