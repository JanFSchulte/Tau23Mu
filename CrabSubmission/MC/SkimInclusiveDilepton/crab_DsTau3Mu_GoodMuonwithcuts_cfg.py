from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimDilepton_DsTau3Mu_GoodMuonWithCuts_MCRun3_v4'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/depot/cms/users/schul105/Tau3Mu/analysis/CMSSW_15_0_6_patch1//src/SkimTools/SkimDilepton/test/run_InclusiveDilepton_GoodMuonSkimAndTree_withcuts_cfg.py'
config.Data.inputDataset = '/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'SkimDilepton_DsTauMu_WithCuts_MCRun3_v3'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 10000
config.JobType.numCores = 4
config.Site.storageSite = 'T2_US_Purdue'
config.Site.ignoreGlobalBlacklist  = True
config.Data.allowNonValidInputDataset = True
