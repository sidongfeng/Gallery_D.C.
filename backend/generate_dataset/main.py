import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path)
import verbo.generate_verbo
import rico.generate_rico
import pandas as pd

def main():
	# generate widgets dataset
	id = 0
	df = pd.DataFrame(columns=['id','name','color','coordinates','dimensions','package_name','text','widget_class','application_name','downloads','url',
			'category','Developer','font','sims','date'])
	df = df.fillna(0)
	id, df = verbo.generate_verbo.generate(id,df)
	id, df = rico.generate_rico.generate(id,df)
	# write results
	f = open('./result.csv','w')
	f.write(df.to_csv(index=False))
	f.close()

if __name__ == '__main__': 
	main()
