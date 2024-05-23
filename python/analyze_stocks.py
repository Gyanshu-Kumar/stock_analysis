import pandas as pd
import numpy as np
import math
import sys
from datetime import datetime

# Load the data
df = pd.read_csv("python/Stock market cleaned data form 2019.csv")
df.drop("Unnamed: 0", axis=1, inplace=True)
df.set_index(pd.DatetimeIndex(df.Date.values), inplace=True)
df.drop("Date", axis=1, inplace=True)

# Read year input from command line arguments
yr = int(sys.argv[1])

# Filter data based on the year input
if yr == 1:
    df = df['2023-05-22':'2024-05-22']
elif yr == 3:
    df = df['2021-05-22':'2024-05-22']

# Perform analysis
daily_simple_returns = df.pct_change(1)
annual_returns = daily_simple_returns.mean() * 252
annual_risks = daily_simple_returns.std() * math.sqrt(252)

df2 = pd.DataFrame()
df2['Expected Annual Returns'] = annual_returns
df2['Expected Annual Risks'] = annual_risks
df2['Company Symbol'] = df2.index
df2['Ratio'] = df2['Expected Annual Returns'] / df2['Expected Annual Risks']
df2.sort_values(by="Ratio", axis=0, ascending=False, inplace=True)

remove_list = []
for ticker in df2['Company Symbol'].values:
    no_better_asset = df2.loc[(df2['Expected Annual Returns'] > df2['Expected Annual Returns'][ticker]) & 
                              (df2['Expected Annual Risks'] < df2['Expected Annual Risks'][ticker])].empty
    if not no_better_asset:
        remove_list.append(ticker)

findf = df2.drop(remove_list)

output_ticker = list(findf['Company Symbol'])
output_returns = list(findf['Expected Annual Returns'] * 100)

assets = findf.index
num_assets = len(assets)
n = 1.0 / float(num_assets)
weights = [n] * num_assets
weights = np.array(weights)

output_port_ar = round(np.sum(weights * output_returns), 2)
print("Companies: ", output_ticker, "\nReturns: ", output_returns, "\nTotal Portfolio Return: ", output_port_ar)
