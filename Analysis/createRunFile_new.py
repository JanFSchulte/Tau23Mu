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
parser.add_argument("dataset", type=str, choices=['data', 'data_control','data_phimunu', 'MC'], help="Specify if data or Monte Carlo")
parser.add_argument("year", type=str, choices=['2022', '2022EE','2023', '2023BPix', '2024'], help="Specify year of Monte Carlo")
parser.add_argument("anatype", type=str, choices=['tau3mu', 'control','phimunu'], help="Specify analysis type")
#parser.add_argument("--run", type=str, default='', choices=['2022B', '2022C_0', '2022C_1', '2022C_2', '2022C_3', '2022C_4', '2022C_5', '2022C_6', '2022C_7', '2022D_0', '2022D_1', '2022D_2', '2022D_3', '2022D_4', '2022D_5', '2022D_6', '2022D_7', '2022D-v1_0', '2022D-v1_1', '2022D-v1_2', '2022D-v1_3', '2022D-v1_4', '2022D-v1_5', '2022D-v1_6', '2022D-v1_7', '2022D-v2_0', '2022D-v2_1', '2022D-v2_2', '2022D-v2_3', '2022D-v2_4', '2022D-v2_5', '2022D-v2_6', '2022D-v2_7', '2022E_0', '2022E_1', '2022E_2', '2022E_3', '2022E_4', '2022E_5', '2022E_6', '2022E_7', '2022F_0', '2022F_1', '2022F_2', '2022F_3', '2022F_4', '2022F_5', '2022F_6', '2022F_7', '2022G_0', '2022G_1', '2022G_2', '2022G_3', '2022G_4', '2022G_5', '2022G_6', '2022G_7', '2023C-v1_0', '2023C-v1_1', '2023C-v1_2', '2023C-v1_3', '2023C-v1_4', '2023C-v1_5', '2023C-v1_6', '2023C-v1_7', '2023C-v2_0', '2023C-v2_1', '2023C-v2_2', '2023C-v2_3', '2023C-v2_4', '2023C-v2_5', '2023C-v2_6', '2023C-v2_7', '2023C-v3_0', '2023C-v3_1', '2023C-v3_2', '2023C-v3_3', '2023C-v3_4', '2023C-v3_5', '2023C-v3_6', '2023C-v3_7', '2023C-v4_0', '2023C-v4_1', '2023C-v4_2', '2023C-v4_3', '2023C-v4_4', '2023C-v4_5', '2023C-v4_6', '2023C-v4_7', '2023D-v1_0', '2023D-v1_1', '2023D-v1_2', '2023D-v1_3', '2023D-v1_4', '2023D-v1_5', '2023D-v1_6', '2023D-v1_7', '2023D-v2_0', '2023D-v2_1', '2023D-v2_2', '2023D-v2_3', '2023D-v2_4', '2023D-v2_5', '2023D-v2_6', '2023D-v2_7'], help="run in data")
parser.add_argument("--run", type=str)

# Optional Arguments
parser.add_argument("--outName", type=str, default="test", help="Specify name for output files")
parser.add_argument("--n", type=int, default=255, help="number of .root files per job")
parser.add_argument("--MCprocess", type=str, default='', choices=['Ds', 'B0', 'Bp', 'DsPhiPi', 'DsPhiMuNu'], help="process in Monte Carlo")
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
elif args.dataset == 'data_phimunu':
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.run+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+temp.replace("_phimunu","")+'" "'+args.run+'"'
elif args.dataset == 'MC':
   out_filename = 'AnalysedTree_'+args.dataset+'_'+args.MCprocess+'_'+args.anatype
   temp = '_'+args.anatype
   option_string = ' "'+args.dataset+temp.replace("_tau3mu","")+'" "'+args.MCprocess+'"'

#startTime = datetime.datetime.now().strftime("%Y%m%d_%H%M")

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

if args.anatype == 'tau3mu':
   #### 2022
   if args.dataset == 'data' and args.run == '2022B':
      path = '' 
   if args.dataset == 'data' and args.run == '2022C_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_stream0_Mini_v3/240725_160353' 
   if args.dataset == 'data' and args.run == '2022C_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_stream1_Mini_v3/240725_160422'
   if args.dataset == 'data' and args.run == '2022C_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_stream2_Mini_v3/240725_160452' 
   if args.dataset == 'data' and args.run == '2022C_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_stream3_Mini_v3/240725_160521' 
   if args.dataset == 'data' and args.run == '2022C_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_stream4_Mini_v3/240725_160550' 
   if args.dataset == 'data' and args.run == '2022C_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_stream5_Mini_v3/240725_160620' 
   if args.dataset == 'data' and args.run == '2022C_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_stream6_Mini_v3/240725_160649' 
   if args.dataset == 'data' and args.run == '2022C_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_stream7_Mini_v3/240725_160718' 
   if args.dataset == 'data' and args.run == '2022D-v1_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD-v1_stream0_Mini_v3/240725_175346'
   if args.dataset == 'data' and args.run == '2022D-v1_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD-v1_stream1_Mini_v3/240725_175416'
   if args.dataset == 'data' and args.run == '2022D-v1_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD-v1_stream2_Mini_v3/240725_175446'
   if args.dataset == 'data' and args.run == '2022D-v1_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD-v1_stream3_Mini_v3/240725_175515'
   if args.dataset == 'data' and args.run == '2022D-v1_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD-v1_stream4_Mini_v3/240725_175545'
   if args.dataset == 'data' and args.run == '2022D-v1_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD-v1_stream5_Mini_v3/240725_175614'
   if args.dataset == 'data' and args.run == '2022D-v1_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD-v1_stream6_Mini_v3/240725_175644'
   if args.dataset == 'data' and args.run == '2022D-v1_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD-v1_stream7_Mini_v3/240725_175714'
   if args.dataset == 'data' and args.run == '2022D-v2_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD-v2_stream0_Mini_v3/240725_174955'
   if args.dataset == 'data' and args.run == '2022D-v2_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD-v2_stream1_Mini_v3/240725_175025'
   if args.dataset == 'data' and args.run == '2022D-v2_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD-v2_stream2_Mini_v3/240725_175054'
   if args.dataset == 'data' and args.run == '2022D-v2_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD-v2_stream3_Mini_v3/240725_175123'
   if args.dataset == 'data' and args.run == '2022D-v2_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD-v2_stream4_Mini_v3/240725_175156'
   if args.dataset == 'data' and args.run == '2022D-v2_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD-v2_stream5_Mini_v3/240725_175226'
   if args.dataset == 'data' and args.run == '2022D-v2_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD-v2_stream6_Mini_v3/240725_175255'
   if args.dataset == 'data' and args.run == '2022D-v2_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD-v2_stream7_Mini_v3/240725_175324'
   if args.dataset == 'data' and args.run == '2022E_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraE_stream0_Mini_v3/240725_174548'
   if args.dataset == 'data' and args.run == '2022E_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraE_stream1_Mini_v3/240725_174618'
   if args.dataset == 'data' and args.run == '2022E_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraE_stream2_Mini_v3/240725_174647'
   if args.dataset == 'data' and args.run == '2022E_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraE_stream3_Mini_v3/240725_174717'
   if args.dataset == 'data' and args.run == '2022E_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraE_stream4_Mini_v3/240725_174746'
   if args.dataset == 'data' and args.run == '2022E_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraE_stream5_Mini_v3/240725_174816'
   if args.dataset == 'data' and args.run == '2022E_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraE_stream6_Mini_v3/240725_174847'
   if args.dataset == 'data' and args.run == '2022E_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraE_stream7_Mini_v3/240725_174918'
   if args.dataset == 'data' and args.run == '2022F_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraF_stream0_Mini_v3/240725_174201'
   if args.dataset == 'data' and args.run == '2022F_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraF_stream1_Mini_v3/240725_174231'
   if args.dataset == 'data' and args.run == '2022F_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraF_stream2_Mini_v3/240725_174301'
   if args.dataset == 'data' and args.run == '2022F_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraF_stream3_Mini_v3/240725_174331'
   if args.dataset == 'data' and args.run == '2022F_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraF_stream4_Mini_v3/240725_174400'
   if args.dataset == 'data' and args.run == '2022F_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraF_stream5_Mini_v3/240725_174429'
   if args.dataset == 'data' and args.run == '2022F_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraF_stream6_Mini_v3/240725_174458'
   if args.dataset == 'data' and args.run == '2022F_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraF_stream7_Mini_v3/240725_174528'
   if args.dataset == 'data' and args.run == '2022G_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraG_stream0_Mini_v3/240725_173710'
   if args.dataset == 'data' and args.run == '2022G_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraG_stream1_Mini_v3/240725_173739'
   if args.dataset == 'data' and args.run == '2022G_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraG_stream2_Mini_v3/240725_173809'
   if args.dataset == 'data' and args.run == '2022G_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraG_stream3_Mini_v3/240725_173838'
   if args.dataset == 'data' and args.run == '2022G_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraG_stream4_Mini_v3/240725_173907'
   if args.dataset == 'data' and args.run == '2022G_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraG_stream5_Mini_v3/240725_173937'
   if args.dataset == 'data' and args.run == '2022G_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraG_stream6_Mini_v3/240725_174006'
   if args.dataset == 'data' and args.run == '2022G_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraG_stream7_Mini_v3/240725_174036'
   if args.dataset == 'data' and args.run == '2023C-v1_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_v1_stream0_Mini_v1/240909_133532'
   if args.dataset == 'data' and args.run == '2023C-v1_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_v1_stream1_Mini_v1/240911_132059'
   if args.dataset == 'data' and args.run == '2023C-v1_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_v1_stream2_Mini_v1/240909_135245'
   if args.dataset == 'data' and args.run == '2023C-v1_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_v1_stream3_Mini_v1/240909_135255'
   if args.dataset == 'data' and args.run == '2023C-v1_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_v1_stream4_Mini_v1/240909_135304'
   if args.dataset == 'data' and args.run == '2023C-v1_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_v1_stream5_Mini_v1/240909_135313'
   if args.dataset == 'data' and args.run == '2023C-v1_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_v1_stream6_Mini_v1/240909_135323'
   if args.dataset == 'data' and args.run == '2023C-v1_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_v1_stream7_Mini_v1/240909_135333'
   if args.dataset == 'data' and args.run == '2023C-v2_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_v2_stream0_Mini_v1/240909_135342'
   if args.dataset == 'data' and args.run == '2023C-v2_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_v2_stream1_Mini_v1/240909_135350'
   if args.dataset == 'data' and args.run == '2023C-v2_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_v2_stream2_Mini_v1/240909_135400'
   if args.dataset == 'data' and args.run == '2023C-v2_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_v2_stream3_Mini_v1/240909_135409'
   if args.dataset == 'data' and args.run == '2023C-v2_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_v2_stream4_Mini_v1/240909_135418'
   if args.dataset == 'data' and args.run == '2023C-v2_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_v2_stream5_Mini_v1/240909_135427'
   if args.dataset == 'data' and args.run == '2023C-v2_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_v2_stream6_Mini_v1/240909_135440'
   if args.dataset == 'data' and args.run == '2023C-v2_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_v2_stream7_Mini_v1/240909_135449'
   if args.dataset == 'data' and args.run == '2023C-v3_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_v3_stream0_Mini_v1/240909_135458'
   if args.dataset == 'data' and args.run == '2023C-v3_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_v3_stream1_Mini_v1/240909_135508'
   if args.dataset == 'data' and args.run == '2023C-v3_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_v3_stream2_Mini_v1/240909_135517'
   if args.dataset == 'data' and args.run == '2023C-v3_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_v3_stream3_Mini_v1/240909_135527'
   if args.dataset == 'data' and args.run == '2023C-v3_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_v3_stream4_Mini_v1/240909_135536'
   if args.dataset == 'data' and args.run == '2023C-v3_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_v3_stream5_Mini_v1/240909_135546'
   if args.dataset == 'data' and args.run == '2023C-v3_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_v3_stream6_Mini_v1/240909_135556'
   if args.dataset == 'data' and args.run == '2023C-v3_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_v3_stream7_Mini_v1/240909_135604'
   if args.dataset == 'data' and args.run == '2023C-v4_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_v4_stream0_Mini_v1/240909_135615'
   if args.dataset == 'data' and args.run == '2023C-v4_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_v4_stream1_Mini_v1/240909_135625'
   if args.dataset == 'data' and args.run == '2023C-v4_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_v4_stream2_Mini_v1/240909_135635'
   if args.dataset == 'data' and args.run == '2023C-v4_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_v4_stream3_Mini_v1/240911_132143'
   if args.dataset == 'data' and args.run == '2023C-v4_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_v4_stream4_Mini_v1/240909_135658'
   if args.dataset == 'data' and args.run == '2023C-v4_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_v4_stream5_Mini_v1/240909_135709'
   if args.dataset == 'data' and args.run == '2023C-v4_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_v4_stream6_Mini_v1/240909_135718'
   if args.dataset == 'data' and args.run == '2023C-v4_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_v4_stream7_Mini_v1/240909_135728'
   if args.dataset == 'data' and args.run == '2023D-v1_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraD_v1_stream0_Mini_v1/240909_135737'
   if args.dataset == 'data' and args.run == '2023D-v1_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraD_v1_stream1_Mini_v1/240909_135750'
   if args.dataset == 'data' and args.run == '2023D-v1_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraD_v1_stream2_Mini_v1/240909_135759'
   if args.dataset == 'data' and args.run == '2023D-v1_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraD_v1_stream3_Mini_v1/240909_135808'
   if args.dataset == 'data' and args.run == '2023D-v1_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraD_v1_stream4_Mini_v1/240909_135822'
   if args.dataset == 'data' and args.run == '2023D-v1_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraD_v1_stream5_Mini_v1/240909_135831'
   if args.dataset == 'data' and args.run == '2023D-v1_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraD_v1_stream6_Mini_v1/240909_135841'
   if args.dataset == 'data' and args.run == '2023D-v1_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraD_v1_stream7_Mini_v1/240909_135851'
   if args.dataset == 'data' and args.run == '2023D-v2_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraD_v2_stream0_Mini_v1/240909_135900'
   if args.dataset == 'data' and args.run == '2023D-v2_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraD_v2_stream1_Mini_v1/240909_135909'
   if args.dataset == 'data' and args.run == '2023D-v2_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraD_v2_stream2_Mini_v1/240909_135918'
   if args.dataset == 'data' and args.run == '2023D-v2_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraD_v2_stream3_Mini_v1/240909_135929'
   if args.dataset == 'data' and args.run == '2023D-v2_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraD_v2_stream4_Mini_v1/240911_132214'
   if args.dataset == 'data' and args.run == '2023D-v2_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraD_v2_stream5_Mini_v1/240909_140002'
   if args.dataset == 'data' and args.run == '2023D-v2_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraD_v2_stream6_Mini_v1/240909_140011'
   if args.dataset == 'data' and args.run == '2023D-v2_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraD_v2_stream7_Mini_v1/240909_140025'



if args.anatype == 'control':
   if args.dataset == 'data_control' and args.run == '2022C_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraC_10Dec2022_stream0_Mini_v1/241002_185219'
   if args.dataset == 'data_control' and args.run == '2022C_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraC_10Dec2022_stream1_Mini_v1/241002_185648'
   if args.dataset == 'data_control' and args.run == '2022C_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraC_10Dec2022_stream2_Mini_v1/241002_185905'
   if args.dataset == 'data_control' and args.run == '2022C_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraC_10Dec2022_stream3_Mini_v1/241002_190338'
   if args.dataset == 'data_control' and args.run == '2022C_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraC_10Dec2022_stream4_Mini_v1/241002_190347'
   if args.dataset == 'data_control' and args.run == '2022C_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraC_10Dec2022_stream5_Mini_v1/241002_190355'
   if args.dataset == 'data_control' and args.run == '2022C_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraC_10Dec2022_stream6_Mini_v1/241002_190402'
   if args.dataset == 'data_control' and args.run == '2022C_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraC_10Dec2022_stream7_Mini_v1/241002_190410'
   if args.dataset == 'data_control' and args.run == '2022D_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraD_10Dec2022_stream0_Mini_v1/241002_191052'
   if args.dataset == 'data_control' and args.run == '2022D_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraD_10Dec2022_stream1_Mini_v1/241002_191312'
   if args.dataset == 'data_control' and args.run == '2022D_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraD_10Dec2022_stream2_Mini_v1/241002_191530'
   if args.dataset == 'data_control' and args.run == '2022D_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraD_10Dec2022_stream3_Mini_v1/241002_191538'
   if args.dataset == 'data_control' and args.run == '2022D_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraD_10Dec2022_stream4_Mini_v1/241002_192640'
   if args.dataset == 'data_control' and args.run == '2022D_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraD_10Dec2022_stream5_Mini_v1/241002_192650'
   if args.dataset == 'data_control' and args.run == '2022D_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraD_10Dec2022_stream6_Mini_v1/241002_193121'
   if args.dataset == 'data_control' and args.run == '2022D_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraD_10Dec2022_stream7_Mini_v1/241002_193340'
   if args.dataset == 'data_control' and args.run == '2022E_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraE_10Dec2022_stream0_Mini_v1/241002_194021'
   if args.dataset == 'data_control' and args.run == '2022E_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraE_10Dec2022_stream1_Mini_v1/241002_194239'
   if args.dataset == 'data_control' and args.run == '2022E_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraE_10Dec2022_stream2_Mini_v1/241002_194249'
   if args.dataset == 'data_control' and args.run == '2022E_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraE_10Dec2022_stream3_Mini_v1/241002_194719'
   if args.dataset == 'data_control' and args.run == '2022E_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraE_10Dec2022_stream4_Mini_v1/241002_194728'
   if args.dataset == 'data_control' and args.run == '2022E_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraE_10Dec2022_stream5_Mini_v1/241002_194945'
   if args.dataset == 'data_control' and args.run == '2022E_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraE_10Dec2022_stream6_Mini_v1/241002_194953'
   if args.dataset == 'data_control' and args.run == '2022E_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraE_10Dec2022_stream7_Mini_v1/241002_195002'
   if args.dataset == 'data_control' and args.run == '2022F_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraF_22Sep2023_stream0_Mini_v1/241002_195010'
   if args.dataset == 'data_control' and args.run == '2022F_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraF_22Sep2023_stream1_Mini_v1/241002_195017'
   if args.dataset == 'data_control' and args.run == '2022F_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraF_22Sep2023_stream2_Mini_v1/241002_195235'
   if args.dataset == 'data_control' and args.run == '2022F_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraF_22Sep2023_stream3_Mini_v1/241002_195703'
   if args.dataset == 'data_control' and args.run == '2022F_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraF_22Sep2023_stream4_Mini_v1/241002_195712'
   if args.dataset == 'data_control' and args.run == '2022F_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraF_22Sep2023_stream5_Mini_v1/241002_195721'
   if args.dataset == 'data_control' and args.run == '2022F_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraF_22Sep2023_stream6_Mini_v1/241002_195729'
   if args.dataset == 'data_control' and args.run == '2022F_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraF_22Sep2023_stream7_Mini_v1/241002_195948'
   if args.dataset == 'data_control' and args.run == '2022G_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraG_22Sep2023_stream0_Mini_v1/241002_195955'
   if args.dataset == 'data_control' and args.run == '2022G_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraG_22Sep2023_stream1_Mini_v1/241002_200632'
   if args.dataset == 'data_control' and args.run == '2022G_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraG_22Sep2023_stream2_Mini_v1/241002_200641'
   if args.dataset == 'data_control' and args.run == '2022G_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraG_22Sep2023_stream3_Mini_v1/241002_200902'
   if args.dataset == 'data_control' and args.run == '2022G_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraG_22Sep2023_stream4_Mini_v1/'
   if args.dataset == 'data_control' and args.run == '2022G_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraG_22Sep2023_stream5_Mini_v1/241002_201551'
   if args.dataset == 'data_control' and args.run == '2022G_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraG_22Sep2023_stream6_Mini_v1/241002_201600'
   if args.dataset == 'data_control' and args.run == '2022G_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraG_22Sep2023_stream7_Mini_v1/241002_201608'

   if args.dataset == 'data_control' and args.run == '2023C-v1_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraC_v1_stream0_Mini_v1/241002_143019'
   if args.dataset == 'data_control' and args.run == '2023C-v1_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraC_v1_stream1_Mini_v1/241002_143237'
   if args.dataset == 'data_control' and args.run == '2023C-v1_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraC_v1_stream2_Mini_v1/241002_143245'
   if args.dataset == 'data_control' and args.run == '2023C-v1_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraC_v1_stream3_Mini_v1/241002_143503'
   if args.dataset == 'data_control' and args.run == '2023C-v1_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraC_v1_stream4_Mini_v1/241002_143512'
   if args.dataset == 'data_control' and args.run == '2023C-v1_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraC_v1_stream5_Mini_v1/241002_144156'
   if args.dataset == 'data_control' and args.run == '2023C-v1_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraC_v1_stream6_Mini_v1/241002_144206'
   if args.dataset == 'data_control' and args.run == '2023C-v1_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraC_v1_stream7_Mini_v1/241002_144215'
   if args.dataset == 'data_control' and args.run == '2023C-v2_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraC_v2_stream0_Mini_v1/241002_144854'
   if args.dataset == 'data_control' and args.run == '2023C-v2_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraC_v2_stream1_Mini_v1/241002_145113'
   if args.dataset == 'data_control' and args.run == '2023C-v2_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraC_v2_stream2_Mini_v1/241002_145543'
   if args.dataset == 'data_control' and args.run == '2023C-v2_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraC_v2_stream3_Mini_v1/241002_150012'
   if args.dataset == 'data_control' and args.run == '2023C-v2_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraC_v2_stream4_Mini_v1/241002_150231'
   if args.dataset == 'data_control' and args.run == '2023C-v2_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraC_v2_stream5_Mini_v1/241002_150450'
   if args.dataset == 'data_control' and args.run == '2023C-v2_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraC_v2_stream6_Mini_v1/241002_150709'
   if args.dataset == 'data_control' and args.run == '2023C-v2_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraC_v2_stream7_Mini_v1/241002_151138'
   if args.dataset == 'data_control' and args.run == '2023C-v3_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraC_v3_stream0_Mini_v1/241002_151606'
   if args.dataset == 'data_control' and args.run == '2023C-v3_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraC_v3_stream1_Mini_v1/241002_151615'
   if args.dataset == 'data_control' and args.run == '2023C-v3_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraC_v3_stream2_Mini_v1/241002_152044'
   if args.dataset == 'data_control' and args.run == '2023C-v3_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraC_v3_stream3_Mini_v1/241002_152303'
   if args.dataset == 'data_control' and args.run == '2023C-v3_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraC_v3_stream4_Mini_v1/241002_152527'
   if args.dataset == 'data_control' and args.run == '2023C-v3_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraC_v3_stream5_Mini_v1/241002_152955'
   if args.dataset == 'data_control' and args.run == '2023C-v3_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraC_v3_stream6_Mini_v1/241002_153005'
   if args.dataset == 'data_control' and args.run == '2023C-v3_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraC_v3_stream7_Mini_v1/241002_153225'
   if args.dataset == 'data_control' and args.run == '2023C-v4_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraC_v4_stream0_Mini_v1/241002_153233'
   if args.dataset == 'data_control' and args.run == '2023C-v4_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraC_v4_stream1_Mini_v1/241002_153450'
   if args.dataset == 'data_control' and args.run == '2023C-v4_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraC_v4_stream2_Mini_v1/241002_153918'
   if args.dataset == 'data_control' and args.run == '2023C-v4_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraC_v4_stream3_Mini_v1/241002_154351'
   if args.dataset == 'data_control' and args.run == '2023C-v4_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraC_v4_stream4_Mini_v1/241002_154817'
   if args.dataset == 'data_control' and args.run == '2023C-v4_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraC_v4_stream5_Mini_v1/241002_155036'
   if args.dataset == 'data_control' and args.run == '2023C-v4_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraC_v4_stream6_Mini_v1/241002_155051'
   if args.dataset == 'data_control' and args.run == '2023C-v4_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraC_v4_stream7_Mini_v1/241002_155943'
   if args.dataset == 'data_control' and args.run == '2023D-v1_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraD_v1_stream0_Mini_v1/241002_160414'
   if args.dataset == 'data_control' and args.run == '2023D-v1_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraD_v1_stream1_Mini_v1/241002_160635'
   if args.dataset == 'data_control' and args.run == '2023D-v1_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraD_v1_stream2_Mini_v1/241002_161103'
   if args.dataset == 'data_control' and args.run == '2023D-v1_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraD_v1_stream3_Mini_v1/241002_161322'
   if args.dataset == 'data_control' and args.run == '2023D-v1_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraD_v1_stream4_Mini_v1/241002_161542'
   if args.dataset == 'data_control' and args.run == '2023D-v1_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraD_v1_stream5_Mini_v1/241002_161801'
   if args.dataset == 'data_control' and args.run == '2023D-v1_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraD_v1_stream6_Mini_v1/241002_161809'
   if args.dataset == 'data_control' and args.run == '2023D-v1_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraD_v1_stream7_Mini_v1/241002_161819'
   if args.dataset == 'data_control' and args.run == '2023D-v2_0':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass0/SkimPhiPi_2022eraD_v2_stream0_Mini_v1/241002_162036'
   if args.dataset == 'data_control' and args.run == '2023D-v2_1':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass1/SkimPhiPi_2022eraD_v2_stream1_Mini_v1/241002_162044'
   if args.dataset == 'data_control' and args.run == '2023D-v2_2':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass2/SkimPhiPi_2022eraD_v2_stream2_Mini_v1/241002_162052'
   if args.dataset == 'data_control' and args.run == '2023D-v2_3':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass3/SkimPhiPi_2022eraD_v2_stream3_Mini_v1/241002_162100'
   if args.dataset == 'data_control' and args.run == '2023D-v2_4':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass4/SkimPhiPi_2022eraD_v2_stream4_Mini_v1/241002_162318'
   if args.dataset == 'data_control' and args.run == '2023D-v2_5':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass5/SkimPhiPi_2022eraD_v2_stream5_Mini_v1/241002_162536'
   if args.dataset == 'data_control' and args.run == '2023D-v2_6':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass6/SkimPhiPi_2022eraD_v2_stream6_Mini_v1/241002_163004'
   if args.dataset == 'data_control' and args.run == '2023D-v2_7':
      path = '/store/user/jschulte/ParkingDoubleMuonLowMass7/SkimPhiPi_2022eraD_v2_stream7_Mini_v1/241002_163013'
   
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



if args.anatype == 'phimunu':
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
        path = '/store/user/jschulte/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_2023_MCRun3_Ds_new_Mini_v1/240909_140412'
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
            path = '/store/user/bsimon/DstoPhiMuNu-Phito2Mu_Fil-Mu_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiMuNu_MCRun3_2024/250407_172728/'
if args.dataset == 'MC' and args.MCprocess == 'DsPhiPi':
    if args.year == "2022": 
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2022/241002_193241'
    elif args.year == "2022EE": 
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2022EE/241002_193403/'
    elif args.year == "2023":    
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2023/241002_193902/'
    elif args.year == '2024':
        path = '/store/user/bsimon/DstoPhiPi-Phito2Mu_Fil-Mu_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2024/250407_172148'
    else:    
        path = '/store/user/jschulte/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_2023BPix/241002_194239/'


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
