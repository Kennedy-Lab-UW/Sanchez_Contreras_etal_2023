#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 09:12:42 2023

@author: scottrk
"""
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from GlobalVars_ import tissue_type, tissue_type_abbrev, old_mouse_id
                        

def countmut_import(countmut_file, tissue):
    countmut_data = pd.read_csv(countmut_file, skiprows=11)

    countmut_data = countmut_data.query("REGION=='OVERALL' & \
                                        MUTATION_TYPE in ['C>A', 'G>T']")
    countmut_data.reset_index(inplace=True)                                    
    countmut_data = pd.concat([countmut_data, pd.DataFrame({"Tissue":[tissue, tissue]})], axis=1)
    #numerator = countmut_data['COUNT'].sum()
    #denominator = countmut_data['DENOMINATOR'].sum()
    
    return countmut_data #pd.DataFrame({"Tissue":tissue, "Frequency":numerator/denominator}, index=[0])

def setup_figure():
    fig, ax = plt.subplots(nrows=1, ncols=1)
    return fig, ax


df_list = []

for mouse in old_mouse_id:

    for tissue in tissue_type:
        sample = glob.glob('data/mutation_freq_files/sscs/' + mouse + '_' + 
                           tissue + '_*')
        if len(sample) == 1:
            df_list.append(countmut_import(sample[0], tissue))
        
final_df = pd.concat(df_list)
#final_df = final_df.reindex()

fig, ax = setup_figure()

ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

sns.barplot(x='Tissue', y='FREQUENCY', data=final_df, hue="MUTATION_TYPE",
            errorbar='sd',edgecolor='black', errwidth=1,
            capsize=0.1, errcolor='black', ax=ax)

sns.stripplot(x="Tissue", y="FREQUENCY", data=final_df, hue="MUTATION_TYPE",
              ax=ax, alpha=0.7, dodge=True, color='black', legend=False)

sns.despine(ax=ax)

ax.set_xticklabels(tissue_type_abbrev[:-1])
fig.canvas.draw()
plt.setp(ax.get_yaxis().get_offset_text(), visible=False)
order_of_mag = ax.get_yaxis().get_offset_text().get_text()[-2:]
string = "Mutation Frequency ($\mathregular{10^{" + str(order_of_mag) + "}}$)"
ax.set_ylabel(string, fontsize=12)
ax.legend(ncols=2, frameon=False, title=None, framealpha=1, loc='upper left')

fig.savefig('figures/Figure_3_Figure_Supplement_2.png', dpi=600, facecolor='white')
fig.savefig('figures/Figure_3_Figure_Supplement_2.pdf', dpi=600, facecolor='white')