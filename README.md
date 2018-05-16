preprocess.py -> preprocess the GOLDEN log files

auto_test.py -> preprocess the TEST log files

parselog.py -> parses the log into template files

[NEW]step4.py -> compares the test templates to the train templates and generates folder structure to allow learning
[OLD]tester.py -> compares the test templates to the train templates

### To learn stuff
parselog_and_save.py -> parses the log into template files and save elarnt model to models/ folder

python3 parselog_and_save.py 'test/inputdir/' 'test/out1'


learn_more.py -> Use the models from parselog_and_save.py and folder structure from step4.py to make model learn more

python3 learn_more.py 'test/newtemplates/' 'test/out1/' 'test/out2'
