# This script runs the apriori algorithm to get frequencies of different drug combinations

def Drug_combinations(concatenated_df, min_supp, output_directory):

    import os
    import glob
    import csv
    import numpy
    from numpy import loadtxt
    import pandas as pd


    #Select the drug related column

    dataset = concatenated_df.ix[:,1].values.tolist()

    #The input to the apriori function needs to be a one-hot encoded pandas dataframe

    from mlxtend.preprocessing import TransactionEncoder

    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Here you can pass a parameter to inidicate the miminum support you want

    from mlxtend.frequent_patterns import apriori

    results_df = apriori(df, min_support=min_supp, use_colnames=True)

    #Save the results

    numpy.savetxt(output_directory + 'Apriori_results.tsv', results_df, delimiter='\t', fmt="%s")

    return results_df
