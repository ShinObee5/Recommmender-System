import pandas as pd
import re as re
from nltk.corpus import stopwords

import warnings
from PIL import Image
from wordcloud import WordCloud
import numpy as np
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

df = pd.read_csv('App_dev_desc.csv',encoding= 'unicode_escape')
print("Original DataFrame:")
print(df)

#Remove same courses in the dataframe  
# sorting by Title
df.sort_values("Title", inplace = True) 
  
# dropping ALL duplicte values and keeps only the first occurence
df.drop_duplicates(subset ="Title", 
                     keep = 'first', inplace = True) 




def find_capital_word(str1):
    result = re.findall(r'\b[A-Z]\w+', str1)
    return result

df['tags']=df['Description'].apply(lambda cw : find_capital_word(cw))
print("\nExtract words starting with capital words from the sentences':")
print(df)

#We have Extracted all the capital words
#Removing the Stopwords
  
  
mystopwords=stopwords.words('English')+['Continue','Seperate','Use','Complete','Book','Step','REAL','ANY','Start','Real','Using','Grasp','Build','Create','The','Be','By','Learn','Guide','Manage','You','Get','Use','Make','Master','To','Understand','How','Become','Write']


#Function to extract tags from the description              
def filter(tags):
    filtered_sentence = []
    for i in tags:
        if i not in mystopwords and i not in filtered_sentence:
                filtered_sentence.append(i) 
    return filtered_sentence
     

df['Tags_fin']=df['tags'].apply(lambda cw : filter(cw))
#Creates Dummy columns so that the model can be trained with Doc2Vec 
all_tags=[]
for i in df['Tags_fin']:
    for j in i:
        all_tags.append(j)


all_tags=set(all_tags)

all_tags=list(all_tags)


def check(x,i):
    if i in x:
        return 1
    else:
        return 0


for i in all_tags:
    df[i]=df['Tags_fin'].apply(lambda x:check(x,i) )   
    
df.drop('tags', axis=1, inplace=True)
df.to_csv('tag_gen.csv')
df['tag_vector'] = df.iloc[:,12:].values.tolist()




# compute Jaccard Index to get most similar movies to target movie


pd.reset_option('display.max_colwidth')

target_course = 'Advanced Javascript'


target_tag_list = df[df.Title == target_course].Tags_fin.values[0]
course_Tags_fin_list_sim = df[['Title','HeadLine','Tags_fin']]
course_Tags_fin_list_sim['jaccard_sim'] = course_Tags_fin_list_sim.Tags_fin.map(lambda x: len(set(x).intersection(set(target_tag_list))) / len(set(x).union(set(target_tag_list))))
print(f'courses most similar to {target_course} based on Tags_fin:')
text = (course_Tags_fin_list_sim.sort_values(by = 'jaccard_sim', ascending = False).head(25)['Tags_fin'].values)
course_Tags_fin_list_sim.sort_values(by = 'jaccard_sim', ascending = False).head(10)



#Training the DOC2VEC model

stop_words = stopwords.words('english')


df['tags_str'] = [','.join(map(str, l)) for l in df['Tags_fin']]
tagsframe=df['tags_str'].copy()

# tokenize document and clean
def word_tokenize_clean(doc):
  
  # split into lower case word tokens
  tokens = word_tokenize(doc.lower())
  
  # remove tokens that are not alphabetic (including punctuation) and not a stop word
  tokens = [word for word in tokens if word.isalpha() and not word in stop_words]
  
  return tokens

# preprocess corpus of movie tags before feeding it into Doc2Vec model
course_tags_doc = [TaggedDocument(words=word_tokenize_clean(D), tags=[str(i)]) for i, D in enumerate(tagsframe)]


# instantiate Doc2Vec model

max_epochs = 50
vec_size = 20
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm=0) # paragraph vector distributed bag-of-words (PV-DBOW)
  
model.build_vocab(course_tags_doc)

# train Doc2Vec model
# stochastic (random initialization), so each run will be different unless you specify seed

print('Epoch', end = ': ')
for epoch in range(max_epochs):
  print(epoch, end = ' ')
  model.train(course_tags_doc,
              total_examples=model.corpus_count,
              epochs=model.epochs)
  # decrease the learning rate
  model.alpha -= 0.0002
  # fix the learning rate, no decay
  model.min_alpha = model.alpha

# listing space embeddings
course_tags_vectors = model.docvecs.vectors_docs

course_tags_vectors.shape



# top courses movies based on cosine similarity

course = 'Good Will Hunting'

course_index = course_tags_list[course_tags_list["Title"] ==course].index.values[0]

print(course_tags_vectors[course_index])

sims = model.docvecs.most_similar(positive = [course_index], topn = 30)

for i, j in sims:
  print(course_tags_list.loc[int(i), "Title"].strip())

# dimensionality reduction to 2D
course_tags_vectors_umap = umap.UMAP(n_neighbors = 5,
                          min_dist = 0.001,
                          metric = 'cosine').fit_transform(course_tags_vectors)

x, y = course_tags_vectors_umap.T[0], course_tags_vectors_umap.T[1]
