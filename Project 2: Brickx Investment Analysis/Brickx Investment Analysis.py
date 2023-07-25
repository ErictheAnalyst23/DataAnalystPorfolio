#!/usr/bin/env python
# coding: utf-8

# # Project - Brickx Investment Analysis
# 
# This project will explore the KPIs of an investment portfolio from the Brickx investment platform. The analysis will investigate the relevant time series of dividend distributed from each property and whether there is a correlation between the average brick (unit) price of a property and the dividend paid to investors each month. This will be accomplished through analysing data from data collected from the Brickx website which has been cleaned through SQLite.
# 
# Through this project, the following questions will be explored:
# 
# + What is the distribution of investments into each state for this portfolio?
# + How much rental income was collected from each property?
# + Which property has provided the highest rental yield?
# + Is there a correlation between average brick (unit) price and the average monthly dividend?
# 
# **Data sources**
# 
# - Brickx data: https://www.brickx.com/properties
# 
# - SQLite data cleaning (GitHub): https://github.com/ErictheAnalyst23/DataAnalystPorfolio/blob/main/SQL%20Queries/SP1%3A%20Brickx_SQL_Analysis

# ## Importing Modules into Jupyter Notebook

# To investigate the listed questions for this project, the following modules were imported.

# In[192]:


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime


# ## Information about the datasets used
# 
# Two datasets were used for this project. The original data was cleaned using SQLite. 
# 
# The first `csv` file 'BrickxKPIs.csv' provides key metrics about each property in the portfolio, whilst the second file 'BrickxGrowth.csv' provides information regarding any changes over a period of time.  
# 
# ### Loading the dataset into notebook
# 
# 'BrickxKPIs.csv' will be read into a DataFrame called df_KPI, followed by a quick inspection of the DataFrame using .head() to check its contents.
# 

# In[193]:


df_KPI = pd.read_csv('BrickxKPIs.csv')


# In[194]:


df_KPI.head()


# ## Check number of rows and columns in 'BrickxKPI' dataset
# 
# There is a total of 13 columns in this dataset. 
# 
# Column names:
# - Property
# - state
# - suburb
# - zipcode
# - total_brickx_purchased
# - total_purchase_price
# - avg_purchase_price
# - total_dividend
# - total_fees
# - Total_investment
# - total_sell_price
# - total_bricks_sold
# - avg_sell_price

# In[195]:


print(df_KPI.info(verbose=True))


# #### Notes:
# 
# Zipcode and total_bricks_purchased are floats in this dataset. These will be converted into integers as they only exist as whole numbers.

# ## Check for any null values
# 
# It can be observed that the columns 'total_sell_price', 'total_bricks_sold' and 'avg_sell_price' have null values which is understandable as these properties have not been sold from the portfolio. However, let's check if there are null values in any other columns.
# 
# #### Quick summary
# 
# It can be observed there are two properties with 'null' values, they also don't have a relevant state, suburb or zipcode attached to it. This would imply these are not part of the portfolio and can be removed from the dataset.
# 
# #### Change to column names into lower cases
# 
# Columns 'Property' and 'Total_investment' both start with upper case whilst the rest start with a lower case. For simplity of later analysis, the two columns will be converted into lower cases.

# In[196]:


df_KPI.isnull().sum()


# In[197]:


df_KPI = df_KPI.rename(columns = str.lower) 

df_KPI


# # Drop Null Values and Convert Data Types
# 
# Any rows with null values for the 'property' column is not apart of the investment portfolio and should therefore be dropped from the analysis.

# In[198]:


df_KPI = df_KPI.dropna(subset =['property'])

df_KPI


# In[199]:


df_KPI['zipcode'] = df_KPI['zipcode'].astype(int)

df_KPI['total_bricks_purchased'] = df_KPI['total_bricks_purchased'].astype(int)


# In[200]:


df_KPI.info()


# 

# # Exploration of the dataset
# 
# ### What are the unique properties in this investment portfolio?
# 

# In[201]:


unique_property = df_KPI.property.unique()

print('The names of the properties invested in this portfolio is ' + str(unique_property) + '.')

num_unique_property = df_KPI.property.nunique()

print('The number of unique properties in this portfolio is: ' + str(num_unique_property) + '.')


# In[202]:


# Summary statistics of the dataset

df_KPI.describe()


# ### First Question: What is the distribution of investments for each state?
# 
# Why this question was asked:
# - To examine the level of diversification in this portfolio and to ensure its not heavily focused on a particular state; a similar step will be taken when looking at individual properties.
# 
# How will this be completed:
# - Using the groupby statement and adding the total purchase prices together.   

# In[203]:


amount_invested_prop = df_KPI.groupby('property').total_purchase_price.max().sort_values(ascending=False).reset_index()

amount_invested_prop.columns = ['property', 'total_purchase_price']

print(amount_invested_prop)


#        - ENMO1 had the largest investment of $1455.
#        
#        - BANO1 had the smallest investment of $69.

# In[204]:


plt.figure(figsize = (15,8))
sns.barplot(x = 'total_purchase_price', y = 'property', data = amount_invested_prop)
plt.title('Total investment in each property on Brickx')
plt.xlabel('Total investment ($AUD)')
plt.show()
plt.close()


# In[205]:


amount_invested_state = df_KPI.groupby('state').total_purchase_price.sum().sort_values(ascending=False).reset_index()

amount_invested_state.columns = ['state', 'total_purchase_price']

print(amount_invested_state)


# In[206]:


plt.figure(figsize = (15,8))
sns.barplot(x = 'total_purchase_price', y = 'state', data = amount_invested_state)
plt.title('Total investment in each state on Brickx')
plt.xlabel('Total investment ($AUD)')
plt.show()
plt.clf()


# ### Summary for question
# 
# The results show the portfolio has heavily favoured properties in New South Wales with Victoria having less than half the amount (NSW: $5708 |VIC: $2444). Overall, this portfolio is overly exposed in New South Wales with very little exposure placed into properties in South and Western Australia. Therefore, it might be worthwhile to look at diversifying into properties outside of New South Wales.
# 
# Let's also explore whether a particular property within each state is properly diversified.

# In[207]:


propertystate = df_KPI.groupby(['state', 'property']).total_purchase_price.sum().unstack()

propertystate


# In[208]:


ax = propertystate.plot(kind = 'bar', figsize = (8,6), stacked = True)

ax.set_xlabel('States in Australia')

ax.set_ylabel('Cost of Investment ($AUD)')

plt.show()


# ### Summary for question
# 
# Whilst the portfolio has a larger exposure in New South Wales and Victoria, the stacked bar chart also shows us within these states the portfolio is much more diversified. 
# 

# # Second Question: Which property provided the highest rental income?

# In[209]:


dividend_prop = df_KPI.groupby('property').total_dividend.max().sort_values(ascending=False).reset_index()

dividend_prop.columns = ['property', 'total_dividend_collected']

print(dividend_prop)


# In[210]:


plt.figure(figsize = (15,8))
sns.barplot(x = 'total_dividend_collected', y = 'property', data = dividend_prop)
plt.title('Total dividend collected per property')
plt.xlabel('Total dividend collected ($AUD)')
plt.show()
plt.clf()


# ### Summary for question
# 
# CLN02 provided the highest amount of dividend for this portfolio even though it was ranked 10th in total amount invested. This would indicate that the property had a high rental yield and/or held within the portfolio longer compared to the other properties. Hence, in the next section, we will explore the average rental yield of each property to see which would be the best for distribution purposes. 

# # Loading the dataset into notebook (BrickxGrowth)
# 
# 'BrickxGrowth.csv' will be read into a DataFrame called df_Growth, followed by a quick inspection of the DataFrame using .head() to check its contents.

# In[211]:


df_Growth = pd.read_csv('BrickxGrowth.csv')

df_Growth.head()


# ## Check for any null values
# 
# It can be observed that the columns 'total_sell_price', 'total_bricks_sold' and 'avg_sell_price' have null values which is understandable as these properties have not been sold from the portfolio. However, let's check if there are null values in any other columns.
# 
# 

# In[212]:


df_Growth.isnull().sum()


# In[213]:


df_Growth = df_Growth.rename(columns = str.lower) 

df_Growth


# ## Explore for any changes in monthly dividend from each property

# In[214]:


# Boxplot to examine the dividend per individual brick
plt.figure(figsize = (10, 10))
sns.boxplot(x = "property", y = 'dividend_per_brick_month', data = df_Growth)
plt.ylabel('Dividend per brick for each month ($AUD)')
plt.show()


# #### NOTE
# 
# The box plot shows there have been some fluctuations in the dividend distributed by each property. Some potential reasons for this is likely due repair works for the individual property and the increases in cash rate. 

# In[215]:


fig = plt.figure(figsize = (10, 10))
# The gca() method returns the axes of the current plot, or creates a new one if none exists.
ax = fig.gca()
df_Growth.hist(ax = ax)


# #### To track the changes in dividend per brick (unit) for each month it was held
# 
# A line plot is used to track changes in monthly dividend for an individual unit for each property. The values of months held corresponds to the length of time the property was in the investor's portfolio (It does not reflect the same period of time). 
# 
# It can be seen there have been fluctuations in the dividend of each property. Certain properties that were held during the RBA's cash rate increases has seen the 'geared' properties reduce its rental income per unit.

# In[216]:


graph_dividend = sns.FacetGrid(df_Growth, col="property", col_wrap=3,
                      hue = "property", sharey = False, sharex = False)

graph_dividend = (graph_dividend.map(sns.lineplot, 'month_held', 'dividend_per_brick_month')
         .add_legend()
         .set_axis_labels("month_held","dividend_per_brick_month"));


# #### NOTE
# 
# The line plot demonstrates that TAR01 (29 months) was held the longest followed by CLN02 (28 months) which may explain why CLN02 has provided the highest amount of dividend for this portfolio. 
# 
# The graphs also indicate that majority of the distributions have remained relatively unchanged; however, some properties have also seen significant decreases in the rental income provided.

# # Find the changes in rental yield of the portfolio
# 
# When it comes to property investment, monetary gain can be achieved through either capital gains or rental income.

# In[217]:


df_merged = df_KPI.merge(df_Growth, on='property', how='inner')

df_merged


# In[218]:


df_merged['annual_dividend'] = round(((df_merged['dividend_per_brick_month']/df_merged['avg_purchase_price'])*12)*100, 2)

df_merged['month_year'] = pd.to_datetime(df_merged['date']).dt.strftime('%m-%Y')

df_merged


# In[219]:


r_yield = df_merged.groupby(['state', 'property']).annual_dividend.mean().sort_values(ascending=False).reset_index()

r_yield


# In[220]:


r_yield = df_merged.groupby(['state', 'property']).annual_dividend.mean().sort_values(ascending=False).reset_index()

r_yield

# Bar plot to show the average annual dividend yield

plt.figure(figsize = (10,8))
sns.barplot(data = r_yield, x = 'property', y = 'annual_dividend', hue = 'state')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
plt.title('Average Rental Yield of Each Property by State')
plt.ylabel('Rental Yield (%)')
plt.xlabel('State')
plt.xticks(rotation=45, horizontalalignment = 'right')
plt.legend(title='State')
plt.show()
plt.clf()


# In[221]:


# Bar plot to show the average rental yield of properties in each state

plt.figure(figsize = (10,8))
sns.barplot(data = r_yield, x = 'state', y = 'annual_dividend')
plt.title('Average Rental Yield from Properties in Each State')
plt.ylabel('Rental Yield (%)')
plt.xlabel('State')
plt.show()
plt.clf()


# ### Summary for Question: Finding the top 5 properties in providing rental yield
# 
# Through the groupby statement, we calculated the property with the highest rental yields from this Brickx portfolio. A bar chart was also used to visualise which states in Australia were these high rental yield properties from and found the properties in Victoria provided the highest average rental yield. 
# 
# The top 5 highest rental yield properties in this portfolio is:
# + CLN02 (Victoria) - 6.18%
# + TAR01 (Victoria) - 5.87%
# + SOM01 (Victoria) - 4.74%
# + NML01 (Victoria) - 3.90%
# + ENM01 (New South Wales) - 2.97%
# 

# #### Tracking the changes in rental yield of the portfolio

# In[222]:


yield_change = df_merged[['property','state', 'date','annual_dividend','running_total_dividend', 'month_year']]

yield_change

yield_change.groupby('date')

yield_change


# In[223]:


# Convert 'date' column to datetime data type
yield_change['date'] = pd.to_datetime(yield_change['date'])

plt.figure(figsize=(15,10))

sns.lineplot(x = yield_change['date'], y = yield_change['annual_dividend'])
plt.title('Changes in rental yield')
plt.ylabel('Dividend Collected ($AUD)')
plt.xticks(rotation = 45, horizontalalignment = 'right')
plt.show()
plt.clf()


# In[224]:


# Convert 'date' column to datetime data type
df_merged['date'] = pd.to_datetime(df_merged['date'])

# Changes in rental yield for each state

sns.lineplot(data = df_merged, x = 'date', y = 'annual_dividend', hue = 'state')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
plt.title('Changes in rental yield')
plt.ylabel('Rental yield (%)')
plt.xticks(rotation = 45, horizontalalignment = 'right')
plt.show()
plt.clf()


# In[225]:


plt.figure(figsize=(15,10))

graph_dividend = sns.FacetGrid(df_merged, col="state", col_wrap=2,
                               hue="state", sharey=False, sharex=False)

graph_dividend = (graph_dividend.map(sns.lineplot, 'date', 'annual_dividend')
                  .set_axis_labels("Date", "Dividend Yield%")).set_xticklabels(rotation=45, horizontalalignment='right')
plt.tight_layout()
plt.show()


# In[226]:


plt.figure(figsize=(15,10))

graph_dividend1 = sns.FacetGrid(df_merged, col="property", col_wrap=3,
                               hue="state", sharey=False, sharex=False)

graph_dividend1 = (graph_dividend1.map(sns.lineplot, 'date', 'annual_dividend')
                  .set_axis_labels("Date", "Dividend Yield%")).set_xticklabels(rotation=45, horizontalalignment='right')
plt.tight_layout()
plt.show()


# ### Additional Notes for Question: Finding the top 5 properties in providing rental yield
# 
# The current portfolio contains only properties in Victoria. Whilst the average rental yield for the Victorian based properties are higher than the other states, since April-2022, the line plots shows a continual decrease in the rental yield as a consequence of the interest rate hikes. This negatively affects the investor's returns as majority of these properties are negatively geared and with interest rate hikes, the distribution to the investor is reduce as the repayment of interest has increased.

# ## Fourth Question: Is there a correlation between average unit price and dividend distribution?
# 
# Purpose:
# To identify whether purchasing higher priced units will lead to greater dividend distribution. This will be achievd by graphing scatterplots of the two variables.
# 
# A scatter plot was used for this section to identify whether there was a correlation between the average unit purchase price of each property and the monthly dividend from that property.

# In[227]:


corr_d_p = df_merged.groupby(['property', 'state', 'avg_purchase_price']).dividend_per_brick_month.mean().sort_values(ascending=False).reset_index()

corr_d_p.columns = ['property', 'state', 'avg_purchase_price', 'dividend_per_brick_month']

print(corr_d_p)


# In[228]:


plt.figure(figsize = (10, 10))
# Plot a scatterplot of total_purchases vs. income
sns.scatterplot(x = 'avg_purchase_price', y = 'dividend_per_brick_month', data = corr_d_p, hue = corr_d_p['state'])
plt.title("The correlation between unit price and rental income")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
plt.xlabel('Average Unit Purchase Price ($AUD)')
plt.ylabel('Average Brick Dividend per Month ($AUD)')
plt.show()
plt.close()


# In[229]:


plt.figure()

# Plot a regression line on the scatter plot.
sns.regplot(x = corr_d_p['avg_purchase_price'], y = corr_d_p['dividend_per_brick_month'], scatter_kws ={'color':'black'}, line_kws={'color':'red'})
plt.title("The correlation between unit price and rental income")
plt.xlabel('Average Unit Purchase Price ($AUD)')
plt.ylabel('Average Brick Dividend per Month ($AUD)')
plt.show()


# In[230]:


graph = sns.FacetGrid(corr_d_p, col="state", col_wrap=3,
                      hue = "state", sharey = False, sharex = False)
graph = (graph.map(sns.scatterplot,"avg_purchase_price", "dividend_per_brick_month")
         .add_legend()
         .set_axis_labels("Average Purchase Price ($AUD)", "Dividend per Brick ($AUD)"));


# In[231]:


graph = sns.FacetGrid(corr_d_p, col="state", col_wrap=3, hue="state", sharey=False, sharex=False)

graph = (graph.map(sns.regplot, "avg_purchase_price", "dividend_per_brick_month")
         .add_legend()
         .set_axis_labels("Average Purchase Price ($AUD)", "Dividend per Brick ($AUD)"))

plt.show()


# The overall relationship between `average unit purchase price` and `average brick dividend per month` is weak but linear. 

# # Conclusion
# 
# + What is the distribution of investments into each state for this portfolio?
# This portfolio has invested in four states, New South Wales, Victoria, South Australia and Western Australia. Whilst majority of the money was invested in properties in New South Wales, the portfolio did diversify this investment into multiple properties.
# 
# + How much rental income was collected from each property?
# The top 3 properties that has provided the highest rental income CLN02, ENM01 and TAR01.
# 
# + Which property has provided the highest rental yield?
# The top 3 properties in terms of rental yield were all from Victoria in the following order CLN02 (6.18%), TAR01 (5.87%) and SOM01(4.74%).
# 
# 
# + Is there a correlation between average brick (unit) price and the average monthly dividend?
# There was a weak correlation between the average brick price and the average monthly dividend provided by this brick unit.

# From this point, I went to tableau to further visualise this data:
# 
# https://public.tableau.com/app/profile/eric.wong8260/viz/BrickxAnalysis/Dashboard1

# In[ ]:




