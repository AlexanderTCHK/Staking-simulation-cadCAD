from .utils import *
import random
from uuid import uuid4

# Behaviors
def define_opening_status_beh(params, substep, state_history, prev_state):
    """
    Defines agent open_status depending on the conditions: 
    - if the agent has already opened a position 
    - pool rate > N 
    - entry quota (maximum agent/s per day) < Z
    """
    print("---------------------------------Behavior define_opening_status_beh---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    pool = prev_state['pool']
    pool_rate = pool['pool_rate']
    total_agents_per_day = 1

    added_agents = 0
    
    agents = prev_state['agents']
      
    ready_to_open = {}

    pool_rate_bool = pool_rate > 5
    

    for label, value in agents.items():
            opened_position = value['opened_position']
            added_agents_bool = added_agents < total_agents_per_day
            if not opened_position and pool_rate_bool and added_agents_bool:
                ready_to_open[label] = True
                added_agents += 1
            else:
                ready_to_open[label] = False
    print('ready_to_open', ready_to_open)
    return {'ready_to_open': ready_to_open}

def open_close_position_beh(params, substep, state_history, prev_state):
    """
    Sets agent's opene_position to True if opening_status is True
    """
    print("---------------------------------Behavior open_close_position_beh---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    agents = prev_state['agents']

    open_position = {}

    pool_investment_delta = 0
    pool_total_agents = 0

    for label, value in agents.items():
            ready_to_open_bool = value['ready_to_open']
            investment_amount = value['investment_amount']
            if ready_to_open_bool:
                open_position[label] = True
                pool_total_agents += 1
                pool_investment_delta += investment_amount


    print('open_position', open_position)
    return {'open_position': open_position,
            'pool_total_agents': pool_total_agents,
            'pool_investment_delta': pool_investment_delta}

def setting_deposit_days_beh(params, substep, state_history, prev_state):
    """
    Feeds the hungry prey with all food located on its site.
    """
    print("---------------------------------Behavior setting_deposit_days_beh---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    pool = prev_state['pool']
    pool_rate = pool['pool_rate']
    agents = prev_state['agents']

    deposit_days= {}
    

    for label, value in agents.items():
            ready_to_open = value['ready_to_open']
            if ready_to_open:
                deposit_days[label] = 3
                

    print("deposit_days", deposit_days)
    return {'setting_deposit_days': deposit_days}

def deposit_days_countdown_beh(params, substep, state_history, prev_state):
    print("---------------------------------Behavior deposit_days_countdown_beh---------------------------------")
    print("Prev_state: ", "\n", prev_state, "\n")
    agents = prev_state['agents']
    invested_tokens = prev_state['pool']['invested_tokens']
    token_per_investment = 1000 / invested_tokens

    delta_deposit_days = {}
    open_position = {}
    tokens_income = {}
    investment_amount = {}

    for key, value in agents.items():
        if value['deposit_days'] == 1:
            open_position[key] = False
            delta_deposit_days[key] = -1
            investment_amount[key] = value['tokens_income']
            tokens_income[key] = 0       
        elif value['deposit_days'] > 1:
            delta_deposit_days[key] = -1
            tokens_income[key] = token_per_investment * value['investment_amount']
    return {'delta_deposit_days': delta_deposit_days,
            'open_position': open_position,
            'tokens_income': tokens_income,
            'investment_amount': investment_amount}

# def agent_olden(params, substep, state_history, prev_state):
#     print("************************Behaviors************************")
#     agents = prev_state['agents']
#     print("digest_and_olden/prev_state['agents']", agents)
#     delta_food = {}
#     for key, value in agents.items():
#         if value['days_for_waiting'] > 0:
#             delta_food[key] = -1
#         else:
#             delta_food[key] = 0
    
#     delta_age = {agent: +1 for agent in agents.keys()}
#     print("agent_delta_food", delta_food, "\n")
#     return {'agent_delta_food': delta_food,
#             'agent_delta_age': delta_age}

# def reproduce_agents(params, substep, state_history, prev_state):
#     """
#     Generates an new agent through an nearby agent pair, subject to rules.
#     Not done.
#     """
#     agents = prev_state['agents']
#     sites = prev_state['sites']
#     food_threshold = params['reproduction_food_threshold']
#     reproduction_food = params['reproduction_food']
#     reproduction_probability = params['reproduction_probability']
#     busy_locations = [agent['location'] for agent in agents.values()]
#     already_reproduced = []
#     new_agents = {}
#     agent_delta_food = {}
#     for agent_type in set(agent['type'] for agent in agents.values()):
#         # Only reproduce agents of the same type
#         specific_agents = {label: agent for label, agent in agents.items()
#                            if agent['type'] == agent_type}
#         for agent_label, agent_properties in specific_agents.items():
#             location = agent_properties['location']
#             if (agent_properties['food'] < food_threshold or agent_label in already_reproduced):
#                 continue
#             kind_neighbors = nearby_agents(location, specific_agents)
#             available_partners = [label for label, agent in kind_neighbors.items()
#                                   if agent['food'] >= food_threshold
#                                   and label not in already_reproduced]
#             reproduction_location = get_free_location(location, sites, busy_locations)

#             if reproduction_location is not False and len(available_partners) > 0:
#                 reproduction_partner_label = random.choice(available_partners)
#                 reproduction_partner = agents[reproduction_partner_label]
#                 already_reproduced += [agent_label, reproduction_partner_label]

#                 agent_delta_food[agent_label] = -1.0 * reproduction_food
#                 agent_delta_food[reproduction_partner_label] = -1.0 * reproduction_food
#                 new_agent_properties = {'type': agent_type,
#                                         'location': reproduction_location,
#                                         'food': 2.0 * reproduction_food,
#                                         'age': 0}
#                 new_agents[uuid4()] = new_agent_properties
#                 busy_locations.append(reproduction_location)
#     return {'agent_delta_food': agent_delta_food,'agent_create': new_agents}


# Mechanisms
def define_opening_status_mech(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism define_opening_status_mech---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    for label, value in policy_input['ready_to_open'].items():
        updated_agents[label]['ready_to_open'] = value
    print('updated_agents', updated_agents)
    return ('agents', updated_agents)

def open_close_position_mech(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism open_close_position_mech---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    print("*" * 10)
    print(policy_input)
    for label, value in policy_input['open_position'].items():
        updated_agents[label]['opened_position'] = value
    print('updated_agents', updated_agents)
    return ('agents', updated_agents)

def setting_deposit_days_mech(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism setting_deposit_days_mech---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    for label, val in policy_input['setting_deposit_days'].items():
        updated_agents[label]['deposit_days'] += val
    print("updated_agents", updated_agents)
    return ('agents', updated_agents)

def setting_pool_total_agents_mech(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism setting_pool_total_agents_mech---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    
    updated_pool = prev_state['pool'].copy()
    updated_pool['total_agents'] += policy_input['pool_total_agents']
    updated_pool['invested_tokens'] += policy_input['pool_investment_delta']
    
    print("updated_pool", updated_pool)
    return ('pool', updated_pool)

def deposit_days_countdown_mech(params, substep, state_history, prev_state, policy_input):
    print("---------------------------------Mechanism deposit_days_countdown_mech---------------------------------")
    print("Policy_input: ", "\n", policy_input, "\n")
    updated_agents = prev_state['agents'].copy()
    for agent, val in policy_input['delta_deposit_days'].items():
        updated_agents[agent]['deposit_days'] += val

    for agent, val in policy_input['open_position'].items():
        updated_agents[agent]['opened_position'] = False
    
    for agent, val in policy_input['tokens_income'].items():
        updated_agents[agent]['tokens_income'] = val

    for agent, val in policy_input['investment_amount'].items():
        updated_agents[agent]['investment_amount'] = val

    print("updated_agents", updated_agents)
    return ('agents', updated_agents)

# def agent_age(params, substep, state_history, prev_state, policy_input):
#     print("************************Mechanisms************************")
#     print("agent_food_age/policy_input", policy_input)
#     delta_day_by_agent = policy_input['agent_delta_day']
#     delta_age_by_agent = policy_input['agent_delta_age']
#     updated_agents = prev_state['agents'].copy()

#     for agent, delta_day in delta_day_by_agent.items():
#         updated_agents[agent]['days_for_waiting'] += delta_day
#     for agent, delta_age in delta_age_by_agent.items():
#         updated_agents[agent]['age'] += delta_age
#     print("updated_agents", updated_agents, "\n")
#     return ('agents', updated_agents)

# def agent_create(params, substep, state_history, prev_state, policy_input):
#     updated_agents = prev_state['agents'].copy()
#     for label, food in policy_input['agent_delta_food'].items():
#         updated_agents[label]['food'] += food
#     for label, properties in policy_input['agent_create'].items():
#         updated_agents[label] = properties
#     return ('agents', updated_agents)


# def site_food(params, substep, state_history, prev_state, policy_input):
#     updated_pool = prev_state['pool']
#     for label, delta_food in policy_input['site_delta_food'].items():
#         updated_pool[label] += delta_food
#     return ('pool', updated_pool)



