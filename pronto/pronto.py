import glob
import logging
import os

# get tumor mutational burden label
def get_tmb_string(val):
	level = "Not available"
	if(0 <= val <= 5):
		level = "lav"
	elif(5 < val <= 20):
		level = "intermediær"
	elif(val > 20):
		level = "høy"
	return "{} mut/Mb; {}\n".format(val, level)

# use glob to find file in different folder structures
def glob_sample_file(*path_units):
	glob_string = os.path.join(*path_units)
	files = glob.glob(glob_string, recursive=True)
	if len(files) == 1:
		return files[0]
	else:
		logging.error("unsuccessful glob: {}".format(glob_string))
		raise ValueError
