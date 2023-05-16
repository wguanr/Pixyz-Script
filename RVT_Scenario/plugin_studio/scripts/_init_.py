import os

root = 'F:\PCG\pixyz\RVT_Scenario\_input'
exts = ['.rvt', '.rfa']

def scan(root):
	"""Recursively scans given root directory and returns list of files"""
	files = []

	for entry in os.scandir(root):
		while entry.is_dir():
			pass

	return files


for x in os.scandir(root):
	print(x.name)
