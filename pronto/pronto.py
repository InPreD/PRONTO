def get_tmb_string(val):
	level = "Not available"
	if(0 <= val <= 5):
		level = "lav"
	elif(5 < val <= 20):
		level = "intermediær"
	elif(val > 20):
		level = "høy"
	return "{} mut/Mb; {}\n".format(val, level)