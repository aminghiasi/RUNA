#!/usr/bin/env python

'''
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Analyzer 
'''

import sys,os,time
import argparse
from collections import OrderedDict
from multiprocessing import Process
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2F, TMath
from array import array
try: 
	from RUNA.RUNAnalysis.commonFunctions import *
	from RUNA.RUNAnalysis.cuts import selection
	from RUNA.RUNAnalysis.scaleFactors import scaleFactor
except ImportError: 
	sys.path.append('../python') 
	from commonFunctions import *
	from cuts import selection
	from scaleFactors import scaleFactor

gROOT.SetBatch()
boostedMassAveBins = array( 'd', [ 0, 3, 6, 9, 12, 16, 19, 23, 26, 30, 34, 39, 43, 47, 52, 57, 62, 67, 72, 78, 83, 89, 95, 102, 108, 115, 122, 129, 137, 144, 153, 161, 170, 179, 188, 197, 207, 218, 228, 240, 251, 263, 275, 288, 301, 315, 329, 344, 359, 375, 391, 408, 425, 443, 462, 482, 502 ] )
######################################
def myAnalyzer( dictSamples, listCuts, signalName, RANGE, UNC ):

	outputFileName = 'Rootfiles/RUNMiniBoostedAnalysis_'+grooming+'_'+signalName+UNC+'_'+RANGE+'_'+args.version+'p7.root' 
	outputFile = TFile( outputFileName, 'RECREATE' )

	###################################### output Tree
	#tree = TTree('RUNAFinTree'+grooming, 'RUNAFinTree'+grooming)
	#AvgMass = array( 'f', [ 0. ] )
	#tree.Branch( 'AvgMass', AvgMass, 'AvgMass/F' )
	#Scale = array( 'f', [ 0. ] )
	#tree.Branch( 'Scale', Scale, 'Scale/F' )


	################################################################################################## Histos
	massBins = 100
	massXmin = 0.
	massXmax = 500.
	listOfOptions = [ [ j,k] for j in range(len(listCuts)-1) for k in range(1, len(listCuts) ) if k > j ]

	for sam in dictSamples:
		allHistos[ "cutFlow_"+sam ] = TH1F( "cutflow_"+sam, "cutflow_"+sam, len(listCuts), 0., len(listCuts) )
		allHistos[ "cutFlow_Scaled_"+sam ] = TH1F( "cutflow_scaled_"+sam, "cutflow_scaled_"+sam, len(listCuts), 0., len(listCuts) )
		allHistos[ "cutFlow_Scaled_Weights_"+sam ] = TH1F( "cutflow_scaled_weights_"+sam, "cutflow_scaled_weights_"+sam, len(listCuts), 0., len(listCuts) )
		allHistos[ "HT_"+sam ] = TH1F( "HT_"+sam, "HT_"+sam, 5000, 0., 5000 )
		allHistos[ "HT_"+sam ].Sumw2()
		allHistos[ "MET_"+sam ] = TH1F( "MET_"+sam, "MET_"+sam, 500, 0., 500 )
		allHistos[ "MET_"+sam ].Sumw2()
		allHistos[ "massAve_"+sam ] = TH1F( "massAve_"+sam, "massAve_"+sam, 500, 0., 500 )
		allHistos[ "massAve_"+sam ].Sumw2()
		allHistos[ "numJets_"+sam ] = TH1F( "numJets_"+sam, "numJets_"+sam, 20, 0., 20 )
		allHistos[ "numJets_"+sam ].Sumw2()
		allHistos[ "jet1Pt_"+sam ] = TH1F( "jet1Pt_"+sam, "jet1Pt_"+sam, 2000, 0., 2000 )
		allHistos[ "jet1Pt_"+sam ].Sumw2()
		allHistos[ "jet2Pt_"+sam ] = TH1F( "jet2Pt_"+sam, "jet2Pt_"+sam, 2000, 0., 2000 )
		allHistos[ "jet2Pt_"+sam ].Sumw2()
		allHistos[ "jet1CosThetaStar_"+sam ] = TH1F( "jet1CosThetaStar_"+sam, "jet1CosThetaStar_"+sam, 20, 0., 1 )
		allHistos[ "jet1CosThetaStar_"+sam ].Sumw2()
		allHistos[ "jet2CosThetaStar_"+sam ] = TH1F( "jet2CosThetaStar_"+sam, "jet2CosThetaStar_"+sam, 20, 0., 1 )
		allHistos[ "jet2CosThetaStar_"+sam ].Sumw2()
		allHistos[ "jet1Tau32_"+sam ] = TH1F( "jet1Tau32_"+sam, "jet1Tau32_"+sam, 20, 0., 1 )
		allHistos[ "jet1Tau32_"+sam ].Sumw2()
		allHistos[ "jet2Tau32_"+sam ] = TH1F( "jet2Tau32_"+sam, "jet2Tau32_"+sam, 20, 0., 1 )
		allHistos[ "jet2Tau32_"+sam ].Sumw2()
		allHistos[ "jet1RhoDDT_"+sam ] = TH1F( "jet1RhoDDT_"+sam, "jet1RhoDDT_"+sam, 200, -10, 10 )
		allHistos[ "jet1RhoDDT_"+sam ].Sumw2()
		allHistos[ "jet2RhoDDT_"+sam ] = TH1F( "jet2RhoDDT_"+sam, "jet2RhoDDT_"+sam, 200, -10, 10 )
		allHistos[ "jet2RhoDDT_"+sam ].Sumw2()
		allHistos[ "jet1Tau21VsRhoDDT_"+sam ] = TH2F( "jet1Tau21VsRhoDDT_"+sam, "jet1Tau21VsRhoDDT_"+sam, 20, 0., 1., 200, -10, 10 )
		allHistos[ "jet1Tau21VsRhoDDT_"+sam ].Sumw2()
		allHistos[ "jet2Tau21VsRhoDDT_"+sam ] = TH2F( "jet2Tau21VsRhoDDT_"+sam, "jet2Tau21VsRhoDDT_"+sam, 20, 0., 1., 200, -10, 10 )
		allHistos[ "jet2Tau21VsRhoDDT_"+sam ].Sumw2()
		allHistos[ "jet1Tau21DDT_"+sam ] = TH1F( "jet1Tau21DDT_"+sam, "jet1Tau21DDT_"+sam, 30, -1, 2 )
		allHistos[ "jet1Tau21DDT_"+sam ].Sumw2()
		allHistos[ "jet2Tau21DDT_"+sam ] = TH1F( "jet2Tau21DDT_"+sam, "jet2Tau21DDT_"+sam, 30, -1, 2 )
		allHistos[ "jet2Tau21DDT_"+sam ].Sumw2()
		allHistos[ "jet1Tau21DDTVsRhoDDT_"+sam ] = TH2F( "jet1Tau21DDTVsRhoDDT_"+sam, "jet1Tau21DDTVsRhoDDT_"+sam, 20, 0., 1., 200, -10, 10 )
		allHistos[ "jet1Tau21DDTVsRhoDDT_"+sam ].Sumw2()
		allHistos[ "jet2Tau21DDTVsRhoDDT_"+sam ] = TH2F( "jet2Tau21DDTVsRhoDDT_"+sam, "jet2Tau21DDTVsRhoDDT_"+sam, 20, 0., 1., 200, -10, 10 )
		allHistos[ "jet2Tau21DDTVsRhoDDT_"+sam ].Sumw2()
		#if 'high' in args.RANGE:
		allHistos[ "jet1Tau31_"+sam ] = TH1F( "jet1Tau31_"+sam, "jet1Tau31_"+sam, 20, 0., 1 )
		allHistos[ "jet1Tau31_"+sam ].Sumw2()
		allHistos[ "jet2Tau31_"+sam ] = TH1F( "jet2Tau31_"+sam, "jet2Tau31_"+sam, 20, 0., 1 )
		allHistos[ "jet2Tau31_"+sam ].Sumw2()
		allHistos[ "jet1SubjetPtRatio_"+sam ] = TH1F( "jet1SubjetPtRatio_"+sam, "jet1SubjetPtRatio_"+sam, 20, 0., 1 )
		allHistos[ "jet1SubjetPtRatio_"+sam ].Sumw2()
		allHistos[ "jet2SubjetPtRatio_"+sam ] = TH1F( "jet2SubjetPtRatio_"+sam, "jet2SubjetPtRatio_"+sam, 20, 0., 1 )
		allHistos[ "jet2SubjetPtRatio_"+sam ].Sumw2()
		allHistos[ "jet1BtagCSV_"+sam ] = TH1F( "jet1BtagCSV_"+sam, "jet1BtagCSV_"+sam, 5, 0., 5 )
		allHistos[ "jet1BtagCSV_"+sam ].Sumw2()
		allHistos[ "jet2BtagCSV_"+sam ] = TH1F( "jet2BtagCSV_"+sam, "jet2BtagCSV_"+sam, 5, 0., 5 )
		allHistos[ "jet2BtagCSV_"+sam ].Sumw2()
		allHistos[ "jetsBtagCSV_"+sam ] = TH1F( "jetsBtagCSV_"+sam, "jetsBtagCSV_"+sam, 5, 0., 5 )
		allHistos[ "jetsBtagCSV_"+sam ].Sumw2()

		allHistos[ "deltaEtaDijet_n-1_"+sam ] = TH1F( "deltaEtaDijet_n-1_"+sam, "deltaEtaDijet_n-1_"+sam, 50, 0., 5 )
		allHistos[ "deltaEtaDijet_n-1_"+sam ].Sumw2()
		allHistos[ "prunedMassAsym_n-1_"+sam ] = TH1F( "prunedMassAsym_n-1_"+sam, "prunedMassAsym_n-1_"+sam, 20, 0., 1 )
		allHistos[ "prunedMassAsym_n-1_"+sam ].Sumw2()
		allHistos[ "jet1Tau21_n-1_"+sam ] = TH1F( "jet1Tau21_n-1_"+sam, "jet1Tau21_n-1_"+sam, 20, 0., 1 )
		allHistos[ "jet1Tau21_n-1_"+sam ].Sumw2()
		allHistos[ "jet2Tau21_n-1_"+sam ] = TH1F( "jet2Tau21_n-1_"+sam, "jet2Tau21_n-1_"+sam, 20, 0., 1 )
		allHistos[ "jet2Tau21_n-1_"+sam ].Sumw2()
		'''
		if 'low' in args.RANGE:
			allHistos[ "jet1Tau31_n-1_"+sam ] = TH1F( "jet1Tau31_n-1_"+sam, "jet1Tau31_n-1_"+sam, 20, 0., 1 )
			allHistos[ "jet1Tau31_n-1_"+sam ].Sumw2()
			allHistos[ "jet2Tau31_n-1_"+sam ] = TH1F( "jet2Tau31_n-1_"+sam, "jet2Tau31_n-1_"+sam, 20, 0., 1 )
			allHistos[ "jet2Tau31_n-1_"+sam ].Sumw2()
		'''
		listCuts.append( [ 'btag' ] )
		for var in listCuts:
			if 'deltaEta' in var[0]: 
				allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 50, 0., 5. )
				for var1 in listCuts: allHistos[ var[0]+'_'+var1[0]+"_"+sam ] = TH1F( var[0]+'_'+var1[0]+"_"+sam, var[0]+'_'+var1[0]+"_"+sam, 50, 0., 5. )
			else: 
				allHistos[ var[0]+'_'+sam ] = TH1F( var[0]+'_'+sam, var[0]+'_'+sam, 20, 0., 1. )
				for var1 in listCuts: allHistos[ var[0]+'_'+var1[0]+"_"+sam ] = TH1F( var[0]+'_'+var1[0]+"_"+sam, var[0]+'_'+var1[0]+"_"+sam, 20, 0., 1. )
			allHistos[ var[0]+'_'+sam ].Sumw2()
			allHistos[ "massAve_"+var[0]+'_'+sam ] = TH1F( "massAve_"+var[0]+'_'+sam, "massAve_"+var[0]+'_'+sam, massBins, massXmin, massXmax )
			allHistos[ "massAve_"+var[0]+'_'+sam ].Sumw2()

			allHistos[ "HT_"+var[0]+"_"+sam ] = TH1F( "HT_"+var[0]+"_"+sam, "HT_"+var[0]+"_"+sam, 5000, 0., 5000 )
			allHistos[ "HT_"+var[0]+"_"+sam ].Sumw2()
			allHistos[ "MET_"+var[0]+"_"+sam ] = TH1F( "MET_"+var[0]+"_"+sam, "MET_"+var[0]+"_"+sam, 500, 0., 500 )
			allHistos[ "MET_"+var[0]+"_"+sam ].Sumw2()
			allHistos[ "numJets_"+var[0]+"_"+sam ] = TH1F( "numJets_"+var[0]+"_"+sam, "numJets_"+var[0]+"_"+sam, 20, 0., 20 )
			allHistos[ "numJets_"+var[0]+"_"+sam ].Sumw2()
			allHistos[ "jet1Pt_"+var[0]+"_"+sam ] = TH1F( "jet1Pt_"+var[0]+"_"+sam, "jet1Pt_"+var[0]+"_"+sam, 2000, 0., 2000 )
			allHistos[ "jet1Pt_"+var[0]+"_"+sam ].Sumw2()
			allHistos[ "jet2Pt_"+var[0]+"_"+sam ] = TH1F( "jet2Pt_"+var[0]+"_"+sam, "jet2Pt_"+var[0]+"_"+sam, 2000, 0., 2000 )
			allHistos[ "jet2Pt_"+var[0]+"_"+sam ].Sumw2()
		listCuts.remove( ['btag'] )

		for ind in listOfOptions:
			tmpName = listCuts[ind[0]][0]+'Vs'+listCuts[ind[1]][0]+'_'+sam
			allHistos[ tmpName ] = TH2F( tmpName, tmpName, 
					(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
					(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
					)
			allHistos[ tmpName ].Sumw2()

			#tmpNameSam = listCuts[-2][0]+'Vs'+listCuts[-1][0]+'_'+sam
			tmpNameSam = tmpName #listCuts[-2][0]+'Vs'+listCuts[-1][0]+'_'+sam
			#if 'RPV' in sam: massBins = 50
			#allHistos[ "massAve_"+tmpNameSam+'_ABCDProj' ] = TH1F( "massAve_"+tmpNameSam+'_ABCDProj', "massAve_"+tmpNameSam+'_ABCDProj', len(boostedMassAveBins)-1, boostedMassAveBins)
			#allHistos[ "massAve_"+tmpNameSam+'_BC' ] = TH1F( "massAve_"+tmpNameSam+'_BC', "massAve_"+tmpNameSam+'_BC',  len(boostedMassAveBins)-1, boostedMassAveBins )
			#else:
			allHistos[ "massAve_"+tmpNameSam+'_ABCDProj' ] = TH1F( "massAve_"+tmpNameSam+'_ABCDProj', "massAve_"+tmpNameSam+'_ABCDProj', massBins, massXmin, massXmax )
			allHistos[ "massAve_"+tmpNameSam+'_BC' ] = TH1F( "massAve_"+tmpNameSam+'_BC', "massAve_"+tmpNameSam+'_BC', massBins, massXmin, massXmax )
			allHistos[ "massAve_"+tmpNameSam+'_ABCDProj' ].Sumw2()
			allHistos[ "massAve_"+tmpNameSam+'_BC' ].Sumw2()

			allHistos[ tmpNameSam+'_Bkg' ] = TH2F( tmpNameSam+'_Bkg', tmpNameSam+'_Bkg', 
					#(50 if 'deltaEta' in listCuts[-2][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[-2][0] else 1. ),
					#(50 if 'deltaEta' in listCuts[-1][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[-1][0] else 1. ) 
					(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
					(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
					)
			allHistos[ tmpNameSam+'_Bkg' ].Sumw2()

			for k in [ 'A', 'B', 'C', 'D' ]:
				#allHistos[ "massAve_"+tmpNameSam+'_'+k ] = TH1F( "massAve_"+tmpNameSam+'_'+k, "massAve_"+tmpNameSam+'_'+k,  len(boostedMassAveBins)-1, boostedMassAveBins )
				allHistos[ "massAve_"+tmpNameSam+'_'+k ] = TH1F( "massAve_"+tmpNameSam+'_'+k, "massAve_"+tmpNameSam+'_'+k, massBins, massXmin, massXmax )
				allHistos[ "massAve_"+tmpNameSam+'_'+k ].Sumw2()
				allHistos[ tmpNameSam+'_'+k ] = TH2F( tmpNameSam+'_'+k, tmpNameSam+'_'+k, 
						#(50 if 'deltaEta' in listCuts[-2][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[-2][0] else 1. ),
						#(50 if 'deltaEta' in listCuts[-1][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[-1][0] else 1. ) 
						(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
						(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
						)
				allHistos[ tmpNameSam+'_'+k ].Sumw2()

				allHistos[ "massAve_"+tmpNameSam+'_btag_'+k ] = TH1F( "massAve_"+tmpNameSam+'_btag_'+k, "massAve_"+tmpNameSam+'_btag_'+k, massBins, massXmin, massXmax )
				allHistos[ "massAve_"+tmpNameSam+'_btag_'+k ].Sumw2()
				allHistos[ tmpNameSam+'_btag_'+k ] = TH2F( tmpNameSam+'_btag_'+k, tmpNameSam+'_btag_'+k, 
						#(50 if 'deltaEta' in listCuts[-2][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[-2][0] else 1. ),
						#(50 if 'deltaEta' in listCuts[-1][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[-1][0] else 1. ) 
						(50 if 'deltaEta' in listCuts[ind[0]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[0]][0] else 1. ),
						(50 if 'deltaEta' in listCuts[ind[1]][0] else 20 ), 0., (5. if 'deltaEta' in listCuts[ind[1]][0] else 1. ) 
						)
				allHistos[ tmpNameSam+'_btag_'+k ].Sumw2()
	#print allHistos

	################################################################################################## Running the Analysis
	for sample in dictSamples:

		####### Get GenTree 
		inputFile, events, numEntries = getTree( dictSamples[ sample ], ('BoostedAnalysisPlotsPuppi'+( '' if 'PDF' in UNC else UNC)+'/RUNATree' if 'Puppi' in args.grooming else 'BoostedAnalysisPlots'+( '' if 'PDF' in UNC else UNC)+'/RUNATree' ) )
		print '-'*40
		print '------> ', sample
		print '------> Number of events: '+str(numEntries)
		d = 0
		cutFlowList = OrderedDict()
		cutFlowScaledList = OrderedDict()
		cutFlowScaledListWeights = OrderedDict()
		cutFlowList[ 'Process' ] = 0
		cutFlowList[ 'Preselection' ] = 0
		cutFlowScaledList[ 'Process' ] = 0
		cutFlowScaledList[ 'Preselection' ] = 0
		cutFlowScaledListWeights[ 'Process' ] = 0
		cutFlowScaledListWeights[ 'Preselection' ] = 0
		for k in listCuts: 
			cutFlowList[ k[0] ] = 0
			cutFlowScaledList[ k[0] ] = 0
			cutFlowScaledListWeights[ k[0] ] = 0
		cutFlowList[ 'btag' ] = 0
		cutFlowScaledList[ 'btag' ] = 0
		cutFlowScaledListWeights[ 'btag' ] = 0

		for i in xrange(numEntries):
			events.GetEntry(i)

			#---- progress of the reading --------
			fraction = 10.*i/(1.*numEntries)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)
			#if ( i > 100000 ): break

			Run      = events.run
			Lumi     = events.lumi
			NumEvent = events.event
			puWeight	= events.puWeight
			if 'v06' in args.version: pdfWeight	= events.pdfWeight
			lumiWeight	= events.lumiWeight
			HT		= events.HT
			MET		= events.MET
			numJets		= events.numJets
			massAve		= getattr( events, (args.grooming+"MassAve").replace('Puppi','') )
			jet1Mass	= getattr( events, 'jet1'+(args.grooming+"Mass").replace('pruned','Pruned').replace('soft','Soft').replace('Puppi',''))
			jet2Mass	= getattr( events, 'jet2'+(args.grooming+"Mass").replace('pruned','Pruned').replace('soft','Soft').replace('Puppi',''))
			jet1Pt          = events.jet1Pt
			jet2Pt          = events.jet2Pt
			jet1Eta          = events.jet1Eta
			jet2Eta          = events.jet2Eta
			jet1CosThetaStar	= events.jet1CosThetaStar
			jet2CosThetaStar	= events.jet2CosThetaStar
			jet1BtagCSV		= ( events.jet1btagCSVv2 > 0.800 )
			jet2BtagCSV		= ( events.jet2btagCSVv2 > 0.800 )
			
			#print 'Entry ', Run, ':', Lumi, ':', NumEvent

			if 'DATA' in sample: scale = 1
			#elif 'RPV' in sample: scale = 2606 * puWeight * SF
			else: scale = 2666 * puWeight * lumiWeight

			if 'PDF' in UNC:
				if 'Up' in UNC: scale = scale*(1+pdfWeight)
				else: scale = scale*(1-pdfWeight)

			cutFlowList[ 'Process' ] += 1
			cutFlowScaledList[ 'Process' ] += scale
			cutFlowScaledList[ 'Process' ] += (puWeight*puWeight)

			########## DDT
			jet1RhoDDT = TMath.Log( jet1Mass*jet1Mass/jet1Pt )
			jet2RhoDDT = TMath.Log( jet2Mass*jet2Mass/jet2Pt )
			jet1Tau21DDT = events.jet1Tau21 + 0.063 * jet1RhoDDT 
			jet2Tau21DDT = events.jet2Tau21 + 0.063 * jet2RhoDDT 
			
			#### Pre-selection
			HTCut = ( HT > 900 )
			dijetCut =  ( numJets > 1 )
			#jetPtCut =  ( jet1Pt > 500 ) and ( jet2Pt > 450 )
			jetPtCut =  ( jet1Pt > 150 ) and ( jet2Pt > 150 )
			
			#if HTCut and dijetCut and jetPtCut:
			if HTCut and dijetCut :
				cutFlowList[ 'Preselection' ] += 1
				cutFlowScaledList[ 'Preselection' ] += scale
				cutFlowScaledList[ 'Preselection' ] += (puWeight*puWeight)
				sigCutsList = []
				allHistos[ "HT_"+sam ].Fill( HT, scale )
				allHistos[ "MET_"+sam ].Fill( MET, scale )
				allHistos[ "massAve_"+sam ].Fill( massAve, scale )
				allHistos[ "numJets_"+sam ].Fill( numJets, scale )
				allHistos[ "jet1Pt_"+sam ].Fill( jet1Pt, scale )
				allHistos[ "jet2Pt_"+sam ].Fill( jet2Pt, scale )
				allHistos[ "jet1RhoDDT_"+sam ].Fill( jet1RhoDDT, scale )
				allHistos[ "jet2RhoDDT_"+sam ].Fill( jet2RhoDDT, scale )
				allHistos[ "jet1Tau21VsRhoDDT_"+sam ].Fill( events.jet1Tau21, jet1RhoDDT, scale )
				allHistos[ "jet2Tau21VsRhoDDT_"+sam ].Fill( events.jet2Tau21, jet2RhoDDT, scale )
				allHistos[ "jet1Tau21DDT_"+sam ].Fill( jet1Tau21DDT, scale )
				allHistos[ "jet2Tau21DDT_"+sam ].Fill( jet2Tau21DDT, scale )
				allHistos[ "jet1Tau21DDTVsRhoDDT_"+sam ].Fill( jet1Tau21DDT, jet1RhoDDT, scale )
				allHistos[ "jet2Tau21DDTVsRhoDDT_"+sam ].Fill( jet2Tau21DDT, jet2RhoDDT, scale )
				allHistos[ "prunedMassAsym_"+sam ].Fill( events.prunedMassAsym, scale )
				allHistos[ "deltaEtaDijet_"+sam ].Fill( events.deltaEtaDijet, scale )
				allHistos[ "jet1CosThetaStar_"+sam ].Fill( jet1CosThetaStar, scale )
				allHistos[ "jet2CosThetaStar_"+sam ].Fill( jet2CosThetaStar, scale )
				allHistos[ "jet1Tau21_"+sam ].Fill( events.jet1Tau21, scale )
				allHistos[ "jet2Tau21_"+sam ].Fill( events.jet2Tau21, scale )
				allHistos[ "jet1Tau31_"+sam ].Fill( events.jet1Tau31, scale )
				allHistos[ "jet2Tau31_"+sam ].Fill( events.jet2Tau31, scale )
				allHistos[ "jet1Tau32_"+sam ].Fill( events.jet1Tau32, scale )
				allHistos[ "jet2Tau32_"+sam ].Fill( events.jet2Tau32, scale )
				allHistos[ "jet1SubjetPtRatio_"+sam ].Fill( events.jet1SubjetPtRatio, scale )
				allHistos[ "jet2SubjetPtRatio_"+sam ].Fill( events.jet2SubjetPtRatio, scale )
				allHistos[ "jet1BtagCSV_"+sam ].Fill( 1 if jet1BtagCSV else 0 )
				allHistos[ "jet2BtagCSV_"+sam ].Fill( 1 if jet2BtagCSV else 0 )

				bothBtag = ( jet1BtagCSV and jet2BtagCSV )
				oneBtag = ( jet1BtagCSV or jet2BtagCSV )
				if bothBtag: allHistos[ "jetsBtagCSV_"+sam ].Fill( 2 )
				elif oneBtag: allHistos[ "jetsBtagCSV_"+sam ].Fill( 1 )
				else: allHistos[ "jetsBtagCSV_"+sam ].Fill( 0 )

				for var in listCuts:
					#allHistos[ var[0]+'_'+sample ].Fill( getattr( events, var[0] ), scale )
					nextCut = False
					if ( getattr( events, var[0] ) < var[1] ): nextCut = True 
					else: nextCut = False
					sigCutsList.append( nextCut )

					if all(sigCutsList): 
						allHistos[ 'massAve_'+var[0]+'_'+sample ].Fill( massAve, scale )  ### adding two prong scale factor
						allHistos[ 'jet1Tau21_'+var[0]+'_'+sample ].Fill( events.jet1Tau21, scale )
						allHistos[ 'jet2Tau21_'+var[0]+'_'+sample ].Fill( events.jet2Tau21, scale )
						#if 'low' in args.RANGE: allHistos[ 'jet1Tau31_'+var[0]+'_'+sample ].Fill( events.jet1Tau31, scale )
						#if 'low' in args.RANGE: allHistos[ 'jet2Tau31_'+var[0]+'_'+sample ].Fill( events.jet2Tau31, scale )
						allHistos[ 'prunedMassAsym_'+var[0]+'_'+sample ].Fill( events.prunedMassAsym, scale )
						allHistos[ 'deltaEtaDijet_'+var[0]+'_'+sample ].Fill( events.deltaEtaDijet, scale )
						allHistos[ "HT_"+var[0]+"_"+sam ].Fill( HT, scale )
						allHistos[ "MET_"+var[0]+"_"+sam ].Fill( MET, scale )
						allHistos[ "numJets_"+var[0]+"_"+sam ].Fill( numJets, scale )
						allHistos[ "jet1Pt_"+var[0]+"_"+sam ].Fill( jet1Pt, scale )
						allHistos[ "jet2Pt_"+var[0]+"_"+sam ].Fill( jet2Pt, scale )
						cutFlowList[ var[0] ] += 1
						cutFlowScaledList[ var[0] ] += scale
						cutFlowScaledList[ var[0] ] += (puWeight*puWeight)

				#if oneBtag and all(sigCutsList): 
				if bothBtag and all(sigCutsList): 
					allHistos[ 'massAve_btag_'+sample ].Fill( massAve, scale )  ### adding two prong scale factor
					allHistos[ 'jet1Tau21_btag_'+sample ].Fill( events.jet1Tau21, scale )
					allHistos[ 'jet2Tau21_btag_'+sample ].Fill( events.jet2Tau21, scale )
					#if 'low' in args.RANGE: allHistos[ 'jet1Tau31_btag_'+sample ].Fill( events.jet1Tau31, scale )
					#if 'low' in args.RANGE: allHistos[ 'jet2Tau31_btag_'+sample ].Fill( events.jet2Tau31, scale )
					allHistos[ 'prunedMassAsym_btag_'+sample ].Fill( events.prunedMassAsym, scale )
					allHistos[ 'deltaEtaDijet_btag_'+sample ].Fill( events.deltaEtaDijet, scale )
					allHistos[ "HT_btag_"+sam ].Fill( HT, scale )
					allHistos[ "MET_btag_"+sam ].Fill( MET, scale )
					allHistos[ "numJets_btag_"+sam ].Fill( numJets, scale )
					allHistos[ "jet1Pt_btag_"+sam ].Fill( jet1Pt, scale )
					allHistos[ "jet2Pt_btag_"+sam ].Fill( jet2Pt, scale )
					cutFlowList[ 'btag' ] += 1
					cutFlowScaledList[ 'btag' ] += scale
					cutFlowScaledList[ 'btag' ] += (puWeight*puWeight)
				#### n-1 plots
				'''
				if ( 'low' in args.RANGE ):
					if ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ) and (  getattr( events, listCuts[1][0] ) < listCuts[1][1] ) and ( getattr( events, listCuts[2][0] ) < listCuts[2][1] ) and ( getattr( events, listCuts[3][0] ) < listCuts[3][1] ) and ( getattr( events, listCuts[4][0] ) < listCuts[4][1] ): allHistos[ 'deltaEtaDijet_n-1_'+sample ].Fill( events.deltaEtaDijet, scale )
					if ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ) and (  getattr( events, listCuts[1][0] ) < listCuts[1][1] ) and ( getattr( events, listCuts[2][0] ) < listCuts[2][1] ) and ( getattr( events, listCuts[3][0] ) < listCuts[3][1] ) and ( getattr( events, listCuts[5][0] ) < listCuts[5][1] ): allHistos[ 'prunedMassAsym_n-1_'+sample ].Fill( events.prunedMassAsym, scale )
					if ( getattr( events, listCuts[2][0] ) < listCuts[2][1] ) and ( getattr( events, listCuts[3][0] ) < listCuts[3][1] ) and ( getattr( events, listCuts[4][0] ) < listCuts[4][1] ) and ( getattr( events, listCuts[5][0] ) < listCuts[5][1] ): 
						allHistos[ 'jet1Tau21_n-1_'+sample ].Fill( events.jet1Tau21, scale )
						allHistos[ 'jet2Tau21_n-1_'+sample ].Fill( events.jet2Tau21, scale )
					if ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ) and ( getattr( events, listCuts[1][0] ) < listCuts[1][1] ) and ( getattr( events, listCuts[4][0] ) < listCuts[4][1] ) and ( getattr( events, listCuts[5][0] ) < listCuts[5][1] ): 
						allHistos[ 'jet1Tau31_n-1_'+sample ].Fill( events.jet1Tau31, scale )
						allHistos[ 'jet2Tau31_n-1_'+sample ].Fill( events.jet2Tau31, scale )
				else:
				'''
				if ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ) and (  getattr( events, listCuts[1][0] ) < listCuts[1][1] ) and ( getattr( events, listCuts[3][0] ) < listCuts[3][1] ): allHistos[ 'prunedMassAsym_n-1_'+sample ].Fill( events.prunedMassAsym, scale )
				if ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ) and (  getattr( events, listCuts[1][0] ) < listCuts[1][1] ) and ( getattr( events, listCuts[2][0] ) < listCuts[2][1] ): allHistos[ 'deltaEtaDijet_n-1_'+sample ].Fill( events.deltaEtaDijet, scale )
				if ( getattr( events, listCuts[2][0] ) < listCuts[2][1] ) and ( getattr( events, listCuts[3][0] ) < listCuts[3][1] ): 
					allHistos[ 'jet1Tau21_n-1_'+sample ].Fill( events.jet1Tau21, scale )
					allHistos[ 'jet2Tau21_n-1_'+sample ].Fill( events.jet2Tau21, scale )

				##########

				for Ind in listOfOptions:
					allHistos[ listCuts[Ind[0]][0]+'Vs'+listCuts[Ind[1]][0]+'_'+sample ].Fill( getattr( events, listCuts[Ind[0]][0] ), getattr( events, listCuts[Ind[1]][0] ), scale )
					tmpSigCutsList = [ x for i,x in enumerate(sigCutsList) if i not in Ind ]
					
				##### Bkg estimation/ABCD method
				if ( all(sigCutsList[:-2]) ): # and ( getattr( events, listCuts[5][0] ) > (listCuts[5][1]*2) )): 
					allHistos[ listCuts[-2][0]+'Vs'+listCuts[-1][0]+'_'+sample+'_Bkg' ].Fill( getattr( events, listCuts[0][0] ), getattr( events, listCuts[1][0] ), scale )
					plotABCD( [ ( getattr( events, listCuts[-2][0] ) < listCuts[-2][1] ), ( getattr( events, listCuts[-1][0] ) < listCuts[-1][1] ) ], [ listCuts[-2][0], listCuts[-1][0] ], events, massAve, scale, sample )

					if bothBtag: plotABCD( [ ( getattr( events, listCuts[-2][0] ) < listCuts[-2][1] ), ( getattr( events, listCuts[-1][0] ) < listCuts[-1][1] ) ], [ listCuts[-2][0], listCuts[-1][0] ], events, massAve, scale, sample+'_btag' )

				####### bkg estimation alternatives
				if sigCutsList[2]: 
					allHistos[ 'jet1Tau21VsdeltaEtaDijet_'+sample+'_Bkg' ].Fill( getattr( events, 'jet1Tau21' ), getattr( events, 'deltaEtaDijet' ), scale )
					allHistos[ 'jet2Tau21VsdeltaEtaDijet_'+sample+'_Bkg' ].Fill( getattr( events, 'jet2Tau21' ), getattr( events, 'deltaEtaDijet' ), scale )
					plotABCDv2( [ ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ), ( getattr( events, listCuts[1][0] ) < listCuts[1][1] ), ( getattr( events, listCuts[-1][0] ) < listCuts[-1][1] ) ], [ listCuts[0][0], listCuts[-1][0] ], events, massAve, scale, sample )
					plotABCDv2( [ ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ), ( getattr( events, listCuts[1][0] ) < listCuts[1][1] ), ( getattr( events, listCuts[-1][0] ) < listCuts[-1][1] ) ], [ listCuts[1][0], listCuts[-1][0] ], events, massAve, scale, sample )

				'''
				if sigCutsList[-1]: 
					allHistos[ 'jet1Tau21VsprunedMassAsym_'+sample+'_Bkg' ].Fill( getattr( events, 'jet1Tau21' ), getattr( events, 'prunedMassAsym' ), scale )
					allHistos[ 'jet2Tau21VsprunedMassAsym_'+sample+'_Bkg' ].Fill( getattr( events, 'jet2Tau21' ), getattr( events, 'prunedMassAsym' ), scale )
					plotABCDv2( [ ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ), ( getattr( events, listCuts[1][0] ) < listCuts[1][1] ), ( getattr( events, listCuts[-2][0] ) < listCuts[-2][1] ) ], [ listCuts[0][0], listCuts[-2][0] ], events, massAve, scale, sample )
					plotABCDv2( [ ( getattr( events, listCuts[0][0] ) < listCuts[0][1] ), ( getattr( events, listCuts[1][0] ) < listCuts[1][1] ), ( getattr( events, listCuts[-2][0] ) < listCuts[-2][1] ) ], [ listCuts[1][0], listCuts[-2][0] ], events, massAve, scale, sample )
				'''

						

		dummy = 1
		for q in cutFlowList: 
			allHistos[ 'cutFlow_'+sample ].SetBinContent( dummy, cutFlowList[q] )
			allHistos[ 'cutFlow_'+sample ].GetXaxis().SetBinLabel( dummy, q )
			allHistos[ 'cutFlow_Scaled_'+sample ].SetBinContent( dummy, cutFlowScaledList[q] )
			allHistos[ 'cutFlow_Scaled_'+sample ].GetXaxis().SetBinLabel( dummy, q )
			allHistos[ 'cutFlow_Scaled_Weights_'+sample ].SetBinContent( dummy, cutFlowScaledListWeights[q] )
			allHistos[ 'cutFlow_Scaled_Weights_'+sample ].GetXaxis().SetBinLabel( dummy, q )
			dummy+=1

	for sample in dictSamples:
		nameABCD = listCuts[-2][0]+'Vs'+listCuts[-1][0]+'_'+sample
		allHistos[ 'massAve_'+nameABCD+'_BC' ].Multiply( allHistos[ 'massAve_'+nameABCD+'_B' ], allHistos[ 'massAve_'+nameABCD+'_C' ], 1, 1, '')
		allHistos[ 'massAve_'+nameABCD+'_ABCDProj' ].Divide( allHistos[ 'massAve_'+nameABCD+'_BC' ], allHistos[ 'massAve_'+nameABCD+'_D' ], 1, 1, '')
		'''
		### The two lines above are doing exactly the following:
		for ibin in range( 0, allHistos[ 'massAve_'+nameABCD+'_B' ].GetNbinsX() ):
			Bcont = allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinContent( ibin )
			Berr = allHistos[ 'massAve_'+nameABCD+'_B' ].GetBinError( ibin )
			Ccont = allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinContent( ibin )
			Cerr = allHistos[ 'massAve_'+nameABCD+'_C' ].GetBinError( ibin )
			Dcont = allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinContent( ibin )
			Derr = allHistos[ 'massAve_'+nameABCD+'_D' ].GetBinError( ibin )

			try: Nbkg = ( Bcont * Ccont ) / Dcont
			except ZeroDivisionError: Nbkg = 0
			allHistos[ "massAve_"+nameABCD+'_ABCDProj' ].SetBinContent( ibin, Nbkg )
			#try: NbkgErr = Nbkg * TMath.Sqrt( TMath.Power( Berr / Bcont, 2 ) + TMath.Power( Cerr / Ccont, 2 ) + TMath.Power( Derr / Dcont, 2 ) )
			try: NbkgErr = Nbkg * TMath.Sqrt( TMath.Power( TMath.Sqrt(Bcont) / Bcont, 2 ) + TMath.Power( TMath.Sqrt(Ccont) / Ccont, 2 ) + TMath.Power( TMath.Sqrt(Dcont) / Dcont, 2 ) )
			except ZeroDivisionError: NbkgErr = 0
			allHistos[ "massAve_"+nameABCD+'_ABCDProj' ].SetBinError( ibin, NbkgErr )
		'''


	outputFile.Write()
	##### Closing
	print 'Writing output file: '+ outputFileName
	outputFile.Close()


def plotABCD( listSel, var, fromTree, massAve, scale, sample ):
	"""docstring for plotABCD"""

	nameABCD = var[0]+'Vs'+var[1]+'_'+sample
	if listSel[0] and listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_A' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_A' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif listSel[0] and not listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_B' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_B' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif not listSel[0] and listSel[1]: 
		allHistos[ 'massAve_'+nameABCD+'_C' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_C' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	else:
		allHistos[ 'massAve_'+nameABCD+'_D' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_D' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )

def plotABCDv2( listSel, var, fromTree, massAve, scale, sample ):
	"""docstring for plotABCD"""

	nameABCD = var[0]+'Vs'+var[1]+'_'+sample
	if (listSel[0] and listSel[1]) and listSel[2]: 
		allHistos[ 'massAve_'+nameABCD+'_A' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_A' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif (listSel[0] and listSel[1]) and not listSel[2]: 
		allHistos[ 'massAve_'+nameABCD+'_B' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_B' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif not listSel[0] and not listSel[1] and listSel[2]: 
		allHistos[ 'massAve_'+nameABCD+'_C' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_C' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )
	elif not listSel[0] and not listSel[1] and not listSel[2]: 
		allHistos[ 'massAve_'+nameABCD+'_D' ].Fill( massAve, scale )
		allHistos[ nameABCD+'_D' ].Fill( getattr( fromTree, var[0] ), getattr( fromTree, var[1] ), scale )




#################################################################################
if __name__ == '__main__':

	usage = 'usage: %prog [options]'
	
	parser = argparse.ArgumentParser()
	parser.add_argument( '-m', '--mass', action='store', dest='mass', default=100, help='Mass of the Stop' )
	parser.add_argument( '-g', '--grooming', action='store',  dest='grooming', default='pruned', help='Jet Algorithm' )
	parser.add_argument( '-p', '--process', action='store',  dest='process', default='single', help='Process: all or single.' )
	parser.add_argument( '-d', '--decay', action='store',  dest='decay', default='UDD312', help='Decay: UDD312 or UDD323.' )
	parser.add_argument( '-s', '--sample', action='store',   dest='samples', default='RPV', help='Type of sample' )
	parser.add_argument( '-r', '--range', action='store',  dest='RANGE', default='low', help='Range: low, med, high.' )
	parser.add_argument( '-u', '--unc', action='store',  dest='unc', default='', help='Process: all or single.' )
	parser.add_argument( '-b', '--batchSys', action='store',  dest='batchSys', type=bool, default=False, help='Process: all or single.' )
	parser.add_argument( '-v', '--version', action='store', default='v05', dest='version', help='Version of the RUNAnalysis file.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	mass = args.mass
	process = args.process
	grooming = args.grooming
	samples = args.samples

	if args.batchSys: folder = '/cms/gomez/archiveEOS/Archive/763patch2/v5/'
	else: folder = 'Rootfiles/'

	allSamples = {}
	allSamples[ 'DATA' ] = folder+'/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_'+args.version+'.root'
	#if not 'Dibosons' in mass: allSamples[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ] = folder+'/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v2p0_v01.root'
	allSamples[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ] = folder+'/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'QCDHTAll' ] = folder+'/RUNAnalysis_QCDHTAll_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'QCDPtAll' ] = folder+'/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'TTJets' ] = folder+'/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'WJetsToQQ' ] = folder+'/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'ZJetsToQQ' ] = folder+'/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	allSamples[ 'Dibosons' ] = folder+'/RUNAnalysis_Dibosons_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	#allSamples[ 'WWTo4Q' ] = folder+'/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	#allSamples[ 'ZZTo4Q' ] = folder+'/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'
	#allSamples[ 'WZ' ] = folder+'/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'

	cutList = ( 'Dibosons' if 'Dibosons' in mass else 'RPVStopStopToJets_'+args.decay+'_M-'+mass )
	#try: cuts = selection[ cutList ]
	try: cuts = [ [ 'jet1Tau21', 0.45 ], [ 'jet2Tau21', 0.45 ], [ 'prunedMassAsym', 0.10 ], [ 'deltaEtaDijet', 1.5 ] ]
	except KeyError: 
		print 'Mass', mass, 'not in list.'
		sys.exit(0)
		
	if 'RPV' in samples: samples = 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass)
	if 'single' in process: 
		for q in allSamples:
			if q in samples:
				dictSamples = { q: allSamples[ q ] } 
				signalSample = q
	else: 
		dictSamples = allSamples
		signalSample = 'RPVStopStopToJets_'+args.decay+'_M-'+mass+'_All'

	allHistos = {}

	if ('RPV' in samples) and args.unc:
		for uncType in [ args.unc+'Up', args.unc+'Down' ]: 
			p = Process( target=myAnalyzer, args=( dictSamples, cuts, signalSample, args.RANGE, uncType ) )
			p.start()
			p.join()
	else:
		p = Process( target=myAnalyzer, args=( dictSamples, cuts, signalSample, args.RANGE, '' ) )
		p.start()
		p.join()
