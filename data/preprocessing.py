import pandas as pd
import geopandas as gpd
import os

current_wd = os.getcwd()
print(f'Working directory is now: {current_wd}.')

health_data = pd.read_csv(r'data\health_outcomes.csv')
states_gdf = gpd.read_file(r'data\states\tl_2024_us_state.shp')

northeast = ['CT','ME','MA','NH','RI','VT','NJ','NY','PA']
midwest = ['IL','IN','MI','OH','WI','IA','KS','MN','MO','NE','ND','SD']
south = ['DE','FL','GA','MD','NC','SC','VA','DC','WV','AL','KY','MS','TN','AR','LA','OK','TX']
west = ['AZ','CO','ID','MT','NV','NM','UT','WY','AK','CA','HI','OR','WA']

def assign_region(state):
    if state in northeast:
        return 1
    elif state in midwest:
        return 2
    elif state in south:
        return 3
    elif state in west:
        return 4

states_gdf['REGION'] = states_gdf['STUSPS'].apply(assign_region)

# Dissolve to regions
regions_gdf = states_gdf.dissolve(by="REGION").reset_index()

# Aggregate IPUMS data
region_summary = (
    health_data
    .groupby("REGION")
    .agg(uninsured_rate=("HINOTCOV", "mean"))
    .reset_index()
)

# Merge
health_gdf = regions_gdf.merge(region_summary, on="REGION")

# Plot
health_gdf.plot(column="uninsured_rate", legend=True)

import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
import shapely

print('Geometry type: ', health_gdf.geom_type)
print("\n Coordinate reference system:", health_gdf.crs)