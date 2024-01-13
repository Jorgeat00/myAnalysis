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
		
		global sel
		sel=False #variable para poner condiciones en los jets


		#muones
		self.CreateTH1F("InvMassmu", "m_{#mu#mu} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Ptmuon", "Pt_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		
		#electrones
		self.CreateTH1F("InvMass", "m_{#mu#mu} (GeV)", 20, 0.00, 300.00)
		
		for i in range(5):
			self.CreateTH1F("InvMass%d" %(i+1), "m_{ee} (GeV)", 20, 0.00, 300.00)
			
		'''
		self.CreateTH1F("InvMass1", "m_{ee} (GeV)", 20, 0.00, 300.00)
		'''
		self.CreateTH1F("momentodi", "Pt di (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("MT", "MT_{ee}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Pt", "Pt_{ee}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Dphi", "#Delta#phi_{ee}", 20, 0.00, 300.00)
		self.CreateTH1F("Phi", "phi", 20, -3.00, 4.00)
		self.CreateTH1F("Carga", "carga ", 20, 0,10.00)
		
		'''
		self.CreateTH1F("nJets", "n Jets", 20, 0,10.00)
		self.CreateTH1F("nJets_0", "n Jets", 20, 0,10.00)
		'''
		
		#jets
		if sel==False:
			for i in range(4): #se podria poner una variable global para el no de condiciones
				self.CreateTH1F("nJets_%d" %(i), "n Jets", 20, 0,20.00)
		else:
			self.CreateTH1F("nJets", "n Jets", 20, 0,10.00)
			
		self.CreateTH1F("InvMassjets", "m_{jet} (GeV)", 20, 0.00, 30.00)
		#self.CreateTH1F("bTags", "carga ", 20, 0,10.00)
		self.CreateTH1F("nCons","n part en el jet",20,0,100.00)
		
		#leptones
		self.CreateTH1F("InvMasslep", "m_{lep} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Ptlep", "Pt_{lep} (GeV)", 20, 0.00, 300.00)
		
	
		
	def insideLoop(self,t):
		# WRITE YOU ANALYSIS HERE
		
		#muones
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
			invmass = fun.InvMass(self.muons[0], self.muons[1]) if len(self.muons) >= 2 else 0
			self.obj['InvMassmu'].Fill(invmass)
			self.obj['Ptmuon'].Fill(t.Muon_pt[i])
			
		#electrones
		self.electrons=[]
		
	
		for j in range(t.nElectron):
			#condiciones de cribado para los sucesos del tree
			
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			if not t.Electron_tightCharge[j]: continue # Tight ID
			if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			if dxy > 0.05 or dz > 0.1: continue # Tight IP
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			self.electrons.append(fun.lepton(p, charge, 11)) # 13 for muons
			
			#calculo de diferentes magnitudes, ya sea con formula o iterando los valores
			
			invmass = fun.InvMass(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			dipt= fun.DiPt(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			masat= fun.MT(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			dphi=fun.DeltaPhi(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			pt=t.Electron_pt[j]
			phi=t.Electron_phi[j]
			# Filling the histograms
			if invmass <15: continue
			#if invmass < 105 and invmass >75: continue
			#self.obj['InvMass'].Fill(invmass, self.EventWeight) 
			self.obj['InvMass'].Fill(invmass) 
			self.obj['momentodi'].Fill(dipt) 
			self.obj['MT'].Fill(masat)	
			self.obj['Pt'].Fill(pt)
			self.obj['Dphi'].Fill(dphi)
			self.obj['Phi'].Fill(phi)
			self.obj['Carga'].Fill(charge)
		
		
		'''
		
		self.elec1=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			#if not t.Electron_tightCharge[j]: continue # Tight ID
			#if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			#if dxy > 0.05 or dz > 0.1: continue # Tight IP
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			self.elec1.append(fun.lepton(p, charge, 11)) # 13 for muons
			
			#calculo de diferentes magnitudes, ya sea con formula o iterando los valores
			
			invmass = fun.InvMass(self.elec1[0], self.elec1[1]) if len(self.elec1) >= 2 else 0
			#if invmass < 15: continue #para quitar los sucesos correspondientes a fotones
			self.obj['InvMass1'].Fill(invmass) 
		
		self.elec2=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			#if not t.Electron_tightCharge[j]: continue # Tight ID
			#if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			#if dxy > 0.05: continue 
			if dz > 0.1: continue # Tight IP
			#if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			self.elec2.append(fun.lepton(p, charge, 11)) # 13 for muons
			
			#calculo de diferentes magnitudes, ya sea con formula o iterando los valores
			
			invmass = fun.InvMass(self.elec2[0], self.elec2[1]) if len(self.elec2) >= 2 else 0
			self.obj['InvMass2'].Fill(invmass) 
			
		self.elec3=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			#if not t.Electron_tightCharge[j]: continue # Tight ID
			#if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			if dxy > 0.05: continue 
			#if dz > 0.1: continue # Tight IP
			#if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			self.elec3.append(fun.lepton(p, charge, 11)) # 13 for muons
			
			#calculo de diferentes magnitudes, ya sea con formula o iterando los valores
			
			invmass = fun.InvMass(self.elec3[0], self.elec3[1]) if len(self.elec3) >= 2 else 0
			self.obj['InvMass3'].Fill(invmass) 
		
		
		self.elec4=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			if not t.Electron_tightCharge[j]: continue # Tight ID
			#if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			#if dxy > 0.05: continue 
			#if dz > 0.1: continue # Tight IP
			#if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			self.elec4.append(fun.lepton(p, charge, 11)) # 13 for muons
			
			#calculo de diferentes magnitudes, ya sea con formula o iterando los valores
			
			invmass = fun.InvMass(self.elec4[0], self.elec4[1]) if len(self.elec4) >= 2 else 0
			self.obj['InvMass4'].Fill(invmass)
		
		self.elec5=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			#if not t.Electron_tightCharge[j]: continue # Tight ID
			if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			#if dxy > 0.05: continue 
			#if dz > 0.1: continue # Tight IP
			#if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			self.elec5.append(fun.lepton(p, charge, 11)) # 13 for muons
			
			#calculo de diferentes magnitudes, ya sea con formula o iterando los valores
			
			invmass = fun.InvMass(self.elec5[0], self.elec5[1]) if len(self.elec5) >= 2 else 0
			self.obj['InvMass5'].Fill(invmass)
			
		'''
		ncond=5
		for i in range(ncond):
			self.elec=[]
			for j in range(t.nElectron):
				p=TLorentzVector()
				p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
				charge = t.Electron_charge[j]
				if i==0:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					
				elif i==1:
					dxy = abs(t.Electron_dxy[j]) 
					dz  = abs(t.Electron_dz[j] )
					#if dxy > 0.05: continue 
					if dz > 0.1: continue # Tight IP
					
				elif i==2:
					dxy = abs(t.Electron_dxy[j]) 
					dz  = abs(t.Electron_dz[j] )
					if dxy > 0.05: continue 
					#if dz > 0.1: continue # Tight IP 
					
				elif i==3:
					if not t.Electron_tightCharge[j]: continue # Tight ID
					
				elif i==4:
					if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)

				self.elec.append(fun.lepton(p, charge, 11)) # 13 for muons

				invmass = fun.InvMass(self.elec[0], self.elec[1]) if len(self.elec) >= 2 else 0
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
		'''
			#for imu in range(t.nMuon):
		#for imu in range(len(self.muons)): #con esto salen cerca de 6000. Sin ello salen los 10000
		#for i in range(t.nElectron):
	  # Invariant mass, using a predefined function 
			invmass = fun.InvMass(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			dipt= fun.DiPt(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			masat= fun.MT(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			dphi=fun.DeltaPhi(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			#pt=t.Electron_pt[i]
			#phi=t.Electron_phi[i]
			njets=t.nJet
			
				# Filling the histograms
			#self.obj['InvMass'].Fill(invmass, self.EventWeight) #probar solo con invmass (cambia bastante)
			self.obj['InvMass'].Fill(invmass) 
			self.obj['momentodi'].Fill(dipt) 
			self.obj['MT'].Fill(masat)	
			#self.obj['Pt'].Fill(pt)
			self.obj['Dphi'].Fill(dphi)
			#self.obj['Phi'].Fill(phi)
			self.obj['nJets'].Fill(njets)
		
		'''
		
		#leptones
		self.leptones=[] #funciona, pero parece un poco forzado
		for i in range(t.nMuon):
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
		
		'''
		#jets
		self.jets=[]
		for i in range(t.nJet):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Jet_pt[i], t.Jet_eta[i], t.Jet_phi[i],t.Jet_mass[i])
			self.jets.append(fun.jet(p))
			#tambien estan DeepC, DeepFlavB, DeepFlavC
			if t.Jet_btagDeepFlavB[i] <0.8: continue #quedan 92 de 10000
			if t.Jet_btagDeepB[i] <0.2: continue #salen casi 500
			if t.Jet_btagCSVV2[i] <0: continue #4175
			if t.Jet_btagCMVA[i] <0: continue #308
			#con todas las condiciones salen solo 30 sucesos
			btags=fun.GetNBtags(self.jets) #no se que hace
			self.obj['bTags'].Fill(btags)
			invmass=t.Jet_mass[i]
			npart=t.Jet_nConstituents[i]
			njet=t.nJet
			#invmass = fun.InvMass(self.jets[0], self.jets[1]) if len(self.jets) >= 2 else 0 #esto sale 0 o cercano a 0
			self.obj['InvMassjets'].Fill(invmass) #salen mas sucesos que los analizados
			self.obj['nCons'].Fill(npart)
			self.obj['nJets'].Fill(njet)
		'''
		#jets
		for k in range(4): #funciona 
			self.jets=[]
			cond=k
			#sel=False
			for i in range(t.nJet):
				p=TLorentzVector()
				p.SetPtEtaPhiM(t.Jet_pt[i], t.Jet_eta[i], t.Jet_phi[i],t.Jet_mass[i])
				if sel==False:  #funciona pero no tiene mucho sentido
					if cond==0:
						if  t.Jet_btagDeepFlavB[i] <0.3: continue
					elif cond==1:
						if  t.Jet_btagDeepB[i] <0: continue
					elif cond==2:
						if t.Jet_btagCSVV2[i] <0: continue
					elif cond==3:
						if t.Jet_btagCMVA[i] <0: continue
				self.jets.append(fun.jet(p))
				#con todas las condiciones salen solo 30 sucesos
				#btags=fun.GetNBtags(self.jets) #no se que hace
				#self.obj['bTags'].Fill(btags)
				invmass=t.Jet_mass[i]
				npart=t.Jet_nConstituents[i]
				njet=t.nJet
				#invmass = fun.InvMass(self.jets[0], self.jets[1]) if len(self.jets) >= 2 else 0 #esto sale 0 o cercano a 0
				self.obj['InvMassjets'].Fill(invmass) #salen mas sucesos que los analizados
				self.obj['nCons'].Fill(npart)
				if sel==False:
					self.obj['nJets_%d' %(k)].Fill(njet)
				else: self.obj['nJets'].Fill(njet)

	
	
	
	def log(self): #imprime cosas despues del bucle
		#numero de sucesos para cada condicion
		todas=self.obj['InvMass'].GetEntries()
		cpt=self.obj['InvMass1'].GetEntries()
		cdz=self.obj['InvMass2'].GetEntries()
		cdxy=self.obj['InvMass3'].GetEntries()
		ctight=self.obj['InvMass4'].GetEntries()
		creliso=self.obj['InvMass5'].GetEntries()
		suc=[todas,cpt,cdz,cdxy,ctight,creliso]
		total=self.getInputs(self)[0][1] #valor total de sucesos analizados (del .cfg)
		porcen=[]
		for i in suc: porcen.append(i/total*100. )
		
		print('------------') #esta duplicado para que aparezca tambien por pantalla aparte de guardarse
		print('Numero total de sucesos: ')
		print(total)
		print('Porcentaje de sucesos aplicando Pt>20: ')
		print(porcen[1])
		print('Con dz>0.1: ')
		print(porcen[2])
		print('Con dxy>0.05: ')
		print(porcen[3])
		print('Solo con electrones tight: ')
		print(porcen[4])
		print('Con la aislacion menor que 0.15: ')
		print(porcen[5])
		print('Sucesos con todas las condiciones: ')
		print(porcen[0])
		
		#prints
		sys.stdout=open('test.txt','w')
		print('Estadisticas de la seleccion de sucesos de DY o TT')
		print('------------')
		print('Numero total de sucesos: ')
		print(total)
		print('Porcentaje de sucesos aplicando Pt>20: ')
		print(porcen[1])
		print('Con dz>0.1: ')
		print(porcen[2])
		print('Con dxy>0.05: ')
		print(porcen[3])
		print('Solo con electrones tight: ')
		print(porcen[4])
		print('Con la aislacion menor que 0.15: ')
		print(porcen[5])
		print('Sucesos con todas las condiciones: ')
		print(porcen[0])
		
		sys.stdout.close()
		

