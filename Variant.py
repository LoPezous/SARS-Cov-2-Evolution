import pandas as pd
import numpy as np

#USER INPUT
country = input('Select Country: ')
variant = input('Select Variant: ')

#Genral data manip
df = pd.read_csv('covid-variants.csv')
df.head()
#df.dropna()
df1 = df.groupby(['location']).count()
df1 = df1.sort_values('variant')
df1

#USA Data manip
dfus = df[df['location']== country]
dfus = dfus[dfus['num_sequences'] != 0]
dfus['Year'] = dfus['date'].apply(lambda x: x[:4])
dfus['month'] = dfus['date'].apply(lambda x: x[5:7])
dfus['month-day'] = dfus['date'].apply(lambda x: x[5:])
df2 = dfus.groupby(['date']).count()
df2 = df2.sort_values('date')
df2['date']=df2.index


dfdelta = df[df['variant']==variant]
dfdeltaus = dfdelta[dfdelta['location']=='United States']
dfdeltaus = dfdeltaus.sort_values('date')


#VISUALIZATION


import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from scipy.stats import kendalltau

#Set up
fig = plt.figure(figsize = (16,11))
ax1 = plt.subplot(2, 1, 1)
ax2 = plt.subplot(2, 1 , 2, sharex = ax1)

#Plot 1 (Diversity)
x = list(df2.index)
y = df2['variant']
ax1.plot(x,y,'-', alpha = 1, color = 'g')


#Plot 2 (Delta)
x2 = dfdeltaus['date']
y2 = dfdeltaus['perc_sequences']
ax2.plot(x2,y2,'-', alpha = 1, color = 'purple')


#First occurence of Delta in samples
ax1.axvline(x=list(dfdeltaus[dfdeltaus['num_sequences'] > 10]['date'])[0], c = 'r', label = 'First '+str(variant)+ 'Variant Identified')
ax2.axvline(x=list(dfdeltaus[dfdeltaus['num_sequences'] > 10]['date'])[0], c = 'r', label = 'First '+str(variant)+' Delta Variant Identified')



ax1.set_xticks(x[::4])
ax1.set_ylim(ymin=0)
ax1.fill_between(x,y, alpha = 0.25, color = 'g')
ax2.fill_between(x2,y2,alpha = 0.25, color = 'purple')


#Correlation between Diversity and delta growth after first occurence of delta and before artifact drop in delta
data1 = df2[(df2['date'] > list(dfdeltaus[dfdeltaus['num_sequences'] > 10]['date'])[0]) & (df2['date'] < '2021-07-26')]
data1 = data1['variant']

data2 = dfdeltaus[(dfdeltaus['date'] > list(dfdeltaus[dfdeltaus['num_sequences'] > 10]['date'])[0]) & (dfdeltaus['date'] <'2021-07-26')]
data2 = data2['perc_sequences']

corr, _ = spearmanr(data1, np.log(data2))

#Text
ax2.set_xlabel('Sample dates', fontsize = 22)
ax1.set_ylabel('Variant diversity', fontsize = 22)
ax2.set_ylabel('Percentage of '+ str(variant)+' Variant in Samples', fontsize = 22)
ax1.set_title('SARS-CoV-2 Variant Diversity Compared To '+ str(variant)+ ' Variant Growth '+'('+str(country)+')', fontsize = 25)
ax1.legend(fontsize = 18)

ax2.text(0.925, 0.5, 'Correlation: '+ str(corr), fontsize=20,transform=plt.gcf().transFigure)
ax2.text(0.925, 0.475, 'P-value: '+ str(_), fontsize=20,transform=plt.gcf().transFigure)
