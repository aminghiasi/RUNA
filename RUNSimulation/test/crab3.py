from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'name_v7125'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'PrivateMC'
config.JobType.generator = 'lhe'
config.JobType.psetName = 'test'

config.Data.outputPrimaryDataset = 'NAME'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 2000
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'GENSIM_Moriond17'
config.Site.storageSite = 'T3_US_FNALLPC'

