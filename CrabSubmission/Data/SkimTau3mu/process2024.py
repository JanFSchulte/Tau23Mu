import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--submit', action='store_true')
parser.add_argument('-r', '--resubmit', action='store_true')

a = parser.parse_args()

#portions = ['Cv1', 'Cv2', 'Cv3', 'Cv4', 'Dv1', 'Dv2']
portions = ['C', 'D','Ev1', 'Ev2','F', 'G','H', 'Iv1', 'Iv2']

'''
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
'''

eras = {'Ev1': 'E',
	'Ev2': 'E',
	'Iv1': 'I',
	'Iv2': 'I',
	'C': 'C',
	'D': 'D',
	'F': 'F',
	'G': 'G',
	'H': 'H'}

versions = {'Ev1': 'v1',
	    'Ev2': 'v2',
	    'Iv1': 'v1',
	    'Iv2': 'v2',
	    'C': 'v1',
	    'D': 'v1',
	    'F': 'v1',
	    'G': 'v1',
	    'H': 'v1'}

template = '''
from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimDsTau3mu_2024era{era}_{version}_stream{stream}_Mini_v1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/depot/cms/users/simon73/Run3Tau3Mu_3/CMSSW_14_0_18/src/SkimTools/SkimTau3Mu/test/run_Data2024_PatAndTree_cfg.py'

config.Data.inputDataset = '/ParkingDoubleMuonLowMass{stream}/Run2024{era}-PromptReco-{version}/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 50
config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_378981_386951_Golden.json'
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.publication = True
config.Data.outputDatasetTag = 'SkimDsTau3mu_2024era{era}_{version}_stream{stream}_Mini_v1'
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
        #print("crab_Tau3Mu_reco2024_Run{era}_{version}_stream{stream}_cfg.py".format(**args))
        #continue
        #if i == 4 and portion == "Dv2": args['subversion'] = '2'
        #if i == 3 and portion == "Cv4": args['subversion'] = '2'
        #if i == 1 and portion == "Cv1": args['subversion'] = '2'
        if a.submit:
            crabCfg = template.format(**args)

            cfgName = "crab_Tau3Mu_reco2024_Run{era}_{version}_stream{stream}_cfg.py".format(**args)
            with open(cfgName, "w") as text_file:
                text_file.write(crabCfg)

            subprocess.call(["crab", "submit", cfgName])
        if a.resubmit:
           folder = "crab_projects/crab_SkimTau3Mu_2024era{era}_{version}_stream{stream}_Mini_v1".format(**args)
           print (folder)
           subprocess.call(['crab', 'resubmit', folder])
