from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimDilepton_MCRun3CandsOnly_Mini_v3'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_10/src/SkimTools/SkimDilepton/test/run_InclusiveDileptonCandsOnly_SkimAndTree_cfg.py'
config.Data.inputDataset = '/InclusiveDileptonMinBias_TuneCP5Plus_13p6TeV_pythia8/Run3Summer22MiniAODv3-Pilot_124X_mcRun3_2022_realistic_v12-v5/MINIAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2500
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'SkimDilepton_MCRun3CandsPnly_Mini_v3'
config.JobType.allowUndistributedCMSSW = True 
config.Site.storageSite = 'T2_US_Purdue'
config.Site.ignoreGlobalBlacklist  = True