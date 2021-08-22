df = pd.read_csv('covid-variants.csv')
df.head()
df.dropna()

country = input('Select Country: ')

dfus = df[df['location']== country]
dfus = dfus[dfus['num_sequences'] != 0]
dfus['Year'] = dfus['date'].apply(lambda x: x[:4])
dfus['month'] = dfus['date'].apply(lambda x: x[5:7])
dfus['month-day'] = dfus['date'].apply(lambda x: x[5:])

dfvar = dfus
liste_var = []

for x in dfvar['variant']:
    if x not in liste_var:
        liste_var.append(x)
d = {}
for i in liste_var:
    d["{}".format(i)] = df[df['variant']==str(i)]
    
plt.figure(figsize = (10,10))
axe = plt.subplot()
for x in liste_var:
    
    axe.plot(d[x].sort_values('date')['date'],d[x].sort_values('date')['num_sequences'],'o-', label = str(x))
plt.legend()
plt.title('Evolution of SARS-CoV-2 Variants')
plt.xticks(rotation=89)
