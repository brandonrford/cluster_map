# -*- coding: utf-8 -*-
"""complex_modeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/153plmt7zbnmKLLN6jMIBNIe53HOTAzGJ
"""
"""Google Colab
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
"""

import numpy as np 

# data processing
import pandas as pd 

# data visualization
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import style

# Import Kmodes
"""!pip install kmodes"""
from kmodes.kmodes import KModes

#load in data
master_df = pd.read_csv("data/religion_data_master.csv")

#Clustering

society_name = master_df['society_name']
data = master_df[["society_name","roleofgods_label","religion_label","domesticated_label","animalshunted_label"]]
data = data.set_index('society_name')
data

# Elbow Curve (optimal K value)
cost = []
K = range(1,5)
for num_clusters in list(K):
    kmode = KModes(n_clusters=num_clusters, init = "random", n_init = 5, verbose=1)
    kmode.fit_predict(data)
    cost.append(kmode.cost_)
    
plt.plot(K, cost, 'bx-')
plt.xlabel('No. of clusters')
plt.ylabel('Cost')
plt.title('Elbow Method For Optimal k')
plt.show()

# Building the model with 3 clusters
kmode = KModes(n_clusters=3, init = "random", n_init = 5, verbose=1)
clusters = kmode.fit_predict(data)
clusters

data

data.insert(0, "Cluster", clusters, True)
data.to_csv("data/clusters.csv")

data

data = pd.read_csv("data/clusters_mapdata.csv")

data

pivottable = pd.pivot_table(data, index=['domesticated_label','animalshunted_label','roleofgods_label','religion_label'],aggfunc=np.mean)
pivottable.to_csv('clusters_pivottable.csv')

pivottable

for col in data:
    plt.subplots(figsize = (15,5))
    sns.countplot(x='Cluster',hue=col, data = data)
    plt.show()