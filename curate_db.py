import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict

def get_assem_comp_dict(assem_dict, assem_df):
    comp_dict = {}
    for index, row in assem_df.iterrows():
        comp_dict[row['name']] = row['total_mass_g']
    total_mass_assem = sum(comp_dict.values())
    for key, val in comp_dict.items():
        assem_dict[key] = val / total_mass_assem
    return assem_dict

def get_first_from_column(df, column_name):
    return np.array(df[column_name])[0]

df = pd.read_csv('./db/udb_1yr.dat', sep='\t')

assembly_ids = np.unique(df['assembly_id'])
n_assem = len(assembly_ids)
print('Number of assemblies')
print(n_assem)
one_percent = n_assem // 100
print('One Percent')
print(one_percent)
new_dict = OrderedDict({})
i = 0 
for assem in assembly_ids:
    assem_df = df.loc[df['assembly_id'] == assem]
    assem_dict = {}
    assem_dict['reactor_type'] = get_first_from_column(assem_df, 'reactor_type')
    assem_dict['total_mass'] = get_first_from_column(assem_df, 'initial_uranium_kg')
    assem_dict['init_enr'] = get_first_from_column(assem_df, 'initial_enrichment')
    assem_dict['bu'] = get_first_from_column(assem_df, 'discharge_burnup')
    assem_dict = get_assem_comp_dict(assem_dict, assem_df)
    new_dict[assem] = assem_dict
    if i%one_percent == 0:
        print('%i %% Done' %int(i / one_percent))
    i += 1

new_df = pd.DataFrame.from_dict(new_dict, orient='index')
new_df.to_csv('./curated.csv')
