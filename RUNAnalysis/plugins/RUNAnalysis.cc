// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNAnalysis
// 
/**\class RUNAnalysis RUNAnalysis.cc Ntuples/Ntuples/plugins/RUNAnalysis.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Tue, 14 Oct 2014 23:13:13 GMT
//
//


// system include files
#include <memory>
#include <vector>
#include <TLorentzVector.h>
#include <TH2.h>
#include <TTree.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"
#include "RUNA/RUNAnalysis/interface/PUReweighter.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNAnalysis : public EDAnalyzer {
   public:
      explicit RUNAnalysis(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNAnalysis();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;
      virtual void clearVariables();
      virtual void beginRun(const Run&, const EventSetup&) override;

      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      PUReweighter PUWeight_;
      int lhaPdfId;

      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      bool bjSample;
      bool isData;
      string dataPUFile;
      string jecVersion;
      TString systematics;
      double scale;
      double cutHT;
      double cut4JetPt;
      double cutMassAsym;
      double cutDelta;
      double cutDEta;
      double cutDeltaR;
      double cutCosThetaStar;

      vector<string> triggerPass;
      vector<JetCorrectorParameters> jetPar;
      FactorizedJetCorrector * jetJEC;
      JetCorrectionUncertainty *jetCorrUnc;

      vector<float> *jetsPt = new std::vector<float>();
      vector<float> *jetsEta = new std::vector<float>();
      vector<float> *jetsPhi = new std::vector<float>();
      vector<float> *jetsE = new std::vector<float>();
      vector<float> *jetsQGL = new std::vector<float>();
      vector<float> *jetsCSVv2 = new std::vector<float>();
      vector<float> *jetsCMVAv2 = new std::vector<float>();
      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float HT = 0, mass1 = -999, mass2 = -999, avgMass = -999, MET = -999,
	    delta1 = -999, delta2 = -999, massAsym = -999, eta1 = -999, eta2 = -999, deltaEta = -999, 
	    deltaR = -999, cosThetaStar1 = -999, cosThetaStar2 = -999,
	    puWeight = -999, genWeight = -999, lumiWeight = -999, pdfWeight = -999 ;
      vector<float> scaleWeights, pdfWeights, alphaWeights;

      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetQGL_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetCSVv2_;
      EDGetTokenT<vector<float>> jetCMVAv2_;
      EDGetTokenT<vector<float>> jetArea_;
      EDGetTokenT<vector<float>> jetGenPt_;
      EDGetTokenT<vector<float>> jetGenEta_;
      EDGetTokenT<vector<float>> jetGenPhi_;
      EDGetTokenT<vector<float>> jetGenE_;
      EDGetTokenT<int> NPV_;
      EDGetTokenT<vector<float>> metPt_;
      EDGetTokenT<int> trueNInt_;
      EDGetTokenT<vector<int>> bunchCross_;
      EDGetTokenT<vector<float>> rho_;
      EDGetTokenT<vector<int>> puNumInt_;
      EDGetTokenT<unsigned int> lumi_;
      EDGetTokenT<unsigned int> run_;
      EDGetTokenT<ULong64_t> event_;
      EDGetTokenT<GenEventInfoProduct> generator_;
      EDGetTokenT<LHEEventProduct> extLHEProducer_;

      // Trigger
      EDGetTokenT<vector<float>> triggerBit_;
      EDGetTokenT<vector<string>> triggerName_;
      
      //Jet ID
      EDGetTokenT<vector<float>> jecFactor_;
      EDGetTokenT<vector<float>> neutralHadronEnergy_;
      EDGetTokenT<vector<float>> neutralEmEnergy_;
      EDGetTokenT<vector<float>> chargedHadronEnergy_;
      EDGetTokenT<vector<float>> chargedEmEnergy_;
      EDGetTokenT<vector<float>> chargedHadronMultiplicity_;
      EDGetTokenT<vector<float>> neutralHadronMultiplicity_;
      EDGetTokenT<vector<float>> chargedMultiplicity_;
      EDGetTokenT<vector<float>> muonEnergy_; 


};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNAnalysis::RUNAnalysis(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
	jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
	jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
	jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
	jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
	jetQGL_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetQGL"))),
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetCSVv2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVv2"))),
	jetCMVAv2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCMVAv2"))),
	jetArea_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetArea"))),
	jetGenPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenPt"))),
	jetGenEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenEta"))),
	jetGenPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenPhi"))),
	jetGenE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetGenE"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
	metPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("metPt"))),
	trueNInt_(consumes<int>(iConfig.getParameter<InputTag>("trueNInt"))),
	bunchCross_(consumes<vector<int>>(iConfig.getParameter<InputTag>("bunchCross"))),
	rho_(consumes<vector<float>>(iConfig.getParameter<InputTag>("rho"))),
	puNumInt_(consumes<vector<int>>(iConfig.getParameter<InputTag>("puNumInt"))),
	lumi_(consumes<unsigned int>(iConfig.getParameter<InputTag>("Lumi"))),
	run_(consumes<unsigned int>(iConfig.getParameter<InputTag>("Run"))),
	event_(consumes<ULong64_t>(iConfig.getParameter<InputTag>("Event"))),
	generator_(consumes<GenEventInfoProduct>(iConfig.getParameter<InputTag>("generator"))),
	extLHEProducer_(consumes<LHEEventProduct>(iConfig.getParameter<InputTag>("extLHEProducer"))),
	// Trigger
	triggerBit_(consumes<vector<float>>(iConfig.getParameter<InputTag>("triggerBit"))),
	triggerName_(consumes<vector<string>>(iConfig.getParameter<InputTag>("triggerName"))),
	//Jet ID,
	jecFactor_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jecFactor"))),
	neutralHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronEnergy"))),
	neutralEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralEmEnergy"))),
	chargedHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedHadronEnergy"))),
	chargedEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedEmEnergy"))),
	chargedHadronMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedHadronMultiplicity"))),
	neutralHadronMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronMultiplicity"))),
	chargedMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedMultiplicity"))),
	muonEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonEnergy")))
{
	consumes<LHERunInfoProduct,edm::InRun> (edm::InputTag("externalLHEProducer"));
	scale 		= iConfig.getParameter<double>("scale");
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	cutHT 		= iConfig.getParameter<double>("cutHT");
	cut4JetPt 	= iConfig.getParameter<double>("cut4JetPt");
	cutMassAsym     = iConfig.getParameter<double>("cutMassAsym");
	cutDelta        = iConfig.getParameter<double>("cutDelta");
	cutDEta      	= iConfig.getParameter<double>("cutDEta");
	cutDeltaR 	= iConfig.getParameter<double>("cutDeltaR");
	cutCosThetaStar = iConfig.getParameter<double>("cutCosThetaStar");
	triggerPass 	= iConfig.getParameter<vector<string>>("triggerPass");
	isData 		= iConfig.getParameter<bool>("isData");
	dataPUFile 	= iConfig.getParameter<string>("dataPUFile");
	jecVersion 	= iConfig.getParameter<string>("jecVersion");
	systematics 	= iConfig.getParameter<string>("systematics");

	/////// JECs
	string tmpPrefix = jecVersion;
	string prefix;
	if (isData) prefix = tmpPrefix + "_DATA_";
	else prefix = tmpPrefix + "_MC_";

	// all jet
	vector<string> jecPayloadNames_;
	jecPayloadNames_.push_back(prefix + "L1FastJet_AK4PFchs.txt");
	jecPayloadNames_.push_back(prefix + "L2Relative_AK4PFchs.txt");
	jecPayloadNames_.push_back(prefix + "L3Absolute_AK4PFchs.txt");
	if (isData) jecPayloadNames_.push_back(prefix + "L2L3Residual_AK4PFchs.txt");

	for ( vector<string>::const_iterator payloadBegin = jecPayloadNames_.begin(), payloadEnd = jecPayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
		JetCorrectorParameters pars(*ipayload);
		jetPar.push_back(pars);
	}
	jetJEC = new FactorizedJetCorrector(jetPar);

	// jec uncertainty
	JetCorrectorParameters jecUncParam( prefix + "Uncertainty_AK4PFchs.txt");
	jetCorrUnc  = new JetCorrectionUncertainty( jecUncParam);
}


RUNAnalysis::~RUNAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNAnalysis::analyze(const Event& iEvent, const EventSetup& iSetup) {


	/*vector<Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

	Handle<vector<float> > jetPt;
	iEvent.getByToken(jetPt_, jetPt);

	Handle<vector<float> > jetEta;
	iEvent.getByToken(jetEta_, jetEta);

	Handle<vector<float> > jetPhi;
	iEvent.getByToken(jetPhi_, jetPhi);

	Handle<vector<float> > jetE;
	iEvent.getByToken(jetE_, jetE);

	Handle<vector<float> > jetQGL;
	iEvent.getByToken(jetQGL_, jetQGL);

	Handle<vector<float> > jetMass;
	iEvent.getByToken(jetMass_, jetMass);

	Handle<vector<float> > jetCSVv2;
	iEvent.getByToken(jetCSVv2_, jetCSVv2);

	Handle<vector<float> > jetCMVAv2;
	iEvent.getByToken(jetCMVAv2_, jetCMVAv2);

	Handle<vector<float> > jetArea;
	iEvent.getByToken(jetArea_, jetArea);

	Handle<vector<float> > jetGenPt;
	iEvent.getByToken(jetGenPt_, jetGenPt);

	Handle<vector<float> > jetGenEta;
	iEvent.getByToken(jetGenEta_, jetGenEta);

	Handle<vector<float> > jetGenPhi;
	iEvent.getByToken(jetGenPhi_, jetGenPhi);

	Handle<vector<float> > jetGenE;
	iEvent.getByToken(jetGenE_, jetGenE);

	Handle<int> NPV;
	iEvent.getByToken(NPV_, NPV);

	Handle<int> trueNInt;
	iEvent.getByToken(trueNInt_, trueNInt);

	Handle<vector<int>> bunchCross;
	iEvent.getByToken(bunchCross_, bunchCross);

	Handle<vector<float>> rho;
	iEvent.getByToken(rho_, rho);

	Handle<vector<int>> puNumInt;
	iEvent.getByToken(puNumInt_, puNumInt);

	Handle<unsigned int> Lumi;
	iEvent.getByToken(lumi_, Lumi);

	Handle<unsigned int> Run;
	iEvent.getByToken(run_, Run);

	Handle<ULong64_t> ievent;
	iEvent.getByToken(event_, ievent);

	Handle<vector<float> > metPt;
	iEvent.getByToken(metPt_, metPt);

	/// Trigger
	Handle<vector<float> > triggerBit;
	iEvent.getByToken(triggerBit_, triggerBit);

	Handle<vector<string> > triggerName;
	iEvent.getByToken(triggerName_, triggerName);

	/// Jet ID
	Handle<vector<float> > jecFactor;
	iEvent.getByToken(jecFactor_, jecFactor);

	Handle<vector<float> > neutralHadronEnergy;
	iEvent.getByToken(neutralHadronEnergy_, neutralHadronEnergy);

	Handle<vector<float> > neutralEmEnergy;
	iEvent.getByToken(neutralEmEnergy_, neutralEmEnergy);

	Handle<vector<float> > chargedHadronEnergy;
	iEvent.getByToken(chargedHadronEnergy_, chargedHadronEnergy);

	Handle<vector<float> > chargedEmEnergy;
	iEvent.getByToken(chargedEmEnergy_, chargedEmEnergy);

	Handle<vector<float> > chargedHadronMultiplicity;
	iEvent.getByToken(chargedHadronMultiplicity_, chargedHadronMultiplicity);

	Handle<vector<float> > neutralHadronMultiplicity;
	iEvent.getByToken(neutralHadronMultiplicity_, neutralHadronMultiplicity);

	Handle<vector<float> > chargedMultiplicity;
	iEvent.getByToken(chargedMultiplicity_, chargedMultiplicity);

	Handle<vector<float> > muonEnergy;
	iEvent.getByToken(muonEnergy_, muonEnergy);

	if ( !isData ) {

		// all this section is based on https://github.com/jkarancs/B2GTTrees/blob/master/plugins/B2GEdmExtraVarProducer.cc#L215-L281
		/////////// GEN weight
		Handle<GenEventInfoProduct> genEvtInfo; 
		iEvent.getByToken( generator_, genEvtInfo );
		genWeight = genEvtInfo->weight();	
		//vector<double> evtWeights = genEvtInfo->weights();

		/////////// LHE weight
		Handle<LHEEventProduct> lheEvtInfo;
		iEvent.getByToken( extLHEProducer_, lheEvtInfo );
		// This function will return all the weights from the lheEvtInfo (scaleWeights, pdfWeights, alphaWeights)
		getWeights( lheEvtInfo, lhaPdfId, scaleWeights, pdfWeights, alphaWeights );

		//// Calculating the RMS from the pdfWeights, per event
		double sum = accumulate(pdfWeights.begin(), pdfWeights.end(), 0.0);
		double mean = sum / pdfWeights.size();
		vector<double> diff(pdfWeights.size());
		transform(pdfWeights.begin(), pdfWeights.end(), diff.begin(), [mean](double x) { return x - mean; });
		double sq_sum = inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);
		pdfWeight = sqrt(sq_sum / pdfWeights.size());
		////////////////////////////////////////////////////
	}

	bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );
	// PU Reweight
	if ( isData ) puWeight = 1;
	else puWeight = PUWeight_.getPUWeight( *trueNInt, *bunchCross );
	//puWeight = 1;
	histos1D_[ "PUWeight" ]->Fill( puWeight );
	lumiWeight = scale;
	double totalWeight = puWeight * lumiWeight;
	
	cutmap["Processed"] += totalWeight;

	int numPV = *NPV;
	vector< myJet > JETS;
	vector< float > tmpTriggerMass;
	int numberJets = 0;
	double rawHT = 0;
	//bool bTagCSVv2 = 0;
	HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		rawHT += (*jetPt)[i];
		histos1D_[ "rawJetPt" ]->Fill( (*jetPt)[i] , totalWeight );

		bool idL = jetID( (*jetEta)[i], (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*muonEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		TLorentzVector tmpJet, rawJet, corrJet, genJet, smearJet;
		tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );
		rawJet = tmpJet* (*jecFactor)[i] ;

		double JEC = corrections( rawJet, (*jetArea)[i], (*rho)[i] ,*NPV, jetJEC); 
		double sysJEC = 0;
		double sysJER = 1;
		if ( !isData ) {
			if ( systematics.Contains("JESUp") ){
				double JESUp = uncertainty( rawJet, jetCorrUnc, true );
				sysJEC = ( + JESUp );
			} else if  ( systematics.Contains("JESDown") ){
				double JESDown = uncertainty( rawJet, jetCorrUnc, false );
				sysJEC = ( - JESDown );
			}

			// Based on this: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCMSDataAnalysisSchool2015KoreaJetExercise#Resolution
			if ( systematics.Contains("JERUp") ){
				double JERUp = getJER( (*jetEta)[i], 1 );
				double corrJetPt = (*jetPt)[i] * JEC;
				double deltaPtUp = ( corrJetPt - (*jetGenPt)[i] ) * (JERUp-1.0);
				sysJER = max( 0.0, ( corrJetPt + deltaPtUp ) / corrJetPt );
			} else if  ( systematics.Contains("JERDown") ){
				double JERDown = getJER( (*jetEta)[i], -1 );
				double corrJetPt = (*jetPt)[i] * JEC;
				double deltaPtDown = ( corrJetPt - (*jetGenPt)[i] ) * (JERDown-1.0);
				sysJER = max( 0.0, ( corrJetPt + deltaPtDown ) / corrJetPt );
			}
		} 
		corrJet = rawJet* ( ( JEC * sysJER ) + sysJEC  );

		if( corrJet.Pt() > 80 && idL ) { 

			HT += corrJet.Pt();
			++numberJets;
			//if ( (*jetCSVv2)[i] > 0.244 ) bTagCSVv2 = 1; 	// CSVv2L
			//if ( (*jetCSVv2)[i] > 0.679 ) bTagCSVv2 = 1; 	// CSVv2M
			//if ( (*jetCSVv2V1)[i] > 0.405 ) bTagCSVv2 = 1; 	// CSVv2V1L
			//if ( (*jetCSVv2V1)[i] > 0.783 ) bTagCSVv2 = 1; 	// CSVv2V1M
			double jec = 1. / ( rawJet.E() ); //(*jecFactor)[i] * (*jetE)[i] );
			histos1D_[ "jetPt" ]->Fill( corrJet.Pt() , totalWeight );
			histos1D_[ "jetEta" ]->Fill( corrJet.Eta() , totalWeight );
			histos1D_[ "neutralHadronEnergy" ]->Fill( (*neutralHadronEnergy)[i] * jec, totalWeight );
			histos1D_[ "neutralEmEnergy" ]->Fill( (*neutralEmEnergy)[i] * jec, totalWeight );
			histos1D_[ "chargedHadronEnergy" ]->Fill( (*chargedHadronEnergy)[i] * jec, totalWeight );
			histos1D_[ "chargedEmEnergy" ]->Fill( (*chargedEmEnergy)[i] * jec, totalWeight );
			histos1D_[ "numConst" ]->Fill( (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i], totalWeight );
			histos1D_[ "chargedMultiplicity" ]->Fill( (*chargedMultiplicity)[i] * jec, totalWeight );

			myJet tmpJET;
			tmpJET.p4 = corrJet;
			tmpJET.btagCSVv2 = (*jetCSVv2)[i];
			tmpJET.btagCMVAv2 = (*jetCMVAv2)[i];
			tmpJET.qgl = (*jetQGL)[i];
			tmpJET.nhf = (*neutralHadronEnergy)[i] * jec;
			tmpJET.nEMf = (*neutralEmEnergy)[i] * jec;
			tmpJET.chf = (*chargedHadronEnergy)[i] * jec;
			tmpJET.cEMf = (*chargedEmEnergy)[i] * jec;
			tmpJET.numConst = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i];
			tmpJET.chm = (*chargedMultiplicity)[i] * jec;
			JETS.push_back( tmpJET );
		}
	}

	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1; tmpP2 = p2;  return tmpP1.M() > tmpP2.M(); }); 
	numJets = numberJets;
	histos1D_[ "jetNum" ]->Fill( numJets, totalWeight );
	histos1D_[ "NPV" ]->Fill( numPV, totalWeight );
	histos1D_[ "NPV_NOPUWeight" ]->Fill( numPV );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT , totalWeight );
	if ( rawHT > 0 ) histos1D_[ "rawHT" ]->Fill( rawHT , totalWeight );
	MET = (*metPt)[0];

	clearVariables();

	if ( ORTriggers ) {
		
		cutmap["Trigger"] += totalWeight;
		histos1D_[ "HT_cutTrigger" ]->Fill( HT , totalWeight );
		histos1D_[ "jetNum_cutTrigger" ]->Fill( numJets, totalWeight );
		for (int i = 0; i < numJets; i++) {
			histos1D_[ "jetPt_cutTrigger" ]->Fill( JETS[i].p4.Pt(), totalWeight );
			histos1D_[ "jetEta_cutTrigger" ]->Fill( JETS[i].p4.Eta(), totalWeight );
		}
		event		= *ievent;
		run		= *Run;
		lumi		= *Lumi;

		if( numJets > 3 ) { 
			
			cutmap["4Jets"] += totalWeight;
			histos1D_[ "HT_cut4Jets" ]->Fill( HT, totalWeight );
			histos1D_[ "jetNum_cut4Jets" ]->Fill( numJets, totalWeight );
			histos1D_[ "jet1Pt_cut4Jets" ]->Fill( JETS[0].p4.Pt(), totalWeight );
			histos1D_[ "jet2Pt_cut4Jets" ]->Fill( JETS[1].p4.Pt(), totalWeight );
			histos1D_[ "jet3Pt_cut4Jets" ]->Fill( JETS[2].p4.Pt(), totalWeight );
			histos1D_[ "jet4Pt_cut4Jets" ]->Fill( JETS[3].p4.Pt(), totalWeight );
			histos1D_[ "MET_cut4Jets" ]->Fill( MET, totalWeight );
			histos1D_[ "METHT_cut4Jets" ]->Fill( MET/HT, totalWeight );

			if( ( numJets == 4 ) && ( HT > cutHT ) && ( JETS[3].p4.Pt() > cut4JetPt ) ){
				
				vector<double> tmpDijetR;
				double dR12 = JETS[0].p4.DeltaR( JETS[1].p4 );
				double dR34 = JETS[2].p4.DeltaR( JETS[3].p4 );
				bool maxdR1234 = (dR12 > dR34);
				double deltaR1234 = abs( dR12 - 0.8 )  + abs( dR34 - 0.8 );
				tmpDijetR.push_back( deltaR1234 );

				double dR13 = JETS[0].p4.DeltaR( JETS[2].p4 );
				double dR24 = JETS[1].p4.DeltaR( JETS[3].p4 );
				bool maxdR1324 = (dR13 > dR24);
				double deltaR1324 = abs( dR13 - 0.8 )  + abs( dR24 - 0.8 );
				tmpDijetR.push_back( deltaR1324 );

				double dR14 = JETS[0].p4.DeltaR( JETS[3].p4 );
				double dR23 = JETS[1].p4.DeltaR( JETS[2].p4 );
				bool maxdR1423 = (dR14 > dR23);
				double deltaR1423 = abs( dR14 - 0.8 )  + abs( dR23 - 0.8 );
				tmpDijetR.push_back( deltaR1423 );

				//LogWarning("test") << min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin()  << " " << deltaR1234 << " " << deltaR1324 << " " << deltaR1423 ;
				int minDeltaR = min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin();
				TLorentzVector j1, j2, j3, j4;
				double qgl1 = -9999, qgl2 = -9999, qgl3 = -9999, qgl4 = -9999;

				if( minDeltaR == 0 ){
					if ( maxdR1234 ){
						j1 = JETS[0].p4;
						j2 = JETS[1].p4;
						j3 = JETS[2].p4;
						j4 = JETS[3].p4;
						qgl1 = JETS[0].qgl;
						qgl2 = JETS[1].qgl;
						qgl3 = JETS[2].qgl;
						qgl4 = JETS[3].qgl;
					} else{
						j1 = JETS[2].p4;
						j2 = JETS[3].p4;
						j3 = JETS[0].p4;
						j4 = JETS[1].p4;
						qgl1 = JETS[2].qgl;
						qgl2 = JETS[3].qgl;
						qgl3 = JETS[0].qgl;
						qgl4 = JETS[1].qgl;
					}
				} else if ( minDeltaR == 1 ) {
					if ( maxdR1324 ){
						j1 = JETS[0].p4;
						j2 = JETS[2].p4;
						j3 = JETS[1].p4;
						j4 = JETS[3].p4;
						qgl1 = JETS[0].qgl;
						qgl2 = JETS[2].qgl;
						qgl3 = JETS[1].qgl;
						qgl4 = JETS[3].qgl;
					} else {
						j1 = JETS[1].p4;
						j2 = JETS[3].p4;
						j3 = JETS[0].p4;
						j4 = JETS[2].p4;
						qgl1 = JETS[1].qgl;
						qgl2 = JETS[3].qgl;
						qgl3 = JETS[0].qgl;
						qgl4 = JETS[2].qgl;
					}
				} else if ( minDeltaR == 2 ) {
					if ( maxdR1423 ){
						j1 = JETS[0].p4;
						j2 = JETS[3].p4;
						j3 = JETS[1].p4;
						j4 = JETS[2].p4;
						qgl1 = JETS[0].qgl;
						qgl2 = JETS[3].qgl;
						qgl3 = JETS[1].qgl;
						qgl4 = JETS[2].qgl;
					} else {
						j1 = JETS[1].p4;
						j2 = JETS[2].p4;
						j3 = JETS[0].p4;
						j4 = JETS[3].p4;
						qgl1 = JETS[1].qgl;
						qgl2 = JETS[2].qgl;
						qgl3 = JETS[0].qgl;
						qgl4 = JETS[3].qgl;
					}
				}

				jetsPt->push_back( j1.Pt() );
				jetsPt->push_back( j2.Pt() );
				jetsPt->push_back( j3.Pt() );
				jetsPt->push_back( j4.Pt() );
				jetsEta->push_back( j1.Eta() );
				jetsEta->push_back( j2.Eta() );
				jetsEta->push_back( j3.Eta() );
				jetsEta->push_back( j4.Eta() );
				jetsPhi->push_back( j1.Phi() );
				jetsPhi->push_back( j2.Phi() );
				jetsPhi->push_back( j3.Phi() );
				jetsPhi->push_back( j4.Phi() );
				jetsE->push_back( j1.E() );
				jetsE->push_back( j2.E() );
				jetsE->push_back( j3.E() );
				jetsE->push_back( j4.E() );
				jetsQGL->push_back( qgl1 );
				jetsQGL->push_back( qgl2 );
				jetsQGL->push_back( qgl3 );
				jetsQGL->push_back( qgl4 );

				mass1 = ( j1 + j2 ).M();
				mass2 = ( j3 + j4 ).M();
				avgMass = ( mass1 + mass2 ) / 2;
				delta1 = ( j1.Pt() + j2.Pt() ) - avgMass;
				delta2 = ( j3.Pt() + j4.Pt() ) - avgMass;
				massAsym = TMath::Abs( mass1 - mass2 ) / (mass1 + mass2) ;
				eta1 = ( j1 + j2 ).Eta();
				eta2 = ( j3 + j4 ).Eta();
				deltaEta = TMath::Abs( eta1 - eta2 );
				deltaR = abs( ( j1.DeltaR( j2 ) - 0.8 )  + abs( ( j3.DeltaR( j4 ) - 0.8 ) ) );
				cosThetaStar1 = cosThetaStar( j1, j2 );
				cosThetaStar2 = cosThetaStar( j3, j4 );

				RUNAtree->Fill();

				cutmap["BestPair"] += totalWeight;
				histos1D_[ "HT_cutBestPair" ]->Fill( HT, totalWeight );
				histos1D_[ "MET_cutBestPair" ]->Fill( MET, totalWeight );
				histos1D_[ "METHT_cutBestPair" ]->Fill( MET/HT, totalWeight );
				histos1D_[ "jetNum_cutBestPair" ]->Fill( numJets, totalWeight );
				histos1D_[ "jet1Pt_cutBestPair" ]->Fill( JETS[0].p4.Pt(), totalWeight );
				histos1D_[ "jet2Pt_cutBestPair" ]->Fill( JETS[1].p4.Pt(), totalWeight );
				histos1D_[ "jet3Pt_cutBestPair" ]->Fill( JETS[2].p4.Pt(), totalWeight );
				histos1D_[ "jet4Pt_cutBestPair" ]->Fill( JETS[3].p4.Pt(), totalWeight );
				histos1D_[ "jet1QGL_cutBestPair" ]->Fill( qgl1, totalWeight );
				histos1D_[ "jet2QGL_cutBestPair" ]->Fill( qgl2, totalWeight );
				histos1D_[ "jet3QGL_cutBestPair" ]->Fill( qgl3, totalWeight );
				histos1D_[ "jet4QGL_cutBestPair" ]->Fill( qgl4, totalWeight );
				histos1D_[ "NPV_cutBestPair" ]->Fill( numPV, totalWeight );
				for (int i = 0; i < numJets; i++) {
					histos1D_[ "neutralHadronEnergy_cutBestPair" ]->Fill( JETS[i].nhf, totalWeight );
					histos1D_[ "neutralEmEnergy_cutBestPair" ]->Fill( JETS[i].nEMf, totalWeight );
					histos1D_[ "chargedHadronEnergy_cutBestPair" ]->Fill( JETS[i].chf, totalWeight );
					histos1D_[ "chargedEmEnergy_cutBestPair" ]->Fill( JETS[i].cEMf, totalWeight );
					histos1D_[ "numConst_cutBestPair" ]->Fill( JETS[i].numConst, totalWeight );
					histos1D_[ "chargedMultiplicity_cutBestPair" ]->Fill( JETS[i].chm, totalWeight );
				}

				histos1D_[ "massAve_cutBestPair" ]->Fill( avgMass, totalWeight );
				histos1D_[ "massAsym_cutBestPair" ]->Fill( massAsym, totalWeight );
				histos1D_[ "deltaEta_cutBestPair" ]->Fill( deltaEta, totalWeight );
				histos1D_[ "minDeltaR_cutBestPair" ]->Fill( minDeltaR , totalWeight );
				histos1D_[ "deltaR_cutBestPair" ]->Fill( deltaR , totalWeight );
				histos1D_[ "cosThetaStar1_cutBestPair" ]->Fill( cosThetaStar1 , totalWeight );
				histos1D_[ "cosThetaStar2_cutBestPair" ]->Fill( cosThetaStar2 , totalWeight );
				histos2D_[ "deltavsMassAve_cutBestPair" ]->Fill( avgMass, delta1 , totalWeight );
				histos2D_[ "deltavsMassAve_cutBestPair" ]->Fill( avgMass, delta2 , totalWeight );
				histos2D_[ "dijetsEta_cutBestPair" ]->Fill( eta1, eta2, totalWeight );

				if ( massAsym < cutMassAsym ) { 
					cutmap["MassAsym"] += totalWeight;
					histos1D_[ "HT_cutMassAsym" ]->Fill( HT, totalWeight );
					histos1D_[ "jetNum_cutMassAsym" ]->Fill( numJets, totalWeight );
					histos1D_[ "jet1Pt_cutMassAsym" ]->Fill( JETS[0].p4.Pt(), totalWeight );
					histos1D_[ "jet2Pt_cutMassAsym" ]->Fill( JETS[1].p4.Pt(), totalWeight );
					histos1D_[ "jet3Pt_cutMassAsym" ]->Fill( JETS[2].p4.Pt(), totalWeight );
					histos1D_[ "jet4Pt_cutMassAsym" ]->Fill( JETS[3].p4.Pt(), totalWeight );
					histos1D_[ "massAve_cutMassAsym" ]->Fill( avgMass, totalWeight );
					histos1D_[ "massAsym_cutMassAsym" ]->Fill( massAsym, totalWeight );
					histos1D_[ "deltaEta_cutMassAsym" ]->Fill( deltaEta, totalWeight );
					histos1D_[ "minDeltaR_cutMassAsym" ]->Fill( minDeltaR , totalWeight );
					histos2D_[ "deltavsMassAve_cutMassAsym" ]->Fill( avgMass, delta1 , totalWeight );
					histos2D_[ "deltavsMassAve_cutMassAsym" ]->Fill( avgMass, delta2 , totalWeight );
					histos2D_[ "dijetsEta_cutMassAsym" ]->Fill( eta1, eta2, totalWeight );
				
					if ( TMath::Abs(eta1 - eta2) <  cutDEta ) {
						cutmap["DEta"] += totalWeight;
						histos1D_[ "HT_cutDEta" ]->Fill( HT, totalWeight );
						histos1D_[ "jetNum_cutDEta" ]->Fill( numJets, totalWeight );
						histos1D_[ "jet1Pt_cutDEta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
						histos1D_[ "jet2Pt_cutDEta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
						histos1D_[ "jet3Pt_cutDEta" ]->Fill( JETS[2].p4.Pt(), totalWeight );
						histos1D_[ "jet4Pt_cutDEta" ]->Fill( JETS[3].p4.Pt(), totalWeight );
						histos1D_[ "massAve_cutDEta" ]->Fill( avgMass, totalWeight );
						histos1D_[ "massAsym_cutDEta" ]->Fill( massAsym, totalWeight );
						histos1D_[ "deltaEta_cutDEta" ]->Fill( deltaEta, totalWeight );
						histos1D_[ "minDEtaR_cutDEta" ]->Fill( minDeltaR , totalWeight );
						histos2D_[ "deltavsMassAve_cutDEta" ]->Fill( avgMass, delta1 , totalWeight );
						histos2D_[ "deltavsMassAve_cutDEta" ]->Fill( avgMass, delta2 , totalWeight );
						histos2D_[ "dijetsEta_cutDEta" ]->Fill( eta1, eta2, totalWeight );
						
						if ( ( delta1 > cutDelta ) && ( delta2  > cutDelta ) ) {
							cutmap["Delta"] += totalWeight;
							histos1D_[ "HT_cutDelta" ]->Fill( HT, totalWeight );
							histos1D_[ "jetNum_cutDelta" ]->Fill( numJets, totalWeight );
							histos1D_[ "jet1Pt_cutDelta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
							histos1D_[ "jet2Pt_cutDelta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
							histos1D_[ "jet3Pt_cutDelta" ]->Fill( JETS[2].p4.Pt(), totalWeight );
							histos1D_[ "jet4Pt_cutDelta" ]->Fill( JETS[3].p4.Pt(), totalWeight );
							histos1D_[ "massAve_cutDelta" ]->Fill( avgMass, totalWeight );
							histos1D_[ "massAsym_cutDelta" ]->Fill( massAsym, totalWeight );
							histos1D_[ "deltaEta_cutDelta" ]->Fill( deltaEta, totalWeight );
							histos1D_[ "minDeltaR_cutDelta" ]->Fill( minDeltaR , totalWeight );
							histos2D_[ "deltavsMassAve_cutDelta" ]->Fill( avgMass, delta1 , totalWeight );
							histos2D_[ "deltavsMassAve_cutDelta" ]->Fill( avgMass, delta2 , totalWeight );
							histos2D_[ "dijetsEta_cutDelta" ]->Fill( eta1, eta2, totalWeight );
						}
					}
				}
			}

			if ( numJets > 4 ){
				for (unsigned int ijet = 4; ijet < JETS.size(); ijet++) {
					jetsPt->push_back( JETS[ ijet ].p4.Pt() );
					jetsEta->push_back( JETS[ ijet ].p4.Eta() );
					jetsPhi->push_back( JETS[ ijet ].p4.Phi() );
					jetsE->push_back( JETS[ ijet ].p4.E() );
					jetsQGL->push_back( JETS[ ijet ].qgl );
				}
			}
		}
	}
	JETS.clear();
}


// ------------ method called once each job just before starting event loop  ------------
void RUNAnalysis::beginJob() {

	// Calculate PUWeight
	if ( !isData ) PUWeight_.generateWeights( dataPUFile );

	RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
	RUNAtree->Branch( "run", &run, "run/I" );
	RUNAtree->Branch( "lumi", &lumi, "lumi/I" );
	RUNAtree->Branch( "event", &event, "event/I" );
	RUNAtree->Branch( "numJets", &numJets, "numJets/I" );
	RUNAtree->Branch( "numPV", &numPV, "numPV/I" );
	RUNAtree->Branch( "puWeight", &puWeight, "puWeight/F" );
	RUNAtree->Branch( "lumiWeight", &lumiWeight, "lumiWeight/F" );
	RUNAtree->Branch( "pdfWeight", &pdfWeight, "pdfWeight/F" );
	RUNAtree->Branch( "genWeight", &genWeight, "genWeight/F" );
	RUNAtree->Branch( "HT", &HT, "HT/F" );
	RUNAtree->Branch( "mass1", &mass1, "mass1/F" );
	RUNAtree->Branch( "mass2", &mass2, "mass2/F" );
	RUNAtree->Branch( "avgMass", &avgMass, "avgMass/F" );
	RUNAtree->Branch( "delta1", &delta1, "delta1/F" );
	RUNAtree->Branch( "delta2", &delta2, "delta2/F" );
	RUNAtree->Branch( "massAsym", &massAsym, "massAsym/F" );
	RUNAtree->Branch( "eta1", &eta1, "eta1/F" );
	RUNAtree->Branch( "eta2", &eta2, "eta2/F" );
	RUNAtree->Branch( "deltaEta", &deltaEta, "deltaEta/F" );
	RUNAtree->Branch( "deltaR", &deltaR, "deltaR/F" );
	RUNAtree->Branch( "cosThetaStar1", &cosThetaStar1, "cosThetaStar1/F" );
	RUNAtree->Branch( "cosThetaStar2", &cosThetaStar2, "cosThetaStar2/F" );
	RUNAtree->Branch( "jetsPt", "vector<float>", &jetsPt);
	RUNAtree->Branch( "jetsEta", "vector<float>", &jetsEta);
	RUNAtree->Branch( "jetsPhi", "vector<float>", &jetsPhi);
	RUNAtree->Branch( "jetsE", "vector<float>", &jetsE);
	RUNAtree->Branch( "jetsQGL", "vector<float>", &jetsQGL);
	//RUNAtree->Branch( "scaleWeights", &scaleWeights );
	//RUNAtree->Branch( "pdfWeights", &pdfWeights );
	//RUNAtree->Branch( "alphaWeights", &alphaWeights );

	histos1D_[ "rawJetPt" ] = fs_->make< TH1D >( "rawJetPt", "rawJetPt", 100, 0., 1000. );
	histos1D_[ "rawJetPt" ]->Sumw2();
	histos1D_[ "rawHT" ] = fs_->make< TH1D >( "rawHT", "rawHT", 300, 0., 3000. );
	histos1D_[ "rawHT" ]->Sumw2();

	histos1D_[ "jetPt" ] = fs_->make< TH1D >( "jetPt", "jetPt", 100, 0., 1000. );
	histos1D_[ "jetPt" ]->Sumw2();
	histos1D_[ "jetEta" ] = fs_->make< TH1D >( "jetEta", "jetEta", 100, -5., 5. );
	histos1D_[ "jetEta" ]->Sumw2();
	histos1D_[ "jetNum" ] = fs_->make< TH1D >( "jetNum", "jetNum", 10, 0., 10. );
	histos1D_[ "jetNum" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 300, 0., 3000. );
	histos1D_[ "HT" ]->Sumw2();
	histos1D_[ "NPV" ] = fs_->make< TH1D >( "NPV", "NPV", 80, 0., 80. );
	histos1D_[ "NPV" ]->Sumw2();
	histos1D_[ "NPV_NOPUWeight" ] = fs_->make< TH1D >( "NPV_NOPUWeight", "NPV_NOPUWeight", 80, 0., 80. );
	histos1D_[ "NPV_NOPUWeight" ]->Sumw2();
	histos1D_[ "PUWeight" ] = fs_->make< TH1D >( "PUWeight", "PUWeight", 50, 0., 5. );
	histos1D_[ "PUWeight" ]->Sumw2();
	histos1D_[ "neutralHadronEnergy" ] = fs_->make< TH1D >( "neutralHadronEnergy", "neutralHadronEnergy", 50, 0., 1. );
	histos1D_[ "neutralHadronEnergy" ]->Sumw2();
	histos1D_[ "neutralEmEnergy" ] = fs_->make< TH1D >( "neutralEmEnergy", "neutralEmEnergy", 50, 0., 1. );
	histos1D_[ "neutralEmEnergy" ]->Sumw2();
	histos1D_[ "chargedHadronEnergy" ] = fs_->make< TH1D >( "chargedHadronEnergy", "chargedHadronEnergy", 50, 0., 1. );
	histos1D_[ "chargedHadronEnergy" ]->Sumw2();
	histos1D_[ "chargedEmEnergy" ] = fs_->make< TH1D >( "chargedEmEnergy", "chargedEmEnergy", 50, 0., 1. );
	histos1D_[ "chargedEmEnergy" ]->Sumw2();
	histos1D_[ "chargedMultiplicity" ] = fs_->make< TH1D >( "chargedMultiplicity", "chargedMultiplicity", 50, 0., 1. );
	histos1D_[ "chargedMultiplicity" ]->Sumw2();
	histos1D_[ "numConst" ] = fs_->make< TH1D >( "numConst", "numConst", 100, 0., 100. );
	histos1D_[ "numConst" ]->Sumw2();


	histos1D_[ "jetPt_cutTrigger" ] = fs_->make< TH1D >( "jetPt_cutTrigger", "jetPt_cutTrigger", 100, 0., 1000. );
	histos1D_[ "jetPt_cutTrigger" ]->Sumw2();
	histos1D_[ "jetEta_cutTrigger" ] = fs_->make< TH1D >( "jetEta_cutTrigger", "jetEta_cutTrigger", 100, -5., 5. );
	histos1D_[ "jetEta_cutTrigger" ]->Sumw2();
	histos1D_[ "jetNum_cutTrigger" ] = fs_->make< TH1D >( "jetNum_cutTrigger", "jetNum_cutTrigger", 10, 0., 10. );
	histos1D_[ "jetNum_cutTrigger" ]->Sumw2();
	histos1D_[ "HT_cutTrigger" ] = fs_->make< TH1D >( "HT_cutTrigger", "HT_cutTrigger", 300, 0., 3000. );
	histos1D_[ "HT_cutTrigger" ]->Sumw2();


	histos1D_[ "jet1Pt_cut4Jets" ] = fs_->make< TH1D >( "jet1Pt_cut4Jets", "jet1Pt_cut4Jets", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cut4Jets" ]->Sumw2();
	histos1D_[ "jet2Pt_cut4Jets" ] = fs_->make< TH1D >( "jet2Pt_cut4Jets", "jet2Pt_cut4Jets", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cut4Jets" ]->Sumw2();
	histos1D_[ "jet3Pt_cut4Jets" ] = fs_->make< TH1D >( "jet3Pt_cut4Jets", "jet3Pt_cut4Jets", 100, 0., 1000. );
	histos1D_[ "jet3Pt_cut4Jets" ]->Sumw2();
	histos1D_[ "jet4Pt_cut4Jets" ] = fs_->make< TH1D >( "jet4Pt_cut4Jets", "jet4Pt_cut4Jets", 100, 0., 1000. );
	histos1D_[ "jet4Pt_cut4Jets" ]->Sumw2();
	histos1D_[ "jetNum_cut4Jets" ] = fs_->make< TH1D >( "jetNum_cut4Jets", "jetNum_cut4Jets", 10, 0., 10. );
	histos1D_[ "jetNum_cut4Jets" ]->Sumw2();
	histos1D_[ "HT_cut4Jets" ] = fs_->make< TH1D >( "HT_cut4Jets", "HT_cut4Jets", 300, 0., 3000. );
	histos1D_[ "HT_cut4Jets" ]->Sumw2();
	histos1D_[ "MET_cut4Jets" ] = fs_->make< TH1D >( "MET_cut4Jets", "MET_cut4Jets", 20, 0., 200. );
	histos1D_[ "MET_cut4Jets" ]->Sumw2();
	histos1D_[ "METHT_cut4Jets" ] = fs_->make< TH1D >( "METHT_cut4Jets", "METHT_cut4Jets", 50, 0., 1. );
	histos1D_[ "METHT_cut4Jets" ]->Sumw2();

	histos1D_[ "jet1Pt_cutBestPair" ] = fs_->make< TH1D >( "jet1Pt_cutBestPair", "jet1Pt_cutBestPair", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutBestPair" ]->Sumw2();
	histos1D_[ "jet2Pt_cutBestPair" ] = fs_->make< TH1D >( "jet2Pt_cutBestPair", "jet2Pt_cutBestPair", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutBestPair" ]->Sumw2();
	histos1D_[ "jet3Pt_cutBestPair" ] = fs_->make< TH1D >( "jet3Pt_cutBestPair", "jet3Pt_cutBestPair", 100, 0., 1000. );
	histos1D_[ "jet3Pt_cutBestPair" ]->Sumw2();
	histos1D_[ "jet4Pt_cutBestPair" ] = fs_->make< TH1D >( "jet4Pt_cutBestPair", "jet4Pt_cutBestPair", 100, 0., 1000. );
	histos1D_[ "jet4Pt_cutBestPair" ]->Sumw2();
	histos1D_[ "jetNum_cutBestPair" ] = fs_->make< TH1D >( "jetNum_cutBestPair", "jetNum_cutBestPair", 10, 0., 10. );
	histos1D_[ "jetNum_cutBestPair" ]->Sumw2();
	histos1D_[ "HT_cutBestPair" ] = fs_->make< TH1D >( "HT_cutBestPair", "HT_cutBestPair", 300, 0., 3000. );
	histos1D_[ "HT_cutBestPair" ]->Sumw2();
	histos1D_[ "MET_cutBestPair" ] = fs_->make< TH1D >( "MET_cutBestPair", "MET_cutBestPair", 20, 0., 200. );
	histos1D_[ "MET_cutBestPair" ]->Sumw2();
	histos1D_[ "METHT_cutBestPair" ] = fs_->make< TH1D >( "METHT_cutBestPair", "METHT_cutBestPair", 50, 0., 1. );
	histos1D_[ "METHT_cutBestPair" ]->Sumw2();
	histos1D_[ "NPV_cutBestPair" ] = fs_->make< TH1D >( "NPV_cutBestPair", "NPV_cutBestPair", 80, 0., 80. );
	histos1D_[ "NPV_cutBestPair" ]->Sumw2();
	histos1D_[ "neutralHadronEnergy_cutBestPair" ] = fs_->make< TH1D >( "neutralHadronEnergy_cutBestPair", "neutralHadronEnergy", 50, 0., 1. );
	histos1D_[ "neutralHadronEnergy_cutBestPair" ]->Sumw2();
	histos1D_[ "neutralEmEnergy_cutBestPair" ] = fs_->make< TH1D >( "neutralEmEnergy_cutBestPair", "neutralEmEnergy", 50, 0., 1. );
	histos1D_[ "neutralEmEnergy_cutBestPair" ]->Sumw2();
	histos1D_[ "chargedHadronEnergy_cutBestPair" ] = fs_->make< TH1D >( "chargedHadronEnergy_cutBestPair", "chargedHadronEnergy", 50, 0., 1. );
	histos1D_[ "chargedHadronEnergy_cutBestPair" ]->Sumw2();
	histos1D_[ "chargedEmEnergy_cutBestPair" ] = fs_->make< TH1D >( "chargedEmEnergy_cutBestPair", "chargedEmEnergy", 50, 0., 1. );
	histos1D_[ "chargedEmEnergy_cutBestPair" ]->Sumw2();
	histos1D_[ "chargedMultiplicity_cutBestPair" ] = fs_->make< TH1D >( "chargedMultiplicity_cutBestPair", "chargedMultiplicity", 50, 0., 1. );
	histos1D_[ "chargedMultiplicity_cutBestPair" ]->Sumw2();
	histos1D_[ "numConst_cutBestPair" ] = fs_->make< TH1D >( "numConst_cutBestPair", "numConst", 100, 0., 100. );
	histos1D_[ "numConst_cutBestPair" ]->Sumw2();
	histos1D_[ "jet1QGL_cutBestPair" ] = fs_->make< TH1D >( "jet1QGL_cutBestPair", "jet1QGL_cutBestPair", 10, 0., 1. );
	histos1D_[ "jet1QGL_cutBestPair" ]->Sumw2();
	histos1D_[ "jet2QGL_cutBestPair" ] = fs_->make< TH1D >( "jet2QGL_cutBestPair", "jet2QGL_cutBestPair", 10, 0., 1. );
	histos1D_[ "jet2QGL_cutBestPair" ]->Sumw2();
	histos1D_[ "jet3QGL_cutBestPair" ] = fs_->make< TH1D >( "jet3QGL_cutBestPair", "jet3QGL_cutBestPair", 10, 0., 1. );
	histos1D_[ "jet3QGL_cutBestPair" ]->Sumw2();
	histos1D_[ "jet4QGL_cutBestPair" ] = fs_->make< TH1D >( "jet4QGL_cutBestPair", "jet4QGL_cutBestPair", 10, 0., 1. );
	histos1D_[ "jet4QGL_cutBestPair" ]->Sumw2();
	histos1D_[ "massAve_cutBestPair" ] = fs_->make< TH1D >( "massAve_cutBestPair", "massAve_cutBestPair", 200, 0., 2000. );
	histos1D_[ "massAve_cutBestPair" ]->Sumw2();
	histos1D_[ "massAsym_cutBestPair" ] = fs_->make< TH1D >( "massAsym_cutBestPair", "massAsym_cutBestPair", 50, 0., 2. );
	histos1D_[ "massAsym_cutBestPair" ]->Sumw2();
	histos1D_[ "deltaEta_cutBestPair" ] = fs_->make< TH1D >( "deltaEta_cutBestPair", "deltaEta_cutBestPair", 50, 0., 10. );
	histos1D_[ "deltaEta_cutBestPair" ]->Sumw2();
	histos1D_[ "minDeltaR_cutBestPair" ] = fs_->make< TH1D >( "minDeltaR_cutBestPair", "minDeltaR_cutBestPair", 50, 0., 5. );
	histos1D_[ "minDeltaR_cutBestPair" ]->Sumw2();
	histos1D_[ "deltaR_cutBestPair" ] = fs_->make< TH1D >( "deltaR_cutBestPair", "deltaR_cutBestPair", 50, 0., 5. );
	histos1D_[ "deltaR_cutBestPair" ]->Sumw2();
	histos1D_[ "cosThetaStar1_cutBestPair" ] = fs_->make< TH1D >( "cosThetaStar1_cutBestPair", "cosThetaStar1_cutBestPair", 10, 0., 1. );
	histos1D_[ "cosThetaStar1_cutBestPair" ]->Sumw2();
	histos1D_[ "cosThetaStar2_cutBestPair" ] = fs_->make< TH1D >( "cosThetaStar2_cutBestPair", "cosThetaStar2_cutBestPair", 10, 0., 1. );
	histos1D_[ "cosThetaStar2_cutBestPair" ]->Sumw2();
	histos2D_[ "deltavsMassAve_cutBestPair" ] = fs_->make< TH2D >( "deltavsMassAve_cutBestPair", "deltavsMassAve_cutBestPair", 200, 0., 2000.,  300, -500., 1000. );
	histos2D_[ "deltavsMassAve_cutBestPair" ]->Sumw2();
	histos2D_[ "dijetsEta_cutBestPair" ] = fs_->make< TH2D >( "dijetsEta_cutBestPair", "dijetsEta_cutBestPair", 48, -3., 3., 48, -3., 3. );
	histos2D_[ "dijetsEta_cutBestPair" ]->Sumw2();

	histos1D_[ "jet1Pt_cutMassAsym" ] = fs_->make< TH1D >( "jet1Pt_cutMassAsym", "jet1Pt_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet2Pt_cutMassAsym" ] = fs_->make< TH1D >( "jet2Pt_cutMassAsym", "jet2Pt_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet3Pt_cutMassAsym" ] = fs_->make< TH1D >( "jet3Pt_cutMassAsym", "jet3Pt_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet3Pt_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet4Pt_cutMassAsym" ] = fs_->make< TH1D >( "jet4Pt_cutMassAsym", "jet4Pt_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet4Pt_cutMassAsym" ]->Sumw2();
	histos1D_[ "jetNum_cutMassAsym" ] = fs_->make< TH1D >( "jetNum_cutMassAsym", "jetNum_cutMassAsym", 10, 0., 10. );
	histos1D_[ "jetNum_cutMassAsym" ]->Sumw2();
	histos1D_[ "HT_cutMassAsym" ] = fs_->make< TH1D >( "HT_cutMassAsym", "HT_cutMassAsym", 300, 0., 3000. );
	histos1D_[ "HT_cutMassAsym" ]->Sumw2();
	histos1D_[ "massAve_cutMassAsym" ] = fs_->make< TH1D >( "massAve_cutMassAsym", "massAve_cutMassAsym", 200, 0., 2000. );
	histos1D_[ "massAve_cutMassAsym" ]->Sumw2();
	histos1D_[ "massAsym_cutMassAsym" ] = fs_->make< TH1D >( "massAsym_cutMassAsym", "massAsym_cutMassAsym", 50, 0., 2. );
	histos1D_[ "massAsym_cutMassAsym" ]->Sumw2();
	histos1D_[ "deltaEta_cutMassAsym" ] = fs_->make< TH1D >( "deltaEta_cutMassAsym", "deltaEta_cutMassAsym", 50, 0., 10. );
	histos1D_[ "deltaEta_cutMassAsym" ]->Sumw2();
	histos1D_[ "minDeltaR_cutMassAsym" ] = fs_->make< TH1D >( "minDeltaR_cutMassAsym", "minDeltaR_cutMassAsym", 50, 0., 5. );
	histos1D_[ "minDeltaR_cutMassAsym" ]->Sumw2();
	histos2D_[ "deltavsMassAve_cutMassAsym" ] = fs_->make< TH2D >( "deltavsMassAve_cutMassAsym", "deltavsMassAve_cutMassAsym", 200, 0., 2000.,  300, -500., 1000. );
	histos2D_[ "deltavsMassAve_cutMassAsym" ]->Sumw2();
	histos2D_[ "dijetsEta_cutMassAsym" ] = fs_->make< TH2D >( "dijetsEta_cutMassAsym", "dijetsEta_cutMassAsym", 48, -3., 3., 48, -3., 3. );
	histos2D_[ "dijetsEta_cutMassAsym" ]->Sumw2();

	histos1D_[ "jet1Pt_cutDEta" ] = fs_->make< TH1D >( "jet1Pt_cutDEta", "jet1Pt_cutDEta", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutDEta" ]->Sumw2();
	histos1D_[ "jet2Pt_cutDEta" ] = fs_->make< TH1D >( "jet2Pt_cutDEta", "jet2Pt_cutDEta", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutDEta" ]->Sumw2();
	histos1D_[ "jet3Pt_cutDEta" ] = fs_->make< TH1D >( "jet3Pt_cutDEta", "jet3Pt_cutDEta", 100, 0., 1000. );
	histos1D_[ "jet3Pt_cutDEta" ]->Sumw2();
	histos1D_[ "jet4Pt_cutDEta" ] = fs_->make< TH1D >( "jet4Pt_cutDEta", "jet4Pt_cutDEta", 100, 0., 1000. );
	histos1D_[ "jet4Pt_cutDEta" ]->Sumw2();
	histos1D_[ "jetNum_cutDEta" ] = fs_->make< TH1D >( "jetNum_cutDEta", "jetNum_cutDEta", 10, 0., 10. );
	histos1D_[ "jetNum_cutDEta" ]->Sumw2();
	histos1D_[ "HT_cutDEta" ] = fs_->make< TH1D >( "HT_cutDEta", "HT_cutDEta", 300, 0., 3000. );
	histos1D_[ "HT_cutDEta" ]->Sumw2();
	histos1D_[ "massAve_cutDEta" ] = fs_->make< TH1D >( "massAve_cutDEta", "massAve_cutDEta", 200, 0., 2000. );
	histos1D_[ "massAve_cutDEta" ]->Sumw2();
	histos1D_[ "massAsym_cutDEta" ] = fs_->make< TH1D >( "massAsym_cutDEta", "massAsym_cutDEta", 50, 0., 2. );
	histos1D_[ "massAsym_cutDEta" ]->Sumw2();
	histos1D_[ "deltaEta_cutDEta" ] = fs_->make< TH1D >( "deltaEta_cutDEta", "deltaEta_cutDEta", 50, 0., 10. );
	histos1D_[ "deltaEta_cutDEta" ]->Sumw2();
	histos1D_[ "minDEtaR_cutDEta" ] = fs_->make< TH1D >( "minDEtaR_cutDEta", "minDEtaR_cutDEta", 50, 0., 5. );
	histos1D_[ "minDEtaR_cutDEta" ]->Sumw2();
	histos2D_[ "deltavsMassAve_cutDEta" ] = fs_->make< TH2D >( "deltavsMassAve_cutDEta", "deltavsMassAve_cutDEta", 200, 0., 2000.,  300, -500., 1000. );
	histos2D_[ "deltavsMassAve_cutDEta" ]->Sumw2();
	histos2D_[ "dijetsEta_cutDEta" ] = fs_->make< TH2D >( "dijetsEta_cutDEta", "dijetsEta_cutDEta", 48, -3., 3., 48, -3., 3. );
	histos2D_[ "dijetsEta_cutDEta" ]->Sumw2();
	
	
	histos1D_[ "jet1Pt_cutDelta" ] = fs_->make< TH1D >( "jet1Pt_cutDelta", "jet1Pt_cutDelta", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutDelta" ]->Sumw2();
	histos1D_[ "jet2Pt_cutDelta" ] = fs_->make< TH1D >( "jet2Pt_cutDelta", "jet2Pt_cutDelta", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutDelta" ]->Sumw2();
	histos1D_[ "jet3Pt_cutDelta" ] = fs_->make< TH1D >( "jet3Pt_cutDelta", "jet3Pt_cutDelta", 100, 0., 1000. );
	histos1D_[ "jet3Pt_cutDelta" ]->Sumw2();
	histos1D_[ "jet4Pt_cutDelta" ] = fs_->make< TH1D >( "jet4Pt_cutDelta", "jet4Pt_cutDelta", 100, 0., 1000. );
	histos1D_[ "jet4Pt_cutDelta" ]->Sumw2();
	histos1D_[ "jetNum_cutDelta" ] = fs_->make< TH1D >( "jetNum_cutDelta", "jetNum_cutDelta", 10, 0., 10. );
	histos1D_[ "jetNum_cutDelta" ]->Sumw2();
	histos1D_[ "HT_cutDelta" ] = fs_->make< TH1D >( "HT_cutDelta", "HT_cutDelta", 300, 0., 3000. );
	histos1D_[ "HT_cutDelta" ]->Sumw2();
	histos1D_[ "massAve_cutDelta" ] = fs_->make< TH1D >( "massAve_cutDelta", "massAve_cutDelta", 200, 0., 2000. );
	histos1D_[ "massAve_cutDelta" ]->Sumw2();
	histos1D_[ "massAsym_cutDelta" ] = fs_->make< TH1D >( "massAsym_cutDelta", "massAsym_cutDelta", 50, 0., 2. );
	histos1D_[ "massAsym_cutDelta" ]->Sumw2();
	histos1D_[ "deltaEta_cutDelta" ] = fs_->make< TH1D >( "deltaEta_cutDelta", "deltaEta_cutDelta", 50, 0., 10. );
	histos1D_[ "deltaEta_cutDelta" ]->Sumw2();
	histos1D_[ "minDeltaR_cutDelta" ] = fs_->make< TH1D >( "minDeltaR_cutDelta", "minDeltaR_cutDelta", 50, 0., 5. );
	histos1D_[ "minDeltaR_cutDelta" ]->Sumw2();
	histos2D_[ "deltavsMassAve_cutDelta" ] = fs_->make< TH2D >( "deltavsMassAve_cutDelta", "deltavsMassAve_cutDelta", 200, 0., 2000.,  300, -500., 1000. );
	histos2D_[ "deltavsMassAve_cutDelta" ]->Sumw2();
	histos2D_[ "dijetsEta_cutDelta" ] = fs_->make< TH2D >( "dijetsEta_cutDelta", "dijetsEta_cutDelta", 48, -3., 3., 48, -3., 3. );
	histos2D_[ "dijetsEta_cutDelta" ]->Sumw2();


	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("4Jets");
	cutLabels.push_back("BestPair");
	cutLabels.push_back("MassAsym");
	cutLabels.push_back("DEta");
	cutLabels.push_back("Delta");
	cutLabels.push_back("DeltaR");
	cutLabels.push_back("CosTheta");
	cutLabels.push_back("DEta");
	cutLabels.push_back("MassPairing");
	histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflow" ]->Sumw2();
	for( const string &ivec : cutLabels ) cutmap[ ivec ] = 0;
}

// ------------ method called once each job just after ending the event loop  ------------
void RUNAnalysis::endJob() {

	int ibin = 1;
	for( const string &ivec : cutLabels ) {
		histos1D_["hcutflow"]->SetBinContent( ibin, cutmap[ ivec ] );
		histos1D_["hcutflow"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		ibin++;
	}

}

void RUNAnalysis::clearVariables() {

	jetsPt->clear();
	jetsEta->clear();
	jetsPhi->clear();
	jetsE->clear();

}

void RUNAnalysis::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutHT", 800);
	desc.add<double>("cut4JetPt", 80);
	desc.add<double>("cutMassAsym", 1);
	desc.add<double>("cutDelta", 1);
	desc.add<double>("cutDEta", 1);
	desc.add<double>("cutCosThetaStar", 1);
	desc.add<double>("cutDeltaR", 1);
	desc.add<bool>("bjSample", false);
	desc.add<bool>("isData", false);
	desc.add<double>("scale", 1);
	desc.add<string>("dataPUFile", "supportFiles/PileupData2015D_JSON_10-23-2015.root");
	desc.add<string>("jecVersion", "supportFiles/Summer15_25nsV6");
	desc.add<string>("systematics", "None");
	vector<string> HLTPass;
	HLTPass.push_back("HLT_PFHT800");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	desc.add<InputTag>("Lumi", 	InputTag("eventInfo:evtInfoLumiBlock"));
	desc.add<InputTag>("Run", 	InputTag("eventInfo:evtInfoRunNumber"));
	desc.add<InputTag>("Event", 	InputTag("eventInfo:evtInfoEventNumber"));
	desc.add<InputTag>("generator", 	InputTag("generator"));
	desc.add<InputTag>("extLHEProducer", 	InputTag("externalLHEProducer"));
	desc.add<InputTag>("bunchCross", 	InputTag("eventUserData:puBX"));
	desc.add<InputTag>("rho", 	InputTag("vertexInfo:rho"));
	desc.add<InputTag>("puNumInt", 	InputTag("eventUserData:puNInt"));
	desc.add<InputTag>("trueNInt", 	InputTag("eventUserData:puNtrueInt"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK4CHS:jetAK4CHSPt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK4CHS:jetAK4CHSEta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK4CHS:jetAK4CHSPhi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK4CHS:jetAK4CHSE"));
	desc.add<InputTag>("jetQGL", 	InputTag("jetsAK4CHS:jetAK4CHSQGL"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK4CHS:jetAK4CHSMass"));
	desc.add<InputTag>("jetCSVv2", 	InputTag("jetsAK4CHS:jetAK4CHSCSVv2"));
	desc.add<InputTag>("jetCMVAv2", 	InputTag("jetsAK4CHS:jetAK4CHSCMVAv2"));
	desc.add<InputTag>("jetArea", 	InputTag("jetsAK4CHS:jetAK4CHSjetArea"));
	desc.add<InputTag>("jetGenPt", 	InputTag("jetsAK4CHS:jetAK4CHSGenJetPt"));
	desc.add<InputTag>("jetGenEta", 	InputTag("jetsAK4CHS:jetAK4CHSGenJetEta"));
	desc.add<InputTag>("jetGenPhi", 	InputTag("jetsAK4CHS:jetAK4CHSGenJetPhi"));
	desc.add<InputTag>("jetGenE", 	InputTag("jetsAK8CHS:jetAK8CHSGenJetE"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
	desc.add<InputTag>("metPt", 	InputTag("metFull:metFullPt"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK4CHS:jetAK4CHSjecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK4CHS:jetAK4CHSneutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK4CHS:jetAK4CHSneutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK4CHS:jetAK4CHSchargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK4CHS:jetAK4CHSMuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK4CHS:jetAK4CHSchargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK4CHS:jetAK4CHSChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK4CHS:jetAK4CHSneutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK4CHS:jetAK4CHSchargedMultiplicity"));
	// Trigger
	desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	descriptions.addDefault(desc);
}
      
void RUNAnalysis::beginRun(const Run& iRun, const EventSetup& iSetup){

	/* Weights from scale variations, PDFs etc. are stored in the relative product. 
	 * Notice that to be used they need to be renormalized to the central event weight
	 * at LHE level which may be different from genEvtInfo->weight()
	 */
	if (!isData) {
		Handle<LHERunInfoProduct> lheRunInfo;
		iRun.getByLabel( "externalLHEProducer", lheRunInfo );

		if (lheRunInfo.isValid()) {
			// Check which PDF set was used
			lhaPdfId = lheRunInfo->heprup().PDFSUP.first;
			std::cout<<"LHE: LHA PDF ID = "<<lhaPdfId<< "\nLHE:   --> For more info about the sets, check: https://lhapdf.hepforge.org/pdfsets.html"<<std::endl;

			// Check headers
			LHERunInfoProduct lheRunInfoProduct = *(lheRunInfo.product());
			typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;
			size_t iHead = 0;
			for (headers_const_iterator header=lheRunInfoProduct.headers_begin(); header!=lheRunInfoProduct.headers_end(); header++){
				if (header->tag()=="initrwgt") {
					//std::cout<<"LHE: "<<iHead<<" "<<header->tag()<<std::endl;
					for (auto line : header->lines()) {
						//std::cout<<"LHE: "<<line;
						// Fix buggy powheg samples
						if (lhaPdfId==-1 && line.find("weight id=\"2001\"")!=std::string::npos) {
						if (line.find("PDF set = 260001")!=std::string::npos) lhaPdfId = 260000;
						else if (line.find("PDF set = 260401")!=std::string::npos) lhaPdfId = 260400;
						}
					}
				}
				iHead++;
			}
		}
	}
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNAnalysis);
