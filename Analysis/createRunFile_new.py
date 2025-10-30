import sys
import os
import csv
import string
import datetime
import subprocess
from runfiletemplate import get_path

# Define the parser
import argparse
parser = argparse.ArgumentParser(description="Options to give to the script")
# Positional arguments
parser.add_argument("dataset", type=str, choices=['data', 'data_control', 'data_control_2022','data_phimunu', 'MC'], help="Specify if data or Monte Carlo")
parser.add_argument("year", type=str, choices=['2022', '2022EE','2023', '2023BPix', '2024'], help="Specify year of Monte Carlo")
parser.add_argument("anatype", type=str, choices=['tau3mu', 'control','phimunu'], help="Specify analysis type")
#parser.add_argument("--run", type=str, default='', choices=['2022B', '2022C_0', '2022C_1', '2022C_2', '2022C_3', '2022C_4', '2022C_5', '2022C_6', '2022C_7', '2022D_0', '2022D_1', '2022D_2', '2022D_3', '2022D_4', '2022D_5', '2022D_6', '2022D_7', '2022D-v1_0', '2022D-v1_1', '2022D-v1_2', '2022D-v1_3', '2022D-v1_4', '2022D-v1_5', '2022D-v1_6', '2022D-v1_7', '2022D-v2_0', '2022D-v2_1', '2022D-v2_2', '2022D-v2_3', '2022D-v2_4', '2022D-v2_5', '2022D-v2_6', '2022D-v2_7', '2022E_0', '2022E_1', '2022E_2', '2022E_3', '2022E_4', '2022E_5', '2022E_6', '2022E_7', '2022F_0', '2022F_1', '2022F_2', '2022F_3', '2022F_4', '2022F_5', '2022F_6', '2022F_7', '2022G_0', '2022G_1', '2022G_2', '2022G_3', '2022G_4', '2022G_5', '2022G_6', '2022G_7', '2023C-v1_0', '2023C-v1_1', '2023C-v1_2', '2023C-v1_3', '2023C-v1_4', '2023C-v1_5', '2023C-v1_6', '2023C-v1_7', '2023C-v2_0', '2023C-v2_1', '2023C-v2_2', '2023C-v2_3', '2023C-v2_4', '2023C-v2_5', '2023C-v2_6', '2023C-v2_7', '2023C-v3_0', '2023C-v3_1', '2023C-v3_2', '2023C-v3_3', '2023C-v3_4', '2023C-v3_5', '2023C-v3_6', '2023C-v3_7', '2023C-v4_0', '2023C-v4_1', '2023C-v4_2', '2023C-v4_3', '2023C-v4_4', '2023C-v4_5', '2023C-v4_6', '2023C-v4_7', '2023D-v1_0', '2023D-v1_1', '2023D-v1_2', '2023D-v1_3', '2023D-v1_4', '2023D-v1_5', '2023D-v1_6', '2023D-v1_7', '2023D-v2_0', '2023D-v2_1', '2023D-v2_2', '2023D-v2_3', '2023D-v2_4', '2023D-v2_5', '2023D-v2_6', '2023D-v2_7'], help="run in data")
parser.add_argument("--run", type=str)

# Optional Arguments
parser.add_argument("--outName", type=str, default="test", help="Specify name for output files")
parser.add_argument("--n", type=int, default=255, help="number of .root files per job")
parser.add_argument("--MCprocess", type=str, default='', choices=['Ds', 'B0', 'Bp', 'DsPhiPi', 'DsPhiPi2022', 'DsPhiMuNu'], help="process in Monte Carlo")
args = parser.parse_args()

#prepare output filename  and option string
if args.dataset == 'data':
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.run+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+temp.replace("_tau3mu","")+'" "'+args.run+'"'
elif args.dataset == 'data_control':
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.run+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+temp.replace("_control","")+'" "'+args.run+'"'
elif args.dataset == 'data_control_2022':
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.run+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+temp.replace("_control","")+'" "'+args.run+'"'
elif args.dataset == 'data_phimunu':
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.run+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+temp.replace("_phimunu","")+'" "'+args.run+'"'
elif args.dataset == 'MC':
   args.run = "MC"
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.MCprocess+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+'" "'+args.MCprocess+'"'

#startTime = datetime.datetime.now().strftime("%Y%m%d_%H%M")
print (option_string)
# Create target Directory if don't exist
if args.dataset == 'MC':
   output_name = args.MCprocess+"_"+args.anatype+"_"+args.outName
else: 
   output_name = args.run+"_"+args.anatype+"_"+args.outName

if not os.path.exists(output_name):
    os.mkdir(output_name)
    print('Directory '+output_name+' created\n')
else:    
    print('Directory '+output_name+' already exists\n')

if args.anatype == 'tau3mu' and not "MC" in args.dataset:
   stream = args.run.split("_")[-1]
   era = args.run[4]
 
   if '2022' in args.run:
        path = get_path(stream, era, '0',phipi=False, year=2022)

   if '2023' in args.run:
        version = args.run[7]
        path = get_path(stream, era, version ,phipi=False, year=2023)

   if args.dataset == 'data' and args.run == '2024C-v1_0':
      path = get_path(0, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_1':
      path = get_path(1, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_2':
      path = get_path(2, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_3':
      path = get_path(3, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_4':
      path = get_path(4, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_5':
      path = get_path(5, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_6':
      path = get_path(6, 'C', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024C-v1_7':
      path = get_path(7, 'C', '1',phipi=False)

   
   if args.dataset == 'data' and args.run == '2024D-v1_0':
      path = get_path(0, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_1':
      path = get_path(1, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_2':
      path = get_path(2, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_3':
      path = get_path(3, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_4':
      path = get_path(4, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_5':
      path = get_path(5, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_6':
      path = get_path(6, 'D', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024D-v1_7':
      path = get_path(7, 'D', '1',phipi=False)

   if args.dataset == 'data' and args.run == '2024E-v1_0':
      path = get_path(0, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_1':
      path = get_path(1, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_2':
      path = get_path(2, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_3':
      path = get_path(3, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_4':
      path = get_path(4, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_5':
      path = get_path(5, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_6':
      path = get_path(6, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v1_7':
      path = get_path(7, 'E', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_0':
      path = get_path(0, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_1':
      path = get_path(1, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_2':
      path = get_path(2, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_3':
      path = get_path(3, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_4':
      path = get_path(4, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_5':
      path = get_path(5, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_6':
      path = get_path(6, 'E', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024E-v2_7':
      path = get_path(7, 'E', '2',phipi=False)

   if args.dataset == 'data' and args.run == '2024F-v1_0':
      path = get_path(0, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_1':
      path = get_path(1, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_2':
      path = get_path(2, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_3':
      path = get_path(3, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_4':
      path = get_path(4, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_5':
      path = get_path(5, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_6':
      path = get_path(6, 'F', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024F-v1_7':
      path = get_path(7, 'F', '1',phipi=False)

   if args.dataset == 'data' and args.run == '2024G-v1_0':
      path = get_path(0, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_1':
      path = get_path(1, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_2':
      path = get_path(2, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_3':
      path = get_path(3, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_4':
      path = get_path(4, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_5':
      path = get_path(5, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_6':
      path = get_path(6, 'G', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024G-v1_7':
      path = get_path(7, 'G', '1',phipi=False)

   if args.dataset == 'data' and args.run == '2024H-v1_0':
      path = get_path(0, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_1':
      path = get_path(1, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_2':
      path = get_path(2, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_3':
      path = get_path(3, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_4':
      path = get_path(4, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_5':
      path = get_path(5, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_6':
      path = get_path(6, 'H', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024H-v1_7':
      path = get_path(7, 'H', '1',phipi=False)

   if args.dataset == 'data' and args.run == '2024I-v1_0':
      path = get_path(0, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_1':
      path = get_path(1, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_2':
      path = get_path(2, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_3':
      path = get_path(3, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_4':
      path = get_path(4, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_5':
      path = get_path(5, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_6':
      path = get_path(6, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v1_7':
      path = get_path(7, 'I', '1',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_0':
      path = get_path(0, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_1':
      path = get_path(1, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_2':
      path = get_path(2, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_3':
      path = get_path(3, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_4':
      path = get_path(4, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_5':
      path = get_path(5, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_6':
      path = get_path(6, 'I', '2',phipi=False)
   if args.dataset == 'data' and args.run == '2024I-v2_7':
      path = get_path(7, 'I', '2',phipi=False)



if args.anatype == 'control' and not "MC" in args.dataset:
   stream = args.run.split("_")[-1]
   era = args.run[4]

   if '2022' in args.run:
        path = get_path(stream, era, '0',phipi=True, year=2022)

   if '2023' in args.run:
        version = args.run[7]
        path = get_path(stream, era, version ,phipi=True, year=2023)

   if args.dataset == 'data_control' and args.run == '2024C-v1_0':
      path = get_path(0, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_1':
      path = get_path(1, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_2':
      path = get_path(2, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_3':
      path = get_path(3, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_4':
      path = get_path(4, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_5':
      path = get_path(5, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_6':
      path = get_path(6, 'C', '1')
   if args.dataset == 'data_control' and args.run == '2024C-v1_7':
      path = get_path(7, 'C', '1')


   if args.dataset == 'data_control' and args.run == '2024D-v1_0':
      path = get_path(0, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_1':
      path = get_path(1, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_2':
      path = get_path(2, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_3':
      path = get_path(3, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_4':
      path = get_path(4, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_5':
      path = get_path(5, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_6':
      path = get_path(6, 'D', '1')
   if args.dataset == 'data_control' and args.run == '2024D-v1_7':
      path = get_path(7, 'D', '1')

   if args.dataset == 'data_control' and args.run == '2024E-v1_0':
      path = get_path(0, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_1':
      path = get_path(1, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_2':
      path = get_path(2, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_3':
      path = get_path(3, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_4':
      path = get_path(4, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_5':
      path = get_path(5, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_6':
      path = get_path(6, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v1_7':
      path = get_path(7, 'E', '1')
   if args.dataset == 'data_control' and args.run == '2024E-v2_0':
      path = get_path(0, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_1':
      path = get_path(1, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_2':
      path = get_path(2, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_3':
      path = get_path(3, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_4':
      path = get_path(4, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_5':
      path = get_path(5, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_6':
      path = get_path(6, 'E', '2')
   if args.dataset == 'data_control' and args.run == '2024E-v2_7':
      path = get_path(7, 'E', '2')

   if args.dataset == 'data_control' and args.run == '2024F-v1_0':
      path = get_path(0, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_1':
      path = get_path(1, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_2':
      path = get_path(2, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_3':
      path = get_path(3, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_4':
      path = get_path(4, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_5':
      path = get_path(5, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_6':
      path = get_path(6, 'F', '1')
   if args.dataset == 'data_control' and args.run == '2024F-v1_7':
      path = get_path(7, 'F', '1')

   if args.dataset == 'data_control' and args.run == '2024G-v1_0':
      path = get_path(0, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_1':
      path = get_path(1, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_2':
      path = get_path(2, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_3':
      path = get_path(3, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_4':
      path = get_path(4, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_5':
      path = get_path(5, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_6':
      path = get_path(6, 'G', '1')
   if args.dataset == 'data_control' and args.run == '2024G-v1_7':
      path = get_path(7, 'G', '1')

   if args.dataset == 'data_control' and args.run == '2024H-v1_0':
      path = get_path(0, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_1':
      path = get_path(1, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_2':
      path = get_path(2, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_3':
      path = get_path(3, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_4':
      path = get_path(4, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_5':
      path = get_path(5, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_6':
      path = get_path(6, 'H', '1')
   if args.dataset == 'data_control' and args.run == '2024H-v1_7':
      path = get_path(7, 'H', '1')

   if args.dataset == 'data_control' and args.run == '2024I-v1_0':
      path = get_path(0, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_1':
      path = get_path(1, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_2':
      path = get_path(2, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_3':
      path = get_path(3, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_4':
      path = get_path(4, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_5':
      path = get_path(5, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_6':
      path = get_path(6, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v1_7':
      path = get_path(7, 'I', '1')
   if args.dataset == 'data_control' and args.run == '2024I-v2_0':
      path = get_path(0, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_1':
      path = get_path(1, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_2':
      path = get_path(2, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_3':
      path = get_path(3, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_4':
      path = get_path(4, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_5':
      path = get_path(5, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_6':
      path = get_path(6, 'I', '2')
   if args.dataset == 'data_control' and args.run == '2024I-v2_7':
      path = get_path(7, 'I', '2')



if args.anatype == 'phimunu' and not "MC" in args.datset:
   if args.dataset == 'data_phimunu' and args.run == '2022B':
      path = ''
   if args.dataset == 'data_phimunu' and args.run == '2022C_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsPhiMuNu_2022eraC_stream0_Mini_v3/240725_200149/'
   if args.dataset == 'data_phimunu' and args.run == '2022C_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsPhiMuNu_2022eraC_stream1_Mini_v3/240725_200219'
   if args.dataset == 'data_phimunu' and args.run == '2022C_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsPhiMuNu_2022eraC_stream2_Mini_v3/240725_200253'
   if args.dataset == 'data_phimunu' and args.run == '2022C_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsPhiMuNu_2022eraC_stream3_Mini_v3/240725_200324'
   if args.dataset == 'data_phimunu' and args.run == '2022C_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsPhiMuNu_2022eraC_stream4_Mini_v3/240725_200354'
   if args.dataset == 'data_phimunu' and args.run == '2022C_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsPhiMuNu_2022eraC_stream5_Mini_v3/240725_200424'
   if args.dataset == 'data_phimunu' and args.run == '2022C_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsPhiMuNu_2022eraC_stream6_Mini_v3/240725_200454'
   if args.dataset == 'data_phimunu' and args.run == '2022C_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsPhiMuNu_2022eraC_stream7_Mini_v3/240725_200524'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsPhiMuNu_2022eraD-v1_stream0_Mini_v3/240725_200903'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsPhiMuNu_2022eraD-v1_stream1_Mini_v3/240725_200933'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsPhiMuNu_2022eraD-v1_stream2_Mini_v3/240725_201006'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsPhiMuNu_2022eraD-v1_stream3_Mini_v3/240725_201036'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsPhiMuNu_2022eraD-v1_stream4_Mini_v3/240725_201108'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsPhiMuNu_2022eraD-v1_stream5_Mini_v3/240725_201137'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsPhiMuNu_2022eraD-v1_stream6_Mini_v3/240725_201208'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v1_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsPhiMuNu_2022eraD-v1_stream7_Mini_v3/240725_201237'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsPhiMuNu_2022eraD-v2_stream0_Mini_v3/240725_201407'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsPhiMuNu_2022eraD-v2_stream1_Mini_v3/240725_201437'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsPhiMuNu_2022eraD-v2_stream2_Mini_v3/240725_201508'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsPhiMuNu_2022eraD-v2_stream3_Mini_v3/240725_201538'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsPhiMuNu_2022eraD-v2_stream4_Mini_v3/240725_201609'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsPhiMuNu_2022eraD-v2_stream5_Mini_v3/240725_201640'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsPhiMuNu_2022eraD-v2_stream6_Mini_v3/240725_201710'
   if args.dataset == 'data_phimunu' and args.run == '2022D-v2_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsPhiMuNu_2022eraD-v2_stream7_Mini_v3/240725_201739'
   if args.dataset == 'data_phimunu' and args.run == '2022E_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsPhiMuNu_2022eraE_stream0_Mini_v3/240725_202012'
   if args.dataset == 'data_phimunu' and args.run == '2022E_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsPhiMuNu_2022eraE_stream1_Mini_v3/240725_202043'
   if args.dataset == 'data_phimunu' and args.run == '2022E_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsPhiMuNu_2022eraE_stream2_Mini_v3/240725_202115'
   if args.dataset == 'data_phimunu' and args.run == '2022E_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsPhiMuNu_2022eraE_stream3_Mini_v3/240725_202146'
   if args.dataset == 'data_phimunu' and args.run == '2022E_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsPhiMuNu_2022eraE_stream4_Mini_v3/240725_202216'
   if args.dataset == 'data_phimunu' and args.run == '2022E_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsPhiMuNu_2022eraE_stream5_Mini_v3/240725_202245'
   if args.dataset == 'data_phimunu' and args.run == '2022E_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsPhiMuNu_2022eraE_stream6_Mini_v3/240725_202316'
   if args.dataset == 'data_phimunu' and args.run == '2022E_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsPhiMuNu_2022eraE_stream7_Mini_v3/240725_202345'
   if args.dataset == 'data_phimunu' and args.run == '2022F_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsPhiMuNu_2022eraF_stream0_Mini_v3/240725_202614'
   if args.dataset == 'data_phimunu' and args.run == '2022F_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsPhiMuNu_2022eraF_stream1_Mini_v3/240725_202645'
   if args.dataset == 'data_phimunu' and args.run == '2022F_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsPhiMuNu_2022eraF_stream2_Mini_v3/240725_202716'
   if args.dataset == 'data_phimunu' and args.run == '2022F_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsPhiMuNu_2022eraF_stream3_Mini_v3/240725_202746'
   if args.dataset == 'data_phimunu' and args.run == '2022F_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsPhiMuNu_2022eraF_stream4_Mini_v3/240725_202817'
   if args.dataset == 'data_phimunu' and args.run == '2022F_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsPhiMuNu_2022eraF_stream5_Mini_v3/240725_202846'
   if args.dataset == 'data_phimunu' and args.run == '2022F_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsPhiMuNu_2022eraF_stream6_Mini_v3/240725_202915'
   if args.dataset == 'data_phimunu' and args.run == '2022F_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsPhiMuNu_2022eraF_stream7_Mini_v3/240725_202945'
   if args.dataset == 'data_phimunu' and args.run == '2022G_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsPhiMuNu_2022eraG_stream0_Mini_v3/240725_203125'
   if args.dataset == 'data_phimunu' and args.run == '2022G_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsPhiMuNu_2022eraG_stream1_Mini_v3/240725_203155'
   if args.dataset == 'data_phimunu' and args.run == '2022G_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsPhiMuNu_2022eraG_stream2_Mini_v3/240725_203225'
   if args.dataset == 'data_phimunu' and args.run == '2022G_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsPhiMuNu_2022eraG_stream3_Mini_v3/240725_203256'
   if args.dataset == 'data_phimunu' and args.run == '2022G_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsPhiMuNu_2022eraG_stream4_Mini_v3/240725_203326'
   if args.dataset == 'data_phimunu' and args.run == '2022G_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsPhiMuNu_2022eraG_stream5_Mini_v3/240725_203358'
   if args.dataset == 'data_phimunu' and args.run == '2022G_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsPhiMuNu_2022eraG_stream6_Mini_v3/240725_203429'
   if args.dataset == 'data_phimunu' and args.run == '2022G_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsPhiMuNu_2022eraG_stream7_Mini_v3/240725_203459'




if args.dataset == 'MC' and args.MCprocess == 'Ds':
    if args.year == "2022": 
        path = '/store/user/jschulte/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_v3/240815_170259'
    elif args.year == "2022EE": 
        path = '/store/user/jschulte/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_v3/240815_170259'
    elif args.year == "2023":    
        path = '/store/user/jschulte/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_2023_MCRun3_Ds_softMVAVars/250625_140742/'
    elif args.year == "2024":
        path = '/store/user/jschulte/DstoTau-Tauto3Mu_Fil-3Mu_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_2024_softMVAVars_v2/250605_201023/'
    else:    
        path = '/store/user/jschulte/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_2023BPix_MCRun3_Ds_new_Mini_v1/240909_140805'
if args.dataset == 'MC' and args.MCprocess == 'Bp':
   path = '/store/user/jschulte/Pythia8_BuTau3mu_Run3_2022/SkimTau3mu_MCRun3_Bu_Mini_v4/221214_073101'
if args.dataset == 'MC' and args.MCprocess == 'B0':
   path = '/store/user/jschulte/Pythia8_BdTau3mu_Run3_2022/SkimTau3mu_MCRun3_Bd_Mini_v4/221214_073125'
if args.dataset == 'MC' and args.MCprocess == 'DsPhiMuNu':
    if args.anatype == "phimunu":
        if args.year == "2023BPix":
            path = '/store/user/jschulte/DstoPhiMuNu_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_2023BPix_DsPhiMuNu_Mini_v3/240911_163342'
        else:    
            path = '/store/user/jschulte/DstoPhiMuNu_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimDsPhiMuNu_MCRun3_DsPhiMuNu_Mini_v3/240725_195013/'
    else:
        if args.year == "2022":
            path = '/store/user/jschulte/DstoPhiMuNu_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_DsPhiMuNu_Miniv4_2022_NewSamples_v1/241023_143228/'
        elif args.year == "2022EE":
            path = '/store/user/jschulte/DstoPhiMuNu_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_DsPhiMuNu_Miniv4_2022EE_NewSamples_v1/241023_142507/'
        elif args.year == "2023":
            path = '/store/user/jschulte/DstoPhiMuNu_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_DsPhiMuNu_Miniv4_2023_NewSamples_v1/241023_143730/'
        elif args.year == "2023BPix":    
            path = '/store/user/jschulte/DstoPhiMuNu_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_DsPhiMuNu_Miniv4_2023BPix_NewSamples_v1/241023_144017/'
        elif args.year == "2024":
            path = '/store/user/jschulte/DstoPhiMuNu-Phito2Mu_Fil-Mu_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_2024_MCRun3_DsPhiMuNu/250513_130344/'
if args.dataset == 'MC' and (args.MCprocess == 'DsPhiPi' or args.MCprocess == 'DsPhiPi2022'):
    if args.year == "2022": 
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2022_PS/250613_174530'
    elif args.year == "2022EE": 
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2022EE_PS/250613_174559/'
    elif args.year == "2023":    
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2023_PS/250613_174614/'
    elif args.year == '2024':
        path = '/store/user/jschulte/DstoPhiPi-Phito2Mu_Fil-Mu_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2024_softMVAVars/250620_134246/'
    else:    
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2023BPix_PS/250613_174647/'


print(path)
#generating the list of all .root files in given directory and subdirectories
fileList = []
for r, d, f in os.walk('/eos/purdue'+path): # r=root, d=directories, f = files
    for file in f:
        if '.root' in file:
            fileList.append(os.path.join(r.split('/eos/purdue')[-1], file))

#prepare final script
#final_script = open("submit_analysis_"+startTime+".sh", "w")
final_script = open("submit_analysis_"+output_name+".sh", "w")
final_script.write("#!/bin/bash\n")
final_script.write("cd "+output_name+"\n")
final_script.write("export VOMS_PATH=$(echo $(voms-proxy-info | grep path) | sed 's/path.*: //')\n")
final_script.write("export VOMS_USERID=$(echo $(voms-proxy-info | grep path) | sed 's/.*p_u//')\n")
final_script.write("export VOMS_TRG=/home/$USER/x509up_u$VOMS_USERID\n")
final_script.write("cp $VOMS_PATH $VOMS_TRG\n")
final_script.write("export X509_USER_PROXY=$VOMS_TRG\n")




#loop to generate one .cpp+executable+batch system conf file for each group of "n" files
n_chunk = len(fileList)//args.n
print('Number of files is {0:2d}'.format(len(fileList)))
print('Number of jobs is {0:2d}'.format(n_chunk+1))
print (args.dataset+args.MCprocess+'_'+args.anatype)
for file_index in range(n_chunk+1):
      chunk = '' 
      for idx, l in enumerate(fileList):
         if idx < args.n*(file_index+1) and idx >= args.n*file_index:
             l = l.rstrip()
             l = '        chain->AddFile("root://af-a00.cms.rcac.purdue.edu/{}");\n'.format(l)
             chunk = chunk + l
      #analysis.cpp template
      with open("templates/Analysis_template.cpp", "r") as in_file:
          buf = in_file.readlines()
      print (args.dataset, args.run, args.MCprocess, args.anatype, file_index)
      cpp_filename = "Analysis_"+args.dataset+"_"+args.run+args.MCprocess+"_"+args.anatype+"_chunk"+str(file_index)+".cpp"
      with open(cpp_filename, "w") as out_file:
          for lb in buf:
              if lb == '        //AddFile_'+args.dataset+args.MCprocess+'_'+args.anatype+'\n':
                  #write group of files
                  out_file.write(chunk)
              elif lb == '        //OutFile_'+args.dataset+args.MCprocess+'_'+args.anatype+'\n':
                  #write output file name
                  out_file.write('        fileout = "'+out_filename+str(file_index)+'.root";\n')
              else: out_file.write(lb)

              #elif lb == '            TString fileout = "AddOutput_'+args.dataset+args.MCprocess+'_'+args.anatype+'.root";\n':
                  #write output file name
               #   out_file.write('        TString fileout = "'+out_filename+str(file_index)+'.root";\n')
              #else: out_file.write(lb)

      #executable template
      with open("templates/launch_analysis_template.job", "r") as launch_infile:
          buf2 = launch_infile.readlines()

      launch_filename = "launch_analysis_"+args.dataset+"_"+args.run+args.MCprocess+"_"+args.anatype+"_"+str(file_index)+".job"
      with open(output_name+"/"+launch_filename, "w") as launch_outfile:
          for lb2 in buf2:
              if lb2 == "#compile\n":
                  launch_outfile.write("cd "+output_name+"\n")
                  launch_outfile.write("g++ -I $ROOTSYS/include ../"+cpp_filename+" `root-config --glibs` `root-config --libs` `root-config --cflags` -lTMVA -L $ROOTSYS/lib -o executable"+str(file_index)+"\n")
              elif lb2 == "#execute\n":
                  launch_outfile.write('./executable'+str(file_index)+option_string+'\n')
              else: launch_outfile.write(lb2)

      #myCondor template
      #with open("templates/my_HTCondor_template.job", "r") as myCondor_infile:
      #    buf3 = myCondor_infile.readlines()

      #condor_filename = "my_HTCondor_"+args.dataset+"_"+args.run+args.MCprocess+"_"+args.anatype+"_"+str(file_index)+".job"
      #with open(output_name+"/"+condor_filename, "w") as myCondor_outfile:
      #    for lb3 in buf3:
      #        if lb3 == "Executable = launch_analysis_template.job\n":
      #            myCondor_outfile.write("Executable = "+launch_filename+"\n")
      #        else: myCondor_outfile.write(lb3)

      #add lines to final script
      final_script.write("echo sbatch --mem=4G -N1 -n1 --time=12:00:00 --account=cms "+launch_filename+" \n")
      final_script.write("sbatch --mem=4G -N1 -n1 --time=12:00:00 --account=cms "+launch_filename+" \n")

final_script.close()
#submitName = "submit_analysis_"+startTime+".sh"
#source submitName
