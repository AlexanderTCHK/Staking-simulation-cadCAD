# Dependences
import pandas as pd
import numpy as np
from tabulate import tabulate

# Experiments
import run
from parts.utils import *
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 175)

df = run.run()
rdf = run.postprocessing(df)

print(rdf)
# print(tabulate(rdf, headers='keys', tablefmt='grid', showindex="always"))

