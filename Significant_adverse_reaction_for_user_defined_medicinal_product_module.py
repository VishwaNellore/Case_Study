#This script takes the user defined medicinal product and generates a file with the associalted medicinal product combinations and the associated Fisher's exact test p-value corrected for multiple hypothesis testing as well as the PRR 

def Significant_adverse_reaction_for_user_defined_medicinal_product(drug_combination_list, user_medicinal_product, output_directory):

    import csv
    import numpy
    from numpy import loadtxt
    import pandas as pd


    results_df = numpy.zeros((1, 4), dtype = object)
    results_df[:] = ['Medicinal_product_combination', 'Adverse event', 'Fishers_corrected_p_value', 'PRR']
    temp_results_df = numpy.zeros((1, 4), dtype = object)


    #Here for every combination in which the medicinal product specified by the user appears, the adverse event is printed

    for entry in range(0, len(drug_combination_list)):

        if user_medicinal_product in drug_combination_list.ix[entry, 0]:

            temp_results_df[0,0] = drug_combination_list.ix[entry, 0]
            temp_results_df[0,1] = drug_combination_list.ix[entry, 1]
            temp_results_df[0,2] = drug_combination_list.ix[entry, 4]
            temp_results_df[0,3] = drug_combination_list.ix[entry, 5]

            results_df.append(temp_df)


    #Sort the results to show the lowest pvalue by fishers first

    results_df = sorted(results_df,key=lambda x: x[2])

    numpy.savetxt(output_directory + 'Adverse_events_for_medicinal_product_%s.tsv'%user_medicinal_product, results_df, delimiter='\t', fmt="%s")

    return results_df
