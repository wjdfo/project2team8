import os
DATASET_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'datasets')
LOGGING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
TXTDATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'txtdata')

if not os.path.exists(DATASET_DIR):
	os.mkdir(DATASET_DIR)

if not os.path.exists(LOGGING_DIR):
	os.mkdir(LOGGING_DIR)

if not os.path.exists(TXTDATA_DIR):
	os.mkdir(TXTDATA_DIR)