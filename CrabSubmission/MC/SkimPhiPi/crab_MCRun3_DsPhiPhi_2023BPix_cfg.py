from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimPhiPi_MCRun3_2023BPix_PS'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/home/schul105/depot/Tau3Mu/analysis/el8/CMSSW_13_0_21/src/SkimTools/SkimPhiPi/test/run_MC2023BPix_DsPhiPiSkimAndTree_cfg.py'
config.Data.inputDataset = '/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 2500
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'SkimPhiPi_MCRun3_2023BPix_PS'
config.JobType.allowUndistributedCMSSW = True 
config.Site.storageSite = 'T2_US_Purdue'
config.Site.ignoreGlobalBlacklist  = True

