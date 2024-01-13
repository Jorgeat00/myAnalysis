'''
 Analysis myAnalysis, created by xuAnalysis
 https://github.com/GonzalezFJR/xuAnalysis
'''

import os,sys
sys.path.append(os.path.abspath(__file__).rsplit("/xuAnalysis/",1)[0]+"/xuAnalysis/")
from framework.analysis import analysis
import framework.functions as fun
from ROOT import TLorentzVector

systematics = ['']
class myAnalysis(analysis):
	def init(self):
    # Create your histograms here
		self.CreateTH1F("InvMass", "m_{#mu#mu} (GeV)", 20, 0.00, 300.00)

	def insideLoop(self,t):
		# WRITE YOU ANALYSIS HERE

		
		self.muons = []
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
			self.muons.append(fun.lepton(p, charge, 13)) # 13 for muons
		  
			#falta meter algo al histograma
		
		
		# Selection
		'''
		# As an example: select medium ID muons and fill an histogram with the invariant mass
		selMuon = []
		for imu in range(t.nMuon):
			if t.Muon_mediumId[imu]:
				v = TLorentzVector()
				v.SetPtEtaPhiM(t.Muon_pt[imu], t.Muon_eta[imu], t.Muon_phi[imu], t.Muon_mass[imu])
				selMuon.append(fun.lepton(v, t.Muon_charge[imu], 13))

				  # Invariant mass, using a predefined function 
				invmass = fun.InvMass(selMuon[0], selMuon[1]) if len(selMuon) >= 2 else 0
			  

					# Filling the histograms
				self.obj['InvMass'].Fill(invmass, self.EventWeight) #probar solo con invmass
				#self.obj['InvMass'].Fill(invmass) 
		'''
		
		
			#for imu in range(t.nMuon):
		#for imu in range(len(self.muons)): #con esto salen cerca de 4500. Sin ello salen los 10000
		for i in range(t.nMuon):
			  # Invariant mass, using a predefined function 
			invmass = fun.InvMass(self.muons[0], self.muons[1]) if len(self.muons) >= 2 else 0
		  
				# Filling the histograms
			#self.obj['InvMass'].Fill(invmass, self.EventWeight) #probar solo con invmass (cambia bastante)
			self.obj['InvMass'].Fill(invmass) 
		
		
		'''
		for syst in systematics:

			# Requirements
			if not fun.GetValue(t, "",syst)lenfun.GetValue(t, "",syst)(fun.GetValue(t, "",syst)selMuonfun.GetValue(t, "",syst)) >= fun.GetValue(t, "",syst)2fun.GetValue(t, "",syst): return
			#self.obj['InvMass'].Fill(invmass, self.EventWeight)
		'''

