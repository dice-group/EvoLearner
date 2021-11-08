import plistlib
import sys

file_name = sys.argv[1]
system = sys.argv[2]
time = sys.argv[3]

with open(file_name, 'w') as fl:
    fl.write("{\n")
    fl.write("\tconfig = 1;\n")
    fl.write(f"\tlearningsystems = ({system});\n")
    fl.write("\tscenarios = (carcinogenesis/1, lymphography/1, mammographic/1, mutagenesis/42, nctrer/1, premierleague/1, pyrimidine/1 );\n\n")
    fl.write("\tmeasures = (fmeasure, pred_acc);\n")
    fl.write("\tframework = {\n")
    fl.write("\t\tcrossValidationFolds = 10;\n")
    fl.write(f"\t\tmaxExecutionTime = {time};\n")
    fl.write("\t};\n")
    fl.write(f"\tresultOutput = testResult.xml;\n")
    fl.write("}\n")
