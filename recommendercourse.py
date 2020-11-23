import warnings
import re
from PIL import Image
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

warnings.filterwarnings('ignore')
df=pd.read_csv('tag_gen.csv')

course_title=df['Title']
course_tag=pd.DataFrame(df['Tags_fin'])



#Creating binary indicators for the courses
course_tags_stack = df[df['tags_fin'] != ' '].set_index('courseId').genres.str.split(',', expand = True).stack()

course_tags_explode=pd.get_dummies(course_tag, prefix = 'list of str').groupby(level = 0).sum().reset_index()