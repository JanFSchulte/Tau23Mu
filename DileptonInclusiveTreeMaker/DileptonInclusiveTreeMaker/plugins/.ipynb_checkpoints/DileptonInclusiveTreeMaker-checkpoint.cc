/*
 
 Description: [one line class summary]
 
 Implementation:
 [Notes on implementation]
 */
//
// Original Author:  Federica Simone
//
//


// system include files
#include <memory>
#include <algorithm>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include <DataFormats/MuonReco/interface/MuonFwd.h>
#include <DataFormats/MuonReco/interface/Muon.h>
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/Matcher.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "TFile.h"
#include "TH1.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TH2.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"


#include "RecoVertex/KinematicFit/interface/KinematicParticleVertexFitter.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticleFactoryFromTransientTrack.h"
#include "RecoVertex/KinematicFit/interface/MassKinematicConstraint.h"
#include "RecoVertex/KinematicFit/interface/KinematicParticleFitter.h"
#include "RecoVertex/KinematicFitPrimitives/interface/MultiTrackKinematicConstraint.h"
#include "RecoVertex/KinematicFit/interface/KinematicConstrainedVertexFitter.h"
#include "RecoVertex/KinematicFit/interface/TwoTrackMassKinematicConstraint.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/RefCountedKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/TransientTrackKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicTree.h"


#include "RecoVertex/KinematicFit/interface/KinematicParticleVertexFitter.h"
#include "RecoVertex/KinematicFit/interface/KinematicParticleFitter.h"
#include "RecoVertex/KinematicFit/interface/MassKinematicConstraint.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/RefCountedKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/TransientTrackKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/TransientTrackKinematicParticle.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticleFactoryFromTransientTrack.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"


#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackFromFTSFactory.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h"

#include "DataFormats/Candidate/interface/VertexCompositeCandidateFwd.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"

#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"

#include "PhysicsTools/PatUtils/interface/TriggerHelper.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/PatCandidates/interface/TriggerFilter.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/Candidate/interface/OverlapChecker.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

#include "DataFormats/L1Trigger/interface/Muon.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1TGlobalPrescalesVetosRcd.h"
#include "CondFormats/L1TObjects/interface/L1TGlobalPrescalesVetos.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/TrackReco/interface/TrackToTrackMap.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"


OverlapChecker overlap;


////
class DileptonInclusiveTreeMaker : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
    explicit DileptonInclusiveTreeMaker(const edm::ParameterSet&);
    ~DileptonInclusiveTreeMaker();
    
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    float dR(float eta1, float eta2, float phi1, float phi2);
    float dRtriggerMatch(pat::Muon m, std::vector<pat::TriggerObjectStandAlone> triggerObjects);
    float dRtriggerMatchTrk(reco::Track Trk, std::vector<pat::TriggerObjectStandAlone> triggerObjects);
    void beginRun(edm::Run const &, edm::EventSetup const&, edm::Event const&);
    typedef std::pair<const reco::MuonChamberMatch*, const reco::MuonSegmentMatch*> MatchPair;
    const MatchPair& getBetterMatch(const MatchPair&, const MatchPair&) const;
    float dX(const MatchPair&) const;
    float pullX(const MatchPair&) const;
    float pullDxDz(const MatchPair&) const;
    float dY(const MatchPair&) const;
    float pullY(const MatchPair&) const;
    float pullDyDz(const MatchPair&) const;
    
private:
    virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    // virtual void beginRun(edm::Run const &, edm::EventSetup const&) override;
    virtual void endJob() override;
    edm::EDGetTokenT<edm::View<pat::Muon> > muons_;
    edm::EDGetTokenT<edm::View<reco::Vertex> > vertex_;
    //edm::EDGetTokenT<edm::View<reco::Track> > trackToken_;
    //edm::EDGetTokenT<std::vector<pat::PackedCandidate> > trackToken_;
    edm::EDGetTokenT<edm::View<pat::PackedCandidate> > trackToken_;
    //edm::EDGetTokenT<edm::View<reco::CompositeCandidate> > Cand3Mu_;
    edm::EDGetTokenT<edm::View<reco::CompositeCandidate> > Cand2Mu1Track_;
    edm::EDGetTokenT<edm::View<reco::CompositeCandidate> > DiMuon_;
    edm::EDGetTokenT<edm::View<reco::GenParticle> > genParticles_;
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puToken_ ;
    edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
    edm::EDGetTokenT<BXVector<l1t::Muon> > l1muonsToken_;
    edm::EDGetTokenT<reco::BeamSpot> token_BeamSpot;
    //edm::EDGetTokenT<trigger::TriggerEvent> trigeventToken_;
    edm::EDGetToken algToken_;
    edm::EDGetToken algTok_;
    edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> theTransientTrackBuilder_;
    //edm::ESGetToken<L1TUtmTriggerMenu,L1TUtmTriggerMenuRcd> theL1TUtmTriggerMenu_;
    edm::EDGetTokenT<std::vector<pat::PackedCandidate> >srcCands_;
    edm::EDGetTokenT<std::vector<pat::TriggerObjectStandAlone> > triggerObjects_;
    bool is3Mu;
    bool isMc;
    bool isAna;
    bool is2016;
    bool is2017;
    bool is2018;
    bool isBParking;
    //edm::EDGetTokenT<edm::TriggerResults> trigResultsToken;
    //edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigObjCollToken;
    //const TransientTrackBuilder* theTransientTrackBuilder_;
    HLTConfigProvider hltConfig;
    //TPMERegexp* _re;
    
    edm::Service<TFileService> fs;
    l1t::L1TGlobalUtil* gtUtil_; 
    TH1F *hEvents;
    TH1F *hEventsAfterGoodCand;
    
    edm::EDGetToken algInputTag_;
    //edm::EDGetToken algTag_, extTag_;
    const edm::InputTag algTag_, extTag_;
    
    /*
    TH1F *hEvents_3Mu, *hEvents_MuFilter, *hEvents_DiMuonDz, *hEvent_TauCharge, *hEvent_3MuonVtx, *hEvent_3MuonMass, *hEvent_Valid3MuonVtx; 
    TH1F *hGenMuonPt; TH1F *hGenMuonEta;
    TH1F *hMuonPt; TH1F *hMuonP; TH1F *hMuonEta, *hGlobalMuonEta, *hTrackerMuonEta, *hLooseMuonEta, *hSoftMuonEta;
    TH1F *hGlobalMuonPt, *hSoftMuonPt, *hLooseMuonPt, *hTrackerMuonPt;
    TH1F *hMuonNumberOfValidHits;
    TH1F *hMuonDB; TH1F *hMuonTime; TH1F *hMuonTimeErr;
    TH1F *hGenTauPt, *hDiMuonDz, *hDiMuonDR, *hGoodMuSize, *hMuonSize_GoodDiMu;
    TH1F *hThreeMuonInvMass, *hThreeMuonCharge, *hVtxSize, *hTau_vFit_chi2, *h3MuonMassVtxFit;
    TH2F *hMuonTimeVsP;
    */

    /////tree
    TTree*      tree_;
    std::vector<float>  MuonPt, MuonEta, MuonPhi;
    std::vector<double> MuonEnergy,  MuonCharge;
    std::vector<int> GenParticle_PdgId, GenParticle_MotherPdgId, GenParticle_isDs, GenParticle_isB, GenParticle_isBdecay;
    std::vector<double> GenParticle_Pt, GenParticle_Eta, GenParticle_Phi;
    
    //Vtx position
    std::vector<double> Muon_vx, Muon_vy, Muon_vz;
    
    //MuonID
    std::vector<double> Muon_isGlobal, Muon_isTracker, Muon_isSoft, Muon_isLoose, Muon_isMedium, Muon_isPF, Muon_isRPCMuon, Muon_isStandAloneMuon, Muon_isTrackerMuon, Muon_isCaloMuon, Muon_isQualityValid, Muon_isTimeValid, Muon_isIsolationValid, Muon_numberOfMatchedStations, Muon_numberOfMatches;
    
    //MuonTime
    std::vector<double>  Muon_timeAtIpInOut, Muon_timeAtIpInOutErr;
    
    //Muon inner + outer track
    std::vector<double>  Muon_GLnormChi2, Muon_GLhitPattern_numberOfValidMuonHits, Muon_trackerLayersWithMeasurement, Muon_Numberofvalidpixelhits, Muon_outerTrack_p, Muon_outerTrack_eta, Muon_outerTrack_phi, Muon_outerTrack_normalizedChi2, Muon_outerTrack_muonStationsWithValidHits, Muon_innerTrack_p, Muon_innerTrack_eta, Muon_innerTrack_phi, Muon_innerTrack_normalizedChi2, Muon_QInnerOuter;
    
    std::vector<double>   Muon_combinedQuality_updatedSta, Muon_combinedQuality_trkKink, Muon_combinedQuality_glbKink, Muon_combinedQuality_trkRelChi2, Muon_combinedQuality_staRelChi2, Muon_combinedQuality_chi2LocalPosition, Muon_combinedQuality_chi2LocalMomentum, Muon_combinedQuality_localDistance, Muon_combinedQuality_globalDeltaEtaPhi, Muon_combinedQuality_tightMatch, Muon_combinedQuality_glbTrackProbability, Muon_calEnergy_em, Muon_calEnergy_emS9, Muon_calEnergy_emS25, Muon_calEnergy_had, Muon_calEnergy_hadS9, Muon_segmentCompatibility, Muon_caloCompatibility, Muon_ptErrOverPt, Muon_BestTrackPt, Muon_BestTrackPtErr, Muon_BestTrackEta, Muon_BestTrackEtaErr, Muon_BestTrackPhi, Muon_BestTrackPhiErr;
    
    std::vector<int>  Muon_PdgId, Muon_MotherPdgId, Muon_simFlavour;
    
    std::vector<double>  Mu01_Pt, Mu01_Eta, Mu01_Phi, Mu02_Pt, Mu02_Eta, Mu02_Phi, GenMatchMu01_SimPt, GenMatchMu02_SimPt, GenMatchMu01_SimEta, GenMatchMu02_SimEta, GenMatchMu01_SimPhi, GenMatchMu02_SimPhi, GenMatchMu01_Pt, GenMatchMu02_Pt, GenMatchMu01_Eta, GenMatchMu02_Eta, GenMatchMu01_Phi, GenMatchMu02_Phi, GenMatchMu03_Phi;
    
    std::vector<float> Mu01_dRtriggerMatch, Mu02_dRtriggerMatch, Tr_dRtriggerMatch;
    std::vector<float> Mu1_dRtriggerMatch_Mu7, Mu2_dRtriggerMatch_Mu7, Mu3_dRtriggerMatch_Mu7;
    std::vector<float> Mu1_dRtriggerMatch_Mu8, Mu2_dRtriggerMatch_Mu8, Mu3_dRtriggerMatch_Mu8;
    std::vector<float> Mu1_dRtriggerMatch_Mu8_IP5, Mu1_dRtriggerMatch_Mu8_IP6, Mu1_dRtriggerMatch_Mu9_IP0, Mu1_dRtriggerMatch_Mu9_IP3, Mu1_dRtriggerMatch_Mu9_IP4, Mu1_dRtriggerMatch_Mu9_IP5, Mu1_dRtriggerMatch_Mu9_IP6, Mu1_dRtriggerMatch_Mu12_IP6;
    std::vector<double> Mu1_dRtriggerMatch_2017, Mu2_dRtriggerMatch_2017, Mu3_dRtriggerMatch_2017;
    std::vector<double> Mu1_dRtriggerMatch, Mu2_dRtriggerMatch, Mu3_dRtriggerMatch;
    
    std::vector<double> Muon_emEt03, Muon_hadEt03, Muon_nJets03, Muon_nTracks03, Muon_sumPt03, Muon_emEt05, Muon_hadEt05, Muon_nJets05, Muon_nTracks05, Muon_sumPt05,
    Muon_hadVetoEt03,Muon_emVetoEt03, Muon_trackerVetoPt03, Muon_hadVetoEt05, Muon_emVetoEt05, Muon_trackerVetoPt05;
    
    std::vector<double> Triplet_mindca_iso, Triplet_relativeiso, Triplet_relativeiso2;
    std::vector<int>  Mu01_TripletIndex, Mu02_TripletIndex, Tr_TripletIndex, selectedTripletsIndex;
    std::vector<double>  Mu1_NTracks03iso, Mu2_NTracks03iso, Mu3_NTracks03iso;
    
    int TripletCollectionSize, TripletCollectionSize2, PVCollection_Size, MuonCollectionSize, SelectedTripletsSize;

    std::vector<double>  TripletVtx2_x, TripletVtx2_y, TripletVtx2_z, TripletVtx2_Chi2, TripletVtx2_NDOF, Triplet2_Mass, Triplet2_Pt, Triplet2_Eta, Triplet2_Phi, Triplet2_Charge;
    
    std::vector<double>  dxy_mu1,  dxy_mu2,  dxy_mu3,  dxyErr_mu1,  dxyErr_mu2,  dxyErr_mu3;
    
    std::vector<double>  RefittedPV2_x;
    std::vector<double>  RefittedPV2_y;
    std::vector<double>  RefittedPV2_z;
    std::vector<double>  RefittedPV2_NTracks;
    std::vector<int>     RefittedPV2_isValid;
    std::vector<double>  RefittedPV_Chi2, RefittedPV_nDOF;
    std::vector<double>  PV_bis_Chi2, PV_bis_nDOF;
    
    //RefittedPV_Chi2.push_back(PVertex.);
    
    std::vector<double>  FlightDistPVSV2;
    std::vector<double>  FlightDistPVSV2_Err;
    std::vector<double>  FlightDistPVSV2_Significance;
    std::vector<double>  FlightDistPVSV2_chi2;

    std::vector<double>  Track_pt, Track_eta, Track_phi, Track_charge, Track_normalizedChi2, Track_numberOfValidHits, Track_dxy, Track_dxyError, Track_dz, Track_dzError, Track_vx, Track_vy, Track_vz;
    std::vector<double>  Tr_Pt, Tr_Phi, Tr_Eta;
    std::vector<int>  Track_pdgId;
   
    std::vector<double> RefTrack1_Pt, RefTrack1_Eta, RefTrack1_Phi, RefTrack1_TripletIndex;
    std::vector<double> RefTrack2_Pt, RefTrack2_Eta, RefTrack2_Phi, RefTrack2_TripletIndex;
    std::vector<double> RefTrack3_Pt, RefTrack3_Eta, RefTrack3_Phi, RefTrack3_TripletIndex;

    std::vector<double> RefittedSV_Chi2, RefittedSV_nDOF, RefittedSV_Mass;

    std::vector<double> IsoTrackMu1_Pt, IsoTrackMu1_Eta, IsoTrackMu1_Phi;
    std::vector<double> IsoTrackMu2_Pt, IsoTrackMu2_Eta, IsoTrackMu2_Phi;
    std::vector<double> IsoTrackMu3_Pt, IsoTrackMu3_Eta, IsoTrackMu3_Phi;
 
    std::vector<double> PV_x,  PV_y,  PV_z,  PV_NTracks;
    std::vector<double> BS_x,  BS_y,  BS_z;
    std::vector<double> Vtx12_x, Vtx23_x, Vtx13_x, Vtx12_y, Vtx23_y, Vtx13_y, Vtx12_z, Vtx23_z, Vtx13_z, Vtx12_Chi2, Vtx23_Chi2, Vtx13_Chi2, Vtx12_nDOF, Vtx23_nDOF, Vtx13_nDOF;
    
    double x_bs = 0.0;
    double y_bs = 0.0;
    double z_bs = 0.0;
    
    std::vector<int> NGoodTriplets;
    uint  evt, run, lumi, puN;
    std::vector<string>  Trigger_l1name;
    std::vector<int> Trigger_l1Initialdecision, Trigger_l1Finaldecision;
    std::vector<double> Trigger_l1prescale;
    
    
    std::vector<string>  Trigger_hltname;
    std::vector<int> Trigger_hltdecision;
    
    std::vector<double> MuonPt_HLT,  MuonEta_HLT,  MuonPhi_HLT;
    std::vector<double> MuonPt_HLT2017, MuonEta_HLT2017, MuonPhi_HLT2017, MuonPt_HLT_BPMu7, MuonEta_HLT_BPMu7, MuonPhi_HLT_BPMu7, MuonPt_HLT_BPMu8, MuonEta_HLT_BPMu8, MuonPhi_HLT_BPMu8, MuonPt_HLT_BPMu8_IP6,  MuonEta_HLT_BPMu8_IP6, MuonPhi_HLT_BPMu8_IP6, MuonPt_HLT_BPMu8_IP5, MuonEta_HLT_BPMu8_IP5, MuonPhi_HLT_BPMu8_IP5,   MuonPt_HLT_BPMu9_IP0, MuonEta_HLT_BPMu9_IP0, MuonPhi_HLT_BPMu9_IP0, MuonPt_HLT_BPMu9_IP3, MuonEta_HLT_BPMu9_IP3, MuonPhi_HLT_BPMu9_IP3, MuonPt_HLT_BPMu9_IP4,MuonEta_HLT_BPMu9_IP4,MuonPhi_HLT_BPMu9_IP4,MuonPt_HLT_BPMu9_IP5, MuonEta_HLT_BPMu9_IP5,MuonPhi_HLT_BPMu9_IP5,MuonPt_HLT_BPMu9_IP6,MuonEta_HLT_BPMu9_IP6,MuonPhi_HLT_BPMu9_IP6,MuonPt_HLT_BPMu12_IP6,MuonEta_HLT_BPMu12_IP6,MuonPhi_HLT_BPMu12_IP6;
    std::vector<double> MuonPt_HLT_DiMu_Incl, MuonEta_HLT_DiMu_Incl, MuonPhi_HLT_DiMu_Incl;
    std::vector<double> MuonPt_HLT_DiMu_Incl_displ, MuonEta_HLT_DiMu_Incl_displ, MuonPhi_HLT_DiMu_Incl_displ;
    std::vector<double> MuonPt_HLT_Dimuon, MuonEta_HLT_Dimuon, MuonPhi_HLT_Dimuon;
 
    std::vector<double>  Muon_innerTrack_nLostHitsInner, Muon_innerTrack_nLostHitsOuter, Muon_innerTrack_nPixels, Muon_innerTrack_nValidHits, Muon_innerTrack_nLostHitsOn, Muon_innerTrack_highPurity,  Muon_innerTrack_ValidFraction, Muon_Numberofvalidtrackerhits, Muon_validMuonHitComb, Muon_IP2D_BS,  Muon_IP3D_BS,  Muon_IP2D_PV,  Muon_IP3D_PV, Muon_SoftMVA_Val;
    
    std::vector<double>  DistXY_PVSV,  DistXY_significance_PVSV;
    std::vector<double>  Triplet_IsoMu3, Triplet_IsoMu2, Triplet_IsoMu1;
    std::vector<double>  FlightDistBS_SV,  FlightDistBS_SV_Err,  FlightDistBS_SV_Significance;
    std::vector<double>  Mu1_IsGlobal, Mu2_IsGlobal, Mu3_IsGlobal, Mu1_IsPF, Mu2_IsPF, Mu3_IsPF;
    
    std::vector<double> L1Muon_Pt, L1Muon_Eta, L1Muon_Phi, L1Muon_EtaAtVtx, L1Muon_PhiAtVtx, L1Muon_BX, L1Muon_Quality, L1Muon_Charge, L1Muon_ChargeValid, L1Muon_TfMuonIndex, L1Muon_dPhi, L1Muon_dEta, L1Muon_rank, L1Muon_isoSum;
   
    std::vector<double> Muon_combinedQuality_match1_dX, Muon_combinedQuality_match1_pullX, Muon_combinedQuality_match1_pullDxDz, Muon_combinedQuality_match1_dY, Muon_combinedQuality_match1_pullY, Muon_combinedQuality_match1_pullDyDz;
    std::vector<double> Muon_combinedQuality_match2_dX, Muon_combinedQuality_match2_pullX, Muon_combinedQuality_match2_pullDxDz, Muon_combinedQuality_match2_dY, Muon_combinedQuality_match2_pullY, Muon_combinedQuality_match2_pullDyDz;
    

    /////SyncTree
    /*
    TTree*      SyncTree_;
    std::vector<float>  allmuons_pt, leadmuon_pt, leadmuon_phi, leadmuon_eta;
    std::vector<float>  alltracks_pt, leadtrack_pt,  leadtrack_eta,  leadtrack_phi;
    uint nprimevtxs, nmuons, evt, run, lumi;
    */
};



DileptonInclusiveTreeMaker::DileptonInclusiveTreeMaker(const edm::ParameterSet& iConfig){
    //edm::InputTag algInputTag_;
    isMc = iConfig.getUntrackedParameter<bool>("isMcLabel");
    isAna = iConfig.getUntrackedParameter<bool>("isAnaLabel");
    is2016 = iConfig.getUntrackedParameter<bool>("is2016Label");
    is2017= iConfig.getUntrackedParameter<bool>("is2017Label");
    is2018= iConfig.getUntrackedParameter<bool>("is2018Label");
    isBParking= iConfig.getUntrackedParameter<bool>("isBParkingLabel");
    //is3Mu = iConfig.getUntrackedParameter<bool>("is3MuLabel");
    muons_ = consumes<edm::View<pat::Muon> >  (iConfig.getParameter<edm::InputTag>("muonLabel"));
    vertex_ = consumes<edm::View<reco::Vertex> > (iConfig.getParameter<edm::InputTag>("VertexLabel"));
    //trackToken_ = consumes<edm::View<reco::Track> > (iConfig.getParameter<edm::InputTag>("TracksLabel"));
    //trackToken_ = consumes<std::vector<pat::PackedCandidate> > (iConfig.getParameter<edm::InputTag>("TracksLabel"));
    trackToken_ = consumes<edm::View<pat::PackedCandidate> > (iConfig.getParameter<edm::InputTag>("TracksLabel"));
    genParticles_ = consumes<edm::View<reco::GenParticle>  > (iConfig.getParameter<edm::InputTag>("genParticleLabel"));
    srcCands_ = consumes<std::vector<pat::PackedCandidate> >(edm::InputTag("packedPFCandidates"));
    //Cand3Mu_ = consumes<edm::View<reco::CompositeCandidate> > (iConfig.getParameter<edm::InputTag>("Cand3MuLabel"));
    Cand2Mu1Track_ = consumes<edm::View<reco::CompositeCandidate> > (iConfig.getParameter<edm::InputTag>("Cand2Mu1TrackLabel"));
    DiMuon_ = consumes<edm::View<reco::CompositeCandidate> > (iConfig.getParameter<edm::InputTag>("DiMuonLabel"));
    puToken_ =   consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("pileupSummary"));
    triggerToken_ = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults"));
    //trigeventToken_ = consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("triggerSummary"));
    algToken_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("AlgInputTag"));
    algInputTag_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("AlgInputTag"));
    //theL1TUtmTriggerMenu_ = esConsumes<L1TUtmTriggerMenu,L1TUtmTriggerMenuRcd>(edm::ESInputTag("", "TheL1TUtmTriggerMenu"));
    //gtUtil_ = new l1t::L1TGlobalUtil(iConfig, consumesCollector(), *this, algInputTag_, algInputTag_);
    algTok_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("algInputTag"));
    //extTag_ = consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("extInputTag"));
    //edm::InputTag algTag = iConfig.getParameter<edm::InputTag>("algInputTag");
    //edm::InputTag extTag = iConfig.getParameter<edm::InputTag>("extInputTag");
    gtUtil_ = new l1t::L1TGlobalUtil(iConfig, consumesCollector(), *this, algTag_, extTag_, l1t::UseEventSetupIn::Event);
    token_BeamSpot = consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"));
    l1muonsToken_ = consumes<BXVector<l1t::Muon>>(edm::InputTag("gmtStage2Digis", "Muon"  , "RECO"));
    theTransientTrackBuilder_ = esConsumes<TransientTrackBuilder, TransientTrackRecord>(edm::ESInputTag("", "TransientTrackBuilder"));
    triggerObjects_ = consumes<std::vector<pat::TriggerObjectStandAlone> >(iConfig.getParameter<edm::InputTag>("objects"));
    //tauToken_(consumes(iConfig.getParameter("taus"))),
    //metToken_(consumes(iConfig.getParameter("mets")))
    //tree_(0);
    //MuonPt(0);
}


DileptonInclusiveTreeMaker::~DileptonInclusiveTreeMaker()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
}


float DileptonInclusiveTreeMaker::dR(float eta1, float eta2, float phi1, float phi2){
    float dphi=(phi1-phi2);
    float deta=(eta1-eta2);
    float deltaR= TMath::Sqrt(dphi*dphi + deta*deta);
    return deltaR;
}

float DileptonInclusiveTreeMaker::dRtriggerMatch(pat::Muon m, vector<pat::TriggerObjectStandAlone> triggerObjects) {
    float dRmin = 1.;
    for (unsigned int i = 0 ; i < triggerObjects.size() ; i++) {
        float deltaR = sqrt( reco::deltaR2(triggerObjects[i].eta(), triggerObjects[i].phi(), m.eta(), m.phi()));
        //float deltaR = sqrt( pow(triggerObjects[i].eta() - m.eta(), 2) + pow(acos(cos(triggerObjects[i].phi() - m.phi())), 2));
        if (deltaR < dRmin) dRmin = deltaR;
    }
    return dRmin;
}
    
float DileptonInclusiveTreeMaker::dRtriggerMatchTrk(reco::Track Trk, vector<pat::TriggerObjectStandAlone> triggerObjects) {
    float dRmin = 1.;
    for (unsigned int i = 0 ; i < triggerObjects.size() ; i++) {
        float deltaR = sqrt( reco::deltaR2(triggerObjects[i].eta(), triggerObjects[i].phi(), Trk.eta(), Trk.phi()));
        //float deltaR = sqrt( pow(triggerObjects[i].eta() - m.eta(), 2) + pow(acos(cos(triggerObjects[i].phi() - m.phi())), 2));
        if (deltaR < dRmin) dRmin = deltaR;
    }
    return dRmin;
}
    
bool isGoodTrack(const reco::Track &track) {
    if(track.pt()>1){
        if(std::fabs(track.eta())<2.4){
            if(track.hitPattern().trackerLayersWithMeasurement()>5){
                if(track.hitPattern().pixelLayersWithMeasurement()>1) return true;
            }
        }
    }
    return false;
}

typedef std::pair<const reco::MuonChamberMatch*, const reco::MuonSegmentMatch*> MatchPair;
const MatchPair& DileptonInclusiveTreeMaker::getBetterMatch(const MatchPair& match1, const MatchPair& match2) const{

  if (match2.first->detector() == MuonSubdetId::DT and
      match1.first->detector() != MuonSubdetId::DT)
    return match2;

  if ( abs(match1.first->x - match1.second->x) >
       abs(match2.first->x - match2.second->x) )
    return match2;

  return match1;
}


float DileptonInclusiveTreeMaker::dX(const MatchPair& match) const{
  if (match.first and match.second->hasPhi())
    return (match.first->x - match.second->x);
  else
    return 9999.;
}

float DileptonInclusiveTreeMaker::pullX(const MatchPair& match) const{
  if (match.first and match.second->hasPhi())
    return dX(match) /
      sqrt(pow(match.first->xErr, 2) + pow(match.second->xErr, 2));
  else
    return 9999.;
}

float DileptonInclusiveTreeMaker::pullDxDz(const MatchPair& match) const{
  if (match.first and match.second->hasPhi())
    return (match.first->dXdZ - match.second->dXdZ) /
           sqrt(pow(match.first->dXdZErr, 2) + pow(match.second->dXdZErr, 2));
  else
    return 9999.;
}

float DileptonInclusiveTreeMaker::dY(const MatchPair& match) const{
  if (match.first and match.second->hasZed())
    return (match.first->y - match.second->y);
  else
    return 9999.;
}

float DileptonInclusiveTreeMaker::pullY(const MatchPair& match) const{
  if (match.first and match.second->hasZed())
    return dY(match) /
      sqrt(pow(match.first->yErr, 2) + pow(match.second->yErr, 2));
  else
    return 9999.;
}

float DileptonInclusiveTreeMaker::pullDyDz(const MatchPair& match) const{
  if (match.first and match.second->hasZed())
    return (match.first->dYdZ - match.second->dYdZ) /
           sqrt(pow(match.first->dYdZErr, 2) + pow(match.second->dYdZErr, 2));
  else
    return 9999.;
}

typedef std::map<const reco::Track*, reco::TransientTrack> TransientTrackMap;


// auxiliary function to exclude tracks associated to tau lepton decay "leg"
// from primary event vertex refit
bool tracksMatchByDeltaR(const reco::Track* trk1, const reco::Track* trk2)
{
    if ( reco::deltaR(*trk1, *trk2) < 1.e-2 && trk1->charge() == trk2->charge() ) return true;
    else return false;
}
    
void removeTracks(TransientTrackMap& pvTracks_toRefit, const std::vector<reco::Track*> svTracks)
{
    for ( std::vector<reco::Track*>::const_iterator svTrack = svTracks.begin(); svTrack != svTracks.end(); ++svTrack ){
        //--- remove track from list of tracks included in primary event vertex refit
        //    if track matches by reference or in eta-phi
        //    any of the tracks associated to tau lepton decay "leg"
        for ( TransientTrackMap::iterator pvTrack = pvTracks_toRefit.begin(); pvTrack != pvTracks_toRefit.end(); ++pvTrack ) {
            if ( tracksMatchByDeltaR(pvTrack->first, *svTrack) ) {
                pvTracks_toRefit.erase(pvTrack);
                break;
            }
        }
    }
}
    
bool tracksMatchByDeltaR2(const reco::TransientTrack trk1, const reco::Track* trk2)
{
    //cout<<" pv_t eta="<<trk1.track().eta()<<" sv_t eta="<<trk2->eta()<<" deltaR(tk1, tk2)="<<reco::deltaR(trk1.track(), *trk2)<<endl;                 
    if ( reco::deltaR(trk1.track(), *trk2) < 1.e-2 && trk1.track().charge() == trk2->charge() ) return true;
    else return false;
}


    
void removeTracks3(vector<reco::TransientTrack> &pvTracks, const std::vector<reco::Track*> svTracks)
{
    // cout<<"Inside Remove Tracks: pvtracks="<<pvTracks.size()<<endl;                                                                                  
    for ( std::vector<reco::Track*>::const_iterator svTrack = svTracks.begin(); svTrack != svTracks.end(); ++svTrack ){
        for(uint f=0;f<pvTracks.size(); f++){
            if ( tracksMatchByDeltaR2(pvTracks.at(f), *svTrack) ) {
                //cout<<" track to be erased position: "<<f<<" eta="<<pvTracks.at(f).track().eta()<<endl;                                               
                pvTracks.erase(pvTracks.begin()+f);
                break;
            }
        }
    }
}
    
void DileptonInclusiveTreeMaker::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup, const edm::Event& iEvent) {
    //edm::Handle<edm::TriggerResults> trigResults; //our trigger result object
    //edm::InputTag trigResultsTag("TriggerResults"," ","HLT"); //make sure have correct process on MC
    //iEvent.getByLabel(trigResultsTag,trigResults);
    /*
    bool changed = true;
    if (hltConfig.init(iRun, iSetup, trigResultsTag.process(), changed)) {
        // if init returns TRUE, initialisation has succeeded!
        std::cout << "HLT config with process name "<< trigResultsTag.process() << " successfully extracted"<<std::endl;
    }
    else {
        // if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
        // with the file and/or code and needs to be investigated!
        std::cout << "Error! HLT config extraction with process name " << trigResultsTag.process() << " failed"<<std::endl;
        // In this case, all access methods will return empty values!
    }
   */
}
    
    
    
void
DileptonInclusiveTreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    using namespace std;
    using namespace reco;
    using std::vector;
    
    edm::Handle< edm::View<reco::Vertex> >vertices;
    iEvent.getByToken(vertex_, vertices);
    if (vertices->empty()) return; // skip the event if no PV found
    const reco::Vertex &PV = vertices->front();
    
    edm::Handle< edm::View<pat::Muon> > muons;
    iEvent.getByToken(muons_, muons);

    /*
    edm::Handle<edm::View<reco::CompositeCandidate> > Cand3Mu;
    iEvent.getByToken(Cand3Mu_, Cand3Mu);
    */
    edm::Handle<edm::View<reco::CompositeCandidate> > Cand2Mu1Track;
    iEvent.getByToken(Cand2Mu1Track_, Cand2Mu1Track);

    edm::Handle<edm::View<reco::CompositeCandidate> > DiMuon;
    iEvent.getByToken(DiMuon_, DiMuon);

    edm::Handle< edm::View<reco::GenParticle> > genParticles;
    iEvent.getByToken(genParticles_, genParticles);

    //edm::Handle<edm::View<reco::Track> > trackCollection;
    edm::Handle<edm::View<pat::PackedCandidate> > trackCollection;
    //iEvent.getByToken(trackToken_, trackCollection);
    iEvent.getByToken(trackToken_,trackCollection);

    Handle<TriggerResults> triggerResults;
    iEvent.getByToken(triggerToken_, triggerResults);

    //Handle<trigger::TriggerEvent> triggerSummary;
    //iEvent.getByToken(trigeventToken_, triggerSummary);

    Handle<std::vector<pat::TriggerObjectStandAlone> > triggerObjects;
    iEvent.getByToken(triggerObjects_, triggerObjects);
    
    Handle<BXVector<l1t::Muon> > gmuons;
    iEvent.getByToken(l1muonsToken_, gmuons);

    edm::Handle<std::vector<pat::PackedCandidate> > PFCands;
    iEvent.getByToken(srcCands_,PFCands);
    
    
    ///////////////Fill Trigger Vars, L1 and HLT///////////////

cout << "I'm here L1" << endl;
gtUtil_->retrieveL1(iEvent, iSetup, algTok_);
cout << "I'm here L1 bis" << endl;
const vector<pair<string, bool> > initialDecisions = gtUtil_->decisionsInitial();
const vector<pair<string, bool> > finalDecisions = gtUtil_->decisionsFinal();
const vector<pair<string, double> > PSValues = gtUtil_->prescales();

if(initialDecisions.size() != finalDecisions.size()) 
    cout << "L1 initial and final decisions have different size!" << endl;
if (!iEvent.isRealData())
  {
    //cout<<"sto qua is MC"<<endl;
    for (size_t i_l1t = 0; i_l1t < initialDecisions.size(); i_l1t++)
      {
        string l1tName = (initialDecisions.at(i_l1t)).first;
        //cout<<"l1 name="<<l1tName<<endl;
        if(l1tName.find("DoubleMu") != string::npos || l1tName.find("TripleMu") != string::npos ||  l1tName.find("SingleMu")!= string::npos ){
          //cout<<"l1 name="<<l1tName<<endl;
          Trigger_l1name.push_back( l1tName );
          Trigger_l1Initialdecision.push_back( initialDecisions.at(i_l1t).second );
          Trigger_l1Finaldecision.push_back( finalDecisions.at(i_l1t).second );
          Trigger_l1prescale.push_back( 1 );
        }
      }
  }
else
    {
    //ESHandle<L1TGlobalPrescalesVetos> psAndVetos;
    //auto psRcd = iSetup.tryToGet<L1TGlobalPrescalesVetosRcd>();
    //if(psRcd) psRcd->get(psAndVetos);
    //int columnN= gtUtil_->prescaleColumn();
    for (size_t i_l1t = 0; i_l1t < initialDecisions.size(); i_l1t++) {
      string l1tName = (initialDecisions.at(i_l1t)).first;
      if(l1tName.find("DoubleMu") != string::npos || l1tName.find("TripleMu") != string::npos ||  l1tName.find("SingleMu")!= string::npos){
        //cout<<"L1Seed="<<l1tName<<" decision="<<initialDecisions.at(i_l1t).second<<" prescale="<<(psAndVetos->prescale_table_)[columnN][i_l1t]<<endl;
        Trigger_l1name.push_back( l1tName );
        Trigger_l1Initialdecision.push_back( initialDecisions.at(i_l1t).second );
        Trigger_l1Finaldecision.push_back( finalDecisions.at(i_l1t).second );
        Trigger_l1prescale.push_back( PSValues.at(i_l1t).second );
            }
        }
    }
    
    
const TriggerNames &triggerNames = iEvent.triggerNames( *triggerResults );
for (size_t i_hlt = 0; i_hlt != triggerResults->size(); ++i_hlt){
    string hltName = triggerNames.triggerName(i_hlt);
    
    if(hltName.find("HLT_DoubleMu") != string::npos || hltName.find("HLT_DoubleMu3") != string::npos  || hltName.find("HLT_Mu8_IP") != string::npos || (hltName.find("HLT_Mu7_IP") != string::npos) || (hltName.find("HLT_Mu9_IP") != string::npos) || (hltName.find("HLT_Mu12_IP") != string::npos)  ){
    //if(hltName.find("HLT_DoubleMu") != string::npos  || hltName.find("HLT_Mu8_IP") != string::npos || (hltName.find("HLT_Mu7_IP") != string::npos) || (hltName.find("HLT_Mu9_IP") != string::npos) || (hltName.find("HLT_Mu12_IP") != string::npos)  ){
    //cout<<" HLTPath="<<hltName<<" isPassed="<<triggerResults->accept(i_hlt )<<endl;
      Trigger_hltname.push_back(hltName);
      Trigger_hltdecision.push_back(triggerResults->accept(i_hlt ));
    }
}

vector<pat::TriggerObjectStandAlone> TriggerObj_DsTau3Mu,  TriggerObj_DsTau3Mu2017, TriggerObj_Dimuon, TriggerObj_DimuonIncl, TriggerObj_DimuonIncl_displ;
vector<pat::TriggerObjectStandAlone> MuonsObjects_BPMu7, MuonsObjects_BPMu12_IP6, MuonsObjects_BPMu8, MuonsObjects_BPMu8_IP6,MuonsObjects_BPMu8_IP5,MuonsObjects_BPMu9_IP0, MuonsObjects_BPMu9_IP3, MuonsObjects_BPMu9_IP4, MuonsObjects_BPMu9_IP5, MuonsObjects_BPMu9_IP6;

for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
    obj.unpackPathNames(triggerNames);

    for (unsigned h = 0; h < obj.filterLabels().size(); ++h) {
        if(obj.filterLabels()[h]=="hltdstau3muDisplaced3muFltr"){
            TriggerObj_DsTau3Mu.push_back(obj);
        }
        if(obj.filterLabels()[h]=="hltTau3muTkVertexFilter"){
            TriggerObj_DsTau3Mu2017.push_back(obj);
        }
        
        // Inclusive dimu triggers
        if(obj.filterLabels()[h]=="hltDisplacedmumuFilterDoubleMu43LowMass"){
            TriggerObj_DimuonIncl.push_back(obj);
        }
        if(obj.filterLabels()[h]=="hltDisplacedmumuFilterDoubleMu4LowMassDisplaced"){
            TriggerObj_DimuonIncl_displ.push_back(obj);
        }
        
        if(isBParking){
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered8Q"){
                MuonsObjects_BPMu8.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered7IP4Q"){
                MuonsObjects_BPMu7.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered8IP6Q"){
                MuonsObjects_BPMu8_IP6.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered8IP5Q"){
                MuonsObjects_BPMu8_IP5.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP0Q"){
                MuonsObjects_BPMu9_IP0.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP3Q"){
                MuonsObjects_BPMu9_IP3.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP4Q"){
                MuonsObjects_BPMu9_IP4.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9IP5Q"){
                MuonsObjects_BPMu9_IP5.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered9Q"){
                MuonsObjects_BPMu9_IP6.push_back(obj);
            }
            if(obj.filterLabels()[h]=="hltL3fL1sMu22OrParkL1f0L2f10QL3Filtered12Q"){
                MuonsObjects_BPMu12_IP6.push_back(obj);
            }
        }//isBParking
    }//loop on filterLabels
}

for(uint t=0; t<TriggerObj_DsTau3Mu.size();t++){
    MuonPt_HLT.push_back(TriggerObj_DsTau3Mu.at(t).pt());
    MuonEta_HLT.push_back(TriggerObj_DsTau3Mu.at(t).eta());
    MuonPhi_HLT.push_back(TriggerObj_DsTau3Mu.at(t).phi());
}

for(uint t=0; t<TriggerObj_DsTau3Mu2017.size();t++){
    MuonPt_HLT2017.push_back(TriggerObj_DsTau3Mu2017.at(t).pt());
    MuonEta_HLT2017.push_back(TriggerObj_DsTau3Mu2017.at(t).eta());
    MuonPhi_HLT2017.push_back(TriggerObj_DsTau3Mu2017.at(t).phi());
}
    
    // Trigger matching inclusive dimu triggers
    for(uint t=0; t<TriggerObj_DimuonIncl.size();t++){
        MuonPt_HLT_DiMu_Incl.push_back(TriggerObj_DimuonIncl.at(t).pt());
        MuonEta_HLT_DiMu_Incl.push_back(TriggerObj_DimuonIncl.at(t).eta());
        MuonPhi_HLT_DiMu_Incl.push_back(TriggerObj_DimuonIncl.at(t).phi());
    }
    for(uint t=0; t<TriggerObj_DimuonIncl_displ.size();t++){
        MuonPt_HLT_DiMu_Incl_displ.push_back(TriggerObj_DimuonIncl_displ.at(t).pt());
        MuonEta_HLT_DiMu_Incl_displ.push_back(TriggerObj_DimuonIncl_displ.at(t).eta());
        MuonPhi_HLT_DiMu_Incl_displ.push_back(TriggerObj_DimuonIncl_displ.at(t).phi());
    }
    //

if(isBParking){
    for(uint t=0; t<MuonsObjects_BPMu8.size();t++){
        MuonPt_HLT_BPMu8.push_back(MuonsObjects_BPMu8.at(t).pt());
        MuonEta_HLT_BPMu8.push_back(MuonsObjects_BPMu8.at(t).eta());
        MuonPhi_HLT_BPMu8.push_back(MuonsObjects_BPMu8.at(t).phi());
    }
    for(uint t=0; t<MuonsObjects_BPMu7.size();t++){
        MuonPt_HLT_BPMu7.push_back(MuonsObjects_BPMu7.at(t).pt());
        MuonEta_HLT_BPMu7.push_back(MuonsObjects_BPMu7.at(t).eta());
        MuonPhi_HLT_BPMu7.push_back(MuonsObjects_BPMu7.at(t).phi());
    }
    for(uint t=0; t<MuonsObjects_BPMu8_IP6.size();t++){
        MuonPt_HLT_BPMu8_IP6.push_back(MuonsObjects_BPMu8_IP6.at(t).pt());
        MuonEta_HLT_BPMu8_IP6.push_back(MuonsObjects_BPMu8_IP6.at(t).eta());
        MuonPhi_HLT_BPMu8_IP6.push_back(MuonsObjects_BPMu8_IP6.at(t).phi());
    }
    for(uint t=0; t<MuonsObjects_BPMu8_IP5.size();t++){
        MuonPt_HLT_BPMu8_IP5.push_back(MuonsObjects_BPMu8_IP5.at(t).pt());
        MuonEta_HLT_BPMu8_IP5.push_back(MuonsObjects_BPMu8_IP5.at(t).eta());
        MuonPhi_HLT_BPMu8_IP5.push_back(MuonsObjects_BPMu8_IP5.at(t).phi());
    }
    for(uint t=0; t<MuonsObjects_BPMu9_IP0.size();t++){
        MuonPt_HLT_BPMu9_IP0.push_back(MuonsObjects_BPMu9_IP0.at(t).pt());
        MuonEta_HLT_BPMu9_IP0.push_back(MuonsObjects_BPMu9_IP0.at(t).eta());
        MuonPhi_HLT_BPMu9_IP0.push_back(MuonsObjects_BPMu9_IP0.at(t).phi());
    }
    for(uint t=0; t< MuonsObjects_BPMu9_IP3.size();t++){
        MuonPt_HLT_BPMu9_IP3.push_back(MuonsObjects_BPMu9_IP3.at(t).pt());
        MuonEta_HLT_BPMu9_IP3.push_back(MuonsObjects_BPMu9_IP3.at(t).eta());
        MuonPhi_HLT_BPMu9_IP3.push_back(MuonsObjects_BPMu9_IP3.at(t).phi());
    }
    for(uint t=0; t< MuonsObjects_BPMu9_IP4.size();t++){
        MuonPt_HLT_BPMu9_IP4.push_back(MuonsObjects_BPMu9_IP4.at(t).pt());
        MuonEta_HLT_BPMu9_IP4.push_back(MuonsObjects_BPMu9_IP4.at(t).eta());
        MuonPhi_HLT_BPMu9_IP4.push_back(MuonsObjects_BPMu9_IP4.at(t).phi());
    }
    for(uint t=0; t< MuonsObjects_BPMu9_IP5.size();t++){
        MuonPt_HLT_BPMu9_IP5.push_back(MuonsObjects_BPMu9_IP5.at(t).pt());
        MuonEta_HLT_BPMu9_IP5.push_back(MuonsObjects_BPMu9_IP5.at(t).eta());
        MuonPhi_HLT_BPMu9_IP5.push_back(MuonsObjects_BPMu9_IP5.at(t).phi());
    }
    for(uint t=0; t< MuonsObjects_BPMu9_IP6.size();t++){
        MuonPt_HLT_BPMu9_IP6.push_back(MuonsObjects_BPMu9_IP6.at(t).pt());
        MuonEta_HLT_BPMu9_IP6.push_back(MuonsObjects_BPMu9_IP6.at(t).eta());
        MuonPhi_HLT_BPMu9_IP6.push_back(MuonsObjects_BPMu9_IP6.at(t).phi());
    }
    for(uint t=0; t< MuonsObjects_BPMu12_IP6.size();t++){
        MuonPt_HLT_BPMu12_IP6.push_back(MuonsObjects_BPMu12_IP6.at(t).pt());
        MuonEta_HLT_BPMu12_IP6.push_back(MuonsObjects_BPMu12_IP6.at(t).eta());
        MuonPhi_HLT_BPMu12_IP6.push_back(MuonsObjects_BPMu12_IP6.at(t).phi());
    }
}//isBParking


    ///////////////Fill GEN particles///////////////
    if(isMc){
        uint j=0;
        uint ngenP=genParticles->size();
        //cout<<"****************GenLevel Info Begin********************"<<endl;
        for(edm::View<reco::GenParticle>::const_iterator gp=genParticles->begin(); gp!=genParticles->end(), j<ngenP; ++gp , ++j){
            //if(fabs(gp->pdgId())==15) tauRaw = j;
            int isDs = -1; //-1:not Ds //0:is not prompt Ds//1:is prompt pp->Ds//2:is D from B decays
            int isB = -1; //-1:not B //0:is not prompt B//1:is prompt B
            int isBdecay = -1; //-1:not B //0:isB //1: is B to Ds//2: is B to anything else
            if( fabs(gp->pdgId()) == 511 || fabs(gp->pdgId()) == 521 || fabs(gp->pdgId()) == 531 ) { //B0 or B+ or Bs found
                //cout<<"B meson"<<endl;
                isB=0;
                isBdecay=0;
                for(uint t=0; t<gp->numberOfMothers(); t++) {
                    cout<<"  gp->mother("<<t<<")->pdgId() = "<<gp->mother(t)->pdgId()<<endl;
                    if( fabs(gp->mother(t)->pdgId()) == 513 || fabs(gp->mother(t)->pdgId()) == 523 || fabs(gp->mother(t)->pdgId()) == 533 || fabs(gp->mother(t)->pdgId()) == 535 ) { //B*
                        for(uint i=0; i<gp->mother(t)->numberOfMothers(); i++) {
                            //cout<<"    gp->mother("<<t<<")->mother("<<i<<")->pdgId() = "<<gp->mother(t)->mother(i)->pdgId()<<endl;
                            if(fabs(gp->mother(t)->mother(i)->pdgId())==5) { //b quark
                                //cout<<"    prompt"<<endl;
                                isB=1;
                            }
                        }
                    }else{
                        if(fabs(gp->mother(t)->pdgId()) == 5){ //b quark
                            //cout<<"    prompt"<<endl;
                            isB=1;
                        }
                    }
                } 
                //cout<<"B->"<<endl;
                for(uint b=0; b<gp->numberOfDaughters(); b++) {
                    if ( fabs(gp->daughter(b)->pdgId()) == 431 || fabs(gp->daughter(b)->pdgId()) == 433 || fabs(gp->daughter(b)->pdgId()) == 435 ) {
                        //cout<<"   Ds"<<endl;
                        isBdecay=1;
                    }else isBdecay=2;
                }
            }
            if ( fabs(gp->pdgId()) == 431 ) { //Ds
               //cout<<"D_s meson"<<endl;
               isDs=0;
               for(uint t=0; t<gp->numberOfMothers(); t++) {
                   //cout<<"  gp->mother("<<t<<")->pdgId() = "<<gp->mother(t)->pdgId()<<endl;
                   if( fabs(gp->mother(t)->pdgId()) == 433 || fabs(gp->mother(t)->pdgId()) == 435 ) { //D*
                       for(uint i=0; i<gp->mother(t)->numberOfMothers(); i++) {
                           //cout<<"    gp->mother("<<t<<")->mother("<<i<<")->pdgId() = "<<gp->mother(t)->mother(i)->pdgId()<<endl;
                           if(fabs(gp->mother(t)->mother(i)->pdgId())==3 || fabs(gp->mother(t)->mother(i)->pdgId())==4) { //s or c quark
                             cout<<"    prompt"<<endl;
                             isDs=1;
                           }else{
                             if(fabs(gp->mother(t)->mother(i)->pdgId())==521 || fabs(gp->mother(t)->mother(i)->pdgId())==511 || fabs(gp->mother(t)->mother(i)->pdgId())==531) {
                                cout<<"    from B decay"<<endl;
                                isDs=2;
                             }
                          }
                       }
                   }else{
                      if(fabs(gp->mother(t)->pdgId())==3 || fabs(gp->mother(t)->pdgId())==4) { //s or c quark
                         cout<<"    prompt"<<endl;
                         isDs=1;
                      }else{
                         if(fabs(gp->mother(t)->pdgId())==521 || fabs(gp->mother(t)->pdgId())==511 || fabs(gp->mother(t)->pdgId())==531 ){
                            cout<<"    from B decay"<<endl;
                            isDs=2;
                         }
                      }
                   }
               }
            }

            if(fabs(gp->pdgId())==13 || fabs(gp->pdgId())==15  || fabs(gp->pdgId())==11 || fabs(gp->pdgId())==211 || fabs(gp->pdgId())==321 ||  fabs(gp->pdgId())==12  || fabs(gp->pdgId())==14 || fabs(gp->pdgId())==16 || fabs(gp->pdgId())==431 || fabs(gp->pdgId())==333 || fabs(gp->pdgId())==511 || fabs(gp->pdgId())==521) {
                GenParticle_PdgId.push_back(gp->pdgId());
                GenParticle_Pt.push_back(gp->pt());
                GenParticle_Eta.push_back(gp->eta());
                GenParticle_Phi.push_back(gp->phi());
                GenParticle_isDs.push_back(isDs);
                GenParticle_isB.push_back(isB);
                GenParticle_isBdecay.push_back(isBdecay);

                //if(fabs(gp->pdgId())==13 && gp->numberOfMothers() && fabs(gp->mother(0)->pdgId()) ==333 ){
                //    cout<<"Mu from phi pt="<<gp->pt()<<" vz="<<gp->vz()<<endl;
                //}
                if (gp->numberOfMothers()) {GenParticle_MotherPdgId.push_back(gp->mother(0)->pdgId());
                }else{ GenParticle_MotherPdgId.push_back(-99); }
            }
        }//loop genParticle
    }//isMC

    PVCollection_Size = vertices->size();
    uint kk=0;
    std::vector<uint> VtxIdV;
    cout<<"Number of PFCands="<<PFCands->size()<<endl;
    std::vector<uint> SelectedCandIdx;
    vector<pat::PackedCandidate> MyPFCands;
    for (std::vector<pat::PackedCandidate>::const_iterator cand = PFCands->begin(); cand != PFCands->end(), kk!= PFCands->size(); ++cand, ++kk) {
        if (cand->charge()==0) continue;
        if (cand->vertexRef().isNull()) continue;
        if (!(cand->hasTrackDetails()) ) continue;

       int key = cand->vertexRef().key();
       int quality = cand->pvAssociationQuality();
       if(cand->fromPV(cand->vertexRef().key())<2) continue;
       if( cand->fromPV(cand->vertexRef().key())==2 && quality != pat::PackedCandidate::UsedInFitLoose  ) continue;
       VtxIdV.push_back(key);
       SelectedCandIdx.push_back(kk);
       MyPFCands.push_back(*cand);
    }// loop over the PFCandidates




 
    //cout<<"***Number of triplets before selection="<<TripletCollectionSize2<<" after sel="<<SelectedTripletsSize<<endl;
    //cout<<"***Number of Muons="<<muons->size()<<endl;

    uint k=0;
    std::vector<int> MuFilter;
    vector<pat::Muon> MyMu, MyMu2, SyncMu;
    MuonCollectionSize = muons->size();
    
    for(edm::View<pat::Muon>::const_iterator mu=muons->begin(); mu!=muons->end(), k<muons->size(); ++mu, ++k){
        
        MuFilter.push_back(1);
        MyMu.push_back(*mu);
        
        //Basic Kinematics
        MuonPt.push_back(mu->pt());
        MuonEta.push_back(mu->eta());
        MuonPhi.push_back(mu->phi());
        MuonEnergy.push_back(mu->energy());
        MuonCharge.push_back(mu->charge());
        
        Muon_PdgId.push_back(mu->simPdgId());
        Muon_MotherPdgId.push_back(mu->simMotherPdgId());
        Muon_simFlavour.push_back(mu->simFlavour());
        //Vtx position
        Muon_vx.push_back(mu->vx());
        Muon_vy.push_back(mu->vy());
        Muon_vz.push_back(mu->vz());
        
        //MuonID
        Muon_isGlobal.push_back(mu->isGlobalMuon());
        //Muon_isTracker.push_back(mu->isTrackerMuon());
        Muon_isSoft.push_back(mu->isSoftMuon(PV));
        Muon_isLoose.push_back(mu->isLooseMuon());
        Muon_isMedium.push_back(mu->isMediumMuon());
        Muon_isPF.push_back(mu->isPFMuon());
        Muon_isRPCMuon.push_back(mu->isRPCMuon());
        Muon_isStandAloneMuon.push_back(mu->isStandAloneMuon());
        Muon_isTrackerMuon.push_back(mu->isTrackerMuon());
        Muon_isCaloMuon.push_back(mu->isCaloMuon());
        Muon_isQualityValid.push_back(mu->isQualityValid());
        Muon_isTimeValid.push_back(mu->isTimeValid());
        Muon_isIsolationValid.push_back(mu->isIsolationValid());
        Muon_numberOfMatchedStations.push_back(mu->numberOfMatchedStations());
        Muon_numberOfMatches.push_back(mu->numberOfMatches(reco::Muon::SegmentArbitration));
        Muon_SoftMVA_Val.push_back(mu->softMvaValue());
        
        Muon_timeAtIpInOut.push_back(mu->time().timeAtIpInOut);
        Muon_timeAtIpInOutErr.push_back(mu->time().timeAtIpInOutErr);
        
        std::vector<int> fvDThits{0, 0, 0, 0};
        std::vector<int> fvRPChits{0, 0, 0, 0};
        std::vector<int> fvCSChits{0, 0, 0, 0};

        float kVMuonHitComb = 0;
        if (mu->isGlobalMuon()) {
            reco::TrackRef gTrack = mu->globalTrack();
            const reco::HitPattern& gMpattern = gTrack->hitPattern();
            for (int i = 0; i < gMpattern.numberOfAllHits(reco::HitPattern::TRACK_HITS); i++) {
                uint32_t hit = gMpattern.getHitPattern(reco::HitPattern::TRACK_HITS, i);
                if (!gMpattern.validHitFilter(hit)) continue;
                int muStation0 = gMpattern.getMuonStation(hit) - 1;
                if (muStation0 >= 0 && muStation0 < 4) {
                    if(gMpattern.muonDTHitFilter(hit)) fvDThits[muStation0]++;
                    if(gMpattern.muonRPCHitFilter(hit)) fvRPChits[muStation0]++;
                    if(gMpattern.muonCSCHitFilter(hit)) fvCSChits[muStation0]++;
                }
            }

            for (unsigned int station = 0; station < 4; ++station) {
                kVMuonHitComb += (fvDThits[station]) / 2.;
                kVMuonHitComb += fvRPChits[station];
                if (fvCSChits[station] > 6) {
                    kVMuonHitComb += 6;
                }else{ kVMuonHitComb += fvCSChits[station]; }
            }
            Muon_validMuonHitComb.push_back(kVMuonHitComb);
        }else{ Muon_validMuonHitComb.push_back(-99); }

        if (mu->isGlobalMuon()) {
            Muon_GLnormChi2.push_back(mu->globalTrack()->normalizedChi2());
            Muon_GLhitPattern_numberOfValidMuonHits.push_back(mu->globalTrack()->hitPattern().numberOfValidMuonHits());
        }else{
            Muon_GLnormChi2.push_back(-999);
            Muon_GLhitPattern_numberOfValidMuonHits.push_back(-999);
        }
        
        if (mu->innerTrack().isNonnull()){
            Muon_trackerLayersWithMeasurement.push_back(mu->innerTrack()->hitPattern().trackerLayersWithMeasurement());
            bool ishighq = mu->innerTrack()->quality(reco::Track::highPurity);
            Muon_innerTrack_highPurity.push_back(ishighq);
            Muon_Numberofvalidpixelhits.push_back(mu->innerTrack()->hitPattern().numberOfValidPixelHits());
            Muon_innerTrack_ValidFraction.push_back( mu->innerTrack()->validFraction() );
            Muon_Numberofvalidtrackerhits.push_back(mu->innerTrack()->hitPattern().numberOfValidTrackerHits());
            Muon_innerTrack_p.push_back(mu->innerTrack()->p());
            Muon_innerTrack_eta.push_back(mu->innerTrack()->eta());
            Muon_innerTrack_phi.push_back(mu->innerTrack()->phi());
            Muon_innerTrack_normalizedChi2.push_back(mu->innerTrack()->normalizedChi2());
            Muon_innerTrack_nLostHitsInner.push_back(mu->innerTrack()->hitPattern().numberOfLostTrackerHits(reco::HitPattern::MISSING_INNER_HITS));
            Muon_innerTrack_nLostHitsOuter.push_back(mu->innerTrack()->hitPattern().numberOfLostTrackerHits(reco::HitPattern::MISSING_OUTER_HITS));
            Muon_innerTrack_nPixels.push_back(mu->innerTrack()->hitPattern().numberOfValidPixelHits());
            Muon_innerTrack_nValidHits.push_back(mu->innerTrack()->hitPattern().numberOfValidTrackerHits());
            Muon_innerTrack_nLostHitsOn.push_back(mu->innerTrack()->hitPattern().numberOfLostTrackerHits(reco::HitPattern::TRACK_HITS));
        }else{
            Muon_innerTrack_ValidFraction.push_back( -99);
            Muon_innerTrack_highPurity.push_back( -99);
            Muon_trackerLayersWithMeasurement.push_back(-999);
            Muon_Numberofvalidpixelhits.push_back(-999);
            Muon_Numberofvalidtrackerhits.push_back(-999);
            Muon_trackerLayersWithMeasurement.push_back(-999);
            Muon_innerTrack_p.push_back(-999);
            Muon_innerTrack_eta.push_back(-999);
            Muon_innerTrack_phi.push_back(-999);
            Muon_innerTrack_normalizedChi2.push_back(-999);
            Muon_innerTrack_nLostHitsInner.push_back(-99);
            Muon_innerTrack_nLostHitsOuter.push_back(-99);
            Muon_innerTrack_nPixels.push_back(-99);
            Muon_innerTrack_nValidHits.push_back(-99);
            Muon_innerTrack_nLostHitsOn.push_back(-99);
        }
        if (mu->outerTrack().isNonnull()){
            Muon_outerTrack_p.push_back(mu->outerTrack()->p());
            Muon_outerTrack_eta.push_back(mu->outerTrack()->eta());
            Muon_outerTrack_phi.push_back(mu->outerTrack()->phi());
            Muon_outerTrack_normalizedChi2.push_back(mu->outerTrack()->normalizedChi2());
            Muon_outerTrack_muonStationsWithValidHits.push_back(mu->outerTrack()->hitPattern().muonStationsWithValidHits());
        }else{
            Muon_outerTrack_p.push_back(-999);
            Muon_outerTrack_eta.push_back(-999);
            Muon_outerTrack_phi.push_back(-999);
            Muon_outerTrack_normalizedChi2.push_back(-999);
            Muon_outerTrack_muonStationsWithValidHits.push_back(-999);
        }
        if (mu->innerTrack().isNonnull() && mu->outerTrack().isNonnull()){
            Muon_QInnerOuter.push_back(mu->outerTrack()->charge()*mu->innerTrack()->charge());
        }else{ Muon_QInnerOuter.push_back(-999); }
        
        Muon_combinedQuality_updatedSta.push_back(mu->combinedQuality().updatedSta);
        Muon_combinedQuality_trkKink.push_back(mu->combinedQuality().trkKink);
        Muon_combinedQuality_glbKink.push_back(mu->combinedQuality().glbKink);
        Muon_combinedQuality_trkRelChi2.push_back(mu->combinedQuality().trkRelChi2);
        Muon_combinedQuality_staRelChi2.push_back(mu->combinedQuality().staRelChi2);
        Muon_combinedQuality_chi2LocalPosition.push_back(mu->combinedQuality().chi2LocalPosition);
        Muon_combinedQuality_chi2LocalMomentum.push_back(mu->combinedQuality().chi2LocalMomentum);
        Muon_combinedQuality_localDistance.push_back(mu->combinedQuality().localDistance);
        Muon_combinedQuality_globalDeltaEtaPhi.push_back(mu->combinedQuality().globalDeltaEtaPhi);
        Muon_combinedQuality_tightMatch.push_back(mu->combinedQuality().tightMatch);
        Muon_combinedQuality_glbTrackProbability.push_back(mu->combinedQuality().glbTrackProbability);
        
        Muon_segmentCompatibility.push_back(muon::segmentCompatibility(*mu));
        
         // do matching magic
        const int n_stations = 2;
        std::vector<MatchPair> matches;
        for (unsigned int i=0; i < n_stations; ++i)
            matches.push_back(std::pair(nullptr, nullptr));
        
        for (auto& chamberMatch : mu->matches()){
            unsigned int station = chamberMatch.station() - 1;
            if (station >= n_stations) continue;
        
            for (auto& segmentMatch : chamberMatch.segmentMatches){
              if ( not segmentMatch.isMask(reco::MuonSegmentMatch::BestInStationByDR) ||
        	   not segmentMatch.isMask(reco::MuonSegmentMatch::BelongsToTrackByDR) )
        	continue;
        
        
            auto match_pair = MatchPair(&chamberMatch, &segmentMatch);
              
            if (matches[station].first)
        	    matches[station] = getBetterMatch(matches[station], match_pair);
            else
        	    matches[station] = match_pair;
            }
        }
        
        
        Muon_combinedQuality_match1_dX.push_back(dX(matches[0]));
        Muon_combinedQuality_match1_pullX.push_back(pullX(matches[0]));
        Muon_combinedQuality_match1_pullDxDz.push_back(pullDxDz(matches[0]));
        Muon_combinedQuality_match1_dY.push_back(dY(matches[0]));
        Muon_combinedQuality_match1_pullY.push_back(pullY(matches[0]));
        Muon_combinedQuality_match1_pullDyDz.push_back(pullDyDz(matches[0]));
        
        Muon_combinedQuality_match2_dX.push_back(dX(matches[1]));
        Muon_combinedQuality_match2_pullX.push_back(pullX(matches[1]));
        Muon_combinedQuality_match2_pullDxDz.push_back(pullDxDz(matches[1]));
        Muon_combinedQuality_match2_dY.push_back(dY(matches[1]));
        Muon_combinedQuality_match2_pullY.push_back(pullY(matches[1]));
        Muon_combinedQuality_match2_pullDyDz.push_back(pullDyDz(matches[1]));
}
  
    

    if (!iEvent.isRealData()){
        Handle<vector<PileupSummaryInfo> >  PupInfo;
        iEvent.getByToken(puToken_, PupInfo);
        puN = PupInfo->begin()->getTrueNumInteractions();
    }
  
    ////Synch Tree//////
    /*
    double maxPt =0; double maxPhi=0, maxEta=0; vector<pat::Muon> SyncSortedMu ;
    double maxTrPt =0; double maxTrPhi=0, maxTrEta=0; vector<reco::Track> SyncSortedTr ;
    for(uint i=0; i<SyncMu.size();i++){
        if(SyncMu.at(i).pt() > maxPt){
            maxPt  = SyncMu.at(i).pt();
            maxPhi = SyncMu.at(i).phi();
            maxEta = SyncMu.at(i).eta();
            SyncSortedMu.push_back(SyncMu.at(i));
        }
    }
    
    allmuons_pt.push_back(AllMuPt);
    
    leadmuon_pt.push_back(maxPt);
    leadmuon_eta.push_back(maxEta);
    leadmuon_phi.push_back(maxPhi);
    nmuons = SyncMu.size();
    nprimevtxs =vertices->size();
    
    edm::View<reco::Track>::const_iterator trIt  = trackCollection->begin();
    edm::View<reco::Track>::const_iterator trEnd = trackCollection->end();
    
    double AllTrPt=0;
    for (; trIt != trEnd; ++trIt){
        const reco::Track track = (*trIt);
        if(  (track.pt()>1) && (fabs(track.eta())<2.4) && (track.hitPattern().trackerLayersWithMeasurement()>5) && (track.hitPattern().pixelLayersWithMeasurement()>1)  ){
            AllTrPt +=trIt->pt();
            if(track.pt() > maxTrPt){
                maxTrPt = track.pt();
                maxTrEta = track.eta();
                maxTrPhi= track.phi();
            }
        }
    }
    
    alltracks_pt.push_back(AllTrPt);
    leadtrack_pt.push_back(maxTrPt);
    leadtrack_eta.push_back(maxTrEta);
    leadtrack_phi.push_back(maxTrPhi);
    */
    ///////SyncTree
    
    evt   = iEvent.id().event();
    run = iEvent.id().run();
    lumi = iEvent.luminosityBlock();
    reco::BeamSpot beamSpot;
    edm::Handle<reco::BeamSpot> beamSpotHandle;
    iEvent.getByToken(token_BeamSpot, beamSpotHandle);
    const reco::BeamSpot& beamspot = *beamSpotHandle.product();
    
    if ( beamSpotHandle.isValid() ) {
        beamSpot = *beamSpotHandle;
        x_bs = beamSpot.x0();
        y_bs = beamSpot.y0();
        z_bs = beamSpot.z0();
    } else {
        cout << "No beam spot available from EventSetup \n" << endl;
    }
    
    //  SyncTree_->Fill();
    tree_->Fill();
    
    /*
    allmuons_pt.clear();
    alltracks_pt.clear();
    leadmuon_pt.clear();
    leadmuon_phi.clear();
    leadmuon_eta.clear();
    allmuons_pt.clear();
    leadtrack_pt.clear();
    leadtrack_eta.clear();
    leadtrack_phi.clear();
    nmuons = -999;
    */
    run= -999;
    evt= -999;
    lumi= -999;
    puN= -999;
    
    NGoodTriplets.clear();
    GenParticle_PdgId.clear();
    GenParticle_Pt.clear();
    GenParticle_Eta.clear();
    GenParticle_Phi.clear();
    GenParticle_isDs.clear();
    GenParticle_isB.clear();
    GenParticle_isBdecay.clear();
    GenParticle_MotherPdgId.clear();
    
    MuonCollectionSize =0;
    MuonPt.clear();
    MuonEta.clear();
    MuonPhi.clear();
    
    Muon_PdgId.clear();
    Muon_MotherPdgId.clear();
    Muon_simFlavour.clear();
    MuonEnergy.clear();
    MuonCharge.clear();
    
    //Vtx position
    Muon_vx.clear();
    Muon_vy.clear();
    Muon_vz.clear();
    
    //MuonID
    Muon_isGlobal.clear();
    Muon_isSoft.clear();
    Muon_isLoose.clear();
    Muon_isMedium.clear();
    Muon_isPF.clear();
    Muon_isRPCMuon.clear();
    Muon_isStandAloneMuon.clear();
    Muon_isTrackerMuon.clear();
    Muon_isCaloMuon.clear();
    Muon_isQualityValid.clear();
    Muon_isTimeValid.clear();
    Muon_isIsolationValid.clear();
    Muon_numberOfMatchedStations.clear();
    Muon_numberOfMatches.clear();
    Muon_SoftMVA_Val.clear();
    
    //MuonTime
    Muon_timeAtIpInOut.clear();
    Muon_timeAtIpInOutErr.clear();
    
    //Muon inner + outer track
    Muon_GLnormChi2.clear();
    Muon_GLhitPattern_numberOfValidMuonHits.clear();
    
    Muon_trackerLayersWithMeasurement.clear();
    Muon_Numberofvalidpixelhits.clear();
    
    Muon_validMuonHitComb.clear();
    Muon_innerTrack_ValidFraction.clear();
    Muon_Numberofvalidtrackerhits.clear();
    Muon_innerTrack_highPurity.clear();
    Muon_innerTrack_nLostHitsInner.clear();
    Muon_innerTrack_nLostHitsOuter.clear();
    Muon_innerTrack_nPixels.clear();
    Muon_innerTrack_nValidHits.clear();
    Muon_innerTrack_nLostHitsOn.clear();
    
    Muon_outerTrack_p.clear();
    Muon_outerTrack_eta.clear();
    Muon_outerTrack_phi.clear();
    Muon_outerTrack_normalizedChi2.clear();
    Muon_outerTrack_muonStationsWithValidHits.clear();
    Muon_innerTrack_p.clear();
    Muon_innerTrack_eta.clear();
    Muon_innerTrack_phi.clear();
    Muon_innerTrack_normalizedChi2.clear();
    Muon_QInnerOuter.clear();
    
    Muon_combinedQuality_updatedSta.clear();
    Muon_combinedQuality_trkKink.clear();
    Muon_combinedQuality_glbKink.clear();
    Muon_combinedQuality_trkRelChi2.clear();
    Muon_combinedQuality_staRelChi2.clear();
    Muon_combinedQuality_chi2LocalPosition.clear();
    Muon_combinedQuality_chi2LocalMomentum.clear();
    Muon_combinedQuality_localDistance.clear();
    Muon_combinedQuality_globalDeltaEtaPhi.clear();
    Muon_combinedQuality_tightMatch.clear();
    Muon_combinedQuality_glbTrackProbability.clear();
    
    Muon_combinedQuality_match1_dX.clear();
    Muon_combinedQuality_match1_pullX.clear();
    Muon_combinedQuality_match1_pullDxDz.clear();
    Muon_combinedQuality_match1_dY.clear();
    Muon_combinedQuality_match1_pullY.clear();
    Muon_combinedQuality_match1_pullDyDz.clear();
    
    Muon_combinedQuality_match2_dX.clear();
    Muon_combinedQuality_match2_pullX.clear();
    Muon_combinedQuality_match2_pullDxDz.clear();
    Muon_combinedQuality_match2_dY.clear();
    Muon_combinedQuality_match2_pullY.clear();
    Muon_combinedQuality_match2_pullDyDz.clear();
    
    Muon_segmentCompatibility.clear();
    

     Trigger_hltname.clear();
    Trigger_hltdecision.clear();
    NGoodTriplets.clear();
    Triplet_relativeiso2.clear();

    MuonPt_HLT.clear();
    MuonEta_HLT.clear();
    MuonPhi_HLT.clear();
    
    MuonPt_HLT_DiMu_Incl.clear();
    MuonEta_HLT_DiMu_Incl.clear();
    MuonPhi_HLT_DiMu_Incl.clear();
    MuonPt_HLT_DiMu_Incl_displ.clear();
    MuonEta_HLT_DiMu_Incl_displ.clear();
    MuonPhi_HLT_DiMu_Incl_displ.clear();

    MuonPt_HLT2017.clear();
    MuonEta_HLT2017.clear();
    MuonPhi_HLT2017.clear();
    MuonPt_HLT_BPMu7.clear();
    MuonEta_HLT_BPMu7.clear();
    MuonPhi_HLT_BPMu7.clear();
    MuonPt_HLT_BPMu8.clear();
    MuonEta_HLT_BPMu8.clear();
    MuonPhi_HLT_BPMu8.clear();
    MuonPt_HLT_BPMu8_IP6.clear();
    MuonEta_HLT_BPMu8_IP6.clear();
    MuonPhi_HLT_BPMu8_IP6.clear();
    MuonPt_HLT_BPMu8_IP5.clear();
    MuonEta_HLT_BPMu8_IP5.clear();
    MuonPhi_HLT_BPMu8_IP5.clear();
    MuonPt_HLT_BPMu9_IP0.clear();
    MuonEta_HLT_BPMu9_IP0.clear();
    MuonPhi_HLT_BPMu9_IP0.clear();
    MuonPt_HLT_BPMu9_IP3.clear();
    MuonEta_HLT_BPMu9_IP3.clear();
    MuonPhi_HLT_BPMu9_IP3.clear();
    MuonPt_HLT_BPMu9_IP4.clear();
    MuonEta_HLT_BPMu9_IP4.clear();
    MuonPhi_HLT_BPMu9_IP4.clear();
    MuonPt_HLT_BPMu9_IP5.clear();
    MuonEta_HLT_BPMu9_IP5.clear();
    MuonPhi_HLT_BPMu9_IP5.clear();
    MuonPt_HLT_BPMu9_IP6.clear();
    MuonEta_HLT_BPMu9_IP6.clear();
    MuonPhi_HLT_BPMu9_IP6.clear();
    MuonPt_HLT_BPMu12_IP6.clear();
    MuonEta_HLT_BPMu12_IP6.clear();
    MuonPhi_HLT_BPMu12_IP6.clear();
    
    DistXY_PVSV.clear();
    DistXY_significance_PVSV.clear();
    Triplet_IsoMu1.clear();
    Triplet_IsoMu2.clear();
    Triplet_IsoMu3.clear();
    FlightDistBS_SV.clear();
    FlightDistBS_SV_Err.clear();
    FlightDistBS_SV_Significance.clear();
    
    Mu1_IsGlobal.clear();
    Mu2_IsGlobal.clear();
    Mu3_IsGlobal.clear();

    Mu1_IsPF.clear();
    Mu2_IsPF.clear();
    Mu3_IsPF.clear();
    
    L1Muon_Pt.clear();
    L1Muon_Eta.clear();
    L1Muon_Phi.clear();
    L1Muon_EtaAtVtx.clear();
    L1Muon_PhiAtVtx.clear();
    L1Muon_BX.clear();
    L1Muon_Quality.clear();
    L1Muon_ChargeValid.clear();
    L1Muon_Charge.clear();
    L1Muon_TfMuonIndex.clear();
    L1Muon_rank.clear();
    L1Muon_isoSum.clear();

    BS_x.clear();
    BS_y.clear();
    BS_z.clear();


}
    
// ------------ method called once each job just before starting event loop  ------------
void DileptonInclusiveTreeMaker::beginJob() {

    hEvents = fs->make<TH1F>("hEvents","hEvents",10,0,10);
    tree_ = fs->make<TTree>("ntuple","LFVTau ntuple");
    
    tree_->Branch("evt", &evt);
    tree_->Branch("run", &run);
    tree_->Branch("lumi", &lumi);
    tree_->Branch("nPileUpInt", &puN);
    
    tree_->Branch("x_bs", &x_bs);
    tree_->Branch("y_bs", &y_bs);
    tree_->Branch("z_bs", &z_bs);
    
    tree_->Branch("GenParticle_PdgId", &GenParticle_PdgId);
    tree_->Branch("GenParticle_Pt", &GenParticle_Pt);
    tree_->Branch("GenParticle_Eta", &GenParticle_Eta);
    tree_->Branch("GenParticle_Phi", &GenParticle_Phi);
    tree_->Branch("GenParticle_isDs", &GenParticle_isDs);
    tree_->Branch("GenParticle_isB", &GenParticle_isB);
    tree_->Branch("GenParticle_isBdecay", &GenParticle_isBdecay);
    tree_->Branch("GenParticle_MotherPdgId", &GenParticle_MotherPdgId);
    
    tree_->Branch("MuonCollectionSize",&MuonCollectionSize);
    tree_->Branch("MuonPt",&MuonPt);
    tree_->Branch("MuonEnergy", &MuonEnergy);
    tree_->Branch("MuonCharge", &MuonCharge);
    tree_->Branch("MuonEta",&MuonEta);
    tree_->Branch("MuonPhi",&MuonPhi);
    tree_->Branch("Muon_PdgId", &Muon_PdgId);
    tree_->Branch("Muon_MotherPdgId", &Muon_MotherPdgId);
    tree_->Branch("Muon_simFlavour", &Muon_simFlavour);
    
    //Vtx position
    tree_->Branch("Muon_vx", &Muon_vx);
    tree_->Branch("Muon_vy", &Muon_vy);
    tree_->Branch("Muon_vz", &Muon_vz);
    
    //MuonID
    tree_->Branch("Muon_isGlobal", &Muon_isGlobal);
    //tree_->Branch("Muon_isTracker", &Muon_isTracker);
    tree_->Branch("Muon_isSoft", &Muon_isSoft);
    tree_->Branch("Muon_isLoose", &Muon_isLoose);
    tree_->Branch("Muon_isMedium", &Muon_isMedium);
    tree_->Branch("Muon_isPF", &Muon_isPF);
    tree_->Branch("Muon_isRPCMuon", &Muon_isRPCMuon);
    tree_->Branch("Muon_isStandAloneMuon", &Muon_isStandAloneMuon);
    tree_->Branch("Muon_isTrackerMuon", &Muon_isTrackerMuon);
    tree_->Branch("Muon_isCaloMuon", &Muon_isCaloMuon);
    tree_->Branch("Muon_isQualityValid", &Muon_isQualityValid);
    tree_->Branch("Muon_isTimeValid", &Muon_isTimeValid);
    tree_->Branch("Muon_isIsolationValid", &Muon_isIsolationValid);
    tree_->Branch("Muon_numberOfMatchedStations", &Muon_numberOfMatchedStations);
    tree_->Branch("Muon_numberOfMatches", &Muon_numberOfMatches);
    tree_->Branch("Muon_SoftMVA_Val", &Muon_SoftMVA_Val);
    
    tree_->Branch("Muon_timeAtIpInOut",&Muon_timeAtIpInOut);
    tree_->Branch("Muon_timeAtIpInOutErr",&Muon_timeAtIpInOutErr);
    //Muon inner + outer track
    tree_->Branch("Muon_GLnormChi2", &Muon_GLnormChi2);
    tree_->Branch("Muon_GLhitPattern_numberOfValidMuonHits", &Muon_GLhitPattern_numberOfValidMuonHits);
    
    tree_->Branch("Muon_trackerLayersWithMeasurement", &Muon_trackerLayersWithMeasurement);
    tree_->Branch("Muon_Numberofvalidpixelhits", &Muon_Numberofvalidpixelhits);
    
    tree_->Branch("Muon_outerTrack_p", &Muon_outerTrack_p);
    tree_->Branch("Muon_outerTrack_eta", &Muon_outerTrack_eta);
    tree_->Branch("Muon_outerTrack_phi", &Muon_outerTrack_phi);
    tree_->Branch("Muon_outerTrack_normalizedChi2", &Muon_outerTrack_normalizedChi2);
    tree_->Branch("Muon_outerTrack_muonStationsWithValidHits", &Muon_outerTrack_muonStationsWithValidHits);
    tree_->Branch("Muon_innerTrack_p", &Muon_innerTrack_p);
    tree_->Branch("Muon_innerTrack_eta", &Muon_innerTrack_eta);
    
    tree_->Branch("Muon_innerTrack_phi", &Muon_innerTrack_phi);
    tree_->Branch("Muon_innerTrack_normalizedChi2", &Muon_innerTrack_normalizedChi2);
    tree_->Branch("Muon_innerTrack_nLostHitsInner", &Muon_innerTrack_nLostHitsInner);
    tree_->Branch("Muon_innerTrack_nLostHitsOuter", &Muon_innerTrack_nLostHitsOuter);
    tree_->Branch("Muon_innerTrack_nPixels", &Muon_innerTrack_nPixels);
    tree_->Branch("Muon_innerTrack_nValidHits", &Muon_innerTrack_nValidHits);
    tree_->Branch("Muon_innerTrack_nLostHitsOn", &Muon_innerTrack_nLostHitsOn);
    tree_->Branch("Muon_QInnerOuter", &Muon_QInnerOuter);
    
    tree_->Branch("Muon_combinedQuality_updatedSta", &Muon_combinedQuality_updatedSta);
    tree_->Branch("Muon_combinedQuality_trkKink", &Muon_combinedQuality_trkKink);
    tree_->Branch("Muon_combinedQuality_glbKink", &Muon_combinedQuality_glbKink);
    tree_->Branch("Muon_combinedQuality_trkRelChi2", &Muon_combinedQuality_trkRelChi2);
    tree_->Branch("Muon_combinedQuality_staRelChi2", &Muon_combinedQuality_staRelChi2);
    tree_->Branch("Muon_combinedQuality_chi2LocalPosition", &Muon_combinedQuality_chi2LocalPosition);
    tree_->Branch("Muon_combinedQuality_chi2LocalMomentum", &Muon_combinedQuality_chi2LocalMomentum);
    tree_->Branch("Muon_combinedQuality_localDistance", &Muon_combinedQuality_localDistance);
    tree_->Branch("Muon_combinedQuality_globalDeltaEtaPhi", &Muon_combinedQuality_globalDeltaEtaPhi);
    tree_->Branch("Muon_combinedQuality_tightMatch", &Muon_combinedQuality_tightMatch);
    tree_->Branch("Muon_combinedQuality_glbTrackProbability", &Muon_combinedQuality_glbTrackProbability);
    
    tree_->Branch("Muon_combinedQuality_match1_dX", &Muon_combinedQuality_match1_dX);
    tree_->Branch("Muon_combinedQuality_match1_pullX", &Muon_combinedQuality_match1_pullX);
    tree_->Branch("Muon_combinedQuality_match1_pullDxDz", &Muon_combinedQuality_match1_pullDxDz);
    tree_->Branch("Muon_combinedQuality_match1_dY", &Muon_combinedQuality_match1_dY);
    tree_->Branch("Muon_combinedQuality_match1_pullY", &Muon_combinedQuality_match1_pullY);
    tree_->Branch("Muon_combinedQuality_match1_pullDyDz", &Muon_combinedQuality_match1_pullDyDz);
    
    tree_->Branch("Muon_combinedQuality_match2_dX", &Muon_combinedQuality_match2_dX);
    tree_->Branch("Muon_combinedQuality_match2_pullX", &Muon_combinedQuality_match2_pullX);
    tree_->Branch("Muon_combinedQuality_match2_pullDxDz", &Muon_combinedQuality_match2_pullDxDz);
    tree_->Branch("Muon_combinedQuality_match2_dY", &Muon_combinedQuality_match2_dY);
    tree_->Branch("Muon_combinedQuality_match2_pullY", &Muon_combinedQuality_match2_pullY);
    tree_->Branch("Muon_combinedQuality_match2_pullDyDz", &Muon_combinedQuality_match2_pullDyDz);
    
    tree_->Branch("Muon_segmentCompatibility", &Muon_segmentCompatibility);
    tree_->Branch("Muon_validMuonHitComb", &Muon_validMuonHitComb);
    tree_->Branch("Muon_innerTrack_ValidFraction", &Muon_innerTrack_ValidFraction);
    tree_->Branch("Muon_Numberofvalidtrackerhits", &Muon_Numberofvalidtrackerhits);
    tree_->Branch("Muon_innerTrack_highPurity", &Muon_innerTrack_highPurity);
    
    tree_->Branch("Trigger_hltname",&Trigger_hltname);
    tree_->Branch("Trigger_hltdecision",&Trigger_hltdecision);
    
    tree_->Branch("BS_x", &BS_x);
    tree_->Branch("BS_y", &BS_y);
    tree_->Branch("BS_z", &BS_z);
    
    
}
    
    
// ------------ method called once each job just after ending the event loop  ------------
void DileptonInclusiveTreeMaker::endJob() {
    tree_->GetDirectory()->cd();
    tree_->Write();
    //  SyncTree_->GetDirectory()->cd();
    //  SyncTree_->Write();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void DileptonInclusiveTreeMaker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    //desc.add<edm::InputTag>("algInputTag", edm::InputTag("gtStage2Digis"));
    //desc.add<edm::InputTag>("extInputTag", edm::InputTag("gtStage2Digis"));
    descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DileptonInclusiveTreeMaker);
