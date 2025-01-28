import logging
import math
import re

# add and format certain columns to match the MTB format requirements
def create_mtb_columns(df):
	df['Change_summary'] = df.apply(lambda x: format_change_summary(x['Change_summary']), axis=1)
	df['Genomic coordinates in hg19 build'] = df.apply(lambda x: format_genomic_coordinates(x['Genomic_location'], x['DNA_change']), axis=1)
	df['HGVS syntax'] = df.apply(lambda x: format_hgvs_syntax(x['RefSeq_mRNA'], x['cDNA_change']), axis=1)
	df['Read depth(variant reads/total reads)'] = df.apply(lambda x: format_read_depth(x['Depth_tumor_DNA'], x['AF_tumor_DNA']), axis=1)
	df['AF_tumor_DNA'] = df.apply(lambda x: format_af_tumor_dna(x['AF_tumor_DNA']), axis=1)
	return df

# convert dataframe to expected list object with tab separation and line breaks
def dataframe_to_list(df):
	df = df.astype(str)
	df.iloc[:,:-1] = df.iloc[:,:-1] + '\t' # all but the last column get a tab suffix
	df.iloc[:,-1:] = df.iloc[:,-1:] + '\n' # the last column gets a line break suffix
	df = df.rename(columns={c: c+'\t' for c in df.columns if c in df.columns[:-1]}) # all but last column header get a tab suffix
	df = df.rename(columns={c: c+'\n' for c in df.columns if c in df.columns[-1:]}) # the last column header gets a line break suffix
	return [df.columns.values.tolist()] + df.values.tolist()

# return formatted string for allele frequency of tumor dna
def format_af_tumor_dna(af):
	percentage = af * 100
	return '{:.1f}%'.format(percentage)

# return NaN if input is NaN or formatted string for change summary
def format_change_summary(summary):
	try:
		if math.isnan(summary):
			logging.debug(summary)
			return summary
	except:
		[dna_seq_change, _, prot_change, prot_change_2] = str(summary).split(':')
		return '{}{}{}'.format(dna_seq_change, format_prot_change(prot_change), format_prot_change(prot_change_2))

# return formatted string for genomic coordinates
def format_genomic_coordinates(coordinates, dna_change):
	[chr, bp] = coordinates.split(':')
	return 'chr{}:g.{}{}'.format(chr, bp, dna_change)

# return formatted string for HGVS syntax
def format_hgvs_syntax(refseq, cdna):
	return '{}:{}'.format(refseq, cdna)

# return formatted string for protein change
def format_prot_change(input):
	if input == 'NA':
		return ''
	else:
		return ',p.({})'.format(input)

# return formatted string for read depth
def format_read_depth(depth, af):
	variant_reads = depth * af
	return '{:.0f}/{}'.format(variant_reads, depth)

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

# parse keys and divide in keys to include or exclude
def parse_keys(keys):
	key_map = {
		'include': '',
		'exclude': ''
	}
	matches = re.search('^!(\\S*)(?: && !)?(\\S+)?$', keys)
	if matches:
		groups = [match for match in matches.groups() if match is not None]
		key_map['exclude'] = '|'.join(groups)
	else:
		key_map['include'] = keys.replace(',', '|')
	return key_map
