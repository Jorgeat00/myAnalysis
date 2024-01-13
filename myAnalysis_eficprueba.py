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
		#muones
		self.CreateTH1F("InvMassmu", "m_{#mu#mu} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("Ptmuon", "Pt_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		
		self.CreateTH1F("InvMassm", "m_{ee} (GeV)", 20, 0.00, 300.00)
		self.obj["InvMassm"].GetXaxis().SetTitle('Masa') #ejes
			
		self.CreateTH1F('eficienciasmu','eficiencias',5,0,5)
		self.CreateTH1F('eficienciaselec','eficiencias',5,0,5)
		
		#electrones
		self.CreateTH1F("InvMass", "m_{ee} (GeV)", 20, 0.00, 300.00) #20 en general y 25 al poner un limite a la masa menor
		self.obj['InvMass'].GetXaxis().SetTitle('Masa') #ejes
		
		self.CreateTH1F("InvMasse", "m_{ee} (GeV)", 20, 0.00, 300.00)
		self.obj["InvMasse"].GetXaxis().SetTitle('Masa') #ejes
		
		
		#histogramas de los jets
		self.CreateTH1F("nJets", "n Jets", 20, 0,20.00)
		self.obj['nJets'].GetXaxis().SetTitle('nJets') #ejes
		self.CreateTH1F("nCons","n part en el jet",20,0,100.00)
		
		
		#leptones
		self.CreateTH1F("Ptlep", "Pt_{lep} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F('InvMasslep','m_{lep}',20,0.0,300.0)
		self.CreateTH1F('eficlep','cosas',2,0,2)
		
		#histogramas para almacenar las variables de los datos
		self.CreateTH1F("peso", "EventWeight",1, 0.00, 2.00)
		self.CreateTH1F("sucesos", "nEvents",1, 0.00, 2.00)
		self.CreateTH1F("sumpesos", "nSumOfWeights",1, 0.00, 2.00)
		self.CreateTH1F("nelectrones", "nelec",1, 0.00, 2.00)
		self.CreateTH1F("nmuones", "nmu",1, 0.00, 2.00)
		
		
		self.CreateTH1F('nsucjets','no de sucesos en funcion de los jets',5,2,7)
		self.CreateTH1F("histprueba", "Sucesos para cada canal",4,0,4)
		'''
		self.obj['histprueba'].GetXaxis().SetBinLabel(3,'ee') #sirve para poner otro nombre a los bins
		self.obj['histprueba'].GetXaxis().SetBinLabel(2,'#mu#mu')
		self.obj['histprueba'].GetXaxis().SetBinLabel(1,'e#mu')
		self.obj['histprueba'].GetXaxis().SetLabelSize(0.1)
		'''

		#contadores del número de muones y electrones
		self.totM=0 #número total de muones (nMuon)
		self.totE=0 #número total de electrones (nElectron)
		self.nlep=0 #muḿero de muones+ número de electrones
		
		
	def insideLoop(self,t):
		# WRITE YOU ANALYSIS HERE
		#muones
		self.peso=self.EventWeight
		self.muon=[]
		for j in range(t.nMuon):
				p=TLorentzVector()
				p.SetPtEtaPhiM(t.Muon_pt[j], t.Muon_eta[j], t.Muon_phi[j],t.Muon_mass[j])
				charge = t.Muon_charge[j]
				dxy = abs(t.Muon_dxy[j]) 
				dz  = abs(t.Muon_dz[j] )
				tightid=t.Muon_tightId[j]
				iso=t.Muon_pfRelIso04_all[j]
				self.muon.append(fun.lepton(p, charge, 13)) # 13 for muons
				invmass = fun.InvMass(self.muon[0], self.muon[1]) if len(self.muon) >= 2 else 0
				
		ncond=5
		for i in range(ncond):
			if i==0:
				if self.muon.Pt() < 20 or abs(self.muon.Eta()) > 2.4: continue # pt and eta cuts 
				self.obj['eficienciasmu'].Fill(0)
			elif i==1:
				if self.muon.Pt() < 20 or abs(self.muon.Eta()) > 2.4: continue # pt and eta cuts 
				if dz > 0.1 or dxy > 0.05: continue # Tight IP
				self.obj['eficienciasmu'].Fill(1)
			elif i==2: 
				if self.muon.Pt() < 20 or abs(self.muon.Eta()) > 2.4: continue # pt and eta cuts 
				if dz > 0.1 or dxy > 0.05: continue # Tight IP
				if invmass <20: continue
				self.obj['eficienciasmu'].Fill(2)
			elif i==3:
				if self.muon.Pt() < 20 or abs(self.muon.Eta()) > 2.4: continue # pt and eta cuts 
				if dz > 0.1 or dxy > 0.05: continue # Tight IP
				if invmass <20: continue
				if not tightid: continue # Tight ID
				if invmass >75 and invmass <105: continue
				self.obj['eficienciasmu'].Fill(3)
			elif i==4:
				if self.muon.Pt() < 20 or abs(self.muon.Eta()) > 2.4: continue # pt and eta cuts 
				if dz > 0.1 or dxy > 0.05: continue # Tight IP
				if invmass <20: continue
				if not tightid: continue # Tight ID
				if invmass >75 and invmass <105: continue
				if not iso < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
				self.obj['eficienciasmu'].Fill(4)
				self.obj['InvMassm'].Fill(invmass)
			#self.obj['eficienciasmu'].Fill(i)
	
		self.elec=[]
		for j in range(t.nElectron):
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Electron_pt[j], t.Electron_eta[j], t.Electron_phi[j],t.Electron_mass[j])
			charge = t.Electron_charge[j]
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			isoelec=t.Electron_pfRelIso03_all[j]
			cutbased=t.Electron_cutBased[j]
			self.elec.append(fun.lepton(p, charge, 11)) # 13 for muons
			invmass = fun.InvMass(self.elec[0], self.elec[1]) if len(self.elec) >= 2 else 0 #con la masa invariante no hay cortes en 5 TeV ¿?

		if self.elec.Pt() < 20 or abs(self.elec.Eta()) > 2.4: return # pt and eta cuts 
		self.obj['eficienciaselec'].Fill(0)
		if self.elec.Pt() < 20 or abs(self.elec.Eta()) > 2.4: return # pt and eta cuts 
		if dz > 0.1 or dxy > 0.05 : return # Tight IP
		self.obj['eficienciaselec'].Fill(1)
		if self.elec.Pt() < 20 or abs(self.elec.Eta()) > 2.4: return # pt and eta cuts 
		if dz > 0.1 or dxy > 0.05 : return # Tight IP
		if not isoelec < 0.15: return # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
		if invmass < 105 and invmass >75: return #cambia poco con esto
		self.obj['eficienciaselec'].Fill(2)
		if self.elec.Pt() < 20 or abs(self.elec.Eta()) > 2.4: return # pt and eta cuts 
		if dz > 0.1 or dxy > 0.05 : return # Tight IP
		if not isoelec < 0.15: return # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
		if invmass < 105 and invmass >75: return #cambia poco con esto
		if not  >= 4: return #cambio
		#if invmass <20: return
		self.obj['eficienciaselec'].Fill(3)
		if self.elec.Pt() < 20 or abs(self.elec.Eta()) > 2.4: return # pt and eta cuts 
		if dz > 0.1 or dxy > 0.05 : return # Tight IP
		if not isoelec < 0.15: return # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
		if invmass < 105 and invmass >75: return #cambia poco con esto
		if not cutbased >= 4: return #cambio
		if invmass <20: return
		self.obj['InvMasse'].Fill(invmass)
		self.obj['eficienciaselec'].Fill(4)

		#hasta aquí es para sacar las eficiencias de los cortes sobre el número de electrones y muones por separado
		
		
		#leptones
		self.leptones=[] 
		for i in range(t.nMuon):
			self.totM +=1 #este contador es para sacar los porcentajes de los cortes
			if t.nMuon >2: continue
			#if t.nMuon==0 : continue
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i],t.Muon_mass[i])
			charge = t.Muon_charge[i]
			dxy = abs(t.Muon_dxy[i]) 
			dz  = abs(t.Muon_dz[i])
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			if dz > 0.1 or dxy > 0.05: continue # Tight IP
			if not t.Muon_tightId[i]: continue # Tight ID
			if not t.Muon_pfRelIso04_all[i] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
			self.leptones.append(fun.lepton(p, t.Muon_charge[i],13))
			self.nlep +=1 #este contador cuenta el número de leptones que pasan los cortes
			
		for j in range(t.nElectron): 
			self.totE +=1
			if t.nElectron >2 : continue
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.Electron_pt[j],t.Electron_eta[j],t.Electron_phi[j], t.Electron_mass[j])
			charge = t.Electron_charge[j]
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			if dz > 0.1 or dxy > 0.05 : continue # Tight IP
			if not t.Electron_tightCharge[j]: continue 
			if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			self.leptones.append(fun.lepton(v,t.Electron_charge[j],11))
			self.nlep +=1

			
		#jets 
		self.jets=[]
		for i in range(t.nJet): 
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Jet_pt[i], t.Jet_eta[i], t.Jet_phi[i],t.Jet_mass[i])
			if p.Pt() <25 or abs(p.Eta()) > 2.4: continue
			#if  t.Jet_btagDeepFlavB[i] <0.3: continue #estas condiciones al parecer no van a hacer falta (poca estadística)
			self.jets.append(fun.jet(p))
			njet=t.nJet
		'''
		if len(self.leptones) <=2: return
		self.PT=self.leptones[0].Pt()
		self.eta=self.leptones[0].Eta()
		if self.PT <20 or abs(self.eta) >2.3:
			self.obj['eficlep'].Fill(0)
		'''
		
		if len(self.leptones) >=2: #cambio
			if len(self.jets)>=2:
				invmass=fun.InvMass(self.leptones[0], self.leptones[1]) 
				if invmass <20: return #cambio
				if self.leptones[0].charge*self.leptones[1].charge >0: return
				if self.leptones[0].pdgid+self.leptones[1].pdgid==24:#mu + e
					if len(self.jets)==2:
						self.obj['nsucjets'].Fill(2)
					if len(self.jets)==3:
						self.obj['nsucjets'].Fill(3)
					if len(self.jets)==4:
						self.obj['nsucjets'].Fill(4)
					if len(self.jets)==5:
						self.obj['nsucjets'].Fill(5)
					if len(self.jets)>=6:
						self.obj['nsucjets'].Fill(6)
					if invmass >15: #ahora este corte no quita apenas sucesos (1)
						self.obj['histprueba'].Fill(1)

						
				if self.leptones[0].pdgid+self.leptones[1].pdgid==26: # mu+mu
					self.obj['histprueba'].Fill(2)

				if self.leptones[0].pdgid+self.leptones[1].pdgid==22: #e+e
					self.obj['histprueba'].Fill(3)

		#se rellenan los histogramas con variables para calcular el peso (o relacionadas con él)
		self.obj['peso'].SetBinContent(1,self.EventWeight)
		self.obj['sucesos'].SetBinContent(1,self.nEvents)
		self.obj['sumpesos'].SetBinContent(1,self.nSumOfWeights)
		self.obj['nmuones'].SetBinContent(1,self.totM)
		self.obj['nelectrones'].SetBinContent(1,self.totE)
	
	
	
	
############################prints

	def log(self): #imprime cosas despues del bucle
	
		#esto no sirve para toda la muestra, ya que calcula las cosas con varios archivos

		totsuc=self.getInputs(self)[0][1] #valor total de sucesos analizados (del .cfg)
		print('----------------------------') #está duplicado para que aparezca también por pantalla aparte de guardarse
		print('Muones')
		print('Número total de sucesos: ')
		print(totsuc)
		print('Porcentaje de sucesos aplicando Pt>20 (eta < 2.4): ')
		print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(1)/totsuc*100))
		print('Con dz<0.1 o dxy< 0.05: ')
		print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(2)/totsuc*100))
		print('Con muones con una masa >15 GeV: ')
		print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(3)/totsuc*100))
		print('Con muones tight y sin pico del Z: ')
		print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(4)/totsuc*100))
		print('Con el aislamiento menor que 0.15 (todas): ') #aislamiento
		print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(5)/totsuc*100))

		
		print('------------') 
		print('Electrones')
		print('Número total de sucesos: ')
		print(totsuc)
		print('Porcentaje de sucesos aplicando Pt>20 (eta <2.4): ')
		print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(1)/totsuc*100))
		print('Con dz<0.1 o dxy < 0.05: ')
		print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(2)/totsuc*100))
		print('Sin pico del Z (75 < M < 105) y aislamiento < 0.15: ')
		print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(3)/totsuc*100))
		print('Con tight Cut_based (>=4): ')
		print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(4)/totsuc*100))
		print('Con la masa > 20 GeV(todas): ')
		print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(5)/totsuc*100))


		#prints
		#da error al correr DY y TT juntos
		if self.outname=='TT_TuneCP5up':
			#print para los muones
			sys.stdout=open('estad_muones_suma_TT.txt','w')
			print('----------------------------') #está duplicado para que aparezca también por pantalla aparte de guardarse
			print('Muones')
			print('Número total de sucesos: ')
			print(totsuc)
			print('Porcentaje de sucesos aplicando Pt>20 (eta < 2.4): ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(1)/totsuc*100))
			print('Con dz<0.1 o dxy< 0.05: ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(2)/totsuc*100))
			print('Con muones con una masa >15 GeV: ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(3)/totsuc*100))
			print('Con muones tight y sin pico del Z: ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(4)/totsuc*100))
			print('Con el aislamiento menor que 0.15 (todas): ') 
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(5)/totsuc*100))

			
			sys.stdout.close()
			
			
			#print para los electrones
			sys.stdout=open('estad_electrones_suma_TT.txt','w')
			
			print('------------') 
			print('Electrones')
			print('Número total de sucesos: ')
			print(totsuc)
			print('Porcentaje de sucesos aplicando Pt>20 (eta <2.4): ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(1)/totsuc*100))
			print('Con dz<0.1 o dxy < 0.05: ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(2)/totsuc*100))
			print('Sin pico del Z (75 < M < 105) y aislamiento < 0.15: ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(3)/totsuc*100))
			print('Con tight Cut_based (>=4): ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(4)/totsuc*100))
			print('Con la masa > 20 GeV(todas): ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(5)/totsuc*100))
			
			sys.stdout.close()
			
		elif self.outname=='DYJetsToLL_MLL50':
			#print para los muones
			sys.stdout=open('estad_muones_suma_DY.txt','w')
			print('----------------------------') #está duplicado para que aparezca también por pantalla aparte de guardarse
			print('Muones')
			print('Número total de sucesos: ')
			print(totsuc)
			print('Porcentaje de sucesos aplicando Pt>20 (eta < 2.4): ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(1)/totsuc*100))
			print('Con dz<0.1 o dxy< 0.05: ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(2)/totsuc*100))
			print('Con muones con una masa >15 GeV: ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(3)/totsuc*100))
			print('Con muones tight y sin pico del Z: ')
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(4)/totsuc*100))
			print('Con el aislamiento menor que 0.15 (todas): ') 
			print('%1.2f' %(self.obj['eficienciasmu'].GetBinContent(5)/totsuc*100))
		
			
			sys.stdout.close()
			
			
			#print para los electrones
			sys.stdout=open('estad_electrones_suma_DY.txt','w')
				
			print('------------') 
			print('Electrones')
			print('Número total de sucesos: ')
			print(totsuc)
			print('Porcentaje de sucesos aplicando Pt>20 (eta <2.4): ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(1)/totsuc*100))
			print('Con dz<0.1 o dxy < 0.05: ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(2)/totsuc*100))
			print('Sin pico del Z (75 < M < 105) y aislamiento < 0.15: ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(3)/totsuc*100))
			print('Con tight Cut_based (>=4): ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(4)/totsuc*100))
			print('Con la masa > 20 GeV(todas): ')
			print('%1.2f' %(self.obj['eficienciaselec'].GetBinContent(5)/totsuc*100))
			
			sys.stdout.close()
	
