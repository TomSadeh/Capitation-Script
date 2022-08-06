"""
Script by: Tom Sadeh.

A script which downloads population data from stats.oecd,
and calculates standard population for all oecd countries and others with 3 different capitation formulae:
    1. Standard Israel capitation formula.
    2. Israel capitation formula with long-term care.
    3. EU27 capitation formula with no long-term care.   
    
The capitation formulae can be adjusted in the added csv file named "cap.csv".
The date range can be change as desired here in the script.

YOU HAVE TO ENTER A PATH FOR THE CAPITATION FILE, else the script won't work.

Sources:
    Israel standard capitaion formula:
        https://www.btl.gov.il/Mediniyut/Situation/haveruth1/2021/Documents/capitatia_122021.doc
        
        It has 0-1 age group, so I averaged it with the 1-4 age-group, with a weighted average, where the weights are 1 and 3 respectively.
    EU capitation and Israel capitation with long-term care formulae are from Ahdut, Politzer and Ben-Nun here:
        https://tinyurl.com/5drzpuvm
        
    Both docs are in the github repository as well.
If you have any questions please send an email to dtsj89@gmail.com or tsadeh@kohelet.org.il.
"""

# Importing the required libraries.

import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import numpy as np


# Creating an empty DataFrame to contain the results.
results = {'Men' : pd.DataFrame(),
          'Women' : pd.DataFrame(),
          'LTC' : pd.DataFrame(),
          'EU27' : pd.DataFrame()}

# The path for the capitation csv file. Enter your path here.
path = r'C:\Users\User\OneDrive\Documents\Work\Health\Capitation'
# Defining export path. Enter yours here.
export_path = r'C:\Users\User\OneDrive\Documents\Work\Health\Capitation'

# Defining start and end time as datetime objects for the datareader. Adjust the year according to your taste.
start_time = dt.datetime(1960, 1, 1)
end_time = dt.datetime(2022, 1, 1)

# Downloading and reading the population data from stats.oecd.
pop = web.DataReader('HISTPOP', 'oecd', start_time, end_time)
pop = pop.transpose()

# Renaming the columns from datetime objects to the year only. 
pop.columns = pop.columns.year

# Creating an empty DataFrame for combining the 5-year age groups to 10-year age groups, and creating manualy the first one as it needs to be 5-year age group as in the capitation formulae.
new_pop = pd.DataFrame()
new_pop = pd.concat([new_pop, pop.xs('0 to 4', level = 'Age', drop_level = False)])

# Creating a list with the different age groups.
age_list = pop.index.get_level_values('Age').unique()

# The main loop that combines the age groups. Starts from the third group (the first is "Total" and the second is "0 to 4" which we saved earlier), and finishing in the 18th group, as the last one will be added manualy.
for index in np.arange(2,18, step = 2):
    # Creating to cross-sections, one with the first indexed 5-year age group and a second with the next one. Moving the 'Age' index to the columns for later use.
    first_pop = pop.xs(age_list[index], level = 'Age', drop_level = False).reset_index(level = 'Age')
    second_pop = pop.xs(age_list[index + 1], level = 'Age', drop_level = False).reset_index(level = 'Age')
    
    # Combining both cross-sections to a temporary DataFrame.
    temp = (first_pop + second_pop)
    
    # Using the 'Age' column, renaming the 'age' index to a 10-year age group. If it's the first one, using only the first letter of the age group name ('4'), else, using two letters ('15', '25', ect.), and using the last two ('14', '24', ect.).
    if index == 2:
        temp['Age'] = age_list[index][0] + ' to ' + age_list[index + 1][-2:]
    else:
        temp['Age'] = age_list[index][0:2] + ' to ' + age_list[index + 1][-2:] 
    temp.set_index('Age', append = True, inplace = True)
    
    # Combining the temporary DataFrame with the 10-year age groups DataFrame. 
    new_pop = pd.concat([new_pop, temp])    

# Manualy creating the last age group, as it's 85 and above and not a 5 or 10 years age group.
pop_85 = pop.xs('85 and over', level = 'Age', drop_level = False).copy()
new_pop = pd.concat([new_pop, pop_85])

# Creating a dictionary of cross-sections of Men, Women, and two Totals for the Long-Term Care (LCT), and for EU27 capitation formulae.
pop_dict = {'Men' : new_pop.xs('Men', level = 'Sex'),
            'Women' : new_pop.xs('Women', level = 'Sex'),
            'LTC' : new_pop.xs('Total', level = 'Sex'),
            'EU27' : new_pop.xs('Total', level = 'Sex')}

# Loading the capitation csv file.
capitation = pd.read_csv(path + '\cap.csv', index_col = 'Age')

# Creating a dictionary of empty DataFrames to contain the calculations of the standard population per sex and per age group.
capped = {'Men' : pd.DataFrame(),
          'Women' : pd.DataFrame(),
          'LTC' : pd.DataFrame(),
          'EU27' : pd.DataFrame()}

# The main loop that calculates the standard population. Iterating each key in the capped dictionary.
for cap in capped.keys():
    # Merging the relevant capitation formula with the relevant population DataFrame, and then multiplying the DataFrame by this column.
    
    temp = pd.merge(pop_dict[cap], capitation[cap], left_index = True, right_index = True)
    capped[cap] = temp.iloc[:, :-1].multiply(temp.iloc[:, -1], axis = 0, level = ['Country', 'Age'])
    
    # Summing the age groups in each country to get the standard population and saving it to the results DataFrame.
    results[cap] = capped[cap].groupby('Country').agg(np.sum)

# Combining both men and women in the standard Israeli capitation formula.    
results['Israel Cap'] = results['Men'] + results['Women']

# Deleting the irelevant DataFrames.
del results['Men'], results['Women']

# Exporting the results with a for loop for each item in the results dictionary.
for key in results.keys():
    results[key].to_csv(export_path + '\\' + key + '.csv')
