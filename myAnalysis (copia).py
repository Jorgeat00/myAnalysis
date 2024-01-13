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

class myAnalysis(analysis):
	def init(self):    
		# Create your histograms here
		
		self.sel=False #variable para poner condiciones en los jets

		#muones
		self.CreateTH1F("InvMassmu", "m_{#mu#mu} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Ptmuon", "Pt_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		
		for i in range(5):
			self.CreateTH1F("InvMassm%d" %(i+1), "m_{ee} (GeV)", 20, 0.00, 300.00)
			self.obj["InvMassm%d" %(i+1)].GetXaxis().SetTitle('Masa') #ejes
			
		#electrones
		self.CreateTH1F("InvMass", "m_{ee} (GeV)", 20, 0.00, 300.00) #20 en general y 25 al poner un limite a la masa menor
		self.obj['InvMass'].GetXaxis().SetTitle('Masa') #ejes
		for i in range(5):
			self.CreateTH1F("InvMass%d" %(i+1), "m_{ee} (GeV)", 20, 0.00, 300.00)
			self.obj["InvMass%d" %(i+1)].GetXaxis().SetTitle('Masa') #ejes
			
		'''
		self.CreateTH1F("InvMass1", "m_{ee} (GeV)", 20, 0.00, 300.00)
		'''
		self.CreateTH1F("momentodi", "Pt di (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("MT", "MT_{ee}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Pt", "Pt_{ee}(GeV)", 20, 0.00, 300.00)
		#self.CreateTH1F("Dphi", "#Delta#phi_{ee}", 20, 0.00, 300.00)
		#self.CreateTH1F("Phi", "phi", 20, -3.00, 4.00)
		#self.CreateTH1F("eta", "#eta", 20, -3.00, 4.00)
		
		
		
		'''
		self.CreateTH1F("nJets", "n Jets", 20, 0,10.00)
		self.CreateTH1F("nJets_0", "n Jets", 20, 0,10.00)
		'''
		
		
		
		#jets
		if self.sel==False:
			for i in range(4):
				self.CreateTH1F("nJets_%d" %(i), "n Jets", 20, 0,20.00)
				self.obj['nJets_%d' %(i)].GetXaxis().SetTitle('nJets') #ejes
				self.CreateTH1F("nGenJets_%d" %(i), "n Jets", 20, 0,20.00)
				self.obj['nGenJets_%d' %(i)].GetXaxis().SetTitle('nJets') #ejes
		else:
			self.CreateTH1F("nJets", "n Jets", 20, 0,20.00)
		self.CreateTH1F("nGenJets", "n Jets", 20, 0,20.00)
			
		self.CreateTH1F("InvMassjets", "m_{jet} (GeV)", 20, 0.00, 30.00)
		#self.CreateTH1F("bTags", "carga ", 20, 0,10.00)
		self.CreateTH1F("nCons","n part en el jet",20,0,100.00)
			
		self.CreateTH1F("InvMassjetsgen", "m_{jet} (GeV)", 20, 0.00, 30.00)
		self.CreateTH1F('InvMasstot','masa e #mu',20, 0.00, 300.00)
		
		
		#leptones
		self.CreateTH1F("InvMasslep", "m_{lep} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Ptlep", "Pt_{lep} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F('InvMassemu','masa inv e#mu',20, 0.00, 300.00)
		#estos son para dressedLepton
		self.CreateTH1F('InvMassmumulep','masa inv #mu#mu',20, 0.00, 300.00)
		self.CreateTH1F('InvMasseelep','masa inv ee',20, 0.00, 300.00)
		self.CreateTH1F('InvMassselec','masa inv ee',20, 0.00, 300.00)
		self.CreateTH1F('InvMasssmu','masa inv mumu',20, 0.00, 300.00)
		
		#varios
		#self.CreateTH1F('ptfoton','momento fotones',20, 0.00, 300.00)
		self.CreateTH1F('METpt','momento MET',20, 0.00, 300.00)
		self.CreateTH1F('METpt2','momento MET',20, 0.00, 300.00)
		self.CreateTH1F("ptee", "Pt_{lep} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("ptmumu", "Pt_{lep} (GeV)", 20, 0.00, 300.00)
		
		
		
		#prueba
		self.CreateTH1F("peso", "EventWeight",1, 0.00, 2.00)
		#contadores del número de muones y electrones
		self.e=0
		self.mu=0
		self.ne=0
		self.nmu=0
		self.nt=0
		self.totM=0
		self.totE=0
		self.cont=0
		
		self.jm=0 #contadores para el número de leptones en los jets
		self.je=0
	def insideLoop(self,t):
		# WRITE YOU ANALYSIS HERE
		#muones
		self.lep=[]
		for k in range(t.nGenDressedLepton): 
			self.cont +=1
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
				if invmas > 15: self.obj['InvMassemu'].Fill(invmas)
				
			if self.lep[0].pdgid+self.lep[1].pdgid==26: # mu+mu

				if invmas >15: self.obj['InvMassmumulep'].Fill(invmas)
				
			if self.lep[0].pdgid+self.lep[1].pdgid==22: #e+e
				if invmas >15: self.obj['InvMasseelep'].Fill(invmas)
			
		
		
		
		
		
		self.muons = []
		for i in range(t.nMuon):
			p = TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i], t.Muon_mass[i])
			charge = t.Muon_charge[i]
			dxy = abs(t.Muon_dxy[i]) 
			dz  = abs(t.Muon_dz[i] )
			'''
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			if dz > 0.1 or dxy > 0.05: continue # Tight IP
			if not t.Muon_tightId[i]: continue # Tight ID
			if not t.Muon_pfRelIso04_all[i] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
			'''
			''' #condiciones artículo muones
			#if not t.Muon_looseId[i]: continue 
			if not t.Muon_pfRelIso04_all[i] < 0.325: continue # Tight ISO, RelIso04 < 0.15
			dxy = abs(t.Muon_dxy[i]) 
			dz  = abs(t.Muon_dz[i] )
			if dxy > 0.05 or dz > 0.1: continue # Tight IP
			if p.Pt() < 10 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			'''
			
			
			self.muons.append(fun.lepton(p, charge, 13)) # 13 for muons
			invmass = fun.InvMass(self.muons[0], self.muons[1]) if len(self.muons) >= 2 else 0
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			if dz > 0.1 or dxy > 0.05: continue # Tight IP
			if not t.Muon_tightId[i]: continue # Tight ID
			if not t.Muon_pfRelIso04_all[i] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
			if invmass <15: continue
			if invmass >75 and invmass <105: continue
			self.obj['InvMassmu'].Fill(invmass)
			self.obj['Ptmuon'].Fill(t.Muon_pt[i])
			
		ncond=5
		for i in range(ncond):
			self.muon=[]
			for j in range(t.nMuon):
				p=TLorentzVector()
				p.SetPtEtaPhiM(t.Muon_pt[j], t.Muon_eta[j], t.Muon_phi[j],t.Muon_mass[j])
				charge = t.Muon_charge[j]
				dxy = abs(t.Muon_dxy[j]) 
				dz  = abs(t.Muon_dz[j] )
				self.muon.append(fun.lepton(p, charge, 13)) # 13 for muons
				invmass = fun.InvMass(self.muon[0], self.muon[1]) if len(self.muon) >= 2 else 0
				if i==0:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					
				elif i==1:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05: continue # Tight IP
					
				elif i==2: 
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05: continue # Tight IP
					if invmass <15: continue
					
				elif i==3:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05: continue # Tight IP
					if invmass <15: continue
					if not t.Muon_tightId[j]: continue # Tight ID
					if invmass >75 and invmass <105: continue
					
				elif i==4:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05: continue # Tight IP
					if invmass <15: continue
					if not t.Muon_tightId[j]: continue # Tight ID
					if invmass >75 and invmass <105: continue
					if not t.Muon_pfRelIso04_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
					
				self.obj['InvMassm%d' %(i+1)].Fill(invmass)
			
			
		#electrones
		self.electrons=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			
			#tiene que haber algo mal con las condiciones,
			#al cambiarlas de posición sale un porcentaje diferente
			
			#condiciones de corte para los sucesos del tree
			
			''' #condiciones artículo electrones
			if not t.Electron_pfRelIso03_all[j] < 0.085: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			if dxy > 0.05 or dz > 0.1: continue # Tight IP
			if p.Pt() < 10 or abs(p.Eta()) > 2.5: continue # pt and eta cuts 
			'''
			
			#if not t.Electron_tightCharge[j]: continue # Tight ID
			#if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los electrones es 03)
			#if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			#if dz > 0.1 or dxy > 0.05 : continue # Tight IP
			
			
			self.electrons.append(fun.lepton(p, charge, 11)) # 13 for muons
			invmass = fun.InvMass(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			#dipt= fun.DiPt(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			masat= fun.MT(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			#dphi=fun.DeltaPhi(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			pt=t.Electron_pt[j]
			#phi=t.Electron_phi[j]
			#eta=p.Eta()
			
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			if dz > 0.1 or dxy > 0.05 : continue # Tight IP
			if not t.Electron_tightCharge[j]: continue 
			if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			if invmass < 105 and invmass >75: continue #cambia poco con esto
			if invmass <15: continue


			
			# Filling the histograms
			#self.obj['InvMass'].Fill(invmass, self.EventWeight) #al ponerlo con el peso hay que añadir .Sumw2(0)
			#self.obj['InvMass'].Sumw2(0)
			self.obj['InvMass'].Fill(invmass)
			
			#self.obj['momentodi'].Fill(dipt) 
			self.obj['MT'].Fill(masat)	
			self.obj['Pt'].Fill(pt)
			#self.obj['Phi'].Fill(phi)
			#self.obj['eta'].Fill(eta)
		
		
		ncond=5
		for i in range(ncond):
			self.elec=[]
			for j in range(t.nElectron):
				
				p=TLorentzVector()
				p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
				charge = t.Electron_charge[j]
				dxy = abs(t.Electron_dxy[j]) 
				dz  = abs(t.Electron_dz[j] )
				self.elec.append(fun.lepton(p, charge, 11)) # 13 for muons
				invmass = fun.InvMass(self.elec[0], self.elec[1]) if len(self.elec) >= 2 else 0 #con la masa invariante no hay cortes en 5 TeV ¿?
				if i==0:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					
				elif i==1:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05 : continue # Tight IP
					
				elif i==2:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05 : continue # Tight IP
					if not t.Electron_tightCharge[j]: continue 
					if invmass < 105 and invmass >75: continue #cambia poco con esto
					
				elif i==3:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05 : continue # Tight IP
					if not t.Electron_tightCharge[j]: continue 
					if invmass < 105 and invmass >75: continue #cambia poco con esto
					if invmass <15: continue
					
				elif i==4:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05 : continue # Tight IP
					if not t.Electron_tightCharge[j]: continue 
					if invmass < 105 and invmass >75: continue #cambia poco con esto
					if invmass <15: continue
					if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
				

				
				self.obj['InvMass%d' %(i+1)].Fill(invmass)
			
			
		# Selection
		'''
		# As an example: select medium ID muons and fill an histogram with the invariant mass
		selMuon = []
		for imu in range(t.nMuon):
			if t.Muon_mediumId[imu]:
				if not t.Muon_pfRelIso04_all[imu] < 0.15: continue
				v = TLorentzVector()
				v.SetPtEtaPhiM(t.Muon_pt[imu], t.Muon_eta[imu], t.Muon_phi[imu], t.Muon_mass[imu])
				selMuon.append(fun.lepton(v, t.Muon_charge[imu], 13))

				  # Invariant mass, using a predefined function 
				invmass = fun.InvMass(selMuon[0], selMuon[1]) if len(selMuon) >= 2 else 0
			  
					# Filling the histograms
				self.obj['InvMass'].Fill(invmass, self.EventWeight) #probar solo con invmass
				#self.obj['InvMass'].Fill(invmass) 
		
		'''
		
		#leptones
		self.leptones=[] 
		for i in range(t.nMuon):
			if not t.nMuon==2: continue
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i],t.Muon_mass[i])
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue
			self.leptones.append(fun.lepton(p, t.Muon_charge[i],13))
			invmass = fun.InvMass(self.leptones[0], self.leptones[1]) if len(self.leptones) >= 2 else 0
			ptmu=t.Muon_pt[i]
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue #pico del Z
			self.obj['InvMasslep'].Fill(invmass)
			self.obj['Ptlep'].Fill(ptmu)
		
		for j in range(t.nElectron):
			if not t.nElectron==2: continue	
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.Electron_pt[j],t.Electron_eta[j],t.Electron_phi[j], t.Electron_mass[j])
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			self.leptones.append(fun.lepton(v,t.Electron_charge[j],11))
			invmass = fun.InvMass(self.leptones[0], self.leptones[1]) if len(self.leptones) >= 2 else 0
			ptelec=t.Electron_pt[j]
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue
			self.obj['InvMasslep'].Fill(invmass) 
			self.obj['Ptlep'].Fill(ptelec)
		
		
		#clasificación para dos muones y dos electrones 
		self.elec2=[]
		self.mu2=[] 
		for i in range(t.nMuon):
			self.totM +=1
			if not t.nMuon==2: continue
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i],t.Muon_mass[i])
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue
			self.mu2.append(fun.lepton(p, t.Muon_charge[i],13))
			invmass = fun.InvMass(self.mu2[0], self.mu2[1]) if len(self.mu2) >= 2 else 0
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue 
			self.obj['InvMasssmu'].Fill(invmass) 
			self.nmu +=1
			
		for j in range(t.nElectron):
			self.totE +=1
			if not t.nElectron==2: continue	
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.Electron_pt[j],t.Electron_eta[j],t.Electron_phi[j], t.Electron_mass[j])
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			self.elec2.append(fun.lepton(v,t.Electron_charge[j],11))
			invmass = fun.InvMass(self.elec2[0], self.elec2[1]) if len(self.elec2) >= 2 else 0
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue
			self.obj['InvMassselec'].Fill(invmass) 
			self.ne+=1
		
		#esto es para un e y un mu
		self.dos=[]
		for i in range(t.nMuon):
			if not t.nMuon==1: continue
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i],t.Muon_mass[i])
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue
			self.dos.append(fun.lepton(p, t.Muon_charge[i],13))
			invmass = fun.InvMass(self.dos[0], self.dos[1]) if len(self.dos) >= 2 else 0
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue #pico del Z
			self.obj['InvMasstot'].Fill(invmass) 
			self.nt +=1
		
		for j in range(t.nElectron):
			if not t.nElectron==1: continue	
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.Electron_pt[j],t.Electron_eta[j],t.Electron_phi[j], t.Electron_mass[j])
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			self.dos.append(fun.lepton(v,t.Electron_charge[j],11))
			invmass = fun.InvMass(self.dos[0], self.dos[1]) if len(self.dos) >= 2 else 0
			ptelec=t.Electron_pt[j]
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue
			self.obj['InvMasstot'].Fill(invmass) 
			#self.obj['Ptlep'].Fill(ptelec)
			self.nt+=1
		
		'''
		self.leptones=[] 
		self.dos=[]
		self.elec2=[]
		self.mu2=[] 
		for i in range(t.nMuon):
			self.totM +=1
			p=TLorentzVector() #este es para todos los leptones
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i],t.Muon_mass[i])
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue
			self.leptones.append(fun.lepton(p, t.Muon_charge[i],13))
			invmass = fun.InvMass(self.leptones[0], self.leptones[1]) if len(self.leptones) >= 2 else 0
			ptmu=t.Muon_pt[i]
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue #pico del Z
			self.obj['InvMasslep'].Fill(invmass)
			self.obj['Ptlep'].Fill(ptmu)
			
			if t.nMuon==2: #esto es para los sucesos con 2 muones (sin electrones)
				self.mu2.append(fun.lepton(p, t.Muon_charge[i],13))
				invmass = fun.InvMass(self.leptones[0], self.leptones[1]) if len(self.leptones) >= 2 else 0
				ptmu=t.Muon_pt[i]
				if invmass <15: continue
				if invmass < 105 and invmass >75: continue #pico del Z
				self.obj['InvMasssmu'].Fill(invmass)
				self.obj['Ptlep'].Fill(ptmu)
				self.nmu +=1
			
			elif t.nMuon==1: #esto es para los que tienen 1 muón (y supongo que 1 electrón)
				self.dos.append(fun.lepton(p, t.Muon_charge[i],13))
				invmass = fun.InvMass(self.dos[0], self.dos[1]) if len(self.dos) >= 2 else 0
				if invmass <15: continue
				if invmass < 105 and invmass >75: continue #pico del Z
				self.obj['InvMasstot'].Fill(invmass) 
				self.nt +=1
			
			
		for j in range(t.nElectron):
			self.totE +=1
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.Electron_pt[j],t.Electron_eta[j],t.Electron_phi[j], t.Electron_mass[j])
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			self.leptones.append(fun.lepton(v,t.Electron_charge[j],11))
			invmass = fun.InvMass(self.leptones[0], self.leptones[1]) if len(self.leptones) >= 2 else 0
			ptelec=t.Electron_pt[j]
			if invmass <15: continue
			if invmass < 105 and invmass >75: continue
			self.obj['InvMasslep'].Fill(invmass) 
			self.obj['Ptlep'].Fill(ptelec)
			
			if t.nElectron==2: 
				self.elec2.append(fun.lepton(v,t.Electron_charge[j],11))
				invmass1 = fun.InvMass(self.leptones[0], self.leptones[1]) if len(self.leptones) >= 2 else 0
				ptelec=t.Electron_pt[j]
				if invmass1 <15: continue
				if invmass1 < 105 and invmass1 >75: continue
				self.obj['InvMassselec'].Fill(invmass1) 
				self.obj['Ptlep'].Fill(ptelec)
				self.ne +=1
			
			elif t.nElectron==1:

				self.dos.append(fun.lepton(v,t.Electron_charge[j],11))
				invmass2 = fun.InvMass(self.dos[0], self.dos[1]) if len(self.dos) >= 2 else 0
				ptelec=t.Electron_pt[j]
				if invmass2 <15: continue
				if invmass2 < 105 and invmass2 >75: continue
				self.obj['InvMasstot'].Fill(invmass2) 
				#self.obj['Ptlep'].Fill(ptelec)
				self.nt+=1
			
		'''		
		#clasificación de los leptones a partir de la variable DressedLepton
		self.lep=[]
		for k in range(t.nGenDressedLepton): 
			self.cont +=1
			#if not abs(t.GenPart_status[k]) ==1: continue #esto es para todas las partículas generadas, no solo leptones
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.GenDressedLepton_pt[k],t.GenDressedLepton_eta[k],t.GenDressedLepton_phi[k], t.GenDressedLepton_mass[k])
			PDGid=abs(t.GenDressedLepton_pdgId[k])
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			
			if PDGid==11 or PDGid==13:
				self.lep.append(fun.lepton(v,0,PDGid))
							
			if len(self.lep) >=2:  
				invmass=fun.InvMass(self.lep[0], self.lep[1]) 
				
				if self.lep[0].pdgid==11 or self.lep[1].pdgid==11:
					self.e +=1
				if self.lep[0].pdgid==13 or self.lep[1].pdgid==13:
					self.mu +=1
				
				#if self.lep[0].GetPDGid() + self.lep[1].GetPDGid()==24:
				if self.lep[0].pdgid+self.lep[1].pdgid==24: #mu + e
					if invmass < 105 and invmass >75: continue 
					if invmass <15: continue
					self.obj['InvMassemu'].Fill(invmass)

				if self.lep[0].pdgid+self.lep[1].pdgid==26: # mu+mu	
					self.obj['ptmumu'].Fill(v.Pt())		
					if invmass < 105 and invmass >75: continue 
					if invmass <15: continue
					self.obj['InvMassmumulep'].Fill(invmass)

					
				if self.lep[0].pdgid+self.lep[1].pdgid==22: #e+e
					self.obj['ptee'].Fill(v.Pt())
					if invmass < 105 and invmass >75: continue
					if invmass <15: continue
					self.obj['InvMasseelep'].Fill(invmass)

			
		'''
		if len(self.lep) >=2:  
			invmas=fun.InvMass(self.lep[0], self.lep[1]) 
			
			
			
			#if (self.lep[0].pdgid==11 and self.lep[1].pdgid==13):
			#if self.lep[0].GetPDGid() + self.lep[1].GetPDGid()==24:
			if self.lep[0].pdgid+self.lep[1].pdgid==24: #mu + e
				if invmas > 15: self.obj['InvMassemu'].Fill(invmas)
				
			if self.lep[0].pdgid+self.lep[1].pdgid==26: # mu+mu

				if invmas >15: self.obj['InvMassmumulep'].Fill(invmas)
				
			if self.lep[0].pdgid+self.lep[1].pdgid==22: #e+e
				if invmas >15: self.obj['InvMasseelep'].Fill(invmas)
		'''	
		#jets
		for k in range(4):  
			self.jets=[]
			cond=k
			for i in range(t.nJet): 
				p=TLorentzVector()
				p.SetPtEtaPhiM(t.Jet_pt[i], t.Jet_eta[i], t.Jet_phi[i],t.Jet_mass[i])
				if p.Pt() <25 or abs(p.Eta()) > 2.4: continue
				if t.Jet_nMuons[i]==1:
					self.jm +=1
				elif t.Jet_nMuons[i] ==2:
					self.jm +=1
				if t.Jet_nElectrons[i] ==1:
					self.je +=1
				elif t.Jet_nElectrons[i]==2:
					self.je +=1
				if self.sel==False:  #puede dejarse solo con una
					if cond==0:
						if  t.Jet_btagDeepFlavB[i] <0.3: continue #estas condiciones al parecer no van a hacer falta (poca estadística)
					elif cond==1:
						if  t.Jet_btagDeepB[i] <0: continue
					elif cond==2:
						if t.Jet_btagCSVV2[i] <0: continue
					elif cond==3:
						#if t.Jet_btagCMVA[i] <0: continue
						if  t.Jet_btagDeepFlavB[i] <0.3: continue
						if t.nJet < 5: continue
						
						
				self.jets.append(fun.jet(p))
				invmass=t.Jet_mass[i]
				npart=t.Jet_nConstituents[i]
				njet=t.nJet
				#invmass = fun.InvMass(self.jets[0], self.jets[1]) if len(self.jets) >= 2 else 0 #esto sale 0 o cercano a 0
				self.obj['InvMassjets'].Fill(invmass) #salen más sucesos de los analizados
				self.obj['nCons'].Fill(npart)
				if self.sel==False:
					self.obj['nJets_%d' %(k)].Fill(njet)
				else: self.obj['nJets'].Fill(njet)
				
		#jets generados #no sé cuál de las variables es mejor utilizar, esta no tiene el btag
		self.jetsgen=[]
		for i in range(t.nGenJet):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.GenJet_pt[i], t.GenJet_eta[i], t.GenJet_phi[i],t.GenJet_mass[i])
			if p.Pt() <25 or abs(p.Eta()) > 2.4: continue
			self.jetsgen.append(fun.jet(p))
			invmass=t.GenJet_mass[i] #no es invariante, solo es masa
			njet=t.nGenJet
			#invmass = fun.InvMass(self.jets[0], self.jets[1]) if len(self.jets) >= 2 else 0 #esto sale 0 o cercano a 0
			self.obj['InvMassjetsgen'].Fill(invmass) #salen mas sucesos que los analizados
			self.obj['nGenJets'].Fill(njet)
	
		#fotones (para mirar los cortes) #no sirve, salen momentos muy altos
		'''
		fotones=[]
		for i in range(t.nPhoton):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Photon_pt[i], t.Photon_eta[i], t.Photon_phi[i],t.Photon_mass[i])
			self.obj['ptfoton'].Fill(p.Pt())
			
		'''
		
		
		for i in range(t.nElectron): #provisional #6372 muones #10671 electrones
			ptm=t.MET_pt
			self.obj['METpt'].Fill(ptm)
		
		for i in range(t.nMuon): #provisional #6372 muones #10671 electrones
			ptm=t.MET_pt
			self.obj['METpt2'].Fill(ptm)
		
		self.obj['peso'].SetBinContent(1,self.EventWeight)
		
	def log(self): #imprime cosas despues del bucle
		
		#esto no sirve para toda la muestra, ya que calcula las cosas con varios archivos
		todasm=self.obj['InvMassmu'].GetEntries()
		cptm=self.obj['InvMassm1'].GetEntries()
		cdzm=self.obj['InvMassm2'].GetEntries()
		cdxym=self.obj['InvMassm3'].GetEntries()
		ctightm=self.obj['InvMassm4'].GetEntries()
		crelisom=self.obj['InvMassm5'].GetEntries()
		sucm=[todasm,cptm,cdzm,cdxym,ctightm,crelisom]
		#totalm=self.getInputs(self)[0][1] #valor total de sucesos analizados (del .cfg) #a lo mejor también se puede poner el total de muones
		#totalm=self.obj['InvMassmu'].GetEntries()
		totalm=self.totM
		porcenm=[]
		for i in sucm: porcenm.append(i/totalm*100. )
		
		
		
		print('----------------------------') #está duplicado para que aparezca también por pantalla aparte de guardarse
		print('muones')
		print('Número total de sucesos: ')
		print(totalm)
		print('Porcentaje de sucesos aplicando Pt>20: ')
		print('%1.2f' %(porcenm[1]))
		print('Con dz<0.1 o dxy< 0.05: ')
		print('%1.2f' %(porcenm[2]))
		print('Con muones con una masa >15 GeV: ')
		print('%1.2f' %(porcenm[3]))
		print('Con muones tight y sin pico del Z: ')
		print('%1.2f' %(porcenm[4]))
		print('Con la aislación menor que 0.15 (todas): ') #aislamiento
		print('%1.2f' %(porcenm[5]))
		print('Sucesos sin condiciones (menos muones que sucesos totales): ')
		print('%1.2f' %(porcenm[0]))
		
		
		#electrones
		#número de sucesos para cada condición
		todas=self.obj['InvMass'].GetEntries()
		cpt=self.obj['InvMass1'].GetEntries()
		cdz=self.obj['InvMass2'].GetEntries()
		cdxy=self.obj['InvMass3'].GetEntries()
		ctight=self.obj['InvMass4'].GetEntries()
		creliso=self.obj['InvMass5'].GetEntries()
		suc=[todas,cpt,cdz,cdxy,ctight,creliso]
		#total=self.getInputs(self)[0][1] #valor total de sucesos analizados (del .cfg)
		#total=self.obj['InvMass'].GetEntries()
		total=self.totE
		porcen=[]
		for i in suc: porcen.append(i/total*100. )
		
		print('------------') 
		print('Electrones')
		print('Número total de sucesos: ')
		print(total)
		print('Porcentaje de sucesos aplicando Pt>20: ')
		print('%1.2f' %(porcen[1]))
		print('Con dz<0.1 o dxy < 0.05: ')
		print('%1.2f' %(porcen[2]))
		print('Sin pico del Z (75 < M < 105) y tight: ')
		print('%1.2f' %(porcen[3]))
		print('Con la masa invariante > 15 GeV: ')
		print('%1.2f' %(porcen[4]))
		print('Con la aislación menor que 0.15 (todas): ')
		print('%1.2f' %(porcen[5]))
		print('Sucesos sin condiciones (más electrones que sucesos totales): ')
		print('%1.2f' %(porcen[0]))
		
		print('----------------------------------------')
		#print(self.obj['InvMassmumulep'].GetEntries()/self.obj['InvMasseelep'].GetEntries())
		print('número de electrones: ')
		print(self.e)
		print('número de muones: ')
		print(self.mu)
		print('cociente: ')
		#print(float(self.mu)/self.e)
		
		print('Sucesos con dos electrones: ')
		print'Con el número de leptones: ',self.ne
		print'Con dressedLeptons: ',self.obj['InvMasseelep'].GetEntries()

		print('Sucesos con dos muones: ')
		print'Con el número de leptones: ',self.nmu
		print'Con dressedLeptons: ',self.obj['InvMassmumulep'].GetEntries()
		
		print('Sucesos con un electrón y un muón: ')
		print'Con el número de leptones: ',self.nt #suma de sucesos que tienen solo un muón o un electrón
		print'Con dressedLeptons: ',self.obj['InvMassemu'].GetEntries()
		
		
		print('---------------------')
		print('Cálculo del número de sucesos generados')
		if self.outname=='TT_TuneCP5up':
			print('Para TT: ') 
		elif self.outname=='DYJetsToLL_MLL50':
			print('Para DY: ')
		
		print(self.xsec) #N=xsec*lum*ngen/Ntot #Ntot= xsec*Lumtot ¿lum?
		print(self.EventWeight) #da error al correr toda la muestra
		print(self.nSumOfWeights)
		print(self.nEvents) #este y el siguiente salen lo mismo
		print(self.nGenEvents)
		#print(self.xsec*302*self.EventWeight*total) 
		
		print('no de sucesos esperados (para el total) ')
		print(self.cont) #numero de entradas en la variable dressedLepton (sale 4000)
		
		#print(self.xsec*302*self.nEvents/self.nSumOfWeights)
		#print(self.xsec*302*self.EventWeight)
		#print(self.xsec*302*self.EventWeight*total)
		#print(self.xsec*302*self.EventWeight*totalm)
		#prints
		#da error al correr DY y TT juntos
		
		if self.outname=='TT_TuneCP5up':
			#print para los muones
			sys.stdout=open('estad_muones_suma_TT.txt','w')
			print('----------------------------') #está duplicado para que aparezca también por pantalla aparte de guardarse
			print('Muones')
			print('Número total de sucesos: ')
			print(totalm)
			print('Porcentaje de sucesos aplicando Pt>20: ')
			print('%1.2f' %(porcenm[1]))
			print('Con dz<0.1 o dxy< 0.05: ')
			print('%1.2f' %(porcenm[2]))
			print('Con muones con una masa >15 GeV: ')
			print('%1.2f' %(porcenm[3]))
			print('Con muones tight y sin pico del Z: ')
			print('%1.2f' %(porcenm[4]))
			print('Con la aislación menor que 0.15 (todas): ') #aislamiento
			print('%1.2f' %(porcenm[5]))
			print('Sucesos sin condiciones (menos muones que sucesos totales): ')
			print('%1.2f' %(porcenm[0]))
			
			sys.stdout.close()
			
			
			#print para los electrones
			sys.stdout=open('estad_electrones_suma_TT.txt','w')
			print('------------') 
			print('Electrones')
			print('Número total de sucesos: ')
			print(total)
			print('Porcentaje de sucesos aplicando Pt>20: ')
			print('%1.2f' %(porcen[1]))
			print('Con dz<0.1 o dxy < 0.05: ')
			print('%1.2f' %(porcen[2]))
			print('Sin pico del Z (75 < M < 105) y tight: ')
			print('%1.2f' %(porcen[3]))
			print('Con la masa invariante > 15 GeV: ')
			print('%1.2f' %(porcen[4]))
			print('Con la aislación menor que 0.15 (todas): ')
			print('%1.2f' %(porcen[5]))
			print('Sucesos sin condiciones (más electrones que sucesos totales: ')
			print('%1.2f' %(porcen[0]))
				
			sys.stdout.close()
			
		elif self.outname=='DYJetsToLL_MLL50':
			#print para los muones
			sys.stdout=open('estad_muones_suma_DY.txt','w')
			
			print('----------------------------') #está duplicado para que aparezca también por pantalla aparte de guardarse
			print('Muones')
			print('Número total de sucesos: ')
			print(totalm)
			print('Porcentaje de sucesos aplicando Pt>20: ')
			print('%1.2f' %(porcenm[1]))
			print('Con dz<0.1 o dxy< 0.05: ')
			print('%1.2f' %(porcenm[2]))
			print('Con muones con una masa >15 GeV: ')
			print('%1.2f' %(porcenm[3]))
			print('Con muones tight y sin pico del Z: ')
			print('%1.2f' %(porcenm[4]))
			print('Con la aislación menor que 0.15 (todas): ') #aislamiento
			print('%1.2f' %(porcenm[5]))
			print('Sucesos sin condiciones (menos muones que sucesos totales): ')
			print('%1.2f' %(porcenm[0]))
			
			
			sys.stdout.close()
			
			
			#print para los electrones
			sys.stdout=open('estad_electrones_suma_DY.txt','w')
			print('------------') 
			print('Electrones')
			print('Número total de sucesos: ')
			print(total)
			print('Porcentaje de sucesos aplicando Pt>20: ')
			print('%1.2f' %(porcen[1]))
			print('Con dz<0.1 o dxy < 0.05: ')
			print('%1.2f' %(porcen[2]))
			print('Sin pico del Z (75 < M < 105) y tight: ')
			print('%1.2f' %(porcen[3]))
			print('Con la masa invariante > 15 GeV: ')
			print('%1.2f' %(porcen[4]))
			print('Con la aislación menor que 0.15 (todas): ')
			print('%1.2f' %(porcen[5]))
			print('Sucesos sin condiciones (más electrones que sucesos totales): ')
			print('%1.2f' %(porcen[0]))
			
			sys.stdout.close()
		
