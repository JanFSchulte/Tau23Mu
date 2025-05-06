import subprocess, argparse, sys, glob

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--anaType')
parser.add_argument('-o', '--outName')

args = parser.parse_args()

ANALYSISTYPE=args.anaType
OUT_NAME=args.outName


# Control channel
if ANALYSISTYPE == "control":
    print ("DsPhiPi analysis")
    DATATYPE='data_control'
elif ANALYSISTYPE == "tau3mu":
    print ("Tau3mu analysis")
    DATATYPE='data'
elif ANALYSISTYPE == "phimunu":
    print ("Tau3mu phimunu")
    DATATYPE='data_phimunu'
else:
    print ("unsupported analysis type")
    sys.exit()

files = []

for i in ['2024D-v1_0', '2024D-v1_1', '2024D-v1_2', '2024D-v1_3', '2024D-v1_4', '2024D-v1_5', '2024D-v1_6', '2024D-v1_7', '2024E-v1_0', '2024E-v1_1', '2024E-v1_2', '2024E-v1_3', '2024E-v1_4', '2024E-v1_5', '2024E-v1_6', '2024E-v1_7', '2024E-v2_0', '2024E-v2_1', '2024E-v2_2', '2024E-v2_3', '2024E-v2_4', '2024E-v2_5', '2024E-v2_6', '2024E-v2_7', '2024F-v1_0', '2024F-v1_1', '2024F-v1_2', '2024F-v1_3', '2024F-v1_4', '2024F-v1_5', '2024F-v1_6', '2024F-v1_7', '2024G-v1_0', '2024G-v1_1', '2024G-v1_2', '2024G-v1_3', '2024G-v1_4', '2024G-v1_5', '2024G-v1_6', '2024G-v1_7', '2024H-v1_0', '2024H-v1_1', '2024H-v1_2', '2024H-v1_3', '2024H-v1_4', '2024H-v1_5', '2024H-v1_6', '2024H-v1_7', '2024I-v1_0', '2024I-v1_1', '2024I-v1_2', '2024I-v1_3', '2024I-v1_4', '2024I-v1_5', '2024I-v1_6', '2024I-v1_7', '2024I-v2_0', '2024I-v2_1', '2024I-v2_2', '2024I-v2_3', '2024I-v2_4', '2024I-v2_5', '2024I-v2_6', '2024I-v2_7']:

    tmpFiles = glob.glob("%s_%s_%s/*.root"%(i,ANALYSISTYPE,OUT_NAME))
    for f in tmpFiles:
        if "merged" in f: continue
        #fileString+=f
        #fileString+=" "
        files.append(f)

call = ["hadd",'-k', '-f', "AnalysedTree_%s_2024_%s_merged_%s.root"%(DATATYPE, ANALYSISTYPE, OUT_NAME)] + files
print (call)
subprocess.call(call)
#hadd AnalysedTree_${DATATYPE}_${i}_${ANALYSISTYPE}_merged_${OUT_NAME}.root AnalysedTree_${DATATYPE}_${i}_${ANALYSISTYPE}*.root

