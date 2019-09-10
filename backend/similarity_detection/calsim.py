import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import operator
import pandas as pd
from skimage import io
from skimage.transform import resize
import sys
sys.path.append(dir_path)
from sim import _sim_colour, _calc_colour_hist, _calc_texture_hist,_sim_structure

FILE = "./widgets.json"
OUT = "./result.json"

def loading():
    # loading widgets information
    df = pd.read_json(FILE,orient='records')
    R = {}
    for i in df["name"].tolist():
        img = io.imread("./all_widgets/"+i+".png") 
        imgg = io.imread("./all_widgets/"+i+".png",as_gray=True)
        imgg = resize(imgg, (64, 64), anti_aliasing=True, preserve_range=True)
        try:
            R[i] = {"hist_t": _calc_texture_hist(img), "hist_c": _calc_colour_hist(img), "img":imgg}
        except:
            pass
    # loading backup and previous results
    if os.path.exists(OUT):
        df_previous = pd.read_json(OUT,orient='records')
        backup = len(df_previous)
    else:
        df_previous = pd.DataFrame(columns=df.columns)
        df_previous = df_previous.fillna(0)
        backup = 0
    print('Finish loading........')
    print('-'*10)
    return R,df,df_previous,backup

def calsim(R,df,df_previous,backup):
    print("Start from ", backup)
    print('-'*10)
    df = df.iloc[backup:,]
    for row_idx, row in df.iterrows():
        i = row["name"]
        S = {}
        for j in R.keys():
            # check whether the same widget class
            if j != i and j.split("-")[0] == i.split("-")[0]:
                # calculate similarity by colour and structure
                S[j] = _sim_colour(R[i],R[j])+_sim_structure(R[i],R[j])
        # top 5 similar widgets
        sims = [j[0] for j in sorted(S.items(), key=lambda i: i[1],reverse=True)[:5]]
        row["sims"] = sims
        df_previous = df_previous.append(row, ignore_index=True)
        # write result
        f = open(OUT,'w')
        f.write(df_previous.to_json(orient='records'))
        f.close()
        print("#"*10+"  "+str(row_idx)+"  "+"#"*10)

def main():
    R,df,df_previous,backup = loading()
    calsim(R,df,df_previous,backup)

if __name__ == "__main__":
    main()
    
