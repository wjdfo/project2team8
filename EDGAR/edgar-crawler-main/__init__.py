import os
DATASET_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'edgar-datasets')

if not os.path.exists(DATASET_DIR):
	os.mkdir(DATASET_DIR)
