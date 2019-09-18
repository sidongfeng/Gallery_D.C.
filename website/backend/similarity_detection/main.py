import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path)
import calsim

def main():
	# similarity detection
	calsim.main()

if __name__ == '__main__': 
	main()
