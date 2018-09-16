# This script plots the drug combinations most commonly used by patients in FAERS


def Visualize_top_drug_combinations(counts_data, output_directory):

    import csv
    import numpy
    from numpy import loadtxt
    import pandas
    import ast
    import matplotlib 
    matplotlib.use('agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(color_codes=True)

    #Importing the data


    counts_data = pandas.read_csv('/gpfs/fs1/data/gordanlab/vishwa/case_study/Apriori_results_10.tsv', delimiter='\t')
    counts_data = counts_data.head(10)

    #Create a plot

    sns_plot = sns.barplot(y=counts_data.ix[:,0]*number_of_patients, x=counts_data.ix[:,1], data=counts_data, color='salmon')

    #Set the parameters for the plot

    sns_plot.set_title('Drug Combinations most frequently seen in the FAERS database')
    sns_plot.set(xlabel='Drug Combination', ylabel='Number of patients taking this drug combination')
    sns.set(font_scale=4)
    fig = sns_plot.get_legend()
    fig = sns_plot.get_figure()

    #Save the plot

    fig.savefig(output_directory + 'Frequent_drug_combinations.png', transparent='True')


