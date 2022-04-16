# Dependences
from parts.utils import *
from sys_params import agent_params
pool_rate = random.randint(1, 10)

## Initial state object
genesis_states = {
    'agents': generate_agents(agent_params['initial_agent_count']),
    'pool': new_pool(),
    'created_agents': agent_params['initial_agent_count']
}


