from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimDilepton_WithCuts_MCRun3_v2'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/depot/cms/users/schul105/Tau3Mu/analysis/CMSSW_15_0_6_patch1//src/SkimTools/SkimDilepton/test/run_InclusiveDilepton_SkimAndTree_withcuts_cfg.py'
config.Data.inputDataset = '/InclusiveDileptonMinBias_TuneCP5Plus_13p6TeV_pythia8/Run3Summer22MiniAODv4-validDigi_130X_mcRun3_2022_realistic_v5-v4/MINIAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2500
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'SkimDilepton_WithCuts_MCRun3'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 4000
config.Site.storageSite = 'T2_US_Purdue'
config.Site.ignoreGlobalBlacklist  = True
config.Data.allowNonValidInputDataset = True
