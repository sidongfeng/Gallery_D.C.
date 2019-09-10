import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path)
import pandas as pd
from color import get_color

def main():
	# color detection
    df = pd.read_json('widgets.json',orient='record')
    for i, row in df.iterrows():
        colors = get_color('./all_widgets/'+row['name']+'.png')
        df.at[i,'color'] = colors
        break
    f = open('widgets1.json','w')
    f.write(df.to_json(orient='records'))
    f.close()

if __name__ == '__main__': 
	main()
