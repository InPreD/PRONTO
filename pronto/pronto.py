import glob
import logging
import os

# get tumor mutational burden label
def get_tmb_string(val):
	level = "Not available"
	if(0 <= val <= 5):
		level = "Lav"
	elif(5 < val <= 20):
		level = "Intermediær"
	elif(val > 20):
		level = "Høy"
	return "{} mut/Mb; {}\n".format(val, level)

# use glob to find file in different folder structures
def glob_tsoppi_file(is_error, root, run_id, *path_units):
	glob_string_ous = os.path.join(root, '{}_TSO_500_LocalApp_postprocessing_results'.format(run_id), *path_units)
	glob_string_hus = os.path.join(root, run_id, '{}_ppr'.format(run_id), *path_units)
	files = []
	for gl in (glob_string_ous, glob_string_hus):
		files.extend(glob.glob(gl))
	if len(files) == 1:
		return files[0]
	elif not is_error:
		logging.warning("unsuccessful glob strings for {}:\n{}\n{}".format(run_id, glob_string_ous, glob_string_hus))
	else:
		logging.error("unsuccessful glob strings for {}:\n{}\n{}".format(run_id, glob_string_ous, glob_string_hus))
		raise ValueError
