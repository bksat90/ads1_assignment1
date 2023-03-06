# -*- coding: utf-8 -*-
"""
Created on Sun Feb  26 12:10:55 2023

@author: bksat
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def UniqueColVariables(dframe):
    """
    Function UniqueColVariables return the unique numpy array of elements for
    Country and Year Columns in the dataframe
    """
    countries = dframe['Country'].unique()
    years = dframe['Year'].unique()
    return countries, years


def KeepG7(df):
    """
    Function KeepG7 filters G7 countries in the input data frame
    """
    G7 = ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom',
          'United States']
    df = df[df['Country'].isin(G7)]
    return df


def PreprocessDF(df):
    """
    Function PreprocessDF keeps data from 1985 from which user can see
    significant growth in the data, sorts the data, and renames the columns
    """
    df = df[df_rawmob['Year'] >= 1985]
    df = df.rename(columns={'Country or Area': 'Country'})

    df = df.sort_values(['Country', 'Year'],
                        ascending=[True, True])
    df = df.reset_index(drop=True)

    return df


def TransformDF(df):
    """
    Function TransformDF transforms the data from the given format to
    a dataframe format which can be easily used to plot the graphs.
    """
    countries, years = UniqueColVariables(df)
    # countries list
    cntrs_list = countries.tolist()
    # number of years in total
    no_of_yrs = len(years)
    # creating an empty dataframe with columns as year
    mod_df = pd.DataFrame(columns=years)
    
    # country counter is used to maitain which country is used in the process
    cnt_ind = 0
    # iterate through every row in the dataframe
    for ind in range(0, len(df), no_of_yrs):
        # temporary dictionary with only country
        temp = {'Country': cntrs_list[cnt_ind]}
        
        # create elements for number of users for each year in the dict temp
        for j in range(no_of_yrs):
            temp[df.loc[ind+j, 'Year']] = df.loc[ind+j, 'Value']
        
        # append the dict temp to modified dictionary
        mod_df = mod_df.append(temp, ignore_index=True)
        cnt_ind += 1

    return mod_df


# main code
# file read from the csv file and ignore footer notes values in last 228 rows
filename = "UNdata_Export_20230305_151939997.csv"
df_rawmob = pd.read_csv(filename, skipfooter=228)
 
# Process dataframe for G7 seven countries
df_processed = PreprocessDF(df_rawmob)
df_G7 = KeepG7(df_processed)
df_G7 = df_G7.reset_index(drop=True) #reset the indices

# Transform the dataframe so that graphs can be plotted
df_mob = TransformDF(df_G7)
df_mob = df_mob.set_index('Country')
df_mob = df_mob.T
df_mob = df_mob.rename(columns={'Country': 'Year'})
df_mob = df_mob.reset_index()


# Keep the values for the year 2014 for all countries
df_2014 = df_processed[df_processed['Year'] == 2014]
df_2014 = df_2014.reset_index(drop=True)

# Keep the values for the year 1994 for all countries
df_1994 = df_processed[df_processed['Year'] == 1994]
df_1994 = df_1994.reset_index(drop=True)

# line graph
plt.figure(figsize=(10, 8))
# line growth of four countries will be displayed
plt.plot(df_mob["index"], df_mob["Canada"], label="Canada")
plt.plot(df_mob["index"], df_mob["United Kingdom"], label="United Kingdom")
plt.plot(df_mob["index"], df_mob["Japan"], label="Japan")
plt.plot(df_mob["index"], df_mob["United States"], label="United States")
# set labels, title, legend and diaplay them
plt.xlabel("Year")
plt.ylabel("Mobile Subscriptions in 100 millions")
plt.legend()
plt.title("Mobile User Subscriptions in Canada, UK, US, and Japan",
          fontweight="bold")
plt.savefig("Mobile_Users_Line.png")
plt.show()


# Keep records of the G7 countries for year 2014
df_G7_2014 = df_mob.iloc[-1].to_numpy()
df_G7_2014 = np.delete(df_G7_2014, 0)

# bar graph
plt.figure(figsize=(10, 8))
names = ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'UK', 'US']
plt.bar(names, df_G7_2014)
plt.xticks(rotation=45)
# set labels, title, legend and diaplay them
plt.xlabel("Countries")
plt.ylabel("Mobile Subscriptions in 100 millions")
plt.title("Mobile User Subscriptions in G7 Countries in 2014",
          fontweight="bold")
plt.savefig("Mobile_Users_Bar.png")
plt.show()



# bins for histopgram
bin_values = [250000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000,
              3500000, 4000000, 4500000]

# Histogram
plt.figure(figsize=(15, 10))
# first subplot for year 1994
plt.subplot(1, 2, 1)
plt.hist(df_1994["Value"], label="1994", bins=bin_values, density=True)
plt.xticks(bin_values)
plt.xlabel("Users in Million")
plt.legend()
plt.title("Distribution of Mobile Subscriptions in 1994 by Countries")
# second subplot for year 2014
plt.subplot(1, 2, 2)
plt.hist(df_2014["Value"], label="2014", bins=bin_values, density=True)
plt.xticks(bin_values)
plt.xlabel("Users in Million")
plt.legend()
plt.title("Distribution of Mobile Subscriptions in 2014 by Countries")
plt.savefig("1994_2014_Histogram.png")
plt.show()