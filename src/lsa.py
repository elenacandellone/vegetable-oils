from src.utils import *
    
# preprocessing of the texts: WordNet lemmatizer is used, as well as the RegExp tokenizer


def tf_preprocess(document):
    new_stopwords = [
        'com', 'http', 'https', 'tinyurl', "t", "RT", 'co', 'bit', 'ly', 'rt',
        'via'
    ]

    # Lemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'[a-z]+')
    stpw = stopwords.words('english')

    stpw.extend(new_stopwords)
    stop_words = set(stpw)

    # Tokenization
    document = document.lower()  # Convert to lowercase
    words = tokenizer.tokenize(document)  # Tokenize
    words = [w for w in words if not w in stop_words]  # Removing stopwords

    # Lemmatization
    for pos in [wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV]:
        words = [wordnet_lemmatizer.lemmatize(x, pos) for x in words]

    return " ".join(words)

# top n keywords
def top_features(vectorizer, n):
    dictionary = vectorizer.get_feature_names_out()
    a = vectorizer.idf_
    scores = pd.DataFrame()
    scores['feature'] = dictionary
    scores['tf-idf'] = a
    scores.sort_values(by=['tf-idf'], inplace=True, ascending=True)
    best_features = scores.head(
        n)['feature'].tolist()  #list the n top features
    return best_features