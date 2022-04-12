# Dependences
from parts.utils import *
from sys_params import initial_values
pool_rate = random.randint(1, 10)

## Initial state object
genesis_states = {
    'agents': generate_agents(initial_values['initial_prey_count']),
    'pool': new_pool()
}


