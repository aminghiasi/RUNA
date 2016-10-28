#!/usr/bin/env python

#from ROOT import RooRealVar, RooDataHist, RooArgList, RooArgSet, RooAddPdf, RooFit, RooGenericPdf, RooWorkspace, RooMsgService, RooHistPdf
from ROOT import *
from array import array
import argparse
import glob,sys, os
import warnings
import random
import numpy as np
from multiprocessing import Process
try: 
	from RUNA.RUNAnalysis.scaleFactors import *
	from RUNA.RUNAnalysis.commonFunctions import *
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError: 
	sys.path.append('../python') 
	from scaleFactors import *
	from commonFunctions import *
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle
#gSystem.SetIncludePath('-I$ROOFITSYS/include')
#if os.access('RooPowerFunction.cxx', os.R_OK): ROOT.gROOT.ProcessLine('.L RooPowerFunction.cxx+')

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
CMS_lumi.writeExtraText = 1
TVirtualFitter.SetMaxIterations(50000000)		######### Trick to increase number of iterations

gStyle.SetOptFit()
gStyle.SetStatY(0.91)
gStyle.SetStatX(0.95)
gStyle.SetStatW(0.15)
gStyle.SetStatH(0.15) 
gStyle.SetTextSize(0.5)

xline = array('d', [0,2000])
yline = array('d', [0,0])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)


def signalInjection():
	"""docstring for signalInjection"""

	xs_obs_limits = array('d')
	xs_exp_limits = array('d')
	xs_exp_limits_1sigma = array('d')
	xs_exp_limits_1sigma_up = array('d')
	xs_exp_limits_2sigma = array('d')
	xs_exp_limits_2sigma_up = array('d')

	XS =  search( dictXS, 'RPVStopStopToJets_UDD312_M-'+str(args.mass) )

	for itest in range( args.numberOfTest ):
		nameOfFile = "higgsCombineUDD312RPVSt_M-"+str(args.mass)+'_'+args.version+".Asymptotic.mH120.root"
		nameOfFileTest = nameOfFile.replace( 'Test_', 'Test'+str(itest)+'_' )
		tmpFile, tmpTree, tmpEntries = getTree( nameOfFileTest, "limit" )

		for i in xrange(tmpEntries):
			tmpTree.GetEntry(i)
			tmp = round( tmpTree.quantileExpected, 2)
			if tmp == 0.03: xs_exp_limits_2sigma.append( tmpTree.limit * XS )
			if tmp == 0.16: xs_exp_limits_1sigma.append( tmpTree.limit * XS )
			if tmp == 0.5: xs_exp_limits.append( tmpTree.limit * XS )
			if tmp == 0.84: xs_exp_limits_1sigma_up.append( tmpTree.limit * XS )
			if tmp == 0.98: xs_exp_limits_2sigma_up.append( tmpTree.limit * XS ) 
			if tmp == -1: xs_obs_limits.append( tmpTree.limit * XS )
	
	minValue = min( xs_obs_limits ) - 50
	maxValue = max( xs_obs_limits ) + 50 
	print minValue, maxValue
	histoSI = TH1F( 'histoSI', 'histoSI', 100, int(minValue), int(maxValue) )
	for i in xs_obs_limits: histoSI.Fill( i )

	c = TCanvas("c", "",800,500)
	histoSI.Draw()
	c.SaveAs( 'test.png' ) #'Plots/'+fileName )
	del c


if __name__ == '__main__':


	parser = argparse.ArgumentParser()
	#parser.add_argument('-t', '--technique', action='store', dest='technique', default='template', help='Process: template or fit.' )
	parser.add_argument('-v', '--version', default='altBkg_signalInjectionTest_Bin5_v05p3', help='Version of the test.' )
	parser.add_argument('-m', '--mass', dest='mass', type=int, default=100, help='To run in a mass point only.' )
	parser.add_argument('-n', '--numberOfTest', dest='numberOfTest', type=int, default=100, help='Number of tests.' )
    	#parser.add_argument('-M', "--MC", dest="addingMCbkg", type=bool, default=False, help="Adding MC bkgs to bkg estimation.")

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	signalInjection()
