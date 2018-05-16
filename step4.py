import sys
import os
import re

OUTPUT_DIR = sys.argv[1]     		# Templates from the golden logs
PREPROCESSED_DIR = sys.argv[2]		# Preproessed test files
OUTFILE = sys.argv[3]				# anamalous file output (single file)
LEARN_FROM_DIR = sys.argv[4]		# File structure to learn stuff from

rex = [('blk_(|-)[0-9]+', 'rx_idk'), ('([0-9]+\.){3}[0-9]+\/[0-9]+', 'rx_ipws'), ('(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', 'rx_ip'), ('([0-9]+\-){2}[0-9]+', 'rx_date'), ('([0-9]+\:){2}[0-9]+', 'rx_time'), ('\ ([0-9]+)(\ |$)', ' rx_num '), ('^([0-9]+)\ ', 'rx_num '), ('\t([0-9]+)(\t|$)', '\trx_num\t'), ('^([0-9]+)\t', '\trx_num\t'),           ('([0-9])', '')]

outputs = []
for subdir, dirs, files in os.walk(OUTPUT_DIR):
	for file in files:
		cur_outputs = []
		printed = False		
		corresponding_preprocessed_file = '_'.join(file.split('_')[1:])
		# print(corresponding_preprocessed_file)

		fulloutfilename = os.path.join(subdir, file)	#Template file full path
		fullprefilename = PREPROCESSED_DIR + corresponding_preprocessed_file	#Corresponding preprocessed file path
		f = open(fullprefilename).readlines()	#Corresponding preprocessed file path
		f_out = open(fulloutfilename).readlines()	#Template file full path
		line_already_printed = []
		for linenum,line in enumerate(f):		#enumerate preproessed file
			if linenum in line_already_printed:
				continue
			line = line.strip()

			#Do regex preprocessing
			for (r1,r2) in rex:
				line = re.sub(r1,r2,line)
			outp = False
			pre_toks = line.split()[1:]
			outnum = -1

			#enumerate over template lines and find matching one
			for outline_num,outline in enumerate(f_out):	
				outline = outline.strip()
				out_toks = outline.split()
				if len(out_toks) != len(pre_toks):
					break
				diff = False
				for token1, token2 in zip(out_toks, pre_toks):
					if token1 == '*':
						continue
					if token1 == token2:
						continue
					diff = True
					break
				# print(diff)

				if diff == False:
					outnum = outline_num
					outp = True
					break
			
			# If any anomalous lines to be printed, add them to 
			# a list to be printed later. One list for main output
			# file, other for file structure for later learning.
			if outp:
				if outnum != -1:
					del f_out[outnum]

				# if f[linenum].strip() not in outputs:

				if not printed:
					# outputs.append('x	*************'+fullprefilename+'***************\n')
					printed = True
				line_already_printed.append(linenum)
				line_already_printed.append(linenum+1)
				# outputs.append('y	####\n')
				outputs.append('y	\n')
				if linenum > 0 and len(f[linenum-1].strip().split())>1:
					outputs.append(f[linenum-1])
				outputs.append(f[linenum])

				cur_outputs.append(f[linenum])
			
				if linenum < len(f)-1 and len(f[linenum+1].strip().split())>1:
					# print('Voila')
					outputs.append(f[linenum+1])

		# Write File structure to learn stuff from if
		# there is anything to be printed.
		if len(cur_outputs) > 0:
			cur_OUTFILE = LEARN_FROM_DIR + corresponding_preprocessed_file
			f = open(cur_OUTFILE, 'w')
			for out in cur_outputs:
				# out = '\t'.join(out.split('\t')[1:])
				f.write(out)
			f.close()
		# break

# Print the final output file
f = open(OUTFILE, 'w')
for out in outputs:
	# tp = out.split(' ')[1:]
	# if len(tp) > 1:
		# out = ' '.join(tp[1:])
	# print(out)
	out = '\t'.join(out.split('\t')[1:])
	# print(out)
	f.write(out)
f.close()
