# Dependences
import pandas as pd
import numpy as np
from tabulate import tabulate

# Experiments
import run
from parts.utils import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 175)

df = run.run()
rdf = run.postprocessing(df)

print(rdf)

# print(tabulate(rdf, headers='keys', tablefmt='grid', showindex="always"))

fig, ax = plt.subplots(3, 1)
ax[0].plot(rdf["timestep"], rdf["pool_rate"])
ax[0].set_xlabel("Timestep")
ax[0].set_ylabel("Pool rate")

ax[1].plot(rdf["timestep"], rdf["pool_active_agents"], color="orange")
ax[1].set_xlabel("Timestep")
ax[1].set_ylabel("Pool active agents")

ax[2].plot(rdf["timestep"], rdf["created_agents"], color="green")
ax[2].set_xlabel("Timestep")
ax[2].set_ylabel("Created agents")


tick_spacing = 10
fig, ax = plt.subplots()
ax.plot(rdf["timestep"], rdf["pool_rate"])
ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax.set_xlabel("Timestep")
ax.set_ylabel("Pool rate")
plt.grid()


fig, ax = plt.subplots()
ax.plot(rdf["timestep"], rdf["pool_active_agents"], color="orange")
ax.set_xlabel("Timestep")
ax.set_ylabel("Pool active agents")

fig, ax = plt.subplots()
ax.plot(rdf["uuid_agent"], rdf["tokens_income"], color="red")
ax.set_xlabel("agents")
ax.set_ylabel("tokens_income")

fig, ax = plt.subplots()
ax.plot(rdf["tokens_income"], rdf["uuid_agent"], color="red")
ax.set_xlabel("tokens_income")
ax.set_ylabel("agents")

# set the spacing between subplots
plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.7)
plt.show()
