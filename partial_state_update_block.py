from parts.environment import *
from parts.agents import *

partial_state_update_block = [
    {
        # environment.py
        'policies': {
            'pool': define_pool_rate
        },
        'variables': {
            'pool': update_pool_rate
        }
    },
    {
        # agents.py
        'policies': {
            'agents': define_deposit_days
        },
        'variables': {
            'agents': update_deposit_days

        }
    },
    {
        # agents.py 
        'policies': {
            'agents': closing_expired_position
        },
        'variables': {
            'agents': update_agent_closing_expired_position,
            'pool': update_pool_closing_expired_position
        }
    },
    {
        # agents.py 
        'policies': {
            'agents': reproduce_agents
        },
        'variables': {
            'agents': agent_create
        }
    },
    {
        # agents.py 
        'policies': {
            'agents': define_ready_to_open_status
        },
        'variables': {
            'agents': update_ready_to_open_status,
        }
    },
    {
        # agents.py 
        'policies': {
            'agents': opening_position
        },
        'variables': {
            'agents': update_agent_opening_position,
            'pool': update_pool_opening_position
        }
    },
    {
        # agents.py 
        'policies': {
            'agents': define_agent_tokens_income
        },
        'variables': {
            'agents': update_agent_tokens_income,
        }
    },
]
