from src.utils import *

def XLM(text_path, model_path, preds_out, scores_out):

    # preprocessing -> removes users and urls
    def preprocess(corpus):
        outcorpus = []
        for text in corpus:
            new_text = []
            for t in text.split(" "):
                t = '@user' if t.startswith('@') and len(t) > 1 else t
                t = 'http' if t.startswith('http') else t
                new_text.append(t)
            new_text = " ".join(new_text)
            outcorpus.append(new_text)
        return outcorpus

    dataset = pd.read_pickle(text_path, compression='gzip')['text'].tolist()

    # pretrained model acquisition
    BATCH_SIZE = 50
    MODEL = model_path
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    _ = model.eval()

    dl = DataLoader(dataset, batch_size=BATCH_SIZE)
    preds_file_exists = os.path.exists(preds_out)
    scores_file_exists = os.path.exists(scores_out)
    all_preds = []
    all_scores = []
    for idx, batch in enumerate(dl):
        if idx % 1000 == 0:
            print('Batch ', idx, ' of ', len(dl))
        text = preprocess(batch)
        encoded_input = tokenizer(text,
                                  return_tensors='pt',
                                  padding=True,
                                  max_length=512,
                                  truncation=True)
        output = model(**encoded_input)
        scores = output[0].detach().numpy()
        scores = softmax(scores, axis=-1)
        preds = np.argmax(scores, axis=-1)
        all_preds.extend(preds)
        all_scores.extend(scores)
        #write on file at each batch

                # Write predictions and scores to file at each batch
        pd.DataFrame(preds).to_csv(preds_out, mode='a', index=False, header=not preds_file_exists)
        pd.DataFrame(scores).to_csv(scores_out, mode='a', index=False, header=not scores_file_exists)

        # After the first write, file_exists should be True
        preds_file_exists = True
        scores_file_exists = True


def process_oil(oil):
    if os.path.exists(f'./data/{oil}/sentiment/pred.csv') and os.path.exists(f'./data/{oil}/sentiment/scores.csv'):
        print(f'Sentiment analysis for {oil} already done')
    else:
        XLM(text_path = f'./data/{oil}/text.pkl.gz',
            model_path = "cardiffnlp/twitter-roberta-base-sentiment",
            preds_out = f'./data/{oil}/sentiment/pred.csv',
            scores_out = f'./data/{oil}/sentiment/scores.csv')

oils = ['coconut','olive','palm'] 

for oil in oils:
    process_oil(oil)
