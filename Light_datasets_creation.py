## LIGHT DATASETS CREATION FOR DOWNLOAD


# GET STARTED

import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from plotly.subplots import make_subplots
# import plotly.express as px


# Check working directory where files will be downloaded
import os
print(os.getcwd())

# DATASETS AND TRANSFORMATION 
dfraw = pd.read_csv('eco2mix-regional-cons-def.csv', sep = ';') # raw dataset  
dfl = pd.read_csv("df_light.csv", sep = ',') # df_light for other plots
temp = pd.read_csv('temperature-quotidienne-regionale.csv', sep = ';')

dfraw2 = dfraw.copy()
dfraw2["Eolien (MW)"] = dfraw2["Eolien (MW)"].replace('ND', np.nan)
dfraw2["Eolien (MW)"] = dfraw2["Eolien (MW)"].replace('-', np.nan)
dfraw2["Eolien (MW)"] = dfraw2["Eolien (MW)"].astype(float)
dfraw2["Production"] = dfraw2["Thermique (MW)"] + dfraw2["Nucléaire (MW)"] + dfraw2["Eolien (MW)"] + dfraw2["Solaire (MW)"] + dfraw2["Hydraulique (MW)"]
dfraw2['Consumption_MWh'] = dfraw2['Consommation (MW)'] * 0.5
dfraw2['Production_MWh'] = dfraw2['Production'] * 0.5
dfraw2['Date'] = pd.to_datetime(dfraw2['Date'])
dfraw2['Month'] = dfraw2['Date'].dt.month
def month_to_season(month):
    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    else:  # For months 12, 1, 2
        return "Winter"
dfraw2['Season'] = dfraw2['Month'].apply(month_to_season)

dfl['Date'] = pd.to_datetime(dfl['Date'])
dfl['Month'] = dfl['Date'].dt.month
dfl['ConsumptionMWh'] = dfl['Consumption'] * 0.5
nuclear_free_regions = ["Bourgogne-Franche-Comte", "Bretagne","Pays de la Loire", "Provence-Alpes-Cote d'Azur", "Ile-de-France"]
dfl['NuclearNan'] = dfl['Nuclear']  # Initialize column with existing values
dfl.loc[dfl['Region'].isin(nuclear_free_regions) & (dfl['Nuclear'] == 0), 'NuclearNan'] = np.nan
dfl["ProductionMWh"] = 0.5 * dfl[
    ["NuclearNan", "Hydro", "Wind", "Solar", "Bioenergy", "Thermal"]
    ].sum(axis=1, min_count=1)


# PAGE 3 GRAPH 1
gbraw= dfraw2.groupby('Month', as_index = False)[['Consumption_MWh', 'Production_MWh']].mean().round()
p3g1 = gbraw.copy()
p3g1.to_csv("p3g1.csv", sep=',', index=False)

# PAGE 3 GRAPH 2
gb2raw= dfraw2.groupby(['Heure', 'Season'], as_index = False)[['Consumption_MWh']].mean().round()
p3g2 = gb2raw.copy()
p3g2.to_csv("p3g2.csv", sep=',', index=False)

# PAGE 3 GRAPH 3
dfl_2022 = dfl[dfl['Year'] == 2022]

# Create gbs (groupby "small") With groupby (by Month) and melt it by month/secto
gbs = dfl_2022.groupby('Month')[['Nuclear', 'Hydro', 'Wind', 'Solar', 'Bioenergy', 'Thermal'] 
                                ].sum().mul(0.5).div(1000000).round(1).reset_index()
p3g3 = gbs.copy()
p3g3.to_csv("p3g3.csv", sep=',', index=False)
p3g3.info()

# PAGE 3 GRAPH 4
gbt = dfl.groupby('Year')[ 
    ['Nuclear', 'Hydro', 'Wind', 'Solar', 'Bioenergy', 'Thermal'] 
    ].sum().mul(0.5).div(1000000).round().reset_index() # replacing * 0.5 / 1000000
p3g4 = gbt.copy()
p3g4.to_csv("p3g4.csv", sep=',', index=False)

# PAGE 3 GRAPH 5
# First approach creates a dataset of shape (4207104, 3), too big.

s1 = pd.melt(dfl, id_vars="Region", 
             value_vars=['ConsumptionMWh', 'ProductionMWh'],
             var_name='Flow', value_name='Value')
s1.info()

# But from this melted dataframe we can characterize the distribution
# of variables by region and for each flow, for future reference
def q2(x):
    return x.quantile(0.5)

def q3(x):
    return x.quantile(0.75)

s2 = s1.groupby(['Region', 'Flow'])['Value'].agg(['min', q2, 'mean', q3, 'max'])
s3 = s2.reset_index()
# s3.to_csv("p3g5.csv", sep=',', index=False)
s3.shape

# Now we proceed to data generation from s3, following a normal distribution
# but keeping extreme values (min and max)

# Function to generate synthetic data
def generate_synthetic_data(row, num_samples=18):
    mean = row['mean']
    # Approximate standard deviation using IQR
    iqr = row['q3'] - row['q2']
    std_dev = iqr / 1.349  # Approximation for normal distribution
    synthetic_data = np.random.normal(mean, std_dev, num_samples)
    return synthetic_data

# Generate synthetic data for each row
synthetic_data_list = []

for index, row in s3.iterrows():
    synthetic_values = generate_synthetic_data(row)
    # Add min and max values
    synthetic_values = np.append(synthetic_values, [row['min'], row['max']])
    for value in synthetic_values:
        synthetic_data_list.append([row['Region'], row['Flow'], value])

# Create a new DataFrame with synthetic data
s4 = pd.DataFrame(synthetic_data_list, columns=['Region', 'Flow', 'Value'])

s4.shape

# Check if the distribution matches the initial distribution closely
# by comparing s5 to s3
s5 = s4.groupby(['Region', 'Flow'])['Value'].agg(['min', q2, 'mean', q3, 'max'])
s5 = s5.reset_index()

# If so, we are confident we can export s4 as p3g5 for Streamlit
s4.to_csv("p3g5.csv", sep=',', index=False)
