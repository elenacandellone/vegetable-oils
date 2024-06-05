from src.utils import *

oils = ['canola', 'coconut', 'olive', 'palm', 'peanut', 'soybean', 'sunflower']

for oil in oils:
    in_path = os.path.normpath('./data_raw/'+oil)            # dataset path
    out_path = os.path.normpath('./data/'+oil+'/')  # output path
    out_path_anon = os.path.normpath('./data_id/'+oil)  # output path
    pickles_gen(in_path, out_path, out_path_anon)
    print(f'{oil} done!')

languages = os.listdir('./data_raw/palm_languages/')

for language in languages:
    in_path = os.path.normpath('./data_raw/palm_languages/'+language)            # dataset path
    out_path = os.path.normpath('./data/palm_languages/'+language+'/')  # output path
    out_path_anon = os.path.normpath('./data_id/palm_languages/'+language)  # output path
    pickles_gen(in_path, out_path, out_path_anon)
    print(f'{language} done!')