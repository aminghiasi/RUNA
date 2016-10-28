#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
import time, os, math, sys
from array import array
import argparse
from collections import OrderedDict
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
	from RUNA.RUNAnalysis.commonFunctions import *
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import * #scaleFactor as SF
	from cuts import selection 
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle
	from commonFunctions import *


gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1,1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

jetMassHTlabY = 0.20
jetMassHTlabX = 0.85


def plotSignalBkg( signalFiles, bkgFiles, dataFile, Groom, nameInRoot, name, xmin, xmax, rebinX, labX, labY, log, posLegend, Norm=False ):
	"""docstring for plot"""

	if 'DATA' in args.process: outputFileName = name+'_'+Groom+'_DATA_PlusBkgQCD'+args.qcd+'_'+args.RANGE+'_'+args.boosted+'AnalysisPlots'+args.version+'.'+args.ext 
	else: outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+args.mass+'_PlusBkgQCD'+args.qcd+'_'+args.RANGE+'_'+args.boosted+'AnalysisPlots'+args.version+'.'+args.ext 
	if log: outputFileName = outputFileName.replace('Plots','Plots_Log')
	print 'Processing.......', outputFileName
	
	if args.final:  legend=TLegend(0.50,0.70,0.95,0.89)
	elif 'DATA' in args.process: legend=TLegend(0.18,0.70,0.70,0.89)
	else:
		if posLegend: legend=TLegend(0.15, 0.60, 0.4, 0.87 )
		else: legend=TLegend(0.75,0.55,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	if 'DATA' in args.process:
		dataHistos = {}
		dataHistos[ 'DATA' ] = dataFile.Get( nameInRoot if '1D' in args.process else nameInRoot+'_DATA' )
		#if 'mass' in nameInRoot: dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( len( boostedMassAveBins )-1, dataHistos[ 'DATA' ].GetName(), boostedMassAveBins )
		#elif rebinX > 1: dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( rebinX )
		if rebinX > 1: dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( rebinX )
		legend.AddEntry( dataHistos[ 'DATA' ], 'Data', 'ep' )

	signalHistos = OrderedDict()
	binWidth = 0
	maxList = []
	if len(signalFiles) > 0:
		for sigSamples in signalFiles:
			print sigSamples
			signalHistos[ sigSamples ] = signalFiles[ sigSamples ][0].Get( ( nameInRoot if '1D' in args.process else nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+sigSamples ) )
			#signalHistos[ sigSamples ] = signalFiles[ sigSamples ][0].Get(  nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_A' )
			#if 'mass' in nameInRoot: signalHistos[ sigSamples ] = signalHistos[ sigSamples ].Rebin( len( boostedMassAveBins )-1, signalHistos[ sigSamples ].GetName(), boostedMassAveBins )
			if rebinX > 1: signalHistos[ sigSamples ] = signalHistos[ sigSamples ].Rebin( rebinX )
			if signalFiles[ sigSamples ][1] != 1: signalHistos[ sigSamples ].Scale( signalFiles[ sigSamples ][1] ) 
			#if not 'DATA' in args.process: legend.AddEntry( signalHistos[ sigSamples ], signalFiles[ sigSamples ][2], 'l' if Norm else 'f' )
			legend.AddEntry( signalHistos[ sigSamples ], signalFiles[ sigSamples ][2], 'l' ) #if Norm else 'f' )
			print sigSamples, round( signalHistos[ sigSamples ].Integral(), 2 )
			if Norm:
				signalHistos[ sigSamples ].SetLineColor( signalFiles[ sigSamples ][3] )
				signalHistos[ sigSamples ].SetLineWidth( 3 )
				signalHistos[ sigSamples ].Scale( 1 / signalHistos[ sigSamples ].Integral() )
				maxList.append( signalHistos[ sigSamples ].GetMaximum() )
			else:
				#signalHistos[ sigSamples ].SetFillStyle( 1001 )
				#signalHistos[ sigSamples ].SetFillColor( signalFiles[ sigSamples ][3] )
				signalHistos[ sigSamples ].SetLineColor( signalFiles[ sigSamples ][3] )
				signalHistos[ sigSamples ].SetFillColor(0)
				signalHistos[ sigSamples ].SetLineWidth(3)
				signalHistos[ sigSamples ].SetLineStyle(2)
			#if 'mass' in nameInRoot: binWidth = '#sigma_{mass}'
			binWidth = int(signalHistos[ sigSamples ].GetBinWidth( 1 ))

	bkgHistos = OrderedDict()
	if len(bkgFiles) > 0:
		for bkgSamples in bkgFiles:
			bkgHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get(  nameInRoot if '1D' in args.process else nameInRoot+'_'+bkgSamples )
			#bkgHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_A' )
			#if 'mass' in nameInRoot: bkgHistos[ bkgSamples ] = bkgHistos[ bkgSamples ].Rebin( len( boostedMassAveBins )-1, bkgHistos[ bkgSamples ].GetName(), boostedMassAveBins )
			if rebinX > 1: bkgHistos[ bkgSamples ] = bkgHistos[ bkgSamples ].Rebin( rebinX )
			if bkgFiles[ bkgSamples ][1] != 1: bkgHistos[ bkgSamples ].Scale( bkgFiles[ bkgSamples ][1] ) 
			legend.AddEntry( bkgHistos[ bkgSamples ], bkgFiles[ bkgSamples ][2], 'l' if Norm else 'f' )
			print bkgSamples, round( bkgHistos[ bkgSamples ].Integral(), 2 )
			if Norm:
				bkgHistos[ bkgSamples ].SetLineColor( bkgFiles[ bkgSamples ][3] )
				bkgHistos[ bkgSamples ].SetLineWidth( 3 )
				bkgHistos[ bkgSamples ].SetLineStyle( 2 )
				bkgHistos[ bkgSamples ].Scale( 1 / bkgHistos[ bkgSamples ].Integral() )
				maxList.append( bkgHistos[ bkgSamples ].GetMaximum() )
			else:
				bkgHistos[ bkgSamples ].SetFillStyle( 1001 )
				bkgHistos[ bkgSamples ].SetFillColor( bkgFiles[ bkgSamples ][3] )
			

	CMS_lumi.extraText = "Simulation Preliminary"
	hBkg = signalHistos[ args.mass ].Clone()
	hBkg.Reset()
	print 'Total Bkg :', round(hBkg.Integral(), 2 )
	#print 'Total Bkg + Signal :', signalHistos[ args.mass ].Integral() + hBkg.Integral(), signalHistos[ args.mass ].Integral() 
	#print 'Contamination :', signalHistos[ args.mass ].Integral() / ( signalHistos[ args.mass ].Integral() + hBkg.Integral() )

	if not Norm:

		for samples in bkgHistos:
			hBkg.Add( bkgHistos[ samples ].Clone() )

		stackHisto = THStack('stackHisto', 'stack')
		#for BkgSamples in bkgHistos: 
		#	stackHisto.Add( bkgHistos[ BkgSamples ] )
		stackHisto.Add( bkgHistos[ 'Dibosons' ] )
		stackHisto.Add( bkgHistos[ 'ZJetsToQQ' ] )
		stackHisto.Add( bkgHistos[ 'WJetsToQQ' ] )
		stackHisto.Add( bkgHistos[ 'TTJets' ] )
		stackHisto.Add( bkgHistos[ 'QCD'+args.qcd+'All' ] )

		if not 'DATA' in args.process: 
			for SigSamples in signalHistos: stackHisto.Add( signalHistos[ SigSamples ] )

  		tdrStyle.SetPadRightMargin(0.05)
  		tdrStyle.SetPadLeftMargin(0.15)
		can = TCanvas('c1', 'c1',  10, 10, 750, ( 600 if args.final else 750 ) )
		if not args.final:
			pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
			pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
			pad1.Draw()
			pad2.Draw()

			pad1.cd()
		if log and not args.final: pad1.SetLogy()
		elif log: can.SetLogy()
		#stackHisto.SetMinimum(0.001)
		stackHisto.Draw('hist')
		if args.final: labelAxis( name, stackHisto, Groom )
		#stackHisto.GetYaxis().SetTitleOffset(1.2)
		if 'massAve_deltaEtaDijet' in nameInRoot: 
			stackHisto.SetMaximum( 7000 ) 
			stackHisto.SetMinimum( 1 )
		if xmax: stackHisto.GetXaxis().SetRangeUser( xmin, xmax )
		#stackHisto.SetMaximum( 70 ) 
		if not 'DATA' in args.process: 
			tmpHisto = signalHistos[ args.mass ].Clone()
			tmpHisto.SetLineColor(kRed-4)
			tmpHisto.SetFillColor(0)
			tmpHisto.SetLineWidth(3)
			tmpHisto.SetLineStyle(2)
			tmpHisto.Draw("hist same")
		#hBkg.SetFillStyle(0)
		hBkg.SetLineColor(kBlack)
		hBkg.SetLineStyle(1)
		hBkg.SetLineWidth(1)
		#hBkg.SetFillStyle(3004)
		#hBkg.SetFillColor( kRed )
		#hBkg.Draw("same")
		stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth)+' GeV' )
		if 'DATA' in args.process: 
			dataHistos[ 'DATA' ].SetMarkerStyle(8)
			dataHistos[ 'DATA' ].Draw('same')
			CMS_lumi.extraText = "Preliminary"
			legend.SetNColumns(2)
			for sample in signalHistos: 
				lowEdgeWindow = int(int(sample) - ( int( massWidthList[int(sample)]) ))
				highEdgeWindow = int(int(sample) + ( int( massWidthList[int(sample)]) ))
				signalHistos[ sample ].GetXaxis().SetRangeUser( lowEdgeWindow, highEdgeWindow )
				signalHistos[ sample ].Draw("hist same")

		CMS_lumi.relPosX = 0.14
		CMS_lumi.CMS_lumi( (can if args.final else pad1), 4, 0)
		legend.Draw()
		if not args.final: 
			if not (labX and labY): 
				if 'mini' in args.process: finalLabels( 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass) ) 
				elif '1D' in args.process:  labels( 'presel', '' )
				else: labels( name, args.camp )
			else: 
				if 'mini' in args.process: finalLabels( 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), labX, labY ) 
				elif '1D' in args.process:  labels( 'presel', '', labX, labY )
				else: labels( name, args.camp, labX, labY )

		if not args.final:
			pad2.cd()
			pad2.SetGrid()
			pad2.SetTopMargin(0)
			pad2.SetBottomMargin(0.3)
			
			if 'DATA' in args.process:
				hRatio = dataHistos[ 'DATA' ].Clone()
				hRatio.Divide( hBkg ) 
				ratioLabel = "Data / MC"
				#hRatio.Add( bkgHistos[ 'QCDPtAll'], -1 )
				#hRatio.Divide( bkgHistos[ 'TTJets'] ) 
				#ratioLabel = "(DATA - MC QCD)/(MC ttbar)"
				hRatio.SetMaximum(2.)
				hRatio.SetMinimum(0.)
				hRatio.SetMarkerStyle(8)
			else:
				hRatio = signalHistos[ args.mass ].Clone()
				hRatio.Reset()
				for ibin in range(0, hRatio.GetNbinsX()):
					binContSignal = signalHistos[ args.mass ].GetBinContent(ibin)
					binContBkg = hBkg.GetBinContent(ibin)
					try: value = binContSignal / TMath.Sqrt( binContSignal + binContBkg )
					#try: value = binContSignal / ( binContSignal + binContBkg )
					except ZeroDivisionError: continue
					hRatio.SetBinContent( ibin, value )
				ratioLabel = "S / #sqrt{S+B}"
			
			labelAxis( name, hRatio, Groom )
			hRatio.GetYaxis().SetTitleOffset(1.2)
			hRatio.GetXaxis().SetLabelSize(0.12)
			hRatio.GetXaxis().SetTitleSize(0.12)
			#hRatio.GetYaxis().SetTitle("S / B")
			hRatio.GetYaxis().SetTitle( ratioLabel )
			hRatio.GetYaxis().SetLabelSize(0.12)
			hRatio.GetYaxis().SetTitleSize(0.12)
			hRatio.GetYaxis().SetTitleOffset(0.45)
			hRatio.GetYaxis().CenterTitle()
			#hRatio.SetMaximum(0.7)
			if xmax: hRatio.GetXaxis().SetRangeUser( xmin, xmax )
			#tmpFit = TF1( 'tmpFit', 'pol0', 60, 200 )
			#hRatio.Fit( 'tmpFit', '', '', 60, 200 )
			hRatio.Draw( ("PES" if 'DATA' in args.process else "hist" ) )
			'''
			tmpFit.SetLineColor( kGreen )
			tmpFit.SetLineWidth( 2 )
			tmpFit.Draw("sames")
			chi2Test = TLatex( 0.7, 0.8, '#splitline{#chi^{2}/ndF = '+ str( round( tmpFit.GetChisquare(), 2 ) )+'/'+str( int( tmpFit.GetNDF() ) )+'}{p0 = '+ str( round( tmpFit.GetParameter( 0 ), 2 ) ) +' #pm '+str(  round( tmpFit.GetParError( 0 ), 2 ) )+'}' )
			chi2Test.SetNDC()
			chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
			chi2Test.SetTextSize(0.10)
			chi2Test.Draw('same')
			'''

			if 'DATA' in args.process: 
				hRatio.GetYaxis().SetNdivisions(505)
				line.Draw('same')

		can.SaveAs( 'Plots/'+outputFileName )
		del can

	else:

  		tdrStyle.SetPadRightMargin(0.05)
		can = TCanvas('c1', 'c1', 750, 500 )
		if log: can.SetLogy()
		signalHistos[args.mass].GetYaxis().SetTitleOffset(1.0)
		signalHistos[args.mass].GetYaxis().SetTitle( ( 'Normalized / '+str(int(binWidth))+' GeV' if name in [ 'massAve', 'HT', 'jet1Pt', 'jet2Pt', 'MET' ] else 'Normalized' ) )
		if xmax: signalHistos[args.mass].GetXaxis().SetRangeUser( xmin, xmax )
		labelAxis( name, signalHistos[args.mass], Groom )
		signalHistos[args.mass].Draw('hist')
		if len(signalHistos) > 1:
			for signalSamples in signalHistos:
				if not args.mass in signalSamples: signalHistos[ signalSamples ].Draw('hist same')
		for bkgSamples in bkgHistos: bkgHistos[ bkgSamples ].Draw('hist same')
		signalHistos[args.mass].SetMaximum( 1.1 * max( maxList ) )

		CMS_lumi.lumi_13TeV = ''
		CMS_lumi.relPosX = 0.11
		CMS_lumi.CMS_lumi(can, 4, 0)
		legend.Draw()
		if not (labX and labY): labels( ( '' if 'n-1' in nameInRoot else 'presel'), args.camp )
		else: labels( ( '' if 'n-1' in nameInRoot else 'presel'), args.camp, labX, labY )

		can.SaveAs( 'Plots/'+outputFileName )
		del can

def plot2DSignalBkg( bkgFiles, Groom, nameInRoot, name, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+args.mass+'_QCD'+args.qcd+'_PlusBkg_'+args.boosted+'AnalysisPlots'+args.version+'.'+args.ext 
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	bkgHistosProfile = OrderedDict()
	tmpText = ''
	if len(bkgFiles) > 0:
		for bkgSamples in bkgFiles:
			tmpText = bkgSamples
			bkgHistos[ bkgSamples ] =  bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_Bkg' )
			bkgHistos[ bkgSamples ] = Rebin2D( bkgHistos[ bkgSamples ], rebinx, rebiny )
			bkgHistosProfile[ bkgSamples ] = bkgHistos[ bkgSamples ].ProfileY( bkgSamples, Ymin, Ymax ) 
			if bkgFiles[ bkgSamples ][1] != 1: bkgHistos[ bkgSamples ].Scale( bkgFiles[ bkgSamples ][1] ) 

	CMS_lumi.extraText = "Simulation Preliminary"
	#if 'QCD' in tmpText: 
	#	hBkg = bkgHistos[ 'QCDHT500to700' ].Clone()
	#	for samples in bkgHistos:
	#		if 'QCDHT500to700' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )
	#else: hBkg = bkgHistos[ tmpText ].Clone()

	hBkg.GetXaxis().SetTitle( titleXAxis )
	hBkg.GetYaxis().SetTitleOffset( 0.9 )
	hBkg.GetYaxis().SetTitle( titleXAxis2 )

	if (Xmax or Ymax):
		hBkg.GetXaxis().SetRangeUser( Xmin, Xmax )
		hBkg.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	hBkg.Draw('colz')

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (legX and legY): labels( name, args.camp )
	else: labels( name, args.camp, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+args.ext, 'gif') )
	del can

def Rebin2D( h1, rebinx, rebiny ):
	"""docstring for Rebin2D"""

	tmph1 = h1.Clone()
	nbinsx = h1.GetXaxis().GetNbins()
	nbinsy = h1.GetYaxis().GetNbins()
	xmin  = h1.GetXaxis().GetXmin()
	xmax  = h1.GetXaxis().GetXmax()
	ymin  = h1.GetYaxis().GetXmin()
	ymax  = h1.GetYaxis().GetXmax()
	nx = nbinsx/rebinx
	ny = nbinsy/rebiny
	h1.SetBins( nx, xmin, xmax, ny, ymin, ymax )

	for biny in range( 1, nbinsy):
		for binx in range(1, nbinsx):
			ibin1 = h1.GetBin(binx,biny)
			h1.SetBinContent( ibin1, 0 )
		
	for biny in range( 1, nbinsy):
		by = tmph1.GetYaxis().GetBinCenter( biny )
		iy = h1.GetYaxis().FindBin(by)
		for binx in range(1, nbinsx):
			bx = tmph1.GetXaxis().GetBinCenter(binx)
			ix  = h1.GetXaxis().FindBin(bx)
			bin = tmph1.GetBin(binx,biny)
			ibin= h1.GetBin(ix,iy)
			cu  = tmph1.GetBinContent(bin)
			h1.AddBinContent(ibin,cu)
	return h1

def plot2D( inFiles, sample, Groom, nameInRoot, name, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+sample+'_'+args.camp+'_'+args.boosted+'AnalysisPlots'+args.version+'.'+args.ext 
	print 'Processing.......', outputFileName
	#for samples in inFiles:
		#h1 = inFiles[ samples ][0].Get( nameInRoot+'_'+sample if 'RPV' in sample else nameInRoot+'_'+samples )
		#h1 = inFiles[ samples ][0].Get( nameInRoot )
	h1 = inFiles.Get( nameInRoot+'_'+sample  )
	#h1 = inFile.Get( 'AnalysisPlots'+Groom+'/'+name )
	#h1 = inFile.Get( 'TriggerEfficiency'+Groom+'/'+name )
	tmph1 = h1.Clone()
	
	### Rebinning
	nbinsx = h1.GetXaxis().GetNbins()
	nbinsy = h1.GetYaxis().GetNbins()
	xmin  = h1.GetXaxis().GetXmin()
	xmax  = h1.GetXaxis().GetXmax()
	ymin  = h1.GetYaxis().GetXmin()
	ymax  = h1.GetYaxis().GetXmax()
	nx = nbinsx/rebinx
	ny = nbinsy/rebiny
	h1.SetBins( nx, xmin, xmax, ny, ymin, ymax )

	for biny in range( 1, nbinsy):
		for binx in range(1, nbinsx):
			ibin1 = h1.GetBin(binx,biny)
			h1.SetBinContent( ibin1, 0 )
		
	for biny in range( 1, nbinsy):
		by = tmph1.GetYaxis().GetBinCenter( biny )
		iy = h1.GetYaxis().FindBin(by)
		for binx in range(1, nbinsx):
			bx = tmph1.GetXaxis().GetBinCenter(binx)
			ix  = h1.GetXaxis().FindBin(bx)
			bin = tmph1.GetBin(binx,biny)
			ibin= h1.GetBin(ix,iy)
			cu  = tmph1.GetBinContent(bin)
			h1.AddBinContent(ibin,cu)

	#h1.Scale( inFiles[ samples ][1] )
	h1.GetXaxis().SetTitle( titleXAxis )
	h1.GetYaxis().SetTitleOffset( 1.0 )
	h1.GetYaxis().SetTitle( titleXAxis2 )

	if (Xmax or Ymax):
		h1.GetXaxis().SetRangeUser( Xmin, Xmax )
		h1.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	if 'Boosted' in args.boosted: h1.SetMaximum(5000)
	h1.Draw('colz')

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (legX and legY): labels( name, args.camp )
	else: labels( name, args.camp, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+args.ext, 'gif') )
	del can


def plotCutFlow( signalFiles, bkgFiles, Groom, name, xmax, log, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+args.mass+'_Bkg_AnalysisPlots'+args.version+'.'+args.ext 
	print 'Processing.......', outputFileName

	histos = {}
	histosErr = {}

	if len(signalFiles) > 0:
		for samples in signalFiles:
			histos[ samples ] = signalFiles[ samples ][0].Get(name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass))
			if signalFiles[ samples ][1] != 1: histos[ samples ].Scale( signalFiles[ samples ][1] ) 

	dummy = 0
	if len(bkgFiles) > 0:
		for samples in bkgFiles:
			dummy += 1
			print samples
			histos[ samples ] = bkgFiles[ samples ][0].Get(name+'_'+samples)
			if bkgFiles[ samples ][1] != 1: histos[ samples ].Scale( bkgFiles[ samples ][1] ) 
			if (dummy == 1): hBkg = histos[ samples ].Clone()

	hSignal = histos[ 'Signal' ].Clone()
	hQCD = histos[ 'QCD'+args.qcd+'All' ].Clone()
	hTTJets = histos[ 'TTJets' ].Clone()
	hWJetsToQQ = histos[ 'WJetsToQQ' ].Clone()
	hWWTo4Q = histos[ 'WWTo4Q' ].Clone()
	hZJetsToQQ = histos[ 'ZJetsToQQ' ].Clone()
	hZZTo4Q = histos[ 'ZZTo4Q' ].Clone()
	hWZ = histos[ 'WZ' ].Clone()

	for bin in range(0,  hSignal.GetNbinsX()):
		hSignal.SetBinContent(bin, 0.)
		hSignal.SetBinError(bin, 0.)
		hQCD.SetBinContent(bin, 0.)
		hQCD.SetBinError(bin, 0.)
		hTTJets.SetBinContent(bin, 0.)
		hTTJets.SetBinError(bin, 0.)
		hWJetsToQQ.SetBinContent(bin, 0.)
		hWJetsToQQ.SetBinError(bin, 0.)
		hWWTo4Q.SetBinContent(bin, 0.)
		hWWTo4Q.SetBinError(bin, 0.)
		hZJetsToQQ.SetBinContent(bin, 0.)
		hZJetsToQQ.SetBinError(bin, 0.)
		hZZTo4Q.SetBinContent(bin, 0.)
		hZZTo4Q.SetBinError(bin, 0.)
		hWZ.SetBinContent(bin, 0.)
		hWZ.SetBinError(bin, 0.)
	
	totalEventsSignal = histos[ 'Signal' ].GetBinContent(1)
	totalEventsQCD = histos[ 'QCD'+args.qcd+'All' ].GetBinContent(1)
	totalEventsTTJets = histos[ 'TTJets' ].GetBinContent(1)
	totalEventsWJetsToQQ = histos[ 'WJetsToQQ' ].GetBinContent(1)
	totalEventsWWTo4Q = histos[ 'WWTo4Q' ].GetBinContent(1)
	totalEventsZJetsToQQ = histos[ 'ZJetsToQQ' ].GetBinContent(1)
	totalEventsZZTo4Q = histos[ 'ZZTo4Q' ].GetBinContent(1)
	totalEventsWZ = histos[ 'WZ' ].GetBinContent(1)
	#print totalEventsSignal, totalEventsQCD

	cutFlowSignalList = []
	cutFlowQCDList = []
	cutFlowTTJetsList = []
	cutFlowWJetsToQQList = []
	cutFlowWWTo4QList = []
	cutFlowZJetsToQQList = []
	cutFlowZZTo4QList = []
	cutFlowWZList = []

	for ibin in range(0, hQCD.GetNbinsX()+1):
	
		cutFlowSignalList.append( histos[ 'Signal' ].GetBinContent(ibin) )
		cutFlowQCDList.append( histos[ 'QCD'+args.qcd+'All' ].GetBinContent(ibin) )
		cutFlowTTJetsList.append( histos[ 'TTJets' ].GetBinContent(ibin) )
		cutFlowWJetsToQQList.append( histos[ 'WJetsToQQ' ].GetBinContent(ibin) )
		cutFlowWWTo4QList.append( histos[ 'WWTo4Q' ].GetBinContent(ibin) )
		cutFlowZJetsToQQList.append( histos[ 'ZJetsToQQ' ].GetBinContent(ibin) )
		cutFlowZZTo4QList.append( histos[ 'ZZTo4Q' ].GetBinContent(ibin) )
		cutFlowWZList.append( histos[ 'WZ' ].GetBinContent(ibin) )

		hSignal.SetBinContent( ibin , histos[ 'Signal' ].GetBinContent(ibin) / totalEventsSignal )
		hQCD.SetBinContent( ibin , histos[ 'QCD'+args.qcd+'All' ].GetBinContent(ibin) / totalEventsQCD )
		hTTJets.SetBinContent( ibin , histos[ 'TTJets' ].GetBinContent(ibin) / totalEventsTTJets )
		hWJetsToQQ.SetBinContent( ibin , histos[ 'WJetsToQQ' ].GetBinContent(ibin) / totalEventsWJetsToQQ )
		hWWTo4Q.SetBinContent( ibin , histos[ 'WWTo4Q' ].GetBinContent(ibin) / totalEventsWWTo4Q )
		hZJetsToQQ.SetBinContent( ibin , histos[ 'ZJetsToQQ' ].GetBinContent(ibin) / totalEventsZJetsToQQ )
		hZZTo4Q.SetBinContent( ibin , histos[ 'ZZTo4Q' ].GetBinContent(ibin) / totalEventsZZTo4Q )
		hWZ.SetBinContent( ibin , histos[ 'WZ' ].GetBinContent(ibin) / totalEventsWZ )
		
	hSB = hSignal.Clone()
	hBkg = hQCD.Clone()
	hBkg.Add( hTTJets )
	hBkg.Add( hWJetsToQQ )
	hBkg.Add( hWWTo4Q )
	hBkg.Add( hZJetsToQQ )
	hBkg.Add( hZZTo4Q )
	hBkg.Add( hWZ )
	hSB.Divide( hBkg )
	hSB.GetXaxis().SetBinLabel( ibin, '')
	print "Signal", cutFlowSignalList
	print "QCD", cutFlowQCDList
	print "TTJets", cutFlowTTJetsList
	print "WJetsToQQ", cutFlowWJetsToQQList
	print "WWTo4Q", cutFlowWWTo4QList
	print "ZJetsToQQ", cutFlowZJetsToQQList
	print "ZZTo4Q", cutFlowZZTo4QList
	print "WZ", cutFlowWZList
	print 'total', [ cutFlowQCDList[i] + cutFlowTTJetsList[i] +cutFlowWJetsToQQList[i] + cutFlowWWTo4QList[i] + cutFlowZJetsToQQList[i] + cutFlowZZTo4QList[i] + cutFlowWZList[i]  for i in range(len(cutFlowQCDList))]

	#hSB = hSignal.Clone()
	#hSB.Divide( hQCD )

	binWidth = histos['Signal'].GetBinWidth(1)

	legend=TLegend(0.60,0.67,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	hSignal.SetLineWidth(2)
	hSignal.SetLineColor(kRed-4)
	hQCD.SetLineWidth(2)
	hQCD.SetLineColor(kBlue-4)
	hTTJets.SetLineWidth(2)
	hTTJets.SetLineColor(kGreen-4)
	hWJetsToQQ.SetLineWidth(2)
	hWJetsToQQ.SetLineColor(kMagenta-4)
	hWWTo4Q.SetLineWidth(2)
	hWWTo4Q.SetLineColor(kMagenta-6)
	#hZJets.SetLineWidth(2)
	#hZJets.SetLineColor(kOrange-4)
	hZZTo4Q.SetLineWidth(2)
	hZZTo4Q.SetLineColor(kMagenta-6)

	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.20,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: 
		pad1.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
		hSignal.GetYaxis().SetTitleOffset(0.9)
	else:
		outName = outputFileName 

	pad1.SetGridx()
	legend.AddEntry( hSignal, args.decay+'RPV #tilde{t} '+args.mass+' GeV' , 'l' )
	legend.AddEntry( hQCD, 'QCD', 'l' )
	legend.AddEntry( hTTJets, 't #bar{t} + Jets' , 'l' )
	legend.AddEntry( hWJetsToQQ, 'W + Jets' , 'l' )
	legend.AddEntry( hWWTo4Q, 'WW (had)' , 'l' )
	#legend.AddEntry( hZJets, 'Z + Jets' , 'l' )
	legend.AddEntry( hZZTo4Q, 'ZZ (had)' , 'l' )
	hSignal.GetYaxis().SetTitle( 'Percentage / '+str(binWidth) )
	hSignal.GetXaxis().SetRangeUser( 1, xmax )

	hSignal.SetMinimum(0.0001)
	hSignal.Draw()
	hQCD.Draw('same')
	hTTJets.Draw('same')
	hWJetsToQQ.Draw('same')
	hWWTo4Q.Draw('same')
	#hZJets.Draw('same')
	hZZTo4Q.Draw('same')

	legend.Draw()
	CMS_lumi.relPosX = 0.14
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	#labels( name, '', '', '' )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	hSB.GetYaxis().SetTitle("S / B")
	hSB.GetYaxis().SetLabelSize(0.12)
	hSB.GetXaxis().SetLabelSize(0.12)
	hSB.GetYaxis().SetTitleSize(0.12)
	hSB.GetXaxis().SetTitleSize(0.12)
	hSB.GetYaxis().SetTitleOffset(0.45)
	#hSB.SetMaximum(0.7)
	hSB.GetXaxis().SetRangeUser( 1, xmax )
	hSB.Sumw2()
	hSB.Draw("hist")

	can.SaveAs( 'Plots/'+outName )
	del can

def plotSignalCutFlow( runaFile, miniRunaFile, xmax, log, Norm=False ):
	"""docstring for plot"""

	outputFileName = 'signalCutFlow_'+args.grooming+'_'+args.decay+'RPVSt'+args.mass+'_Bkg_'+args.RANGE+'_AnalysisPlots'+args.version+'.'+args.ext 
	print 'Processing.......', outputFileName

	if 'low' in args.RANGE: massList = [ 90, 100, 110, 120, 130, 140, 150 ] 
	else: massList = [ 170, 180, 190, 210, 220, 230, 240 ] 

	cutFlowValues = OrderedDict()
	histos = OrderedDict()
	for m in massList:
		RUNAFile = TFile( runaFile.replace( '100', str(m) ) )
		cutFlowRUNA = RUNAFile.Get('BoostedAnalysisPlots/cutflow')
		tmpCutflow = []
		cutLabels = []
		for i in range( 1, cutFlowRUNA.GetNbinsX()+1 ): 
			tmpCutflow.append( cutFlowRUNA.GetBinContent( i ) )
			cutLabels.append( cutFlowRUNA.GetXaxis().GetBinLabel( i ) )

		miniRUNAFile = TFile( miniRunaFile.replace( '100', str(m) ) )
		cutFlowMiniRUNA = miniRUNAFile.Get('cutflow_RPVStopStopToJets_'+args.decay+'_M-'+str(m))
		for j in range( 1, cutFlowMiniRUNA.GetNbinsX()+1 ): 
			tmpCutflow.append( cutFlowMiniRUNA.GetBinContent( j ) )
			cutLabels.append( cutFlowMiniRUNA.GetXaxis().GetBinLabel( j ) )
		cutFlowValues[ m ] = tmpCutflow

	legend=TLegend(0.60,0.67,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	dummy=1
	for p in cutFlowValues:
		histos[ p ] = TH1F( 'cutflow'+str(p), 'cutflow'+str(p), len(cutFlowValues[p]), 0, len(cutFlowValues[p]) )
		for q in range( 1, len(cutFlowValues[p])+1 ):
			histos[p].SetBinContent( q, cutFlowValues[p][q-1]/cutFlowValues[p][0] )
			histos[p].GetXaxis().SetBinLabel( q, cutLabels[q-1] )
		legend.AddEntry( histos[p], args.decay+' RPV #tilde{t} '+str(p)+' GeV' , 'l' )
		histos[ p ].SetLineWidth(2)
		histos[ p ].SetLineColor( dummy )
		dummy+= 1


	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	#pad1 = TPad("pad1", "Fit",0,0.20,1.00,1.00,-1)
	#pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	#pad1.Draw()
	#pad2.Draw()

	can.SetLogy()

	can.SetGridx()
	histos[ massList[0] ].GetYaxis().SetTitle( 'Percentage' )
	histos[ massList[0] ].GetYaxis().SetTitleOffset( 0.8 )
	histos[ massList[0] ].GetXaxis().SetRangeUser( 0, xmax )

	histos[ massList[0] ].Draw()
	for k in histos: 
		if (k != massList[0]): histos[ k ].Draw("same")

	legend.Draw()
	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.lumi_13TeV = ''
	CMS_lumi.relPosX = 0.12
	CMS_lumi.CMS_lumi(can, 4, 0)
	can.SaveAs( 'Plots/'+outputFileName )
	del can

def plotSignalShape( miniRunaFile, nameInRoot, rebinX, log ):
	"""docstring for plot"""

	outputFileName = 'signalShape_'+nameInRoot+'_'+args.grooming+'_'+args.decay+'RPVSt_'+args.RANGE+'_AnalysisPlots'+args.version+'.'+args.ext 
	print 'Processing.......', outputFileName

	legend=TLegend(0.70,(0.5 if 'Tau21' in nameInRoot else 0.60),0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	histos = {}
	files = {}
	dummy=1
	
#	if 'Tau21' in nameInRoot: 
	massList = [80, 100, 120, 140, 150, 170, 190, 210, 240, 300 ]
	massWidthList = [8.56280909196305, 8.950556420141245, 8.814786972730516, 10.392360104091987, 9.435770844457956, 10.268425520508536, 12.86644189449206, 10.084924444431165, 12.94592267653858, 15.762703291273564]
	outputFileName = outputFileName.replace( '_low', '' )
#	else:
#		if 'low' in args.RANGE: massList = [ 80, 100, 120, 140 ] 
#		else: massList = [ 170, 210, 240, 300, 350 ] 

	for M in massList:
		fileName = miniRunaFile.replace( '100', str(M) )
		#if ( 'Tau21' in nameInRoot ) and ( M > 150 ): fileName = fileName.replace( 'low', 'high' )
		files[ M ] = TFile( fileName )
	
	maxList = []
	for m in range( len(massList) ): 
		scale = scaleFactor( 'RPVStopStopToJets_'+args.decay+'_M-'+str(massList[m]) ) * 2666
		histos[ massList[m] ] = files[ massList[m] ].Get( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str( massList[m] ) )
		histos[ massList[m] ].Scale( 1/scale )
		if 'massAve' in nameInRoot: histos[ massList[m] ].Scale( 0.89 ) #### two prong scale factor
		if rebinX > 1: histos[ massList[m] ] = histos[ massList[m] ].Rebin( rebinX )
		legend.AddEntry( histos[ massList[m] ], 'M_{#tilde{t}} = '+str( massList[m] )+' GeV' , 'l' )
		histos[ massList[m] ].SetLineWidth(2)
		histos[ massList[m] ].SetLineColor( dummy )
		histos[ massList[m] ].GetXaxis().SetRangeUser( massList[m]-(int(massWidthList[m])), massList[m]+(int(massWidthList[m]) ) )
		binWidth = histos[ massList[m] ].GetBinWidth(1)
		maxList.append( histos[ massList[m] ].GetMaximum() )
		dummy+= 1
		if dummy == 5: dummy = 6
		if dummy == 9: dummy = 40


	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	if log: can.SetLogy()

	histos[ massList[-1] ].GetYaxis().SetTitle( 'Events / '+str(binWidth)+' GeV' )
	histos[ massList[-1] ].GetYaxis().SetTitleOffset( 0.95 )
	if 'mass' in nameInRoot: histos[ massList[-1] ].GetXaxis().SetRangeUser( 50, 350 ) #(50 if 'low' in args.RANGE else 100 ) , ( 250 if 'low' in args.RANGE else 400 ) )
	elif 'Pt' in nameInRoot: histos[ massList[-1] ].GetXaxis().SetRangeUser( 200, 2000 ) 

	#histos[ massList[-1] ].SetMinimum( (0.1 if 'high' in args.RANGE else 0.00001 ) )
	histos[ massList[-1] ].SetMaximum( 1.2*max(maxList) )
	histos[ massList[-1] ].Draw('hist')
	for k in histos: 
		if (k != massList[-1]): histos[ k ].Draw("hist same")

	legend.Draw()
	labelAxis( nameInRoot, histos[ massList[-1] ], 'pruned' )
	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.lumi_13TeV = ''
	CMS_lumi.relPosX = 0.12
	CMS_lumi.CMS_lumi(can, 4, 0)
	can.SaveAs( 'Plots/'+outputFileName )
	del can


def plotSignalAcceptance( miniRunaFile, nameInRoot, log ):
	"""docstring for plot acceptance"""

	outputFileName = 'signalAcceptance_'+nameInRoot+'_'+args.grooming+'_'+args.decay+'RPVSt_'+args.RANGE+'_AnalysisPlots_diffVersions.'+args.ext 
	print 'Processing.......', outputFileName

	legend=TLegend(0.60,(0.5 if 'Tau21' in nameInRoot else 0.67),0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	histos = {}
	files = {}
	dummy=1
	
#	if 'Tau21' in nameInRoot: 
	#massList = [80, 100, 120, 140, 150, 170, 190, 210, 230, 300, 350 ]
	#outputFileName = outputFileName.replace( '_low', '' )
#	else:
	accXeffGraph= {}
	for ver in [ 'v05p3' ]: # 'v05', 'v05p2', 'v05p3' ]:
		massesList = []
		accXeffList = []
		accXeffErrList = []
		for sel in [ 'low', 'high' ]:
			if args.version in [ 'v05' ]: 
				if 'low' in sel: massList = [ 80, 90, 100, 110, 120, 130, 140, 150 ] 
				else: massList = [ 170, 180, 190, 210, 230, 240, 300, 350 ] 
			else: 
				massList = [ 80, 90, 100, 110, 120, 130, 140, 150, 170, 180, 190, 210, 230, 240, 300] 
				massWidthList = [8.56280909196305, 8.445039648677378, 8.950556420141245, 9.860254339542022, 8.814786972730516, 10.021433248818914, 10.392360104091987, 9.435770844457956, 10.268425520508536, 10.45176971177987, 12.86644189449206, 10.084924444431165, 12.431737065699405, 10.809084324420656, 12.94592267653858, 15.762703291273564]

			for M in massList:
				fileName = miniRunaFile.replace( '100', str(M) ).replace( args.version, ver )
				if ('high' in sel) and ( ver in [ 'v05' ]): fileName = fileName.replace( 'low', 'high' )
				files[ M ] = TFile( fileName )
			
			for m in range( len(massList) ): 
				NAME = 'RPVStopStopToJets_'+args.decay+'_M-'+str( massList[m] )
				scale = scaleFactor( NAME  ) * 2666
				events = search( dictEvents, NAME )[0]
				histos[ massList[m] ] = files[ massList[m] ].Get( nameInRoot+'_'+NAME )
				histos[ massList[m] ].Scale( 1/scale )
				histos[ massList[m] ].Scale( 0.89 ) ### due to two prong tagger
				eventsInWindow = histos[ massList[m] ].Integral( massList[m]-(int(2*massWidthList[m])), massList[m]+(int(2*massWidthList[m])) )
				failedEvents = events - eventsInWindow
				#acceptance = eventsInHisto/events
				#efficiency = eventsInWindow/eventsInHisto
				#accXeff = acceptance * efficiency
				accXeff = eventsInWindow / events 
				accXeffErr = sqrt( (1/failedEvents) + (1/eventsInWindow) ) * failedEvents * eventsInWindow / pow( ( events ), 2 )
				print m, eventsInWindow, accXeff, accXeffErr
				massesList.append( massList[m] )
				accXeffList.append( accXeff )
				accXeffErrList.append( accXeffErr )
		accXeffGraph[ ver ] = TGraphErrors(len(massesList), array( 'd', massesList), array( 'd', accXeffList), array('d', [0]*len(massesList)), array('d', accXeffErrList) )

	multiGraph = TMultiGraph()
	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	#if log: can.SetLogy()
	can.SetLogy()
	'''
	accXeffGraph[ 'v05' ].SetLineColor(1)
	accXeffGraph[ 'v05' ].SetLineWidth(2)
	accXeffGraph[ 'v05' ].SetMarkerStyle(8)
	legend.AddEntry( accXeffGraph[ 'v05' ], 'Nominal', 'l' )
	multiGraph.Add( accXeffGraph[ 'v05' ] )

	accXeffGraph[ 'v05p2' ].SetLineColor(2)
	accXeffGraph[ 'v05p2' ].SetLineWidth(2)
	accXeffGraph[ 'v05p2' ].SetMarkerStyle(8)
	legend.AddEntry( accXeffGraph[ 'v05p2' ], '#tau_{21} < 0.5', 'l' )
	multiGraph.Add( accXeffGraph[ 'v05p2' ] )
	'''

	accXeffGraph[ 'v05p3' ].SetLineColor(kRed)
	accXeffGraph[ 'v05p3' ].SetLineWidth(2)
	accXeffGraph[ 'v05p3' ].SetMarkerStyle(8)
	legend.AddEntry( accXeffGraph[ 'v05p3' ], '#tau_{21} < 0.45', 'l' )
	multiGraph.Add( accXeffGraph[ 'v05p3' ] )

	multiGraph.Draw("ap")
	multiGraph.GetYaxis().SetTitle( 'Acceptance #times efficiency' )
	multiGraph.GetXaxis().SetTitle( "Stop mass [GeV]" )
	multiGraph.GetYaxis().SetTitleOffset( 0.8 )
	#histos[ massList[0] ].GetXaxis().SetRangeUser( (50 if 'low' in args.RANGE else 100 ) , ( 250 if 'low' in args.RANGE else 400 ) )

	#histos[ massList[0] ].SetMinimum( (0.1 if 'high' in args.RANGE else 0.00001 ) )
	#histos[ massList[0] ].SetMaximum( 1.2*max(maxList) )
	#histos[ massList[0] ].Draw('hist')

	#legend.Draw()
	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.lumi_13TeV = ''
	CMS_lumi.relPosX = 0.12
	CMS_lumi.CMS_lumi(can, 4, 0)
	can.SaveAs( 'Plots/'+outputFileName )
	del can

def plotSimple( inFile, sample, Groom, name, xmax, labX, labY, log, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+sample+'_AnalysisPlots'+args.version+'.'+args.ext 
	print 'Processing.......', outputFileName

	histo = inFile.Get( args.boosted+'AnalysisPlots'+Groom+'/'+name )

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )
	binWidth = histo.GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	#histo.SetFillColor(48)
	histo.SetFillStyle(1001)

	tdrStyle.SetPadRightMargin(0.05)
	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )

	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
	else:
		outName = outputFileName 

	legend.AddEntry( histo, sample, 'f' )
	histo.GetYaxis().SetTitleOffset(0.90)
	histo.Draw('hist')
	histo.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	labelAxis( name, histo, '' )
	legend.Draw()
	if not (labX and labY): labels( '', sample )
	else: labels( '', 'MC Truth', labX, labY )
	can.SaveAs( 'Plots/'+outName )
	del can

def plotDiffSample( inFileSample1, inFileSample2, sample1, sample2, Groom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+args.mass+'_Diff'+Diff+'.'+args.ext 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample1.Get( args.boosted+'AnalysisPlots'+Groom+'/'+name )
	histos[ 'Sample2' ] = inFileSample2.Get( args.boosted+'AnalysisPlots'+Groom+'/'+name )

	hSample1 = histos[ 'Sample2' ].Clone()
	hSample2 = histos[ 'Sample1' ].Clone()
	hSample1.Divide( hSample2 )

	binWidth = histos['Sample1'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	if not Norm:
		histos[ 'Sample1' ].SetLineWidth(2)
		histos[ 'Sample1' ].SetLineColor(48)
		histos[ 'Sample2' ].SetLineColor(38)
		histos[ 'Sample2' ].SetLineWidth(2)
		#histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
		#histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )

		can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
		pad1 = TPad("pad1", "Fit",0,0.25,1.00,1.00,-1)
		pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.25,-1);
		pad1.Draw()
		pad2.Draw()

		pad1.cd()
		if log: 
			pad1.SetLogy()
			outName = outputFileName.replace('_Diff','_Log_Diff')
		else:
			outName = outputFileName 

		legend.AddEntry( histos[ 'Sample1' ], sample1, 'l' )
		legend.AddEntry( histos[ 'Sample2' ], sample2, 'l' )
		histos['Sample1'].SetMinimum(10)
		histos['Sample1'].Draw('hist')
		histos['Sample1'].GetYaxis().SetTitleOffset(1.2)
		histos['Sample2'].Draw('hist same')
		histos['Sample1'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		labelAxis( name, histos['Sample1'], Groom )
		legend.Draw()
		if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		pad2.cd()
		hSample1.SetLineColor(48)
		#hSample1.SetFillStyle(1001)
		hSample1.GetYaxis().SetTitle("Ratio")
		hSample1.GetYaxis().SetLabelSize(0.12)
		hSample1.GetXaxis().SetLabelSize(0.12)
		hSample1.GetYaxis().SetTitleSize(0.12)
		hSample1.GetYaxis().SetTitleOffset(0.45)
		#hSample1.SetMaximum(1.0)
		hSample1.Sumw2()
		hSample1.Draw("histe")

		can.SaveAs( 'Plots/'+outName )
		del can
	else:
		histos[ 'Sample1' ].SetLineWidth(2)
		histos[ 'Sample1' ].SetLineColor(48)
		histos[ 'Sample2' ].SetLineColor(38)
		histos[ 'Sample2' ].SetLineWidth(2)

		can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		if log: 
			can.SetLogy()
			outName = outputFileName.replace('_Diff','_Log_Norm_Diff')
			histos[ 'Sample1' ].GetYaxis().SetTitleOffset(1.2)
		else:
			outName = outputFileName.replace('_Diff','_Norm_Diff')

		legend.AddEntry( histos[ 'Sample1' ], sample1 , 'l' )
		legend.AddEntry( histos[ 'Sample2' ], sample2 , 'l' )
		histos['Sample1'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )

		histos['Sample1'].DrawNormalized()
		histos['Sample2'].DrawNormalized('same')

		legend.Draw()
		labelAxis( name, histos['Sample1'], Groom )
		if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can


def plotQuality( dataFile, bkgFiles, Groom, nameInRoot, name, xmin, xmax, rebinX, labX, labY, log, moveCMSlogo=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_QCD'+args.qcd+'_'+args.RANGE+'_dataQuality'+args.boosted+'Plots'+args.version+'.'+args.ext
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Data' ] = dataFile.Get( nameInRoot+'_DATA' if 'qual' in args.process else nameInRoot )
	if rebinX > 1: histos[ 'Data' ].Rebin( rebinX )
	hBkg = histos[ 'Data'].Clone()
	hBkg.Reset()

	for samples in bkgFiles:
		histos[ samples ] = bkgFiles[ samples ][0].Get( nameInRoot+'_'+samples if 'qual' in args.process else nameInRoot )
		if bkgFiles[ samples ][1] != 1: histos[ samples ].Scale( bkgFiles[ samples ][1] ) 
		if rebinX > 1: histos[ samples ].Rebin( rebinX )
		hBkg.Add( histos[ samples ].Clone() )

	hData = histos[ 'Data' ].Clone()
	hRatio = histos[ 'Data' ].Clone()
	hRatio.Divide( hBkg )
	#hData.Scale( 1/hData.Integral() )
	#hBkg.Scale( 1/hBkg.Integral() )
	
	'''
	for bin in range(0,  hSoSB.GetNbinsX()):
		hSoSB.SetBinContent(bin, 0.)
		hSoSB.SetBinError(bin, 0.)

	hSoSB2 = hSoSB.Clone()
	for ibin in range(0, hSoSB.GetNbinsX()):
	
		binContData = histos[ 'Data' ].GetBinContent(ibin)
		binErrData = histos[ 'Data' ].GetBinError(ibin)
		binContBkg = histos[ 'QCD' ].GetBinContent(ibin) + histos[ 'TTJets' ].GetBinContent(ibin) + histos[ 'WJets' ].GetBinContent(ibin) + histos[ 'ZJets' ].GetBinContent(ibin)    
		binErrBkg = histos[ 'QCD' ].GetBinError(ibin)
		try:
			value = binContData / TMath.Sqrt( binContData + binContBkg )
		except ZeroDivisionError: continue
		hSoSB.SetBinContent( ibin, value )
	'''

	binWidth = histos['Data'].GetBinWidth(1)

	if (labY < 0.5) and ( labX < 0.5 ): legend=TLegend(0.20,0.50,0.50,0.62)
	elif (labX < 0.5): legend=TLegend(0.20,0.75,0.50,0.87)
	else: legend=TLegend(0.70,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( hData, 'DATA' , 'ep' )
	legend.AddEntry( hBkg, 'All MC Bkgs', 'lp' )

	hBkg.SetLineColor(kRed-4)
	hBkg.SetLineWidth(2)
	hData.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy() 	
	hData.Draw("E")
	hBkg.Draw('hist same')
	hData.SetMaximum( 1.2* max( hData.GetMaximum(), hBkg.GetMaximum() )  )
	#hData.GetYaxis().SetTitleOffset(1.2)
	if xmax: hData.GetXaxis().SetRangeUser( xmin, xmax )
	#hData.GetYaxis().SetTitle( 'Normalized / '+str(int(binWidth))+' GeV' )
	hData.GetYaxis().SetTitle( ( 'Events / '+str(int(binWidth))+' GeV' if name in [ 'massAve', 'HT', 'jet1Pt', 'jet2Pt', 'MET' ] else 'Events' ) )

	#CMS_lumi.relPosX = 0.13
	if moveCMSlogo: 
		CMS_lumi.cmsTextOffset = 0.1
		CMS_lumi.relPosX = 0.15
	else: 
		CMS_lumi.cmsTextOffset = 0.0
		CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( name, hData, Groom )
	legend.Draw()
	if 'deltaEtaDijet' in args.cut: finalLabels( 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), labX, labY )
	else: 
		if 'n-1' in args.cut: label = 'n-1 selection'
		else: label = 'Preselection'
		if not (labX and labY): setSelection( [ label ], '', ''  )
		else: setSelection( [ label ], labX, labY )

	pad2.cd()
	gStyle.SetOptFit(1)
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	#fitLine = TF1( 'fitLine', 'pol0', 900, 2000)
	#hRatio.Fit( fitLine, 'MIR')
	#hRatio.SetStats(True)
	labelAxis( name.replace( args.cut, ''), hRatio, Groom )
	hRatio.SetMarkerStyle(8)
	hRatio.GetXaxis().SetTitleOffset(1.1)
	hRatio.GetXaxis().SetLabelSize(0.12)
	hRatio.GetXaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetTitle("Data/Bkg")
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetTitleOffset(0.55)
	#if( hRatio.GetMaximum() > 2 ): hRatio.SetMaximum( 2.0 )
	hRatio.SetMaximum( 1.5 )
	hRatio.SetMinimum( 0.5 )
	if xmax: hRatio.GetXaxis().SetRangeUser( xmin, xmax )
	hRatio.GetYaxis().SetNdivisions(505)
	hRatio.GetYaxis().CenterTitle()
	hRatio.Draw('ES')
	#fitLine.Draw("sames")
	'''
	pad2.Update()
	st1 = hRatio.GetListOfFunctions().FindObject("stats")
	st1.SetX1NDC(.75)
	st1.SetX2NDC(.95)
	st1.SetY1NDC(.75)
	st1.SetY2NDC(.95)
	#st1.SetTextColor(kRed)
	pad2.Modified()
	'''
	'''
	hSoSB.SetFillColor(48)
	hSoSB.SetFillStyle(1001)
	hSoSB.GetYaxis().SetTitle("S / #sqrt{S+B}")
	hSoSB.GetYaxis().SetLabelSize(0.12)
	hSoSB.GetXaxis().SetLabelSize(0.12)
	hSoSB.GetYaxis().SetTitleSize(0.12)
	hSoSB.GetYaxis().SetTitleOffset(0.45)
	#hSoSB.SetMaximum(0.7)
	hSoSB.Sumw2()
	if xmax: hSoSB.GetXaxis().SetRangeUser( xmin, xmax )
	hSoSB.Draw("hist")
	'''

	can.SaveAs( 'Plots/'+ outputFileName )
	del can


def tmpplotDiffSample( sample1, sample2, Groom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+args.decay+'RPVSt'+args.mass+'_Diff'+Diff+'.'+args.ext 
	print 'Processing.......', outputFileName

	histos = {}
	#inFileSample1 = TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_pruned_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_v2.root')
	#histos[ 'Sample1' ] = inFileSample1.Get( 'massAve_deltaEtaDijet_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass) )
	inFileSample1 = TFile.Open( sample1 )
	#histos[ 'Sample1' ] = inFileSample1.Get( 'massAve_deltaEtaDijet_TTJets' )
	histos[ 'Sample1' ] = inFileSample1.Get( 'prunedMassAsym_RPVStopStopToJets_UDD312_M-100' )
	#histos[ 'Sample1' ].Rebin(10)
	inFileSample2 = TFile.Open( sample2 )
	#histos[ 'Sample2' ] = inFileSample2.Get( 'massAve_deltaEtaDijet_TTJets' )
	histos[ 'Sample2' ] = inFileSample2.Get( 'BoostedAnalysisPlots/prunedMassAsym_cutHT' )
	#histos[ 'Sample2' ].Rebin(10)
	#histos[ 'Sample2' ].Scale(0.4)

	#hSample1 = histos[ 'Sample2' ].Clone()
	#hSample2 = histos[ 'Sample1' ].Clone()
	#hSample1.Divide( hSample2 )

	binWidth = histos['Sample1'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	#histos[ 'Sample1' ].Scale( 1/ 2666 ) #histos['Sample1'].Integral()  )
	histos[ 'Sample2' ].Scale( 2666 ) #1/ histos['Sample1'].Integral()  )

	histos[ 'Sample1' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetLineColor(48)
	histos[ 'Sample2' ].SetLineColor(38)
	histos[ 'Sample2' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
	#histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	legend.AddEntry( histos[ 'Sample1' ], 'All events', 'l' )
	legend.AddEntry( histos[ 'Sample2' ], 'Only boosted events', 'l' )
	histos['Sample1'].SetMinimum(10)
	histos['Sample1'].Draw('histe')
	histos['Sample1'].GetYaxis().SetTitleOffset(0.9)
	histos['Sample2'].Draw('histe same')
	histos['Sample1'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.lumi_13TeV = ''
	CMS_lumi.relPosX = 0.14
	CMS_lumi.CMS_lumi(can, 4, 0)
	labelAxis( name, histos['Sample1'], '' )
	legend.Draw()
	#if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
	#else: 
	labels( 'presel', '', 0.82, 0.7 )

	can.SaveAs( 'Plots/'+outputFileName )
	del can


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-b', '--boosted', action='store', default='Boosted', help='Boosted or non boosted, example: Boosted' )
	parser.add_argument('-v', '--version', action='store', default='v05p3', help='Version: v01, v02.' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-C', '--cut', action='store', default='_deltaEtaDijet', help='cut, example: cutDEta' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-q', '--qcd', action='store', default='Pt', dest='qcd', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-c', '--camp', action='store', default='RunIISpring15MiniAODv2-74X', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=2666, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--ext', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-u', '--unc', action='store', default='JES', dest='unc',  help='Type of uncertainty' )
	parser.add_argument('-f', '--final', action='store_true', default=False, dest='final',  help='If plot is final' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	
	bkgFiles = OrderedDict() 
	signalFiles = OrderedDict()
	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 1 ) )+" fb^{-1}"
	
	if 'Pt' in args.qcd: 
		bkgLabel='(w QCD pythia8)'
		QCDSF = .77
	else: 
		bkgLabel='(w QCD madgraphMLM+pythia8)'
		QCDSF = 1.05

	if args.process in [ 'jetIDQual', '1D', '1DDATA' ]:
		dataFile = TFile.Open('Rootfiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_'+args.version+'.root')
		signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi, args.decay+' RPV #tilde{t} '+str(args.mass)+' GeV', kRed-4]
		###bkgFiles[ 'QCDHTAll' ] = [ TFile.Open('Rootfiles/RUNAnalysis_QCDHTAll_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi*1.05, 'QCDHT', kBlue-4 ]
		bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi, 't #bar{t} + Jets', kGreen ]
		bkgFiles[ 'WJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi , 'W + Jets', kMagenta ]
		bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi , 'WW (had)', kMagenta+2 ]
		bkgFiles[ 'ZJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi, 'Z + Jets', kOrange ]
		bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi, 'ZZ (had)', kOrange+2 ]
		bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi, 'WZ', kCyan ]
		bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open('Rootfiles/RUNAnalysis_QCD'+args.qcd+'All_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root'), args.lumi*QCDSF, 'QCD'+args.qcd+'', kBlue-4 ]
	else:
		dataFile = TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_DATA_'+args.RANGE+'_'+args.version+'.root')
		signalFiles[ args.mass ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_'+args.RANGE+'_'+args.version+'.root'), 1, 'M_{#tilde{t}} = '+str(args.mass)+' GeV', kRed-4]
		#signalFiles[ '170' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-170_'+args.RANGE+'_'+args.version+'.root'), 1, 'M_{#tilde{t}} = 170 GeV', 46]
		signalFiles[ '240' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-240_'+args.RANGE+'_'+args.version+'.root'), 1, 'M_{#tilde{t}} = 240 GeV', 28]
		#signalFiles[ '300' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-300_'+args.RANGE+'_'+args.version+'.root'), 1, 'M_{#tilde{t}} = 300 GeV', 30]
		bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'Z + Jets', kOrange]
		bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'W + Jets', kMagenta ]
		bkgFiles[ 'Dibosons' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_Dibosons_'+args.RANGE+'_'+args.version+'.root'), 1 , 'Dibosons', kMagenta+2 ]
		#bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WWTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1 , 'WW (had)', kMagenta+2 ]
		#bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZZTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1, 'ZZ (had)', kOrange+2 ]
		#bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WZ_'+args.RANGE+'_'+args.version+'.root'), 1, 'WZ', kCyan ]
		bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_TTJets_'+args.RANGE+'_'+args.version+'.root'),	1.5, 't #bar{t} + Jets', kGreen ]
		bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCD'+args.qcd+'All_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]
		#bkgFiles[ 'QCDPtAll' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCDPtAll_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]

			

	dijetlabX = 0.85
	dijetlabY = 0.55
	subjet112vs212labX = 0.7
	subjet112vs212labY = 0.88
	polAnglabX = 0.2
	polAnglabY = 0.88
	taulabX = 0.90
	taulabY = 0.85
	cosPhilabX = 0.15
	cosPhilabY = 0.45

	massMinX = 0
	massMaxX = 400
	polAngXmin = 0.7
	polAngXmax = 1.0
	HTMinX = 300
	HTMaxX = 1300
	ptMinX = 100
	ptMaxX = 800


	plotList = [ 
		[ '2D', 'Boosted', 'jetTrimmedMassHT', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'Boosted', 'leadMassHT', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],

		[ '2D', 'Boosted', 'leadMassHT_cutTrigger', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'Boosted', 'jet1Tau21VsRhoDDT', 'Leading jet #tau_{21}', 'Leading jet #rho\'', 0, 1, 1, -6, 10, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'Boosted', 'jet2Tau21VsRhoDDT', '2nd Leading jet #tau_{21}', '2nd Leading jet #rho\'', 0, 1, 1, -6, 10, 1, jetMassHTlabX, jetMassHTlabY],

		[ '1D', 'Boosted', 'jet1Pt', 100, 1500, 1, '', '', False],
		[ '1D', 'Boosted', 'jet1Eta', -3, 3, 1, '', '', False],
		[ '1D', 'Boosted', 'jet1Mass', 0, massMaxX, 10, '', '', True, False],
		[ '1DDATA', 'Boosted', 'jet1PrunedMass', '', '', 10, '', '', True, False],
		[ '1D', 'Boosted', 'jet1TrimmedMass', '', '', 10, '', '', True, False],
		[ '1D', 'Boosted', 'HT', 700, 2000, 5, '', '', False],
		[ '1D', 'Boosted', 'jet2Pt', 100, 1500, 1, '', '', False],
		[ '1D', 'Boosted', 'jet2Eta', -3, 3, 1, '', '', False],
		[ '1D', 'Boosted', 'jet2Mass', 0, massMaxX, 1, '', '', False],
		[ '1D', 'Boosted', 'massAve', 0, massMaxX, 1, '', '', False, False],

		[ '1D', 'Resolved', 'HT', 700, 5000, 2, '', '', True],
		[ '1D', 'Resolved', 'jet1Pt', 100, 1500, 2, '', '', True],
		[ '1D', 'Resolved', 'jet2Pt', 0, 1500, 2, '', '', True],
		[ '1D', 'Resolved', 'jet3Pt', 0, 500, 2, '', '', True],
		[ '1D', 'Resolved', 'jet4Pt', 0, 300, 2, '', '', True],
		[ '1D', 'Resolved', 'massAve', 0, 1000, 2, '', '', True],

		[ 'qual', 'Boosted', 'deltaEtaDijet', '', '', 1,  0.90, 0.70, True, False],	### n- 1
		[ 'qual', 'Boosted', 'prunedMassAsym', '', '', 1, (0.90 if 'n-1' in args.cut else 0.40), (0.70 if 'n-1' in args.cut else 0.4), False, ( False if 'n-1' in args.cut else True )],	
#		[ 'qual', 'Boosted', 'jet1Tau21', '', '', 1, 0.9, 0.70, False, False],	### n- 1
#		[ 'qual', 'Boosted', 'jet2Tau21', '', '', 1, 0.9, 0.70, False, False],	### n- 1
#		[ 'qual', 'Boosted', 'jet1Tau31', '', '', 1, 0.9, 0.70, False, False],	### n- 1
#		[ 'qual', 'Boosted', 'jet2Tau31', '', '', 1, 0.9, 0.70, False, False],	### n- 1
#		[ 'qual', 'Boosted', 'jet1Tau32', '', '', 1, 0.9, 0.70, False, False],	### n- 1
		[ 'qual', 'Boosted', 'jet1Tau21', '', '', 1, 0.9, 0.70, False, True],
		[ 'qual', 'Boosted', 'jet2Tau21', '', '', 1, 0.9, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet1Tau31', '', '', 1, 0.4, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet2Tau31', '', '', 1, 0.4, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet1Tau32', '', '', 1, 0.4, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet2Tau32', '', '', 1, 0.4, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet1CosThetaStar', '', '', 1, 0.90, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet2CosThetaStar', '', '', 1, 0.90, 0.70, False, True],
		#[ 'qual', 'Boosted', 'jet1SubjetPtRatio', '', '', 1, 0.90, 0.70, True, True],
		#[ 'qual', 'Boosted', 'jet2SubjetPtRatio', '', '', 1, 0.90, 0.70, True, True],
		[ 'qual', 'Boosted', 'jet1Pt', 100, 1500, 20, 0.90, 0.70, False, False],
		#[ 'qual', 'Boosted', 'jet1Eta', -3, 3, 1, 0.90, 0.70, False, False],
		[ 'qual', 'Boosted', 'jet2Pt', 100, 1500, 20, 0.90, 0.70, False, False],
		#[ 'qual', 'Boosted', 'jet2Eta', -3, 3, 1, 0.90, 0.70, False, False],
		[ 'qual', 'Boosted', 'numJets', 0, 10, 1, 0.90, 0.70, True, False],
		[ 'qual', 'Boosted', 'massAve', 0, 400, 10, 0.90, 0.70, True, False],
		[ 'qual', 'Boosted', 'HT', 700, 2000, 20, 0.90, 0.70, True, False],
		[ 'qual', 'Boosted', 'MET', 0, 100, 10, 0.90, 0.70, False, False],
		[ 'qual', 'Resolved', 'jet1Pt', 100, 1500, 1, 0.90, 0.70, True, False],
		[ 'qual', 'Resolved', 'jet2Pt', 0, 1500, 1, 0.90, 0.70, True, False],
		[ 'qual', 'Resolved', 'jet3Pt', 0, 500, 1, 0.90, 0.70, True, False],
		[ 'qual', 'Resolved', 'jet4Pt', 0, 300, 1, 0.90, 0.70, True, False],
		[ 'qual', 'Resolved', 'HT', 700, 2000, 1, 0.90, 0.70, True, False],
		[ 'qual', 'Resolved', 'jetNum', '', '', 1, 0.90, 0.70, True, False],
		[ 'qual', 'Resolved', 'massAve', 0, 1000, 2, '', '', True, False],
		#[ 'jetIDQual', args.boosted, 'HT', 700, 2000, 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', args.boosted, 'NPV', 0, 30, 1, 0.90, 0.70, False, True],
		[ 'jetIDQual', args.boosted, 'jetNum', '', '', 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1NeutralHadronEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1NeutralEmEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1ChargedHadronEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1ChargedEmEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1ChargedMultiplicity', 0, 0.5, 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1NumConst', '', '', 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', args.boosted, 'jet1Pt', 400, 1500, 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', args.boosted, 'jet1Eta', -3, 3, 5, 0.90, 0.70, False, True],
		[ 'jetIDQual', 'Boosted', 'jet1Mass', 0, 1000, 10, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet1PrunedMass', 0, 1000, 10, 0.90, 0.70, True, False],
		#[ 'jetIDQual', 'Boosted', 'jet1TrimmedMass', 0, 1000, 10, 0.90, 0.70, True, False],
		#[ 'jetIDQual', 'Boosted', 'jet1FilteredMass', 0, 1000, 10, 0.90, 0.70, True, False],
		#[ 'jetIDQual', 'Boosted', 'jet1SoftDropMass', 0, 1000, 10, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2NeutralHadronEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2NeutralEmEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2ChargedHadronEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2ChargedEmEnergy', '', '', 5, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2ChargedMultiplicity', 0, 0.5, 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2NumConst', '', '', 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', args.boosted, 'jet2Pt', 400, 1500, 1, 0.90, 0.70, True, False],
		[ 'jetIDQual', args.boosted, 'jet2Eta', -3, 3, 5, 0.90, 0.70, False, True],
		[ 'jetIDQual', 'Boosted', 'jet2Mass', 0, 1000, 10, 0.90, 0.70, True, False],
		[ 'jetIDQual', 'Boosted', 'jet2PrunedMass', 0, 1000, 10, 0.90, 0.70, True, False],
		#[ 'jetIDQual', 'Boosted', 'jet2TrimmedMass', 0, 1000, 10, 0.90, 0.70, True, False],
		#[ 'jetIDQual', 'Boosted', 'jet2FilteredMass', 0, 1000, 10, 0.90, 0.70, True, False],
		#[ 'jetIDQual', 'Boosted', 'jet2SoftDropMass', 0, 1000, 10, 0.90, 0.70, True, False],
		[ 'jetIDQual', args.boosted, 'MET', '', '', 1, 0.90, 0.70, False, True],
		#[ 'jetIDQual', args.boosted, 'METHT', '', '', 1, 0.90, 0.70, True, False],
		#[ 'jetIDQual', args.boosted, 'NPV_NOPUWeight', '', '', 1, 0.90, 0.70, False, False],
		#[ 'jetIDQual', args.boosted, 'neutralHadronEnergy', '', '', 5, 0.90, 0.70, True, False],
		#[ 'jetIDQual', args.boosted, 'neutralEmEnergy', '', '', 5, 0.90, 0.70, True, False],
		#[ 'jetIDQual', args.boosted, 'chargedHadronEnergy', '', '', 5, 0.90, 0.70, True, False],
		#[ 'jetIDQual', args.boosted, 'chargedEmEnergy', '', '', 5, 0.90, 0.70, True, False],
		#[ 'jetIDQual', args.boosted, 'chargedMultiplicity', 0, 0.5, 1, 0.90, 0.70, True, False],
		#[ 'jetIDQual', args.boosted, 'numConst', '', '', 1, 0.90, 0.70, True, False],

		#[ 'Norm', 'Boosted', 'NPV', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet1Pt', '', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet2Pt', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet1Pt', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet2Pt', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet1Mass', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet2Mass', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet1Mass', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet2Mass', '', '', '', True, False],
		#[ 'Norm', 'Boosted', 'jet1Tau1', '', '', 1, taulabX, taulabY, False, False],
		#[ 'Norm', 'Boosted', 'jet1Tau2', '', '', 1, taulabX, taulabY, False, False],
		#[ 'Norm', 'Boosted', 'jet1Tau3', '', '', 1, taulabX, taulabY, False, False],
		#[ 'Norm', 'Boosted', 'jet1RhoDDT', -6, 10, 5, taulabX, taulabY, False, False],
		#[ 'Norm', 'Boosted', 'jet2RhoDDT', -6, 10, 5, taulabX, taulabY, False, False],
		#[ 'Norm', 'Boosted', 'jet1Tau21DDT', 0, 1.3, 1, taulabX, taulabY, False, False],
		#[ 'Norm', 'Boosted', 'jet2Tau21DDT', 0, 1.3, 1, taulabX, taulabY, False, False],
		[ 'Norm', 'Boosted', 'jet1Tau21', '', '', 1, 0.3, 0.55, False, True ], # (True if 'n-1' in args.cut else False)],
		[ 'Norm', 'Boosted', 'jet2Tau21', '', '', 1, 0.3, 0.55, False, True ],
		[ 'Norm', 'Boosted', 'jet2Tau31', '', '', 1, taulabX, taulabY, False, True ], #(True if 'n-1' in args.cut else False)],
		[ 'Norm', 'Boosted', 'jet1Tau31', '', '', 1, taulabX, taulabY, False, True ], #(True if 'n-1' in args.cut else False)],
		[ 'Norm', 'Boosted', 'prunedMassAsym', '', '', 1, 0.40, 0.80, False, False],
		[ 'Norm', 'Boosted', 'deltaEtaDijet', '', '', 2, '', '', False, False],
		[ 'Norm', 'Boosted', 'jet1Tau32', '', '', 1, taulabX, taulabY, False, True],
		[ 'Norm', 'Boosted', 'jet2Tau32', '', '', 1, taulabX, taulabY, False, True],
		[ 'Norm', 'Boosted', 'jet1SubjetPtRatio', '', '', 1, '', '', True, False],
		[ 'Norm', 'Boosted', 'jet2SubjetPtRatio', '', '', 1, '', '', True, False],
		[ 'Norm', 'Boosted', 'subjetPtRatio', '', '', 1, '', '', True, False],
		[ 'Norm', 'Boosted', 'jet1CosThetaStar', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet21MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet112MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet1JetMassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet212MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet1Subjet2JetMassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet112MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet1JetMassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet212MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'jet2Subjet2JetMassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'subjetPtRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'subjetMass21Ratio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'subjet112MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'subjet212MassRatio', '', '', 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'subjetPolAngle13412', polAngXmin, polAngXmax, 1, '', '', False, False],
		#[ 'Norm', 'Boosted', 'subjetPolAngle31234', polAngXmin, polAngXmax, 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'massRes', '', '', 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'deltaEta', '', '', 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'minDeltaR', '', '', 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'deltaR', '', '', 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'jet4Pt', 0, 300, 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'cosThetaStar1', '', '', 1, '', '', False, False],
		[ 'Norm', 'Resolved', 'cosThetaStar2', '', '', 1, '', '', False, False],


		[ 'simple', 'HT',  1000, '', '', False],
		[ 'simple', 'HT',  1000, '', '', True],
		[ 'simple', 'massAve_cutDijet',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutAsym',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutCosTheta',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutSubjetPtRatio',  massMaxX, '', '', False],
		#[ 'simple', 'massAve_cutSubjetPtRatio',  massMaxX, '', '', True ],
		[ 'simple', 'massAve_cutTau31',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutTau21',  massMaxX, '', '', False],
		
		#[ 'mini', args.boosted, 'massAve', 60, 350, 5, '', '', True, False],
		[ 'miniDATA', 'Boosted', 'massAve', 60, 350, 5, 0.92, 0.85, True, False],
		#[ 'miniDATA', 'Boosted', 'massAve', 0, 500, 10, '', '', True, False],
		[ 'mini', 'Boosted', 'deltaEtaDijet', '', '', 1,  '', '', True, False],	### n- 1
		[ 'mini', 'Boosted', 'prunedMassAsym', '', '', 1, '', '', False, False],	### n- 1
		[ 'mini', 'Boosted', 'jet1Tau21', '', '', 1, '', '', False, False],	### n- 1
		[ 'mini', 'Boosted', 'jet2Tau21', '', '', 1, '', '', False, False],	### n- 1
		[ 'mini', 'Boosted', 'jet1Tau31', '', '', 1, '', '', False, False],	### n- 1
		[ 'mini', 'Boosted', 'jet2Tau31', '', '', 1, '', '', False, False],	### n- 1
		[ 'mini', 'Boosted', 'jet1Tau32', '', '', 1, '', '', False, False],	### n- 1
		[ '2Dmini', 'Boosted', 'massAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet1Tau21', 'Mass Asymmetry', 'Leading jet #tau_{21} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet2Tau21', 'Mass Asymmetry', '2nd Leading jet #tau_{21} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet1Tau31', 'Mass Asymmetry', 'Leading jet #tau_{31} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet2Tau31', 'Mass Asymmetry', '2nd Leading jet #tau_{31} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet1Tau21', '| #eta_{j1} - #eta_{j2} |', 'Leading jet #tau_{21} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet2Tau21', '| #eta_{j1} - #eta_{j2} |', '2nd Leading jet #tau_{21} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet1Tau31', '| #eta_{j1} - #eta_{j2} |', 'Leading jet #tau_{31} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet2Tau31', '| #eta_{j1} - #eta_{j2} |', '2nd Leading jet #tau_{31} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'jet1Tau21VsRhoDDT', 'Leading jet #tau_{21}', 'Leading jet #rho\'', 0, 1, 1, -6, 10, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'jet2Tau21VsRhoDDT', '2nd Leading jet #tau_{21}', '2nd Leading jet #rho\'', 0, 1, 1, -6, 10, 1, jetMassHTlabX, jetMassHTlabY],

		]

	if 'all' in args.single: Plots = [ x[2:] for x in plotList if ( ( args.process in x[0] ) and ( x[1] in args.boosted ) )  ]
	else: Plots = [ y[2:] for y in plotList if ( ( args.process in y[0] ) and ( y[1] in args.boosted ) and ( y[2] in args.single ) )  ]

	if 'Resolved' in args.boosted: args.grooming =  '' 
	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]

	if 'all' in args.cut: 
		if 'Boosted' in args.boosted: listCuts = [ '_jet1Tau21', '_jet2Tau21', '_prunedMassAsym', '_deltaEtaDijet', '_jet1Tau31', '_jet2Tau31' ]
		else: listCuts = [ 'cutMassRes', '_cutDelta', '_cutEtaBand', '_cutDeltaR', '_cutCosTheta', '_cutDEta', '_cutMassPairing' ]
	#elif 'NO' in args.cut: listCuts = [ '_cutNOMassAsym', '_cutTau21_NOMA', '_cutCosTheta_NOMA', '_cutDEta_NOMA' ]
	else: listCuts = [ args.cut ]

	if 'CF' in args.process:
		plotCutFlow( signalFiles, bkgFiles, args.grooming, 'cutflow_scaled', 8, True, True )
	if 'Scf' in args.process:
		plotSignalCutFlow('Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p0_'+args.version+'.root', 'Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_UDD312_M-100_'+args.RANGE+'_'+args.version+'.root', (10 if 'high' in args.RANGE else 12), True, True )
	if 'signal' in args.process:
		plotSignalShape('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_UDD312_M-100_'+args.RANGE+'_'+args.version+'.root', 'massAve'+args.cut, 5, False)
		#plotSignalShape('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_UDD312_M-100_'+args.RANGE+'_'+args.version+'.root', 'jet2Tau21'+args.cut, 1, False)
		#plotSignalShape('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_UDD312_M-100_'+args.RANGE+'_'+args.version+'.root', 'jet2Pt'+args.cut, 20, False)
	if 'acc' in args.process:
		plotSignalAcceptance('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_UDD312_M-100_'+args.RANGE+'_'+args.version+'.root', 'massAve'+args.cut, False)
	if 'tmp' in args.process:
		tmpplotDiffSample('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_UDD312_M-100_'+args.RANGE+'_'+args.version+'.root', 'Rootfiles/RUNResolutionCalc_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p1_v01p1.root', 'pruned', 'prunedMassAsym', '', '', '', False, 'BoostedOnly', True )

	for i in Plots:
		for optGroom in Groommers:
			if args.process in '2D': 
				#plot2D( signalFiles, 'RPVSt'+str(args.mass), optGroom, args.boosted+'AnalysisPlots'+Groom+'/'+[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( bkgFiles, 'QCD', optGroom, args.boosted+'AnalysisPlots'+Groom+'/'+[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( inputFileTTJets, 'TTJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( inputFileWJetsToQQ, 'WJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( inputFileZJetsToQQ, 'ZJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				for bkg in signalFiles: plot2D( signalFiles[ bkg ][0], 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), optGroom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				for bkg in bkgFiles: plot2D( bkgFiles[ bkg ][0], bkg, optGroom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( inputFileTTJets, 'TTJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( inputFileWJetsToQQ, 'WJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )
				#plot2D( inputFileZJetsToQQ, 'ZJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10] )

			elif '1D' in args.process:
				for cut1 in listCuts:
					plotSignalBkg( signalFiles, bkgFiles, dataFile, optGroom, args.boosted+'AnalysisPlots/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
			
			elif ( 'jetIDQual' in args.process ):
				for cut1 in listCuts:
					if 'Boosted' in args.boosted: plotQuality( dataFile, bkgFiles, optGroom, args.boosted+'AnalysisPlots/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					else: plotQuality( dataFile, bkgFiles, '', args.boosted+'AnalysisPlots/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
			elif ( 'qual' in args.process ):
				for cut1 in listCuts:
					if 'Boosted' in args.boosted: plotQuality( dataFile, bkgFiles, optGroom, i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					else: plotQuality( dataFile, bkgFiles, '', i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
			
			elif 'mini' in args.process:
				for cut1 in listCuts:
					if '2D' in args.process: plot2DSignalBkg( signalFiles, optGroom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9] )
					else: plotSignalBkg( signalFiles, bkgFiles, dataFile, optGroom, i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
			
			elif 'Norm' in args.process:
				for cut1 in listCuts:
					#plotSignalBkg( signalFiles, bkgFiles, optGroom, args.boosted+'AnalysisPlots'+optGroom+'/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], True )
					plotSignalBkg( signalFiles, bkgFiles, dataFile, optGroom, i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], i[7], True )


			elif 'simple' in args.process:
				plotSimple( inputFileTTJets, 'TTJets', optGroom, i[0], i[1], i[2], i[3], i[4] )
				plotSimple( inputFileWJetsToQQ, 'WJets', optGroom, i[0], i[1], i[2], i[3], i[4] )
				plotSimple( inputFileZJetsToQQ, 'ZJets', optGroom, i[0], i[1], i[2], i[3], i[4] )
