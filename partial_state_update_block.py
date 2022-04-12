from parts.environment import *
from parts.agents import *

partial_state_update_block = [
    {
        # environment.py
        'policies': {
            'pool_rate': define_pool_rate
        },
        'variables': {
            'pool': update_pool_rate
        }
    },
    {
        # agents.py
        'policies': {
            'increase_agent_age': deposit_days_countdown_beh
        },
        'variables': {
            'agents': deposit_days_countdown_mech

        }
    },
    {
        # agents.py
        'policies': {
            'opening_status_beh': define_opening_status_beh
        },
        'variables': {
            'agents': define_opening_status_mech

        }
    },
    {
        # agents.py
        'policies': {
            'opening_status_beh': open_close_position_beh
        },
        'variables': {
            'agents': open_close_position_mech,
            'pool': setting_pool_total_agents_mech

        }
    },


    {
        # agents.py
        'policies': {
            'feed_prey': setting_deposit_days_beh
        },
        'variables': {
            'agents': setting_deposit_days_mech
        }
    },
        # {
    #     # agents.py
    #     'policies': {
    #         'reproduce_agents': reproduce_agents

    #     },
    #     'variables': {
    #         'agents': agent_create

    #     }
    # },
]
