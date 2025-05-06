#!/bin/bash
# Usage:
#    submitAllJobs.sh <N_files> <AnalysisType>

helpstring="Usage:
submitAllJobs.sh [N_files] [AnalysisType] [OutputName]

N_files: Number of ntuples to be used per job
AnalysisType: Choose between 'tau3mu' and 'control'
"

N_FILES=$1
ANALYSISTYPE=$2
YEAR=$3
OUT_NAME=$4


# Check inputs
if [ -z ${3+x} ]
then
echo ${helpstring}
return
fi

# Control channel
if [ ${ANALYSISTYPE} == "control" ]
then
    echo -e "\nDsPhiPi analysis"
    DATATYPE='data_control'
elif [ ${ANALYSISTYPE} == "tau3mu" ]
then
    echo -e "\nTau3mu analysis"
    DATATYPE='data'
elif [ ${ANALYSISTYPE} == "phimunu" ]
then
    echo -e "\nPhiMuNu analysis"
    DATATYPE='data_phimunu'
fi


for i in 2024D-v1_0 2024D-v1_1 2024D-v1_2 2024D-v1_3 2024D-v1_4 2024D-v1_5 2024D-v1_6 2024D-v1_7 2024E-v1_0 2024E-v1_1 2024E-v1_2 2024E-v1_3 2024E-v1_4 2024E-v1_5 2024E-v1_6 2024E-v1_7 2024E-v2_0 2024E-v2_1 2024E-v2_2 2024E-v2_3 2024E-v2_4 2024E-v2_5 2024E-v2_6 2024E-v2_7 2024F-v1_0 2024F-v1_1 2024F-v1_2 2024F-v1_3 2024F-v1_4 2024F-v1_5 2024F-v1_6 2024F-v1_7 2024G-v1_0 2024G-v1_1 2024G-v1_2 2024G-v1_3 2024G-v1_4 2024G-v1_5 2024G-v1_6 2024G-v1_07 2024H-v1_0 2024H-v1_1 2024H-v1_2 2024H-v1_3 2024H-v1_4 2024H-v1_5 2024H-v1_6 2024H-v1_07 2024I-v1_0 2024I-v1_1 2024I-v1_2 2024I-v1_3 2024I-v1_4 2024I-v1_5 2024I-v1_6 2024I-v1_07 2024I-v2_0 2024I-v2_1 2024I-v2_2 2024I-v2_3 2024I-v2_4 2024I-v2_5 2024I-v2_6 2024I-v2_07
do
    echo -e "\nData $i"
    echo -e "\npython3 createRunFile_new.py --run $i --n ${N_FILES} ${DATATYPE} ${YEAR} ${ANALYSISTYPE} --outName ${OUT_NAME}"
    python3 createRunFile_new.py --run $i --n ${N_FILES} ${DATATYPE} ${YEAR} ${ANALYSISTYPE} --outName ${OUT_NAME}
    sleep 1
    echo -e "\nsubmit_analysis_${i}_${ANALYSISTYPE}_${OUT_NAME}.sh"
    echo "$(pwd)"
#    source submit_analysis_${i}_${ANALYSISTYPE}_${OUT_NAME}.sh
#    cd ..
    sleep 1
done
