# from .utils import *
# import random
# from uuid import uuid4

# # Behaviors
# def define_opening_status_beh(params, substep, state_history, prev_state):
#     """
#     Defines agent open_status depending on the conditions: 
#     - if the agent has already opened a position 
#     - pool rate > N 
#     - entry quota (maximum agent/s per day) < Z
#     """
#     print("---------------------------------Behavior define_opening_status_beh---------------------------------")
#     print("Prev_state: ", "\n", prev_state, "\n")
#     pool = prev_state['pool']
#     pool_rate = pool['pool_rate']
#     total_agents = pool['total_agents']
#     max_agent = pool['max_agent']
#     delta_agent = max_agent - total_agents

#     agents = prev_state['agents']
    

#     pool_rate_bool = pool_rate > 5

#     #Agents who closed positions due to the expiration of the deposit time
#     ready_to_open_initial = {k: v for k, v in agents.items()
#                             if not v['opened_position'] and pool_rate_bool}
    
#     ready_to_open_initial_lst = list(ready_to_open_initial)
#     unique_sample_lst = random.sample(ready_to_open_initial_lst, k=delta_agent)
#     ready_to_open_final = dict(unique_sample_lst)
    
#     ready_to_open = {}
    
#     for label, value in ready_to_open_final.items():
#                 ready_to_open[label] = True
            
#                 ready_to_open[label] = False
#     print('ready_to_open', ready_to_open)
#     print("------------------------------------FINISH define_opening_status_beh-----------------------------------", "\n")
#     return {'ready_to_open': ready_to_open}