# This script does 2 things: 1. Cleans up the data 2. Keeps on the required information and filters out the rest to minimize memory requirement


def Data_preprocessing(list_of_files, output_directory):

    import os
    import glob
    import csv
    import numpy
    from numpy import loadtxt
    import pandas as pd
    import json
    from pandas.io.json import json_normalize
    from urllib2 import Request, urlopen
    import re


    #FDA has individual files which are being combined here into one dataframe for further analysis

    list_of_files = glob.glob('/gpfs/fs1/data/gordanlab/vishwa/case_study/raw_data/*')  

    file_number = 0

    for filename in list_of_files:

        file_number = file_number +1

        print file_number

        with open(filename) as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(json_normalize(data['results']), orient='columns')



        # There's a lot of data that the FDA provides - here select and retain only the data you need to minimize memory requirement


        df0=df["companynumb"]
        df1= df["patient.drug"]
        df2=df["patient.reaction"]
        df3 = pd.concat([df0,df1, df2], axis = 1)


        #Data clean up - sometimes there are spaces, periods, unicode char around the drug names which should be removed cause I need to count occurences of each drug across patients

        for row in range(0, df3.shape[0]):

            drug_list=[]
            reaction_list=[]

            try:

                for each_drug in range(0, len(df3.ix[row, 1])):            

                    each_drug1 = (df3.ix[row, 1][each_drug]['medicinalproduct']).encode("ascii","replace") # remove unicode characters
                    each_drug2 = re.sub(r'\W+','', each_drug1) # remove commas and periods around words
                    drug_list.append(each_drug2.replace(" ", "")) # remove spaces around words


                for reaction in df3.ix[row, 2]:

                    reaction1 = (reaction['reactionmeddrapt']).encode("ascii","replace") # remove unicode characters
                    reaction2 = re.sub(r'\W+','', reaction1)  # remove commas and periods around words
                    reaction_list.append(reaction2.replace(" ", "")) #remove spaces around words


                df3.ix[row,1] = drug_list
                df3.ix[row,2] = reaction_list


            except (KeyError, AttributeError), e:

                print e


        if file_number == 1:

            concatenated_df = df3

        concatenated_df = (pd.concat([concatenated_df, df3], axis=0))



    #Save the clean data from the company name, medicinal product and reaction fields

    numpy.savetxt(output_directory + 'Drug_combination_assoicated_adverse_reactions.tsv', concatenated_df, delimiter="\t", fmt="%s")


    dataset = concatenated_df.ix[:,1].values.tolist()

    numpy.savetxt(output_directory + 'Drug_combination_assoicated_adverse_reactions_input_to_apriori.txt', dataset, fmt="%s")

    return concatenated_df




