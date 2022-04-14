import pandas as pd
from parts.utils import * 
import config
from cadCAD.engine import ExecutionMode, ExecutionContext,Executor
from cadCAD import configs

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
def run():
    '''
    Definition:
    Run simulation
    '''
    # Single
    exec_mode = ExecutionMode()
    local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)

    simulation = Executor(exec_context=local_mode_ctx, configs=config.exp.configs)
    raw_system_events, tensor_field, sessions = simulation.execute()
    # Result System Events DataFrame
    df = pd.DataFrame(raw_system_events)
    return df

#V.3
def postprocessing(df):
    '''
    Definition:
    Refine and extract metrics from the simulation
    
    Parameters:
    df: simulation dataframe
    '''
    #subset to last substep
    df = df[df['substep'] == df.substep.max()]
    
    uuid_agent = df.explode('agents').agents
    
    # Pool
    pool_rate = df['pool'].apply(pd.Series)['pool_rate']
    total_agents = df['pool'].apply(pd.Series)['total_agents']
    invested_tokens = df['pool'].apply(pd.Series)['invested_tokens']

    # Agent metrics
    tokens_income = [d.get('tokens_income') for outer_d in df['agents'] for d in outer_d.values()]
    investment_amount = [d.get('investment_amount') for outer_d in df['agents'] for d in outer_d.values()]
    deposit_days = [d.get('deposit_days') for outer_d in df['agents'] for d in outer_d.values()]
    opened_position = [d.get('opened_position') for outer_d in df['agents'] for d in outer_d.values()]
    ready_to_open = [d.get('ready_to_open') for outer_d in df['agents'] for d in outer_d.values()]

    # Create an analysis dataset
    data = (pd.DataFrame({#'run': df.run,
                          'timestep': df.timestep,
                          #'substep': df.substep,
                          #'pool': df.pool,
                          'pool_rate': pool_rate,
                          'total_agents': total_agents,
                          'invested_tokens': invested_tokens,
                          'uuid_agent': uuid_agent,
                          'deposit_days': deposit_days,
                          'opened_position': opened_position,
                          'ready_to_open': ready_to_open,
                          'investment_amount': investment_amount,
                          'tokens_income': tokens_income})       
          )
    
    return data

#V. 2
# def postprocessing(df):
#     '''
#     Definition:
#     Refine and extract metrics from the simulation
    
#     Parameters:
#     df: simulation dataframe
#     '''
#     # subset to last substep
#     # df = df[df['substep'] == df.substep.max()]
    
#     # Get the ABM results
#     agent_ds = df.agents
#     print(type(agent_ds))
#     print("agent_ds", agent_ds)

#     uuid_agent = df.explode('agents').agents
    
#     # feature3 = [d.get('days_for_waiting') for d in df.agents]
#     # feature3 = agent_ds.apply(lambda x: x.get('tokens_income'))
#     feature3 = agent_ds.map(lambda s: [agent['tokens_income'] for agent in s.values()])
#     feature3 = agent_ds.map(lambda s: agent for agent in s.items())
#     print("feature3", feature3)
   
#     ## Agent metrics
#     tokens_income = agent_ds.map(lambda s: sum([agent['tokens_income'] for agent in s.values()]))
#     counter_30_days = agent_ds.map(lambda s: sum([agent['days_for_waiting'] for agent in s.values()]))
#     opened_position = agent_ds.map(lambda s: sum([agent['opened_position'] for agent in s.values()]))

#     # Create an analysis dataset
#     data = (pd.DataFrame({'run': df.run,
#                           'feature3': feature3,
#                           'timestep': df.timestep,
#                           'substep': df.substep,
#                           'uuid_agent': uuid_agent,
#                           'pool_rate': df.pool,
#                           'counter_30_days': counter_30_days,
#                           'opened_position': opened_position,
#                           'tokens_income': tokens_income})       
#            )
    
#     return data
# df = run()
# rdf = postprocessing(df)

# print(rdf)
# Initial
# def postprocessing(df):
#     '''
#     Definition:
#     Refine and extract metrics from the simulation
    
#     Parameters:
#     df: simulation dataframe
#     '''
#     # subset to last substep
#     df = df[df['substep'] == df.substep.max()]
    
#     # Get the ABM results
#     agent_ds = df.agents
#     site_ds = df.pool
#     timesteps = df.timestep
    
#     # Get metrics

#     ## Agent quantity
#     prey_count = agent_ds.map(lambda s: sum([1 for agent in s.values()]))

#     ## Food quantity
#     pool_rate = site_ds
#     counter_30_days = agent_ds.map(lambda s: sum([agent['days_for_waiting'] for agent in s.values()]))
#     opened_position = agent_ds.map(lambda s: sum([agent['opened_position'] for agent in s.values()]))


#     ## Food metrics
#     tokens_income = agent_ds.map(lambda s: sum([agent['tokens_income'] for agent in s.values()]))

#     # Create an analysis dataset
#     data = (pd.DataFrame({'timestep': timesteps,
#                           'run': df.run,
#                           'prey_count': prey_count,
#                           'pool_rate': pool_rate,
#                           'counter_30_days': counter_30_days,
#                           'opened_position': opened_position,
#                           'tokens_income': tokens_income})       
#            )
    
#     return data