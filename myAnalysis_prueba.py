# -*- coding: utf-8 -*-
'''
 Analysis myAnalysis, created by xuAnalysis
 https://github.com/GonzalezFJR/xuAnalysis
'''

import os,sys
sys.path.append(os.path.abspath(__file__).rsplit("/xuAnalysis/",1)[0]+"/xuAnalysis/")
from framework.analysis import analysis
import framework.functions as fun
from ROOT import TLorentzVector, TCanvas, TGraph
from array import array
#prueba para ver cómo funciona lo de los diccionarios de tt5TeV
class lev():
	dilepton = 0
	ZVeto    = 1
	MET      = 2
	jets2    = 3
	btag1    = 4
	ww       = 5
level = {lev.dilepton:'dilepton', lev.ZVeto:'ZVeto', lev.MET:'MET', lev.jets2:'2jets', lev.btag1:'1btag', lev.ww:'ww'}
invlevel = {'dilepton':lev.dilepton, 'ZVeto':lev.ZVeto, 'MET':lev.MET, '2jets':lev.jets2, '1btag':lev.btag1, 'ww':lev.ww}

class ch():
	ElMu = 0
	MuMu = 1
	ElEl = 2
	Muon = 3
	Elec = 4
chan = {ch.ElMu:'ElMu', ch.MuMu:'MuMu', ch.ElEl:'ElEl'}
#mll   = fun.InvMass(lep0, lep1)

class myAnalysis(analysis):
	def init(self):
		self.CreateTH1F('FiduEvents', 'FiduEvents', 5,0,5)    
		self.CreateTH1F("InvMassmu", "m_{#mu#mu} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F('peso', 'EventWeight',1,0,2)
		self.CreateTH1F('cosa', 'EventWeight',3,0,3)
		self.a=0
		self.nmue=0
		self.nmu =0
		self.ne =0
		#self.selLeptons = []
	def insideLoop(self,t):
		'''
		self.lep=[]
		for k in range(t.nGenDressedLepton): 
			#self.cont +=1
			#if not abs(t.GenPart_status[k]) ==1: continue #esto es para todas las partículas generadas, no solo leptones
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.GenDressedLepton_pt[k],t.GenDressedLepton_eta[k],t.GenDressedLepton_phi[k], t.GenDressedLepton_mass[k])
			PDGid=abs(t.GenDressedLepton_pdgId[k])
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue # pt and eta cuts 
			self.lep.append(fun.lepton(v,0,PDGid))
		
		if len(self.lep) >=2:  
			invmas=fun.InvMass(self.lep[0], self.lep[1]) 
			#if (self.lep[0].pdgid==11 and self.lep[1].pdgid==13):
			#if self.lep[0].GetPDGid() + self.lep[1].GetPDGid()==24:
			
			if self.lep[0].pdgid+self.lep[1].pdgid==24: #mu + e
				self.nmue +=1
				
			if self.lep[0].pdgid+self.lep[1].pdgid==26: # mu+mu
				self.nmu +=1
				
			if self.lep[0].pdgid+self.lep[1].pdgid==22: #e+e
				self.ne +=1
				
			
			if invmas >70 and invmas< 105:
				self.a +=1
		self.muons = []
		for i in range(t.nMuon):
			p = TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i], t.Muon_mass[i])
			charge = t.Muon_charge[i]
			
			self.muons.append(fun.lepton(p, charge, 13)) # 13 for muons
			invmass = fun.InvMass(self.muons[0], self.muons[1]) if len(self.muons) >= 2 else 0
			self.obj['InvMassmu'].Fill(invmass,self.EventWeight)
			self.obj['InvMassmu'].Sumw2(0)
		self.obj['peso'].SetBinContent(1,self.EventWeight)
		'''
		genLep = []
		for i in range(t.nGenDressedLepton):
			p = TLorentzVector()
			p.SetPtEtaPhiM(t.GenDressedLepton_pt[i], t.GenDressedLepton_eta[i], t.GenDressedLepton_phi[i], t.GenDressedLepton_mass[i])
			pdgid = abs(t.GenDressedLepton_pdgId[i])
			if p.Pt() < 12 or abs(p.Eta()) > 2.4: continue
			genLep.append(fun.lepton(p, 0, pdgid))
		pts    = [lep.Pt() for lep in genLep]
		genLep = [lep for _,lep in sorted(zip(pts,genLep))]

		if len(genLep) >= 2:
			genChan = 0
			l0 = genLep[0]; l1 = genLep[1]
			totId = l0.GetPDGid() + l1.GetPDGid()
			if   totId == 24: genChan = ch.ElMu
			elif totId == 22: genChan = ch.ElEl
			elif totId == 26: genChan = ch.MuMu
			genMll = fun.InvMass(l0, l1)

			genMET = t.GenMET_pt
			genJets = []
			ngenJet = 0; ngenBJet = 0
			for i in range(t.nGenJet):
				p = TLorentzVector()
				p.SetPtEtaPhiM(t.GenJet_pt[i], t.GenJet_eta[i], t.GenJet_phi[i], t.GenJet_mass[i])
				if p.Pt() < 25 or abs(p.Eta()) > 2.4: continue
				pdgid = abs(t.GenJet_partonFlavour[i])
				j = fun.jet(p)
				#if not j.IsClean(genLep, 0.4): continue
				genJets.append(j)
				ngenJet += 1
				if pdgid == 5: ngenBJet+=1

        # Fill fidu yields histo 
			if genMll >= 20 and genLep[0].Pt() >= 25:
				self.obj['FiduEvents'].Fill(lev.dilepton)
				if genChan == ch.ElEl or genChan == ch.MuMu:
					if abs(genMll - 90) > 15:
						self.obj['FiduEvents'].Fill(lev.ZVeto)
						if genMET > 30:
							self.obj['FiduEvents'].Fill(lev.MET)
							if ngenJet >= 2:
								self.obj['FiduEvents'].Fill(lev.jets2)
								if ngenBJet >= 1: self.obj['FiduEvents'].Fill(lev.btag1)
				else:
					self.obj['FiduEvents'].Fill(lev.ZVeto)
					self.obj['FiduEvents'].Fill(lev.MET)
					if ngenJet >= 2:
						self.obj['FiduEvents'].Fill(lev.jets2)
						if ngenBJet >= 1: self.obj['FiduEvents'].Fill(lev.btag1)
		
		##### Muons
		self.selLeptons = []
		for i in range(t.nMuon):
			p = TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i], t.Muon_mass[i])
			charge = t.Muon_charge[i]
			# Tight ID
			if not t.Muon_tightId[i]: continue
			#if not t.Muon_mediumId[i]: continue
			# Tight ISO, RelIso04 < 0.15
			if not t.Muon_pfRelIso04_all[i] < 0.15: continue
			# Tight IP
			dxy = abs(t.Muon_dxy[i])
			dz  = abs(t.Muon_dz[i] )
			#if dxy > 0.02 or dz > 0.05: continue
			# pT < 12 GeV, |eta| < 2.4
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue
			self.selLeptons.append(fun.lepton(p, charge, 13))
			masa=fun.InvMass(self.selLeptons[0],self.selLeptons[1]) if len(self.selLeptons) >=2  else 0
			self.obj['InvMassmu'].Fill(masa)
		##### Electrons
		for i in range(t.nElectron):
			p = TLorentzVector()
			pt  = t.Electron_pt[i]
			eta = t.Electron_eta[i]
			
			p.SetPtEtaPhiM(pt, eta, t.Electron_phi[i], t.Electron_mass[i])
			charge = t.Electron_charge[i]

			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue
			self.selLeptons.append(fun.lepton(p, charge, 11))
		
		leps = self.selLeptons
		pts  = [lep.Pt() for lep in leps]
		self.selLeptons = [lep for _,lep in sorted(zip(pts,leps))]
		self.selLeptons.reverse()

		if len(self.selLeptons) <2: continue
		#print(self.selLeptons)
		if self.selLeptons[0].charge*self.selLeptons[1].charge >0 :continue
		if self.selLeptons[0].IsMuon()==True and self.selLeptons[1].IsElec()==True:
			self.obj['cosa'].Fill(0)
		if self.selLeptons[0].IsElec()==True and self.selLeptons[1].IsElec()==True:
			self.obj['cosa'].Fill(1)
		if self.selLeptons[0].IsMuon()==True and self.selLeptons[1].IsMuon()==True:
			self.obj['cosa'].Fill(2)
	def log(self): 
		#print(self.EventWeight) #da error al correr toda la muestra
		#print('Número de sucesos: ')
		print(self.obj['cosa'].GetBinContent(1))
		print(self.obj['cosa'].GetBinContent(2))
		print(self.obj['cosa'].GetBinContent(3))
		#print(self.obj['InvMassmu'].GetEntries())

	

	

