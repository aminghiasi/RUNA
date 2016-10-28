##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException
import glob

config = config()

version = 'v07'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
#config.JobType.psetName = 'RUNBoostedResolutionCalc_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.publication = False
config.Data.ignoreLocality = True
supportFiles = glob.glob('supportFiles/*')
config.JobType.inputFiles = supportFiles

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

	from CRABAPI.RawCommand import crabCommand

	Samples = [ 
#			'/JetHT/jkarancs-B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1-69b00753dd36562e8813bc06510c861e/USER',
#			'/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
#			'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
#			'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
#			'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
#			'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
			
			'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',

#			'/TT_TuneCUETP8M1_13TeV-powheg-pythia8/vorobiev-B2GAnaFW_RunIIFall15MiniAODv2_25ns_v76x_v1p2-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
#			'/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/WWTo4Q_4f_13TeV_amcatnloFXFX_madspin_pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',
#			'/WZ_TuneCUETP8M1_13TeV-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/ZJetsToQQ_HT600toInf_13TeV-madgraph/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/jkarancs-B2GAnaFW_76X_V1p1_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1-bf3ef703e3bdb5dcc5320cf3ff6ce74d/USER',



#			######## Centrally produced
#			'/RPVStopStopToJets_UDD312_M-80_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p1p2-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-90_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-110_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-120_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-130_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-140_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-150_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#
#			'/RPVStopStopToJets_UDD312_M-170_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-180_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-190_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#
#			'/RPVStopStopToJets_UDD312_M-210_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-220_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',	
#			'/RPVStopStopToJets_UDD312_M-230_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p1-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-240_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p1-6ff2d2372798a32b31bae3809d51b58e/USER',
#
##
#			'/RPVStopStopToJets_UDD312_M-300_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-350_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-400_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-450_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-500_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-550_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-600_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-650_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#
#			'/RPVStopStopToJets_UDD312_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#
#			'/RPVStopStopToJets_UDD312_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#			'/RPVStopStopToJets_UDD312_M-950_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
#

			######## UDD323
			#'/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8-600000events/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',


			]

	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		if 'JetHT' in dataset: 
			procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','')+'_'+version
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt'
			#config.Data.lumiMask = 'crab_projects/crab_JetHTjkarancs-B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1-69b00753dd36562e8813bc06510c861e__v04/results/notFinishedLumis.json'
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'jecVersion=Fall15_25nsV2' ]
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 5

		elif 'RPV' in dataset: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 3
			procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0]+dataset.split('/')[2].replace( dataset.split('/')[2].split('-')[0] , '').split('-')[1]+'_'+dataset.split('/')[2].replace(dataset.split('/')[2].split('-')[0], '').split('-')[2]+version
			#procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0]+'ResolCalc'+version
			#config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'systematics=1', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_latest.root' ]
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'systematics=0', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_latest.root' ]
		else: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 100
			procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0].replace('13TeV_amcatnloFXFX_madspin_pythia8','')+dataset.split('/')[2].replace('vorobiev', '').replace('jkarancs', '').split('-')[1]+'_'+dataset.split('/')[2].replace('jkarancs', '').split('-')[2]+version
			#procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0].replace('13TeV_amcatnloFXFX_madspin_pythia8','')+version+'p1'
			#procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0].replace('13TeV_amcatnloFXFX_madspin_pythia8','')+version
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_latest.root' ]
			#config.Data.lumiMask = 'crab_projects/crab_QCD_Pt_300to470_v04/results/failedLumis.json'
		config.General.requestName = procName
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
