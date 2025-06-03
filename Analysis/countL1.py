import ROOT
from setTDRStyle import setTDRStyle
import pickle
import xgboost
import numpy as np
import uproot
import matplotlib.pyplot as plt
import mplhep as hep
from scipy.stats import binomtest

import warnings 
warnings.filterwarnings('ignore') 

def fitAndPlot(ws, obj, label, data=False):
    
    fitResult = ws.pdf("model").fitTo(ws.data("hist%sRoo"%obj), ROOT.RooFit.Save())


    c1 = ROOT.TCanvas("cfrom scipy.stats import binomtest1","c1",700,700)
    c1.cd()    
    plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    style = setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
    plotPad.UseCurrentStyle()
    plotPad.Draw()    
    plotPad.cd()

    ws.var("mass").setBins(40)
    frame = ws.var('mass').frame(ROOT.RooFit.Title('Invariant mass of dimuon pairs'))
    frame.GetXaxis().SetTitle('m_{#mu#mu} [GeV]')
    frame.GetYaxis().SetTitle("Events / 0.01 GeV")
    ROOT.RooAbsData.plotOn(ws.data('hist%sRoo'%obj), frame,ROOT.RooFit.Name("hist%sRoo"%obj))
    ws.pdf('model').plotOn(frame,ROOT.RooFit.Name("model"))
    frame.Draw()


    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.04)
    latex.SetNDC(True)
    latexCMS = ROOT.TLatex()
    latexCMS.SetTextFont(61)
    latexCMS.SetTextSize(0.08)
    latexCMS.SetNDC(True)
    latexCMSExtra = ROOT.TLatex()
    latexCMSExtra.SetTextFont(52)
    latexCMSExtra.SetTextSize(0.045)
    latexCMSExtra.SetNDC(True) 
        
    latex.DrawLatex(0.95, 0.96, "(13.6 TeV)")

    if data:
        cmsExtra = "Preliminary"
    else:    
        cmsExtra = "#splitline{Simulation}{Preliminary}"
    latexCMS.DrawLatex(0.19,0.85,"CMS")
    if "Simulation" in cmsExtra:
        yLabelPos = 0.78    
    else:
        yLabelPos = 0.78    

    latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))                

    latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))                

    latexEta = ROOT.TLatex()
    latexEta.SetTextFont(42)
    latexEta.SetTextAlign(31)
    latexEta.SetTextSize(0.035)
    latexEta.SetNDC(True)        
    if obj == "Trk":
        latexEta.DrawLatex(0.62,0.7,"3rd Muon fired 2Mu1Tk trigger")
    else:    
        latexEta.DrawLatex(0.55,0.7,"3rd Muon fired 3Mu trigger")

    if data:
        c1.SaveAs("DsPhiMuNuFit_Data_%s_%s.pdf"%(label,obj))
    else:    
        c1.SaveAs("DsPhiMuNuFit_MC_%s_%s.pdf"%(label,obj))

    return ws.var("fsig").getVal(), ws.var("fsig").getError()
    
def evalEvent(event, bdts, var_names):
    array = []

    for var in var_names:
        array.append(
            float(event[var])
        )

    array = np.array(array).reshape(1,-1)
    
    preds = [bdt.predict(array) for bdt in bdts]
    return np.mean(preds)

def countL1(df, category=None):

    #print(list(df.keys()))
    num_both = 0
    num_double = 0
    num_triple = 0
    total = 0
    dimu_1 = []
    dimu_2 = []

    #print(len(df))
    for i in range(len(df)):
        event = df.iloc[i]
    
        
        triple_passed = False
        double_passed = False
        '''
        for key in df.keys():
            if 'L1_Double' in key and event[key]==1:
                double_passed = True
    
            if 'L1_Triple' in key and event[key]==1:
                triple_passed = True
        '''
        if event['L1DoubleMu_passed'] == 1:
            double_passed = True
        if event['L1TripleMu_passed'] == 1:
            triple_passed=True
        
        if category is None:
            if event['category'] == 0:
                if evalEvent(event, bdt_A, var_names) < threshes[0]: continue
                else: total += 1
            elif event['category'] == 1:
                if evalEvent(event, bdt_B, var_names) < threshes[1]: continue
                else: total += 1
            elif event['category'] == 2:
                if evalEvent(event, bdt_C, var_names) < threshes[2]: continue
                else: total += 1

        else:
            if event['category'] == category:
                if evalEvent(event, bdts[category], var_names) < threshes[category]: continue
            else:
                continue
        
        if double_passed and triple_passed:
            num_both += 1
        elif double_passed and not(triple_passed):
            num_double += 1
        elif not(double_passed) and triple_passed:
            num_triple += 1
        
        if triple_passed:
            dimu_1.append(event['dimu_OS1'])
            dimu_2.append(event['dimu_OS2'])
    
    #assert total == len(df), print(total, len(df))

    print(f'Passed Both: {num_both}')
    print(f'Passed ONLY Double: {num_double} +- {round(np.sqrt(num_double))}')
    print(f'Passed ONLY Triple: {num_triple} +- {round(np.sqrt(num_triple))}')
    print(f'Total: {total}')
    dfrac = num_double/total
    tfrac = num_triple/total
    
    double_result = binomtest(num_double, total, p=0.5)
    dlow = dfrac - double_result.proportion_ci().low
    dhigh = double_result.proportion_ci().high - dfrac
    
    triple_result = binomtest(num_triple, total, p=0.5)
    tlow = tfrac - triple_result.proportion_ci().low
    thigh = triple_result.proportion_ci().high - tfrac
    
    print(f'Fraction that pass ONLY DoubleMu: {dfrac:.4f} + {dhigh:.4f} - {dlow:.4f}')
    #print('DoubleMu Bounds: ', double_result.proportion_ci())
    print(f'Fraction that pass ONLY TripleMu: {tfrac:.4f} + {thigh:.4f} - {tlow:.4f}')
    #print('TripleMu Bounds: ', triple_result.proportion_ci())
    
    
    
    #print(f'Fraction Passed Double Inclusive: {(num_double+num_both)/total:.4f}')
    #print(f'Fraction Passed Triple Inclusive: {(num_triple+num_both)/total:.4f}')
    
    return dimu_1, dimu_2
    
    
def runCount(ptBin, etaBin, era, data=True, binned=False, category=None):

    num_double = 0
    num_triple = 0
    num_both = 0
    total = 0
    #tree = ROOT.TChain()
    
    if data:
        # ~ tree.Add("AnalysedTree_data_2022_tau3mu_merged_test8.root/FinalTree")
        #tree.Add("AnalysedTree_data_2023_tau3mu_merged_2023v1.root/FinalTree")

        if '2022' in era:
            
            df = uproot.open("/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/AnalysedTree_data_2022_tau3mu_merged_2022_ReadOutBools.root")['FinalTree'].arrays(library='pd')
        elif '2023' in era:
            df = uproot.open("/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/AnalysedTree_data_2023_tau3mu_merged_2023_ReadOutBools.root")['FinalTree'].arrays(library='pd')
        #tree.Add('dataTEST.root/FinalTree')
    else:    
        #tree.Add("AnalysedTree_MC_DsPhiMuNu_tau3mu_%s.root/FinalTree"%era)\
        if era == '2022':
            df = uproot.open("/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/DsPhiMuNu_tau3mu_2022_ReadOutBools/AnalysedTree_MC_DsPhiMuNu_tau3mu0.root")['FinalTree'].arrays(library='pd')
        elif era == '2022EE':
            df = uproot.open("/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/DsPhiMuNu_tau3mu_2022EE_ReadOutBools/AnalysedTree_MC_DsPhiMuNu_tau3mu0.root")['FinalTree'].arrays(library='pd')
        elif era == '2023':
            df = uproot.open("/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/DsPhiMuNu_tau3mu_2023_ReadOutBools/AnalysedTree_MC_DsPhiMuNu_tau3mu0.root")['FinalTree'].arrays(library='pd')
        elif era == '2023BPix':
            df = uproot.open("/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/DsPhiMuNu_tau3mu_2023BPix_ReadOutBools/AnalysedTree_MC_DsPhiMuNu_tau3mu0.root")['FinalTree'].arrays(library='pd')
            
    dimu_1, dimu_2 = countL1(df, category=category)

    
    
    '''
    histTrk = ROOT.TH1F('trkHist','trkHist',40, 0.8,1.2)
    histMu = ROOT.TH1F('muHist','muHist',40, 0.8,1.2)
    
    ptMin = ptBins[ptBin][0]
    ptMax = ptBins[ptBin][1]
    
    etaMin = etaBins[etaBin][0]
    etaMax = etaBins[etaBin][1]
    
    if binned: print(ptMin, ptMax, etaMin, etaMax)
    
    label = ptLabels[ptBin] + "_" + etaLabels[etaBin] + "_" + era
    for ev in tree:
        if binned:
            if (ev.Ptmu3 < ptMin) or (ev.Ptmu3 > ptMax) or (abs(ev.Etamu3) < etaMin) or (abs(ev.Etamu3) > etaMax): continue
        
        if ev.category == 0:
            if evalEvent(ev, bdt_A, var_names) < 0.95: continue
        if ev.category == 'A':
            if evalEvent(ev, bdt_B, var_names) < 0.95: continue
        if ev.category == 'A':
            if evalEvent(ev, bdt_C, var_names) < 0.95: continue
                
        if ev.L1TripleMu_passed == 1 and not(ev.L1DoubleMu_passed == 1): 
            num_triple += 1
        elif not(ev.L1TripleMu_passed == 1) and ev.L1DoubleMu_passed==1:
            num_double += 1
        else:
            num_both += 1
                
        total += 1
    '''
    

    return num_double, num_triple, num_both, total, np.array(dimu_1), np.array(dimu_2)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--binned', type=bool, default=False)
parser.add_argument('--category', type=int, default=None)
args = parser.parse_args()
binned = args.binned
category = args.category


ptBins = [[0,1000], [0,4],[4,1000],[3.5,1000]]
etaBins = [[0,2.4],[0,1.2],[1.2,2.4]]
ptLabels = ["ptInclusive", "pt0to4", 'pt4toInf','pt3p5toInf']
etaLabels = ["etaInclusive", 'eta0to1p2','eta1p2to2p4']
eras = ["2022", "2022EE", "2023", "2023BPix"]

results = []
'''
try:
    for era in eras:
        if binned:
            for i in range(0, len(ptBins)):
                for j in range(0,len(etaBins)):
                    num_double , num_triple, total =  runCount(i,j,era=era, data=False)
                    results.append(["MC", num_double, num_triple, total])
                    num_double , num_triple, total = runCount(i,j,era=era,data=True)
                    results.append(["Data", num_double, num_triple, total])
        
        else:
            num_double , num_triple, total =  runCount(0,0,era=era, data=False)
            results.append(["MC", num_double, num_triple, total])
            num_double , num_triple, total = runCount(0,0,era=era,data=True)
            results.append(["Data", num_double, num_triple, total])
'''     

bdt_A = [pickle.load(open(f'/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/BDTs/model_Cat_A_fold{i}.pkl','rb')) for i in range(4)]
bdt_B = [pickle.load(open(f'/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/BDTs/model_Cat_B_fold{i}.pkl','rb')) for i in range(4)]
bdt_C = [pickle.load(open(f'/depot/cms/users/simon73/Run3Tau3Mu_2/CMSSW_13_0_21/src/Analysis/BDTs/model_Cat_C_fold{i}.pkl','rb')) for i in range(4)]
bdts = [bdt_A, bdt_B, bdt_C]
threshes = [0.94, 0.96, 0.84]
#threshes=[0,0,0]

var_names = [
"cLP"
,"tKink"
,"segmComp"
,"fv_nC"
,"fv_dphi3D"
,"fv_d3Dsig"
,"fv_d3D"
,"mindca_iso"
,"trkRel"
,"d0sig"
,"Ptmu3"
,"d0sig_max"
,"MVASoft1"
,"MVASoft2"
,"MVASoft3"
,"Pt_tripl"
]

eras = ["2023","2023BPix"]

for era in eras:
    print('Era: ', era)
    print('MC')
    num_double , num_triple, num_both, total, MCdimu_1, MCdimu_2 =  runCount(0,0,era=era, data=False)
    results.append(["MC", era, num_double, num_triple, num_both, total])
    print('Data')
    num_double , num_triple, num_both, total, Datadimu_1, Datadimu_2  = runCount(0,0,era=era,data=True)
    
    results.append(["Data", era, num_double, num_triple, num_both, total])

    temp1 = np.concatenate((MCdimu_1, Datadimu_1))
    temp2 = np.concatenate((MCdimu_2, Datadimu_2))

    _, bins1 = np.histogram(temp1, bins=25)
    _, bins2 = np.histogram(temp2, bins=25)

    plt.hist(MCdimu_1, bins=bins1, density=True, color='blue', label='DsPhiMuNu')
    
    counts, bins = np.histogram(Datadimu_1, density=True, bins=bins1)
    counts_raw, _ =  np.histogram(Datadimu_1, density=False, bins=bins1)
    errors = np.sqrt(counts_raw) / (len(Datadimu_1) * np.diff(bins))
    
    bin_centers = 0.5 * (bins[1:] + bins[:-1])  # Calculate bin centers
    xerr = 0.5*(bins[1]-bins[0])
    plt.errorbar(bin_centers, counts, xerr=xerr, yerr=errors, fmt='k.', markersize=5, label='Data')  # 'k.' for black dots

    plt.xlabel(r'$m_{2\mu}$ OS1 [GeV]')
    plt.ylabel('Density')
    plt.legend()
    hep.cms.label(label='Preliminary', com=13.6 , data=True)
    plt.savefig(f'dimu_OS1_{era}.png')
    plt.show()
    plt.clf()
    plt.hist(MCdimu_2, bins=bins2, density=True, color='blue', label='DsPhiMuNu')
    
    counts, bins = np.histogram(Datadimu_2, density=True, bins=bins2)
    counts_raw, _ =  np.histogram(Datadimu_2, density=False, bins=bins2)
    errors = np.sqrt(counts_raw) / (len(Datadimu_2) * np.diff(bins))
    
    bin_centers = 0.5 * (bins2[1:] + bins2[:-1])  # Calculate bin centers
    xerr = 0.5*(bins[1]-bins[0])
    plt.errorbar(bin_centers, counts, xerr=xerr, yerr=errors, fmt='k.', markersize=5, label='Data')  # 'k.' for black dots

    plt.xlabel(r'$m_{2\mu}$ OS2 [GeV]')
    plt.ylabel('Density')
    plt.legend()
    hep.cms.label(label='Preliminary', com=13.6 , data=True)
    plt.savefig(f'dimu_OS2_{era}.png')
    plt.show()
    plt.clf()
            
