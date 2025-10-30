from CRABClient.UserUtilities import config, getUsername
config = config()

config.General.requestName = 'SkimTau3mu_MCRun3_Ds_2024_softMVAVars_v2'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'


config.JobType.psetName = '/home/schul105/depot/Tau3Mu/analysis/CMSSW_15_0_6_patch1/src/SkimTools/SkimTau3Mu/test/run_MC2024_PatAndTree_cfg.py'
config.Data.inputDataset = '/DstoTau-Tauto3Mu_Fil-3Mu_TuneCP5_13p6TeV_pythia8-evtgen/RunIII2024Summer24MiniAOD-140X_mcRun3_2024_realistic_v26-v4/MINIAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 2500
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'SkimTau3mu_MCRun3_Ds_2024_softMVAVars_v2'
config.JobType.allowUndistributedCMSSW = True 
config.Site.storageSite = 'T2_US_Purdue'
config.Site.ignoreGlobalBlacklist  = True

