import generate_dataset.main
import similarity_detection.main

if __name__ == '__main__': 
	# generate widgets database based on coordinates 
	# we obtain Verbo and Rico dataset
	generate_dataset.main.main()
	# Check Similarity on the widgets
	# Objection; 1. remove duplicate widgets
	#			 2. find similiar widgets
	similarity_detection.main.main()
