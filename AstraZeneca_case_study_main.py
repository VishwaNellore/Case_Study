# creates tiny modules of the pathway analysis scripts and merges them here - can run one script instead of many


import time
start_time = time.time()

#import functions

import os
import glob
import csv
import numpy
from numpy import loadtxt
import sys
sys.path.append('/gpfs/fs0/data/gordanlab/vishwa/case_study')


from Data_preprocessing_module import Data_preprocessing
from Drug_combinations_module import Drug_combinations
from Significant_adverse_reactions_module import Significant_adverse_reactions
from Visualize_top_drug_combinations_module import Visualize_top_drug_combinations
from Significant_adverse_reaction_for_user_defined_medicinal_product_module import Significant_adverse_reaction_for_user_defined_medicinal_product

#User input

print ('Please enter the minimum support needed for medicinal product combinations:')
min_supp = raw_input()

print ('Please enter the name of the medicinal product you are interested in:')
user_medicinal_product = raw_input()

print ('Please enter the directory where you want the results stored:')
results = raw_input()

output_directory = '/gpfs/fs1/data/gordanlab/vishwa/case_study/' + results
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


#Process the data through the following pipeline

list_of_files = glob.glob('/gpfs/fs1/data/gordanlab/vishwa/case_study/raw_data/*')

Clean_input_data = Data_preprocessing(list_of_files)

Drug_combination_frequencies = Drug_combinations(Clean_input_data, min_supp)

Visualize_the_drug_combination_data = Visualize_top_drug_combinations(Drug_combination_frequencies)

Signficant_adverse_reactions_for_drug_combination = Significant_adverse_reactions(Clean_input_data, Drug_combination_frequencies)

Significant_adverse_reaction_for_user_defined_medicinal_product = Significant_adverse_reaction_for_user_defined_medicinal_product(Signficant_adverse_reactions_for_drug_combination, user_medicinal_product)


#Results

print('The results for each of the analysis can be found here: /gpfs/fs1/data/gordanlab/vishwa/case_study/%s'%results)

print("--- %s seconds ---" % (time.time() - start_time))
