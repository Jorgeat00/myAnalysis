# -*- coding: utf-8 -*-
'''
 Analysis myAnalysis, created by xuAnalysis
 https://github.com/GonzalezFJR/xuAnalysis
'''
#cambios --> buscar cambio
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
		self.CreateTH1F("InvMassmu", "m_{#mu#mu} (GeV)", 30, 1.00, 200.00)
		self.CreateTH1F("Ptmuon", "Pt_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		
		for i in range(5):
			self.CreateTH1F("InvMassm%d" %(i+1), "m_{ee} (GeV)", 20, 0.00, 200.00)
			self.obj["InvMassm%d" %(i+1)].GetXaxis().SetTitle('Masa') #ejes
		
		#electrones
		self.CreateTH1F("InvMass", "m_{ee} (GeV)", 20, 0.00, 200.00) #20 en general y 25 al poner un limite a la masa menor
		self.obj['InvMass'].GetXaxis().SetTitle('Masa') #ejes
		for i in range(5):
			self.CreateTH1F("InvMass%d" %(i+1), "m_{ee} (GeV)", 20, 0.00, 200.00)
			self.obj["InvMass%d" %(i+1)].GetXaxis().SetTitle('Masa') #ejes
			
		self.CreateTH1F("MT", "MT_{ee}(GeV)", 20, 0.00, 200.00)
		self.CreateTH1F("Pt", "Pt_{ee}(GeV)", 20, 0.00, 300.00)
		#self.CreateTH1F("Dphi", "#Delta#phi_{ee}", 20, 0.00, 300.00)
		#self.CreateTH1F("Phi", "phi", 20, -3.00, 4.00)
		self.CreateTH1F("etamuon", "#eta", 20, -4.00, 4.00)
		
		
		#histogramas de los jets
		self.CreateTH1F("nJets", "n Jets", 20, 0,20.00)
		self.obj['nJets'].GetXaxis().SetTitle('nJets') #ejes
		self.CreateTH1F('jetpt','Pt de los jets',20,0,300.0)
		self.CreateTH1F('nsucjets','no de sucesos en funcion de los jets',5,2,7)
		#self.obj['nsucjets'].GetXaxis().CenterLabels() #no funciona exactamente
		
		
		#leptones
		self.CreateTH1F("Ptlep", "Pt_{lep} (GeV)", 20, 0.00, 300.00)
		self.CreateTH1F('InvMasslep','m_{lep}',20,0.0,300.0)

		
		#varios
		self.CreateTH1F('METpt','momento MET',20, 0.00, 300.00)
		
		#histogramas para los distintos canales de desintegración
		self.CreateTH1F("InvMassmumulep", "m_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("InvMasseelep", "m_{ee}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F('InvMassemulep','masa inv e#mu',20, 0.00, 300.00)
		
		#histogramas para almacenar las variables de los datos
		self.CreateTH1F("peso", "EventWeight",1, 0.00, 2.00)
		self.CreateTH1F("sucesos", "nEvents",1, 0.00, 2.00)
		self.CreateTH1F("sumpesos", "nSumOfWeights",1, 0.00, 2.00)
		self.CreateTH1F("nelectrones", "nelec",1, 0.00, 2.00)
		self.CreateTH1F("nmuones", "nmu",1, 0.00, 2.00)

		#prueba para el número de sucesos
		self.CreateTH1F("histprueba", "Sucesos para cada canal",3,0,3)
		self.obj['histprueba'].GetXaxis().SetBinLabel(3,'ee') #sirve para poner otro nombre a los bins
		self.obj['histprueba'].GetXaxis().SetBinLabel(2,'#mu#mu')
		self.obj['histprueba'].GetXaxis().SetBinLabel(1,'e#mu')
		self.obj['histprueba'].GetXaxis().SetLabelSize(0.1)
		
		
		#contadores del número de muones y electrones
		self.totM=0 #número total de muones (nMuon)
		self.totE=0 #número total de electrones (nElectron)
		self.nlep=0 #número de muones+ número de electrones
		#self.leptones=[]
	
	
	def insideLoop(self,t):
		# WRITE YOU ANALYSIS HERE
		#muones
		self.peso=self.EventWeight
		self.muons = []
		for i in range(t.nMuon):
			p = TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i], t.Muon_mass[i])
			charge = t.Muon_charge[i]
			dxy = abs(t.Muon_dxy[i]) 
			dz  = abs(t.Muon_dz[i] )
			eta=p.Eta()
			
			
			self.muons.append(fun.lepton(p, charge, 13)) # 13 for muons
			invmass = fun.InvMass(self.muons[0], self.muons[1]) if len(self.muons) >= 2 else 0

			#if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			#if dz > 0.1 or dxy > 0.05: continue # Tight IP
			#if not t.Muon_tightId[i]: continue # Tight ID
			#if not t.Muon_pfRelIso04_all[i] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
			#if invmass <15: continue
			#if invmass >75 and invmass <105: continue
			self.obj['InvMassmu'].Fill(invmass)
			self.obj['Ptmuon'].Fill(t.Muon_pt[i])
			self.obj['etamuon'].Fill(eta)
			
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
			
			
			self.electrons.append(fun.lepton(p, charge, 11)) # 13 for muons
			invmass = fun.InvMass(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			masat= fun.MT(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			#dphi=fun.DeltaPhi(self.electrons[0], self.electrons[1]) if len(self.electrons) >= 2 else 0
			pt=t.Electron_pt[j]
	
			
			# Filling the histograms
			#self.obj['InvMass'].Fill(invmass, self.EventWeight) #al ponerlo con el peso hay que añadir .Sumw2(0)
			#self.obj['InvMass'].Sumw2(0)
			self.obj['InvMass'].Fill(invmass)
			
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
					if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
					if invmass < 105 and invmass >75: continue #cambia poco con esto
					
				elif i==3:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05 : continue # Tight IP
					if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
					if invmass < 105 and invmass >75: continue #cambia poco con esto
					if not t.Electron_cutBased[j] >= 4: continue #cambio
					#if invmass <15: continue
				elif i==4:
					if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
					if dz > 0.1 or dxy > 0.05 : continue # Tight IP
					if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
					if invmass < 105 and invmass >75: continue #cambia poco con esto
					if not t.Electron_cutBased[j] >= 4: continue #cambio
					if invmass <15: continue
					
				

				
				self.obj['InvMass%d' %(i+1)].Fill(invmass)
			
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
			#if not t.Electron_tightCharge[j]: continue
			if not t.Electron_cutBased[j] >= 4: continue #cambio 
			if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			self.leptones.append(fun.lepton(v,t.Electron_charge[j],11))
			self.nlep +=1
			
		
		leps = self.leptones #ordena por el pt, por si acaso tiene que ver
		pts  = [lep.Pt() for lep in leps]
		self.leptones = [lep for _,lep in sorted(zip(pts,leps))]
		self.leptones.reverse()
		
		#jets 
		self.jets=[]
		for i in range(t.nJet): 
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Jet_pt[i], t.Jet_eta[i], t.Jet_phi[i],t.Jet_mass[i])
			jetid=t.Jet_jetId[i]
			if not jetid >2: continue #esto quita muchos jets (con 4 quedan mayormente 2 jets)
			if p.Pt() <25 or abs(p.Eta()) > 2.4: continue
			#if  t.Jet_btagDeepFlavB[i] <0.3: continue #estas condiciones al parecer no van a hacer falta (poca estadística)
			self.jets.append(fun.jet(p))
			njet=t.nJet
			self.obj['nJets'].Fill(njet,self.peso)
			self.obj['nJets'].Sumw2(0)
			self.obj['jetpt'].Fill(p.Pt(),self.peso)
			self.obj['jetpt'].Sumw2(0)
			
		
		pt = [v.Pt() for v in self.jets] #ordena por el pt los jets
		self.jets = [j for _,j in sorted(zip(pt,self.jets))]
		
		if len(self.leptones) ==2: #cambio
			if len(self.jets)>=2:
				invmass=fun.InvMass(self.leptones[0], self.leptones[1]) 
				if invmass <20: return #cambio
				if self.leptones[0].charge*self.leptones[1].charge >0: return
				self.pt=self.leptones[0].Pt()
				self.obj['Ptlep'].Fill(self.pt,self.peso)
				self.obj['Ptlep'].Sumw2(0)
				
				self.obj['InvMasslep'].Fill(invmass,self.peso)
				self.obj['InvMasslep'].Sumw2(0)
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
						self.obj['histprueba'].Fill(0)
						self.obj['InvMassemulep'].Fill(invmass,self.peso)
						self.obj['InvMassemulep'].Sumw2(0)
						
				if self.leptones[0].pdgid+self.leptones[1].pdgid==26: # mu+mu
				 
					self.obj['histprueba'].Fill(1)
					if invmass < 105 and invmass> 75:
						self.obj['InvMassmumulep'].Fill(invmass,self.peso)
						self.obj['InvMassmumulep'].Sumw2(0)
				if self.leptones[0].pdgid+self.leptones[1].pdgid==22: #e+e
					self.obj['histprueba'].Fill(2)
					if invmass < 105 and invmass> 75:
						self.obj['InvMasseelep'].Fill(invmass,self.peso)
						self.obj['InvMasseelep'].Sumw2(0)

				
				
		
		
		#prueba MET
		ptm=t.MET_pt
		self.obj['METpt'].Fill(ptm)
		
		#se rellenan los histogramas con variables para calcular el peso (o relacionadas con él)
		self.obj['peso'].SetBinContent(1,self.EventWeight)
		self.obj['sucesos'].SetBinContent(1,self.nEvents)
		self.obj['sumpesos'].SetBinContent(1,self.nSumOfWeights)
		self.obj['nmuones'].SetBinContent(1,self.totM)
		self.obj['nelectrones'].SetBinContent(1,self.totE)
	
	
	
	
############################prints

	def log(self): #imprime cosas despues del bucle
		
		todasm=0
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
		
		#electrones
		#número de sucesos para cada condición
		todas=0
		cpt=self.obj['InvMass1'].GetEntries()
		cdz=self.obj['InvMass2'].GetEntries()
		cdxy=self.obj['InvMass3'].GetEntries()
		ctight=self.obj['InvMass4'].GetEntries()
		creliso=self.obj['InvMass5'].GetEntries()
		suc=[todas,cpt,cdz,cdxy,ctight,creliso]
		#total=self.getInputs(self)[0][1] #valor total de sucesos analizados (del .cfg)
		total=self.totE
		porcen=[]
		for i in suc: porcen.append(i/total*100. )
		
		print('--------------------------------')
		print('número de sucesos para los diferentes canales de desintegración')
		print('Sucesos totales: ')
		print(self.getInputs(self)[0][1])
		print('Sucesos de e mu: ')
		print(self.obj['histprueba'].GetBinContent(1))
		print('Sucesos de mumu: ')
		print(self.obj['histprueba'].GetBinContent(2))
		print('Sucesos de ee: ')
		print(self.obj['histprueba'].GetBinContent(3))
		
		
		
		'''
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
		
		#print(self.xsec*302*self.nEvents/self.nSumOfWeights)
		print(self.xsec*302*self.EventWeight*10000)

		'''
		#print(self.obj['histprueba'].GetBinContent(1)) #lo saca del if sin for

		
		#prints
		#da error al correr DY y TT juntos
		if self.outname=='TT_TuneCP5up':
			#print para los muones
			sys.stdout=open('estad_muones_nuevo_TT.txt','w')
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
			print('Con el aislamiento menor que 0.15 (todas): ') #aislamiento
			print('%1.2f' %(porcenm[5]))
			print('Sucesos sin condiciones (menos muones que sucesos totales): ')
			print('%1.2f' %(porcenm[0]))
			
			sys.stdout.close()
			
			
			#print para los electrones
			sys.stdout=open('estad_electrones_nuevo_TT.txt','w')
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
			print('Con el aislamiento menor que 0.15 (todas): ')
			print('%1.2f' %(porcen[5]))
			print('Sucesos sin condiciones (más electrones que sucesos totales: ')
			print('%1.2f' %(porcen[0]))
				
			sys.stdout.close()
			
		elif self.outname=='DYJetsToLL_MLL50':
			#print para los muones
			sys.stdout=open('estad_muones_nuevo_DY.txt','w')
			
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
			print('Con el aislamiento menor que 0.15 (todas): ') #aislamiento
			print('%1.2f' %(porcenm[5]))
			print('Sucesos sin condiciones (menos muones que sucesos totales): ')
			print('%1.2f' %(porcenm[0]))
			
			
			sys.stdout.close()
			
			
			#print para los electrones
			sys.stdout=open('estad_electrones_nuevo_DY.txt','w')
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
			print('Con el aislamiento menor que 0.15 (todas): ')
			print('%1.2f' %(porcen[5]))
			print('Sucesos sin condiciones (más electrones que sucesos totales): ')
			print('%1.2f' %(porcen[0]))
			
			sys.stdout.close()
		
