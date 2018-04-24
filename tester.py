import sys
import os
import re

# MODEL_FILE = sys.argv[1]
# INPUT_FILE = sys.argv[2]
# OUT_FILE = sys.argv[3]
if len(sys.argv) < 4:
    print('Usage: python tester.py MODEL_DIR/TRAIN_TEMPLATES_DIR/GOLDEN_TEMPLATES_DIR TEST_INPUT_DIR OUTPUT_DIR')
    sys.exit(-1)

MODEL_DIR = sys.argv[1]
TEST_DIR = sys.argv[2]
OUTPUT_DIR = sys.argv[3]


def walk_compare(modeldir=MODEL_DIR, testdir=TEST_DIR):
    model_files = {}    #model filetype vs full path
    for subdir, dirs, files in os.walk(modeldir):
        for file in files:
            fullfilename = os.path.join(subdir, file)
            model_files[file] = fullfilename

    print(model_files.keys())
    test_files = {}
    for subdir, dirs, files in os.walk(testdir):
        for file in files:
            fullfilename = os.path.join(subdir, file)

            file = 'template_' + re.sub('\d', '0', file.split('_')[1] + '_' + file.split('#')[-1] )
            print(file)
            outfilename =  'output_'+'_'.join(fullfilename.split('/')[-1].split('_')[1:])
            # print(file)
            if file in model_files.keys():
                print('processing:',fullfilename)
                comparator(model_files[file], fullfilename, outfilename)
            else:
                print('[IGNORING]:',fullfilename)

            test_files[file] = fullfilename
            


def comparator(model_file, input_file, output_file, outputdir=OUTPUT_DIR):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    f = open(model_file)
    model = f.readlines()
    f.close()

    f = open(input_file)
    inputs = f.readlines()
    f.close()

    outputs = []
    actual_outputs = []
    for inp_line in inputs:
        inp_list = inp_line.split(' ')
        if len(inp_list) == 4 and (inp_list[0] == "FlexiBSC" or inp_list[0] == "mcBSC"):
            continue;
        outp = True
        for mod_line in model:
            inp_line = inp_line.strip()
            mod_line = mod_line.strip()
            inp_list = inp_line.split(' ')
            mod_list = mod_line.split(' ')
            if len(inp_list) != len(mod_list):
                continue;
            diff = False
            # print(inp_list)
            # print(mod_list)
            
            for token1, token2 in zip(mod_list, inp_list):
                if token1 == '*':
                    continue
                if token1 == token2:
                    continue
                diff = True
                break
            # print(diff)
            if diff == False:
                outp = False
                break
        if outp == True:
            outputs.append(inp_line)

    f = open(outputdir+'/'+output_file, 'w')
    for out in outputs:
        f.write(out + "\n")
    f.close()

walk_compare()