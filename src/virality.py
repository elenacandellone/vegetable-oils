from src.utils import *


# count how many times a certain hashtag is present
def CountFrequency(arr):
    return collections.Counter(arr)


def lower(arr):
    return [val.lower() for val in arr]


def hashtag_single_tweet(text):
    hashtags = re.findall("#([a-zA-Z0-9_]{1,50})", text)
    return [str(val.lower()) for val in hashtags]


# extract the list of hashtags, also assigning the sentiment


def hashtag_list_dyn(texts):
    hash_list = []
    array_tweets = texts['text'].tolist()
    df = pd.DataFrame(columns=['date', 'text', 'hashtags'])
    df['date'] = texts['date'].tolist()
    df['year'] = texts['year'].tolist()
    df['month'] = texts['month'].tolist()
    df['text'] = texts['text'].tolist()
    df['day'] = texts['day'].tolist()
    if 'created_at' in texts.columns:
        df['hour'] = texts['created_at'].tolist()
    for i in range(len(array_tweets)):
        if hashtag_single_tweet(array_tweets[i]):
            hash_list.append(hashtag_single_tweet(array_tweets[i]))
        else:
            hash_list.append(np.NaN)
    df['hashtags'] = hash_list
    if 'sentiment' in texts.columns:
        df['sentiment'] = texts['sentiment'].tolist()
    return df

# calculate sigma in case of truncated power-law (there is not built-in function in the package)
def sigma(data, pwl=True):
    import powerlaw
    fit = powerlaw.Fit(data)
    if pwl == True:
        dist = fit.power_law
    else:
        dist = fit.truncated_power_law

    k = dist.alpha
    x_min = dist.xmin
    n = len([x for x in data if x > x_min])
    return (k - 1) / np.sqrt(n)

def to_timestamp(df):
    x = []
    for i in df["hour"].tolist():
        a = pd.Timestamp(i)
        x.append(a)
    return x


def interevent_time(d, hashtag):
    df = d.loc[d['hashtags'] == hashtag][[
        'hour', 'hashtags', 'date'
    ]].sort_values(by='hour').reset_index(drop=True)
    df['hour'] = to_timestamp(df)
    df['Delta'] = df['hour'].diff()
    return df


def seconds_to_hours(vec):
    return np.array(vec) / (60 * 60)


def iet(oil, data_path='./data/'):
    path = f'{data_path}{oil}/' #data path

    tweets_text = pd.read_pickle(path + 'text.pkl.gz',compression='gzip')
    tweets_dates = pd.read_pickle(path + 'dates.pkl.gz',compression='gzip')
    all_tweets = pd.concat([
        tweets_text.reset_index(drop=True),
        tweets_dates.reset_index(drop=True)
    ],
                           axis=1).sort_index()

    df_hashtags = hashtag_list_dyn(all_tweets).explode('hashtags')

    # remove numerical hashtags
    df_hashtags = df_hashtags.loc[(df_hashtags['hashtags'] != '1')
                                  & (df_hashtags['hashtags'] != '2') &
                                  (df_hashtags['hashtags'] != '3')]

    # best 10 hashtags
    best_hash = pd.DataFrame.from_dict(CountFrequency(
        df_hashtags[df_hashtags['hashtags'].notna()]['hashtags'].tolist()),
                                       orient='index').sort_values(
                                           by=0, ascending=False).head(10)
    l = best_hash.index.tolist()

    df_fit = pd.DataFrame()

    fig, axs = plt.subplots(2, 5, figsize=(20, 10), dpi=350)
    fig.subplots_adjust(hspace=.5, wspace=.3)

    axs = axs.ravel()

    for i in tqdm(range(10)):

        hashs = l[i]

        df = interevent_time(df_hashtags, hashs)
        data = seconds_to_hours(
            df['Delta'].dt.total_seconds().tolist()[1:])  #interevent times

        # FITTING PROCEDURE
        fit = pwl.Fit(data, verbose=False)
        pdf = fit.pdf()
        ccdf = fit.ccdf()

        # log-likelihood ration and p-value
        R, p = fit.distribution_compare('power_law',
                                        'truncated_power_law',
                                        normalized_ratio=True)

        # PLOT

        # data
        axs[i].scatter(pdf[0][1:], pdf[1], color='g', label='data')

        # pwl
        fit.power_law.plot_pdf(ax=axs[i],
                               color='b',
                               linestyle='--',
                               linewidth=2.5,
                               label='power law')

        # truncated pwl
        fit.truncated_power_law.plot_pdf(ax=axs[i],
                                         color='r',
                                         linestyle='--',
                                         linewidth=2,
                                         label='truncated power law')

        axs[i].set_yscale('log')
        axs[i].set_xscale('log')
        axs[i].set_title(f'{hashs}', size=25)

        # DataFrame of PARAMETERS
        if R > 0:

            df1 = pd.DataFrame({
                'hashtag': [hashs],
                'best distribution': ['pwl'],
                'n': [len(data)],
                'p': [p],
                'x_min': [fit.power_law.xmin],
                'D': [fit.power_law.D],
                'k': [fit.power_law.alpha],
                'sigma': [fit.power_law.sigma]
            })
        else:
            df1 = pd.DataFrame({
                'hashtag': [hashs],
                'best distribution': ['truncated pwl'],
                'n': [len(data)],
                'p': [p],
                'x_min': [fit.truncated_power_law.xmin],
                'D': [fit.truncated_power_law.D],
                'k': [fit.truncated_power_law.alpha],
                'sigma': [sigma(data, pwl=False)]
            })

        df_fit = pd.concat([df_fit,df1])

    handles, labels = axs[-1].get_legend_handles_labels()
    fig.legend(handles,
               labels,
               loc='upper center',
               bbox_to_anchor=(0.5, -0.0),
               ncol=3,
               prop={'size': 25})

    fig.supxlabel(r'interevent times $\tau$ (hours)', size=30)
    fig.supylabel(r'p($\tau$)', size=30)
    #plt.savefig(f'./plots/IET_{oil}.pdf', bbox_inches='tight')
    plt.show()

    return l, df_fit, df_fit['k'].tolist(), df_fit['sigma'].tolist()

def delta_days():
    from datetime import date
    d0 = date(2007, 3, 13)
    d1 = date(2021,12,31)
    return (d1 - d0).days

def hash_per_day(df, hashtag):
    df1 = df.loc[df['hashtags'] == hashtag]
    df1['date'] = pd.to_datetime(df1['date'], format='%Y-%m-%d')
    return df1['day'].groupby(
        df1['date'].dt.date).size().reset_index(name='counts')

def cascade_size(df_hashtags, hashtag, thr = 0):
    import datetime
    delta = delta_days()
    base = datetime.datetime.today()
    
    date_list = sorted([(base - datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(delta)])
    
    df1 = pd.DataFrame(columns = ['date'])
    df1['date'] = date_list
    
    date_hash = [i.strftime('%Y-%m-%d') for i in hash_per_day(df_hashtags,hashtag)['date'].tolist()]
    df2 = hash_per_day(df_hashtags,hashtag)
    df2['date'] = date_hash
    
    x = pd.merge(df1,df2,how='left',on = 'date')
    x['counts'] = x['counts'].fillna(0)
    x['binary'] = np.where(x['counts'] > 0, 1, 0)
    x['condition'] = x[x['counts'] > thr]['counts']
    x['condition'] = x['condition'].fillna(0)
    return x

def cs(oil,data_path = './data/'):
    path = f'{data_path}{oil}/' #data path

    tweets_text = pd.read_pickle(path + 'text.pkl.gz',compression='gzip')
    tweets_dates = pd.read_pickle(path + 'dates.pkl.gz',compression='gzip')
    all_tweets  = pd.concat([tweets_text.reset_index(drop = True),tweets_dates.reset_index(drop = True)], axis = 1).sort_index()
    
    
    df_hashtags = hashtag_list_dyn(all_tweets).explode('hashtags')
    
    # remove numerical hashtags
    df_hashtags = df_hashtags.loc[(df_hashtags['hashtags'] != '1') & (df_hashtags['hashtags'] != '2') & (df_hashtags['hashtags'] != '3')]
    
    # best 10 hashtags
    best_hash = pd.DataFrame.from_dict(CountFrequency(df_hashtags[df_hashtags['hashtags'].notna()]['hashtags'].tolist()),orient='index').sort_values(by = 0, ascending = False).head(10)
    l = best_hash.index.tolist()


    df_fit = pd.DataFrame()

    fig, axs = plt.subplots(2,5, figsize=(20,10),dpi=350)
    fig.subplots_adjust(hspace = .5, wspace= .3)

    axs = axs.ravel()
    
    for i in tqdm(range(10)):
        
        hashs = l[i]

        df = cascade_size(df_hashtags,hashs) 
        data = df[df['condition']>0]['condition'].tolist()        #cascade size


        # FITTING PROCEDURE
        fit = pwl.Fit(data, verbose = False)
        pdf = fit.pdf()
        ccdf = fit.ccdf()

        # log-likelihood ration and p-value
        R,p = fit.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)

        # PLOT
        
        # data
        axs[i].scatter(pdf[0][1:],pdf[1], color='g', label='data')
        
        # pwl
        fit.power_law.plot_pdf(ax=axs[i], color='b', linestyle='--', linewidth=2.5, label='power law')
        
        # truncated pwl
        fit.truncated_power_law.plot_pdf(ax=axs[i], color='r', linestyle='--', linewidth=2, label='truncated power law')

        axs[i].set_yscale('log')
        axs[i].set_xscale('log')
        axs[i].set_title(f'{hashs}', size = 25)
        
        # DataFrame of PARAMETERS
        if R > 0:
            
            df1 = pd.DataFrame({'hashtag':             [hashs],
                                'best distribution':   ['pwl'],
                                'n':                   [len(data)],
                                'p':                   [p],
                                'x_min':               [fit.power_law.xmin],
                                'D':                   [fit.power_law.D],
                                'k':                   [fit.power_law.alpha],
                                'sigma':               [fit.power_law.sigma]
                               })
        else:
            df1 = pd.DataFrame({'hashtag':             [hashs],
                                'best distribution':   ['truncated pwl'],
                                'n':                   [len(data)],
                                'p':                   [p],
                                'x_min':               [fit.truncated_power_law.xmin],
                                'D':                   [fit.truncated_power_law.D],
                                'k':                   [fit.truncated_power_law.alpha],
                                'sigma':               [sigma(data, pwl = False)]
                               })


        df_fit = pd.concat([df_fit,df1])
    

    handles, labels = axs[-1].get_legend_handles_labels()
    fig.legend(handles, labels,loc='upper center', bbox_to_anchor=(0.5, 0), ncol=3, prop ={'size': 25})


    fig.supxlabel(r'cascade size $CS$', size = 30)
    fig.supylabel(r'p($CS$)', size = 30)
    #plt.savefig(f'./plots/CS_{oil}.pdf', bbox_inches='tight')
    plt.show()
    
    return l, df_fit, df_fit['k'].tolist(), df_fit['sigma'].tolist()

def plot_phase_diagram(results_iet, results_cs, oils, palette, markers, path='plots/phase_diagram.pdf'):
    lw =1
    a = 0.5
    texts = []
    plt.figure(figsize=(5,4),dpi=500)
    plt.axhline(y=2, color='grey', linestyle='--',lw=lw, alpha=a) 
    plt.axvline(x=2, color='grey', linestyle='--',lw=lw, alpha=a)
    plt.axhline(y=3, color='grey', linestyle='--',lw=lw, alpha=a)
    plt.axvline(x=3, color='grey', linestyle='--',lw=lw, alpha=a)

    plt.text(1.05, 2.8, 'I', fontsize=10, weight='bold')
    plt.text(2.05, 2.8, 'II', fontsize=10, weight='bold')
    plt.text(3.5, 2.8, 'III', fontsize=10, weight='bold')
    plt.text(3.5, 3.10, 'IV', fontsize=10, weight='bold')
    plt.text(2.05, 3.10, 'V', fontsize=10, weight='bold')
    plt.text(1.05, 3.10, 'VI', fontsize=10, weight='bold')
    for oil in oils:
        iet = results_iet[oil]
        cs = results_cs[oil]
        hashtags = iet['hashtag'].tolist()
        plt.scatter(iet['alpha'], cs['alpha'], color=palette[oil], label=oil, marker=markers[oil],s=6)
        plt.errorbar(iet['alpha'], cs['alpha'], xerr=iet['sigma'], yerr=cs['sigma'], fmt=markers[oil], color=palette[oil], markersize=0, elinewidth=0.5, alpha=0.5)
        #add hashtags names
        for i, txt in enumerate(iet['hashtag']):
            x_pos = iet['alpha'][i]   # adjust x position based on error bar
            y_pos = cs['alpha'][i]  # adjust y position based on error bar
            texts.append(plt.annotate(txt, (x_pos, y_pos), fontsize=6))
    adjust_text(texts, arrowprops=dict(arrowstyle='->', lw=lw))
    plt.ylim(1,5)
    plt.xlim(1,4)
    plt.xlabel(r'$\alpha_{IET}$')
    plt.ylabel(r'$\alpha_{CS}$')
    plt.legend()
    plt.savefig(path)
    plt.show()
