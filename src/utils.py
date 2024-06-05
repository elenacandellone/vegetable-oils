import os
import re
import tqdm
import pandas as pd
import numpy as np
import collections
import matplotlib.pyplot as plt
import seaborn as sns  
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely.geometry import box
from collections import Counter

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

import powerlaw as pwl
import gzip 
import pickle
from tqdm import tqdm

from datetime import date, datetime, timedelta
from adjustText import adjust_text

from transformers import pipeline
from transformers import AutoTokenizer, AutoConfig
import pandas as pd
from tqdm import tqdm
import os
import multiprocessing as mp
from joblib import Parallel, delayed

import warnings
warnings.simplefilter(action='ignore')


# DATA PROCESSING
def pickles_gen(path, out_path, out_path_anon = None):
    
    # store the names of files that contain certain infos (info can be 'tweets', 'users' or 'places')
    def file_names(filepath, info):
        files = []
        for dirname, _, filenames in os.walk(filepath):
            for filename in filenames:
                if re.search(info, filename):
                    files.append(os.path.join(dirname, filename))
        files = np.sort(files)  
        return files

    tweets_filenames = file_names(path,'tweets')
    users_filenames = file_names(path,'users')
    places_filenames = file_names(path,'places')
    
    
    # I want to define some functions that extract from the dataset just some precise infos, in order to avoid long executions
    def read(file):
        df = pd.read_json(file, lines = True)
        return df

    def dates(file):
        df = read(file)[['created_at']]
        df[['date','time']] = df['created_at'].apply(str).str.split(' ',expand = True)
        df[['year','month','day']] = df['date'].apply(str).str.split('-',expand = True) 
        return df

    def id(file): 
        return read(file)[['id']]

    def text(file):
        return read(file)[['text']]

    def metrics(file):
        if 'public_metrics' in read(file).columns:
            return read(file)[['public_metrics']]

    def author(file):
        return read(file)[['author_id']]
    
    def geo_read(file):
        if 'geo' in read(file).columns:
            return read(file)[['geo']]
        
    def read_all(tweets_filenames, user_filenames, places_filenames):
        d = []
        t = []
        m = []
        a = []
        auth = []
        g = []
        ids = []
        def none_f(data):
            if not data: # <-- add this bit!
                return None

        for file in tqdm.tqdm(tweets_filenames):
            d.append(dates(file))
            t.append(text(file))
            m.append(metrics(file))
            a.append(author(file))
            #g.append(geo_read(file))
            ids.append(id(file))

        for file in tqdm.tqdm(user_filenames):
            auth.append(read(file))
        
        for file in tqdm.tqdm(places_filenames):
            if geo_read(file) is not None:
                g.append(geo_read(file))

        d = pd.concat(d) if len(d) > 0 else pd.DataFrame()
        t = pd.concat(t) if len(t) > 0 else pd.DataFrame()
        m = pd.concat(m) if len(m) > 0 else pd.DataFrame()
        a = pd.concat(a) if len(a) > 0 else pd.DataFrame()
        auth = pd.concat(auth) if len(auth) > 0 else pd.DataFrame()
        g = pd.concat(g) if len(g) > 0 else pd.DataFrame()
        ids = pd.concat(ids) if len(ids) > 0 else pd.DataFrame()
        return d, t, m, a, auth, g,ids
    
    if not os.path.exists(out_path) and not os.path.exists(out_path_anon):

        tweets_dates, tweets_text, tweets_metrics, tweets_authors, users, tweets_geo, tweets_ids = read_all(tweets_filenames, users_filenames, places_filenames)

        os.makedirs(out_path, exist_ok=True)
        os.makedirs(out_path_anon, exist_ok=True)
        tweets_dates.to_pickle(out_path + "/dates.pkl.gz",compression='gzip')
        tweets_text.to_pickle(out_path + "/text.pkl.gz",compression='gzip')
        tweets_metrics.to_pickle(out_path + "/metrics.pkl.gz",compression='gzip')   
        tweets_authors.to_pickle(out_path + "/authors.pkl.gz",compression='gzip')
        users.to_pickle(out_path + "/users.pkl.gz",compression='gzip')
        tweets_geo.to_pickle(out_path + "/geo.pkl.gz",compression='gzip')
        
        # anonymized version
        tweets_ids.to_pickle(out_path + "/ids.pkl.gz",compression='gzip')
        tweets_ids.to_pickle(out_path_anon + "/ids.pkl.gz",compression='gzip')



 

# Define custom visualization parameters
text_color = "#404040"
custom_params = {
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "lines.linewidth": 3,
    "grid.color": "lightgray",
    "legend.frameon": True,
    "xtick.labelcolor": text_color,
    "ytick.labelcolor": text_color,
    "xtick.color": text_color,
    "ytick.color": text_color,
    "text.color": text_color,
    "axes.labelcolor": text_color,
    "axes.titlecolor": text_color,
    "figure.dpi": 200,
    "axes.titlelocation": "center",
    "xaxis.labellocation": "center",
    "yaxis.labellocation": "center",
    "font.size": 14 
}

sns.set_theme(context='paper', style='white', font_scale=1.1, color_codes=True, rc=custom_params)



