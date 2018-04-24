import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import sys

INPUT_FOLDER = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]

if len(sys.argv) < 3:
    print('Usage: python preprocess.py <INPUT_FOLDER> <OUTPUT_FOLDER>')
    sys.exit(-1)

def preprocess_log(log_files=['dataset/mcBSC/Antti_Palojarvi/Examples/Training1/Switch_logs/no_passive_missing/EXT2_BMT.log']):
	cmd_log = {}		# dict of filetype vs (dict of cmd_name vs log content)
	line_num = 1
	for log_filename in log_files:
		log_file = open(log_filename, 'r', encoding = "ISO-8859-1")
		content = log_file.readlines()
		log_file.close()

		collected_log = []
		log_lines = []
		prev_cmd = None
		for line in content:
			if ";" in line:
				words = word_tokenize(line)
				for word in words:
					if word[0] == 'Z':
						w = word.split(':')[0]
						if len(w) > 5:
							w = w[:4]

						if prev_cmd is not None:
							if prev_cmd not in cmd_log:
								cmd_log[prev_cmd] = [collected_log]		#this is a list
							else:
								cmd_log[prev_cmd].append(collected_log)
						prev_cmd = w
						break
				collected_log = [str(line_num)+'\t'+line]
			else:
				collected_log.append(str(line_num)+'\t'+line)
			line_num += 1
		if prev_cmd is not None:
			if prev_cmd not in cmd_log:
				cmd_log[prev_cmd] = [collected_log]		#this is a list
			else:
				cmd_log[prev_cmd].append(collected_log)

	return cmd_log


def zero_digits(s):
    # return s
    return re.sub('\d', '0', s)


filetypes = {}		# file types vs names of file in that type
def walk_process_directory(rootdir=INPUT_FOLDER):
	# filetypes = []
	EXCLUDES = ['.zip', '.ZIP', '.bin','.BIN', '.rar', '.MAP', '.BAK', '.BBX', '.tgz', '.DAT', '.SHL', 'TEST', '0.HW','.tar']
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			filetype = zero_digits(file)
			if file[-4:] not in EXCLUDES and file[-2:] != '.Z' and filetype[-4:] != 'S000' and file != 'info.txt':
				filename = os.path.join(subdir, file)
				print('processing file:',filename)
				flog = preprocess_log([filename])
				filename = filename.replace('/', '#')
				for cmd in flog:
					logs = flog[cmd]
					if cmd == '':
						continue
					out_file = open(directory+'/'+str(cmd)+'_'+str(filename), 'w')
					for log in logs:
						out_file.write(''.join(log))
					out_file.close()


directory = OUTPUT_FOLDER
if not os.path.exists(directory):
	os.makedirs(directory)

filetypes = walk_process_directory()

# # print(filetypes.keys())
# # print(filetypes['SUPERV0.HW'])
# # sys.exit(-1)
# if not os.path.exists(directory):
# 	# print('yo')
# 	os.makedirs(directory)

# for ftype in filetypes:
# 	if ftype == '':
# 		continue
# 	print('processing ftype:',ftype)
# 	flog = preprocess_log(ftype, filetypes[ftype])
# 	# print(flog.keys())
# 	for cmd in flog:
# 		logs = flog[cmd]
# 		if cmd == '':
# 			continue
# 		out_file = open(directory+'/'+str(cmd)+'_'+str(ftype), 'w')
# 		for log in logs:
# 			out_file.write(''.join(log))
# 		out_file.close()

# ftype = 'IP_configurations.txt'
# print(preprocess_log(ftype, filetypes[ftype][:2]))
# process_onekind()
# print(cmd_log)
