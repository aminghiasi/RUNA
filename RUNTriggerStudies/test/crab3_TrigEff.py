##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
from httplib import HTTPException

config = config()

version = 'v05'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNTriggerEfficiency_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.outLFNDirBase = '/store/user/algomez/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 5

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T3_US_Rutgers'
config.Data.outLFNDirBase = '/store/user/algomez/myArea/EOS/'


def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':


	Samples = [ 
			'/JetHT/jkarancs-B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1-69b00753dd36562e8813bc06510c861e/USER',
			'/SingleMuon/jkarancs-B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1-69b00753dd36562e8813bc06510c861e/USER',
			'/MET/jkarancs-B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1-69b00753dd36562e8813bc06510c861e/USER',
			#'/SingleElectron/jkarancs-B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1-69b00753dd36562e8813bc06510c861e/USER',
#			'/VectorDiJet1Jet_M50/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p1-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/VectorDiJet1Jet_M250/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p1-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			]

	
	for dataset in Samples:
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+'_'+version
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','').replace('RUNA','TriggerEfficiency').replace('-0cc1d310cda5930bd3b3a68493077b41','')+'_'+version
		config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt'
		#config.Data.lumiMask = 'testLumi.json'

		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
