import os

def check_dir(path):
		directory = os.path.dirname(path)
		if not os.path.exists(path):
			os.makedirs(path)