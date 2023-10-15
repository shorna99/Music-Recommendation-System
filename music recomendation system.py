# -*- coding: utf-8 -*-
"""spotify.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1be5YYu0t3M1yS2GasIVwarNszvQbYiLj
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
import plotly.express as px
from sklearn.manifold import TSNE
from wordcloud import WordCloud

df = pd.read_csv("/content/data.csv", sep=",")
genres_df = pd.read_csv('/content/data_by_genres.csv', sep=",")
year_df = pd.read_csv('/content/data_by_year.csv', sep=",")
artist_df = pd.read_csv('/content/data_by_artist.csv', sep=",")

df.info()

df.head()

df['decade'] = df['year'].apply(lambda year : f'{(year//10)*10}s' )

decades = df.decade.value_counts()
decades.plot(kind='barh')
plt.xlabel('Decade')
plt.ylabel('Count')
plt.title('Distribution of Music')

song_popularity = df[['name', 'popularity']].set_index('name').to_dict()['popularity']
song_popularity = sorted(song_popularity.items(), key=lambda x: x[1], reverse=True)

wordcloud = WordCloud(width=1600, height=800, max_words=50, background_color='white').generate_from_frequencies(dict(song_popularity))
plt.figure(figsize=(12,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('50 most popular songs 1920-2020', fontsize=20)
plt.show()

kmeans_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('kmeans', KMeans(n_clusters=15))
])

song_kmeans_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('kmeans', KMeans(n_clusters=30))
])

X = genres_df.select_dtypes(np.number)
kmeans_pipeline.fit(X)
genres_df['Cluster'] = kmeans_pipeline.predict(X)

pca_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('PCA', PCA(n_components = 2))
])

genre_visual = pca_pipeline.fit_transform(X)

projection = pd.DataFrame(columns=['x', 'y'], data=genre_visual)
projection['title'] = genres_df.genres
projection['cluster'] = genres_df.Cluster

fig = px.scatter(
    projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title'],title='Clusters of Genres')
fig.show()

tsne_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('tsne', TSNE(n_components=2, verbose=False))
])

genre_embedding = tsne_pipeline.fit_transform(X)
projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding)

projection['title'] = genres_df.genres
projection['cluster'] = genres_df.Cluster

fig = px.scatter(
    projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title'])
fig.show()

from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')  # You can choose a different strategy
X = imputer.fit_transform(X)

X = df.select_dtypes(np.number)

song_kmeans_pipeline.fit(X)
song_clusters = song_kmeans_pipeline.predict(X)
df['Cluster'] = song_clusters

song_embedding = pca_pipeline.fit_transform(X)
projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)

projection['title'] = df.name
projection['cluster'] = df.Cluster

fig = px.scatter(
    projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title'])
fig.show()



