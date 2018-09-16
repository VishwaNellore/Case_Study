#This script takes the drug combinations found through the apriori algorithm and calculates if any of the adverse reactions are significant using the fishers exact test and PRR

def Data_preprocessing(dataset, drug_combination_list):

    import os
    import glob
    import csv
    import numpy
    from numpy import loadtxt
    import pandas as pd
    import ast
    import scipy
    import scipy.stats as stats



    #Here we map each drug combination with all the associated adverse reactions
    #Create a dictionary with the keys as drug combinations and the values as adverse reactions
    #Use frozenset as the key because doesn't depend on the order of the elements, only on elements themselves


    adverse_reaction_dict = {}

    for i in range(0, len(dataset)):

        try:

            current_key = ast.literal_eval(dataset.ix[i, 1])
            current_key_frozen = frozenset(tuple(current_key))

            if current_key_frozen not in adverse_reaction_dict:
                adverse_reaction_dict[current_key_frozen] = []

            if current_key_frozen in adverse_reaction_dict:
                adverse_reaction_dict[current_key_frozen] = adverse_reaction_dict[current_key_frozen] +ast.literal_eval(dataset.ix[i, 2])


        except (SyntaxError, TypeError), e:

            print e, current_key,  current_key_frozen




    #Need to convert the dictionary to list to save

    adverse_reaction_list = numpy.zeros((len(adverse_reaction_dict), 3), dtype = object)
    final_result = numpy.zeros((1, 6), dtype = object)
    final_result[:] = ['Medicinal_product_combination', 'Adverse event', 'Odds ratio', 'Fishers_p_value', 'Fishers_corrected_p_value', 'PRR']
    fishers = numpy.zeros((1, 6), dtype = object)

    row = 0

    total_number_of_adverse_reactions = 0

    for key, value in adverse_reaction_dict.iteritems():


        adverse_reaction_list[row, 0] = str(key).split('[')[1]
        adverse_reaction_list[row,1] = value
        adverse_reaction_list[row,2] = len(adverse_reaction_dict[key])

        total_number_of_adverse_reactions = total_number_of_adverse_reactions + int(adverse_reaction_list[row,2])

        row = row + 1



    #For each adverse reaction - drug combination, create a contingency table

    drug_combination_list = pd.read_csv('/gpfs/fs1/data/gordanlab/vishwa/case_study/Apriori_results_10.tsv', delimiter=' ', names=["Frequency", "Drug_combination"], dtype=object)

    for entry in range(0, len(drug_combination_list)):
        drug_combination_list.ix[entry, 1] = drug_combination_list.ix[entry, 1].split('[')[1]



    for drug_combination in range(0,len(adverse_reaction_list)):

        if adverse_reaction_list[drug_combination, 2] in drug_combination_list.ix[:,1]:

            for adv_reac in numpy.unique(adverse_reaction_list[drug_combination, 1]):

                n1 = adverse_reaction_list[drug_combination, 1].count(adv_reac)

                total_adv_reac = 0

                for each_row in range(0, len(adverse_reaction_list)):

                    for each_value in adverse_reaction_list[each_row,1]:

                        if each_value == adv_reac:

                            total_adv_reac = total_adv_reac+1


                n2 = total_adv_reac - n1

                n3 = len(adverse_reaction_list[drug_combination, 1]) - n1

                n4 = total_number_of_adverse_reactions - n1 -n2 - n3


            #Calculate significance using Fishers exact test and PRR

            try:

                oddsratio, pvalue = stats.fisher_exact([[n1, n2], [n3, n4]], 'greater')

                fishers[0, 0] = adverse_reaction_list[drug_combination, 0]
                fishers[0, 1] = adv_reac
                fishers[0, 2] = oddsratio
                fishers[0, 3] = pvalue
                fishers[0, 5] = (n1/(n1+n3))/(n2/(n2+n4)) #Calculate PRR                                                                                                                  
                final_result.append(fishers)

            except (OverflowError, ZeroDivisionError), e:
                print e



    # Correct for Multiple Hypothesis Testing cause the more drug combinations we test, the more significant results we may get just by chance


    from mht import correct_pvalues_for_multiple_testing

    fishers_corrected = correct_pvalues_for_multiple_testing(final_result[1:,3], correction_type = "Benjamini-Hochberg")
    final_result[1:,4] = fishers_corrected
    final_result = sorted(final_result,key=lambda x: x[4])

    #Save and return results

    numpy.savetxt('/gpfs/fs1/data/gordanlab/vishwa/case_study/Number_of_adverse_events_for_drug_combination.tsv', final_result, delimiter='\t', fmt="%s")

    return fishers
