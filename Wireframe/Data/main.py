import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path)
import verbo.generate_verbo
import pandas as pd

def main():
	counts = verbo.generate_verbo.generate_pascal()

if __name__ == '__main__': 
	main()
