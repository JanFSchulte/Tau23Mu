import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--submit', action='store_true')
parser.add_argument('-r', '--resubmit', action='store_true')

a = parser.parse_args()

portions = ['Cv1', 'Cv2', 'Cv3', 'Cv4', 'Dv1', 'Dv2']

eras = {'Cv1': 'C',
        'Cv2': 'C',
        'Cv3': 'C',
        'Cv4': 'C',
        'Dv1': 'D',
        'Dv2': 'D',
        }

versions = {'Cv1': 'v1',
        'Cv2': 'v2',
        'Cv3': 'v3',
        'Cv4': 'v4',
        'Dv1': 'v1',
        'Dv2': 'v2',
        }



template = '''
from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimPhiPi_2023era{era}_{version}_stream{stream}_PS'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/home/schul105/depot/Tau3Mu/analysis/el8/CMSSW_13_0_21/src/SkimTools/SkimPhiPi/test/run_Data2023_DsPhiPiSkimAndTree_cfg.py'

config.Data.inputDataset = '/ParkingDoubleMuonLowMass{stream}/Run2023{era}-22Sep2023_{version}-v{subversion}/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 50
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json'
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.publication = True
config.Data.outputDatasetTag = 'SkimPhiPi_2022era{era}_{version}_stream{stream}_PS'
config.JobType.allowUndistributedCMSSW = True
config.Site.storageSite = 'T2_US_Purdue'
config.Site.ignoreGlobalBlacklist  = True
'''



for portion in portions:

    for i in range(0,8):

        args = {}
        args["version"] = versions[portion]
        args["era"] = eras[portion]
        args["stream"] = str(i)
        args['subversion'] = "1"
        if i == 4 and portion == "Dv2": args['subversion'] = '2'
        if i == 3 and portion == "Cv4": args['subversion'] = '2'
        if i == 1 and portion == "Cv1": args['subversion'] = '2'
        if a.submit:
            crabCfg = template.format(**args)

            cfgName = "crab_PhiPi_reco2023_Run{era}_{version}_stream{stream}_cfg.py".format(**args)
            with open(cfgName, "w") as text_file:
                text_file.write(crabCfg)
       
            subprocess.call(["crab", "submit", cfgName])
        if a.resubmit:
           folder = "crab_projects/crab_SkimPhiPi_2023era{era}_{version}_stream{stream}_PS".format(**args)
           print (folder)
           subprocess.call(['crab', 'resubmit', folder])
