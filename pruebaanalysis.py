from myAnalysis import *
import framework.functions as fun
import ROOT as r
r.gROOT.SetBatch(1)


pathToTree='/pool/ciencias/nanoAODv6_tt5TeV_24ago2020/trees/'
#reeName='TT_TuneCP5_5p02TeV_0'
#treeName='TT_TuneCP5_5p02TeV_#' #hasta 5
treeName='DY0JetsToLL_MLL_50_TuneCP5_5020GeV_MLM_0'
#treeName='DY0JetsToLL_MLL_50_TuneCP5_5020GeV_MLM_1' 
f=r.TFile.Open(pathToTree+'Tree_'+treeName+'.root')

#ruta a uno de los Tree:
#/beegfs/data/nanoAODv6_tt5TeV_24ago2020/trees/Tree_DY0JetsToLL_MLL_50_TuneCP5_5020GeV_MLM_0.root 
#/beegfs/data/nanoAODv6_tt5TeV_24ago2020/trees/Tree_DYJetsToLL_MLL_50_TuneCP5_5020GeV_amcatnloFXFX_0.root
#/beegfs/data/nanoAODv6_tt5TeV_24ago2020/trees/Tree_TT_TuneCP5_5p02TeV_0.root
#/beegfs/data/nanoAODv6_tt5TeV_24ago2020/trees/
h=r.TH1F('InvMass','Invariant mass of two muons',50,65,105)  #crea el entorno del histograma
t=f.Get('Events') #del archivo de trees coge el de Events
print(t.nMuon)
'''
muons = []
for i in range(t.nMuon):
	p = TLorentzVector()
	p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i], t.Muon_mass[i])
	charge = t.Muon_charge[i]
	if not t.Muon_tightId[i]: continue # Tight ID
	if not t.Muon_pfRelIso04_all[i] < 0.15: continue # Tight ISO, RelIso04 < 0.15
	dxy = abs(t.Muon_dxy[i]) 
	dz  = abs(t.Muon_dz[i] )
	if dxy > 0.05 or dz > 0.1: continue # Tight IP
	if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts
	muons.append(lepton(p, charge, 13)) # 13 for muons
	
	invariantMass= (muons[0]+muons[1]).M()
	
	h.Fill(invariantMass) #rellena el histograma


'''
selMuon = []
PT=[]
Phi=[]

for imu in range(t.nMuon):
	#if t.Muon_mediumId[imu]:
	v = TLorentzVector()
	v.SetPtEtaPhiM(t.Muon_pt[imu], t.Muon_eta[imu], t.Muon_phi[imu], t.Muon_mass[imu])
	selMuon.append(fun.lepton(v, t.Muon_charge[imu], 13))

	pt=t.Muon_pt[imu]
	phi=t.Muon_phi[imu]
	PT.append(v.Pt())
	Phi.append(phi)
	  # Invariant mass, using a predefined function 
	invmass = fun.InvMass(selMuon[0], selMuon[1]) if len(selMuon) >= 2 else 0
  

		# Filling the histograms
	h.Fill(invmass) #probar solo con invmass


#estilo del histograma
h.GetXaxis().SetTitle('m_{#mu#mu} (GeV)') 
h.GetYaxis().SetTitle('Events')
h.SetLineColor(r.kViolet+3)
h.SetFillColor(r.kGreen+2)
h.SetLineWidth(3)
h.SetStats(0)


c=r.TCanvas('c','c',10,10,800,600) # los dos ultimos son la resolucion
h.Draw('hist')

c.Print('cosa.png', 'png')
print('cosa')
'''
cc=r.TCanvas('cc','comparacion',10,10,800,600) # los dos ultimos son la resolucion
cc.SetGrid()
gr=r.TGraph(len(PT),PT,Phi)
gr.SetLineColor( 2 )
gr.SetLineWidth( 4 )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 21 )
gr.SetTitle( 'a simple graph' )
gr.GetXaxis().SetTitle( 'X title' )
gr.GetYaxis().SetTitle( 'Y title' )
gr.Draw( 'ACP' )
'''

