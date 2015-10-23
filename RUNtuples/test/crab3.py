from CRABClient.UserUtilities import config
config = config()

name = 'RunIISpring15DR74_RUNA_Asympt25ns'
version = 'v08'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
config.JobType.pyCfgParams = [ 'DataProcessing=MC25ns' ]
config.JobType.inputFiles = [ 'Summer15_25nsV5_MC.db' ]
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 1
config.Data.totalUnits = 2000
config.Data.publication = True
config.Data.ignoreLocality = True
config.Data.publishDataName = name+'_'+version

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):

	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand
	from multiprocessing import Process

	QCDHT = [ 
			'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_newMiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			'/RPVSt200tobj_13TeV_pythia8/algomez-RunIISpring15DR74_newMiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			'/RPVSt350tobj_13TeV_pythia8/algomez-RunIISpring15DR74_newMiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			]
	
	for dataset in QCDHT:
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+'_'+version
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+name+'_'+version
		config.General.requestName = procName
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
