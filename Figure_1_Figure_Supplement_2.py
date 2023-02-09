#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:30:52 2022

@author: scottrk
"""

import os
import Figure_1_figure_supplement_1
from GlobalVars_ import tissue_type, tissue_type_long, old_mouse_id, tissue_type_abbrev, \
                        color_cycle
from compile_data import calc_depth_plot_data

if __name__ == "__main__":

    fig, axs = Figure_1_figure_supplement_1.setup_figure()

    masked_coords = Figure_1_figure_supplement_1.get_masked_coords("data/misc_items/mm10_mtDNA_masked_regions.bed")

    for index, tissue in enumerate(tissue_type[:-1]):

        if not os.path.isfile("data/imported_data/Figure_1_figure_supplement_2_" + tissue_type_abbrev[index] + "_depth_data.csv"):
            if not os.path.isdir("data/stats/"):
                os.mkdir("data/stats/")

            depth_df = calc_depth_plot_data(old_mouse_id,
                                            tissue,
                                            "data/imported_data/Figure_1_figure_supplement_2_" + tissue_type_abbrev[index] + "_depth_data.csv")
        else:
            depth_df = calc_depth_plot_data(old_mouse_id, tissue)

        Figure_1_figure_supplement_1.depth_plot(depth_df['Mean'], depth_df['Std_dev_upper'],
                                                depth_df['Std_dev_lower'], masked_coords,
                                                axs[index], color_cycle[index])

        axs[index].set_ylim((0, 28000))

        axs[index].set_title(tissue_type_long[index], fontsize=12)

        axs[index].tick_params(labelsize=10)

    axs[7].set_xlabel('Genome Position', size=12)
    fig.suptitle("Old Mouse Depth", y=0.93, fontsize=12)

    if not os.path.isdir("figures"):
        os.mkdir("figures/")

    fig.savefig('figures/Figure_1_Figure_Supplement_2.png', dpi=600, facecolor='white', 
                bbox_inches='tight')
    fig.savefig('figures/Figure_1_Figure_Supplement_2.pdf', dpi=600, facecolor='white', 
                bbox_inches='tight')
