import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('PROC', 
		'JetHT_Run2015C',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)

options.register('local', 
		True,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run locally or crab"
		)
options.register('debug', 
		False,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run just pruned"
		)
options.register('ak4Jet4Pt', 
		80.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"jetPt cut"
		)
options.register('jet1Pt', 
		500.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"jetPt cut"
		)
options.register('jet2Pt', 
		450.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"jetPt cut"
		)
options.register('Asym', 
		0.1,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Asymmetry cut"
		)
options.register('CosTheta', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"CosThetaStar cut"
		)
#options.register('SubPt', 
#		0.3,
#		VarParsing.multiplicity.singleton,
#		VarParsing.varType.float,
#		"Subjet Pt Ratio cut"
#		)
options.register('Tau31', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau31 cut"
		)
options.register('Tau21', 
		0.4,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau21 cut"
		)

options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.PROC

if options.local:
	process.load(NAME+'_RUNA_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
	   fileNames = cms.untracked.vstring(
		   #'/store/user/jkarancs/SusyAnalysis/B2GEdmNtuple/SingleMuon/B2GAnaFW_76X_V1p1_Run2015D-16Dec2015-v1/160401_164605/0000/B2GEDMNtuple_102.root',
		   #'/store/user/jkarancs/SusyAnalysis/B2GEdmNtuple/MET/B2GAnaFW_76X_V1p1_Run2015C_25ns-16Dec2015-v1/160401_164429/0000/B2GEDMNtuple_2.root',
		   #'/store/user/algomez/VectorDiJet1Jet_M50/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p1/160620_083737/0000/B2GEDMNtuple_10.root',
		   '/store/user/algomez/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160427_162123/0000/B2GEDMNtuple_100.root',
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False


if 'MET' in NAME: basedline = 'HLT_PFMET170_HBHECleaned'
elif 'SingleMu' in NAME: basedline =  'HLT_Mu50' #'HLT_IsoMu17_eta2p1_v'
#elif 'SingleElectron' in NAME: basedline =  'HLT_Mu50' #'HLT_IsoMu17_eta2p1_v'
else: basedline = 'HLT_PFHT475'

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerEfficiency_'+NAME+'.root' ) )

process.ResolvedTriggerEfficiency = cms.EDAnalyzer('RUNResolvedTriggerEfficiency',
		cutjetPtvalue 		= cms.double( options.ak4Jet4Pt ),
		bjSample		= cms.bool( bjsample ),
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( ['HLT_PFHT800'] ),

)
process.ResolvedTriggerEfficiencyPFHT7504Jet = process.ResolvedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT750_4JetPt'] ) )
process.ResolvedTriggerEfficiencyPFHT800PFHT7504Jet = process.ResolvedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800', 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiency = cms.EDAnalyzer('RUNBoostedTriggerEfficiency',
		cutjet1Ptvalue 		= cms.double( options.jet1Pt ),
		cutjet2Ptvalue 		= cms.double( options.jet2Pt ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		bjSample		= cms.bool( bjsample ),
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50'] ),

)

process.BoostedTriggerEfficiencySingleMu = process.BoostedTriggerEfficiency.clone( 
		baseTrigger = cms.string( 'HLT_Mu50' ) )

process.BoostedTriggerEfficiencyMET = process.BoostedTriggerEfficiency.clone( 
		baseTrigger = cms.string( 'HLT_PFMET170_HBHECleaned' ) )

process.BoostedTriggerEfficiencyPFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencySingleMuPFHT800 = process.BoostedTriggerEfficiencySingleMu.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyMETPFHT800 = process.BoostedTriggerEfficiencyMET.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyAK8PFHT650PFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencySingleMuAK8PFHT650PFHT800 = process.BoostedTriggerEfficiencySingleMu.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyMETAK8PFHT650PFHT800 = process.BoostedTriggerEfficiencyMET.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyAK8PFHT650Pt360 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30'] ) )

process.BoostedTriggerEfficiencyAK8PFHT650PFHT7504Jets = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiencyAK8PFHT650Pt360PFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencySingleMuAK8PFHT650Pt360PFHT800 = process.BoostedTriggerEfficiencySingleMu.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyMETAK8PFHT650Pt360PFHT800 = process.BoostedTriggerEfficiencyMET.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyAK8PFHT650Pt360PFHT7504Jets = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiencyAK8PFHT650Pt360PFHT7504JetsPFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT750_4JetPt', 'PFHT800'] ) )

process.BoostedTriggerEfficiencyPuppi = process.BoostedTriggerEfficiency.clone(
		jetPt = cms.InputTag("jetsAK8Puppi:jetAK8PuppiPt"),
		jetEta = cms.InputTag("jetsAK8Puppi:jetAK8PuppiEta"),
		jetPhi = cms.InputTag("jetsAK8Puppi:jetAK8PuppiPhi"),
		jetE = cms.InputTag("jetsAK8Puppi:jetAK8PuppiE"),
		jetMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppiMass"),
		jetPrunedMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppiprunedMass"),
		jetFilteredMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppifilteredMass"),
		jetSoftDropMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppisoftDropMass"),
		jetTrimmedMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppitrimmedMass"),
		jetTau1 = cms.InputTag("jetsAK8Puppi:jetAK8Puppitau1"),
		jetTau2 = cms.InputTag("jetsAK8Puppi:jetAK8Puppitau2"),
		jetTau3 = cms.InputTag("jetsAK8Puppi:jetAK8Puppitau3"),
		jetNSubjets = cms.InputTag("jetsAK8Puppi:jetAK8PuppinSubjets"),
		jetSubjetIndex0 = cms.InputTag("jetsAK8Puppi:jetAK8PuppivSubjetIndex0"),
		jetSubjetIndex1 = cms.InputTag("jetsAK8Puppi:jetAK8PuppivSubjetIndex1"),
		jetSubjetIndex2 = cms.InputTag("jetsAK8Puppi:jetAK8PuppivSubjetIndex2"),
		jetSubjetIndex3 = cms.InputTag("jetsAK8Puppi:jetAK8PuppivSubjetIndex3"),
		jetKeys = cms.InputTag("jetKeysAK8Puppi"),
		jetCSVv2 = cms.InputTag("jetsAK8Puppi:jetAK8PuppiCSVv2"),
		jecFactor = cms.InputTag("jetsAK8Puppi:jetAK8PuppijecFactor0"),
		neutralHadronEnergy = cms.InputTag("jetsAK8Puppi:jetAK8PuppineutralHadronEnergy"),
		neutralEmEnergy = cms.InputTag("jetsAK8Puppi:jetAK8PuppineutralEmEnergy"),
		chargedEmEnergy = cms.InputTag("jetsAK8Puppi:jetAK8PuppichargedEmEnergy"),
		muonEnergy = cms.InputTag("jetsAK8Puppi:jetAK8PuppiMuonEnergy"),
		chargedHadronEnergy = cms.InputTag("jetsAK8Puppi:jetAK8PuppichargedHadronEnergy"),
		chargedHadronMultiplicity = cms.InputTag("jetsAK8Puppi:jetAK8PuppiChargedHadronMultiplicity"),
		neutralHadronMultiplicity = cms.InputTag("jetsAK8Puppi:jetAK8PuppineutralHadronMultiplicity"),
		chargedMultiplicity = cms.InputTag("jetsAK8Puppi:jetAK8PuppichargedMultiplicity"),
		)
process.BoostedTriggerEfficiencyPuppiAK8PFHT650PFHT800 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyPuppiAK8PFHT650Pt360 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30'] ) )

process.BoostedTriggerEfficiencyPuppiAK8PFHT650 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50'] ) )

process.BoostedTriggerEfficiencyPuppiAK8Pt360 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFJet360_TrimMass30'] ) )

process.BoostedTriggerEfficiencyPuppiPFHT800 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyPuppiAK8PFHT650Pt360PFHT800 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT800'] ) )


if options.debug:
	process.p = cms.Path( process.BoostedTriggerEfficiency )
else:

	process.p = cms.Path( 
		process.BoostedTriggerEfficiency
		* process.BoostedTriggerEfficiencySingleMu
		* process.BoostedTriggerEfficiencyMET
		* process.BoostedTriggerEfficiencyPFHT800 
		* process.BoostedTriggerEfficiencySingleMuPFHT800 
		* process.BoostedTriggerEfficiencyMETPFHT800 
		#* process.BoostedTriggerEfficiencyAK8PFHT650PFHT7504Jets
		* process.BoostedTriggerEfficiencyAK8PFHT650PFHT800 
		* process.BoostedTriggerEfficiencySingleMuAK8PFHT650PFHT800 
		* process.BoostedTriggerEfficiencyMETAK8PFHT650PFHT800 
		#* process.BoostedTriggerEfficiencyAK8PFHT650Pt360
		* process.BoostedTriggerEfficiencyAK8PFHT650Pt360PFHT800
		* process.BoostedTriggerEfficiencySingleMuAK8PFHT650Pt360PFHT800
		* process.BoostedTriggerEfficiencyMETAK8PFHT650Pt360PFHT800
		#* process.BoostedTriggerEfficiencyPuppiAK8PFHT650PFHT800 
		#* process.BoostedTriggerEfficiencyPuppiAK8PFHT650Pt360
		* process.BoostedTriggerEfficiencyPuppiPFHT800
		* process.BoostedTriggerEfficiencyPuppiAK8PFHT650
		* process.BoostedTriggerEfficiencyPuppiAK8Pt360
		* process.BoostedTriggerEfficiencyPuppiAK8PFHT650Pt360PFHT800
		#* process.BoostedTriggerEfficiencyAK8PFHT650Pt360PFHT7504Jets
		#* process.BoostedTriggerEfficiencyAK8PFHT650Pt360PFHT7504JetsPFHT800
		#* process.ResolvedTriggerEfficiency
		#* process.ResolvedTriggerEfficiencyPFHT7504Jet
		#* process.ResolvedTriggerEfficiencyPFHT800PFHT7504Jet
		)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
