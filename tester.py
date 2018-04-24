import sys

MODEL_FILE = sys.argv[1]
INPUT_FILE = sys.argv[2]
OUT_FILE = sys.argv[3]

f = open(MODEL_FILE)
model = f.readlines()
f.close()

f = open(INPUT_FILE)
inputs = f.readlines()
f.close()

outputs = []
actual_outputs = []
for inp_line in inputs:
    outp = True
    for mod_line in model:
        inp_line = inp_line.strip()
        mod_line = mod_line.strip()
        inp_list = inp_line.split(' ')
        mod_list = mod_line.split(' ')
        if len(inp_list) != len(mod_list):
            continue;
        diff = False
        print(inp_list)
        print(mod_list)
        print("yoyo")
        for token1, token2 in zip(mod_list, inp_list):
            if token1 == '*':
                continue
            if token1 == token2:
                continue
            diff = True
            break
        print(diff)
        if diff == False:
            outp = False
            break
    if outp == True:
        outputs.append(inp_line)

f = open(OUT_FILE, 'w')
for out in outputs:
    f.write(out + "\n")
f.close()