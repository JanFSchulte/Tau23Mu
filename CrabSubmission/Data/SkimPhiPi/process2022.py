import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--submit', action='store_true')
parser.add_argument('-r', '--resubmit', action='store_true')

a = parser.parse_args()

portions = ['C', 'D', 'E', 'F', 'G']

eras = {'C': '10Dec2022',
        'D': '10Dec2022',
        'E': '10Dec2022',
        'F': '22Sep2023',
        'G': '22Sep2023',
        }

versions = {'C': '2',
        'D': '2',
        'E': '2',
        'F': '1',
        'G': '1',
        }


template = '''
from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimPhiPi_2022era{era}_stream{stream}_PS'
config.General.workArea = 'crab_projects2022'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/home/schul105/depot/Tau3Mu/analysis/el8/CMSSW_13_0_21/src/SkimTools/SkimPhiPi/test/{pset}'

config.Data.inputDataset = '/ParkingDoubleMuonLowMass{stream}/Run2022{era}-{version}-v{subversion}/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 50
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json'
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
        args["subversion"] = versions[portion]
        if (portion == 'C' or portion == 'D') and i == 1:
            args['subversion'] = '3'
        if (portion == 'G') and i == 4:
            args['subversion'] = 2
        args["version"] = eras[portion]
        args["era"] = portion
        args["stream"] = str(i)
        args['pset'] = 'run_Data2022A-D_DsPhiPiSkimAndTree_cfg.py'  
        if portion == "E" or portion == "F": args['pset'] = 'run_Data2022E-F_DsPhiPiSkimAndTree_cfg.py'
        elif portion == 'G': args['pset'] = 'run_Data2022G_DsPhiPiSkimAndTree_cfg.py'
        if a.submit:
            crabCfg = template.format(**args)

            cfgName = "crab_PhiPi_reco2022_Run{era}_stream{stream}_cfg.py".format(**args)
            with open(cfgName, "w") as text_file:
                text_file.write(crabCfg)
       
            subprocess.call(["crab", "submit", cfgName])
        if a.resubmit:
           folder = "crab_projects2022/crab_SkimPhiPi_2022era{era}_stream{stream}_PS".format(**args)
           print (folder)
           subprocess.call(['crab', 'resubmit', folder])
