# -*- coding: utf-8 -*-
'''
 Analysis myAnalysis, created by xuAnalysis
 https://github.com/GonzalezFJR/xuAnalysis
'''
#cambios --> buscar cambio
import os,sys

#basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
#sys.path.append(basepath)

sys.path.append(os.path.abspath(__file__).rsplit("/xuAnalysis/",1)[0]+"/xuAnalysis/")
from framework.analysis import analysis
import framework.functions as fun
from ROOT import TLorentzVector, TCanvas, TGraph
from array import array
from modules.SFreader import SFreader

class myAnalysis(analysis):
	def init(self):    
		# Create your histograms here
		#muones
		self.CreateTH1F("Ptmuon", "Pt_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("etamuon", "#eta", 20, -4.00, 4.00)
		
		#electrones			
		self.CreateTH1F("MT", "MT_{ee}(GeV)", 20, 1.00, 300.00)
		self.CreateTH1F("MTttbar", "MT_{ee}(GeV)", 20, 1.00, 300.00)
		self.CreateTH1F("Ptelec", "Pt_{ee}(GeV)", 20, 0.00, 300.00)
		#self.CreateTH1F("Dphi", "#Delta#phi_{ee}", 20, 0.00, 300.00)
		#self.CreateTH1F("Phi", "phi", 20, -3.00, 4.00)
		
		
		#histogramas de los jets
		#canal emu
		self.CreateTH1F('jetpt','Pt de los jets',5,20,120.0)
		self.CreateTH1F('nsucjets','no de sucesos en funcion de los jets',5,2,7)
		for i in range(2,5+1): #cambia los ejes para que los números estén centrados 
			self.obj['nsucjets'].GetXaxis().SetBinLabel(i-1,'%d'%(i))
		self.obj['nsucjets'].GetXaxis().SetBinLabel(5,'#geq 6')
		self.obj['nsucjets'].GetXaxis().SetLabelSize(0.07)
		self.CreateTH1F('cnjets','no de jets',7,0,7)
		#canal mumu
		self.CreateTH1F('jetptmumu','Pt de los jets',5,20,120.0)
		self.CreateTH1F('nsucjetsmumu','no de sucesos en funcion de los jets',5,2,7)
		for i in range(2,5+1):
			self.obj['nsucjetsmumu'].GetXaxis().SetBinLabel(i-1,'%d'%(i))
		self.obj['nsucjetsmumu'].GetXaxis().SetBinLabel(5,'#geq 6')
		self.obj['nsucjetsmumu'].GetXaxis().SetLabelSize(0.07)
		self.CreateTH1F('cnjetsmumu','no de jets',7,0,7)
		#canal ee
		self.CreateTH1F('jetptee','Pt de los jets',5,20,120.0)
		self.CreateTH1F('nsucjetsee','no de sucesos en funcion de los jets',5,2,7)
		for i in range(2,5+1):
			self.obj['nsucjetsee'].GetXaxis().SetBinLabel(i-1,'%d'%(i))
		self.obj['nsucjetsee'].GetXaxis().SetBinLabel(5,'#geq 6')
		self.obj['nsucjetsee'].GetXaxis().SetLabelSize(0.07)
		self.CreateTH1F('cnjetsee','no de jets',7,0,7)
		
		#self.obj['nsucjets'].GetXaxis().CenterLabels() #no funciona exactamente
		
		#leptones
		#canal emu
		self.CreateTH1F("Ptlep2jets", "Pt_{lep} (GeV)", 5, 20.00, 120.00)
		self.CreateTH1F("Ptlep", "Pt_{lep} (GeV)", 20,0.0,300.0)
		self.CreateTH1F("Pt2lep", "Pt_{lep} (GeV)", 4,10.0,90.0)
		#canal mumu
		self.CreateTH1F("Ptlep2jetsmumu", "Pt_{lep} (GeV)", 5, 20.00, 120.00)
		self.CreateTH1F("Ptlepmumu", "Pt_{lep} (GeV)", 20,0.0,300.0)
		self.CreateTH1F("Pt2lepmumu", "Pt_{lep} (GeV)", 4,10.0,90.0)
		#canal ee
		self.CreateTH1F("Ptlep2jetsee", "Pt_{lep} (GeV)", 5, 20.00, 120.00)
		self.CreateTH1F("Ptlepee", "Pt_{lep} (GeV)", 20,0.0,300.0)
		self.CreateTH1F("Pt2lepee", "Pt_{lep} (GeV)", 4,10.0,90.0)
		#general
		self.CreateTH1F('InvMasslep','m_{lep}',20,0.0,300.0)

		
		#varios
		self.CreateTH1F('METpt','momento MET',20, 0.00, 300.00)
		
		#histogramas para los distintos canales de desintegración
		self.CreateTH1F("InvMassmumulep", "m_{#mu#mu}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F("InvMasseelep", "m_{ee}(GeV)", 20, 0.00, 300.00)
		self.CreateTH1F('InvMassemulep','m_{e#mu} (GeV)',20, 0.00, 300.00)
		
		#histogramas para almacenar las variables de los datos
		self.CreateTH1F("peso", "EventWeight",1, 0.00, 2.00)
		self.CreateTH1F("sucesos", "nEvents",1, 0.00, 2.00)
		self.CreateTH1F("sumpesos", "nSumOfWeights",1, 0.00, 2.00)

		#prueba para el número de sucesos
		self.CreateTH1F("canales", "Sucesos para cada canal",3,0,3)
		self.obj['canales'].GetXaxis().SetBinLabel(1,'e#mu') #sirve para poner otro nombre a los bins
		self.obj['canales'].GetXaxis().SetBinLabel(2,'#mu#mu')
		self.obj['canales'].GetXaxis().SetBinLabel(3,'ee') 
		self.obj['canales'].GetXaxis().SetLabelSize(0.1)
		
		#Cálculo de la eficiencia
		self.CreateTH1F("dressed", "numero de sucesos dressed para cada canal",3,0,3)
		self.obj['dressed'].GetXaxis().SetBinLabel(1,'e#mu') 
		self.obj['dressed'].GetXaxis().SetBinLabel(2,'#mu#mu')
		self.obj['dressed'].GetXaxis().SetBinLabel(3,'ee') 
		self.obj['dressed'].GetXaxis().SetLabelSize(0.1)
		
		#scale factors
		self.sfr = SFreader()
		self.sfr.LoadHisto(basepath+'inputs/',sf_tight_id.root,g_fit_eff_eta_incl) #g_eff_ratio_eta_incl
		
	def insideLoop(self,t):
		self.peso=self.EventWeight #al multiplicar por la luminosidad salen cosas mejores salvo en la masa
		if not self.isData: self.peso=self.EventWeight*302 #se debería poner la luminosidad a la hora de juntar los histogramas
		#leptones
		self.leptones=[] 
		self.muons = []
		self.leptonesgen=[]
		passTrig=True
		
		#leptones generados para el cálculo de la eficiencia
		if not self.isData:
			if 'TT' in self.outname:
				for i in range(t.nGenDressedLepton):
					a=TLorentzVector()
					a.SetPtEtaPhiM(t.GenDressedLepton_pt[i],t.GenDressedLepton_eta[i],t.GenDressedLepton_phi[i],t.GenDressedLepton_mass[i])
					pdg=abs(t.GenDressedLepton_pdgId[i])
					self.leptonesgen.append(fun.lepton(a,0,pdg))
				
				if len(self.leptonesgen)>=2:
					if self.leptonesgen[0].pdgid+self.leptonesgen[1].pdgid==24: #emu
						self.obj['dressed'].Fill(0,self.peso)
					elif self.leptonesgen[0].pdgid+self.leptonesgen[1].pdgid==26: #mumu
						self.obj['dressed'].Fill(1,self.peso)
					elif self.leptonesgen[0].pdgid+self.leptonesgen[1].pdgid==22: #ee
						self.obj['dressed'].Fill(2,self.peso)
		
		
		for i in range(t.nMuon):
			if t.nMuon >2: continue
			if t.nMuon==0 : continue
			p=TLorentzVector()
			p.SetPtEtaPhiM(t.Muon_pt[i], t.Muon_eta[i], t.Muon_phi[i],t.Muon_mass[i])
			charge = t.Muon_charge[i]
			dxy = abs(t.Muon_dxy[i]) 
			dz  = abs(t.Muon_dz[i])
			eta=p.Eta()
			if p.Pt() < 20 or abs(p.Eta()) > 2.4: continue # pt and eta cuts 
			if dz > 0.1 or dxy > 0.05: continue # Tight IP
			if not t.Muon_tightId[i]: continue # Tight ID
			if not t.Muon_pfRelIso04_all[i] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03) 
			self.leptones.append(fun.lepton(p, t.Muon_charge[i],13))
		
			self.obj['Ptmuon'].Fill(t.Muon_pt[i],self.peso)
			self.obj['etamuon'].Fill(eta,self.peso)
			
		for j in range(t.nElectron): 
			if t.nElectron >2 : continue
			if t.nElectron ==0: continue
			v=TLorentzVector()
			v.SetPtEtaPhiM(t.Electron_pt[j],t.Electron_eta[j],t.Electron_phi[j], t.Electron_mass[j])
			charge = t.Electron_charge[j]
			dxy = abs(t.Electron_dxy[j]) 
			dz  = abs(t.Electron_dz[j] )
			pt=v.Pt()
			if v.Pt() < 20 or abs(v.Eta()) > 2.4: continue
			if dz > 0.1 or dxy > 0.05 : continue # Tight IP
			#if not t.Electron_tightCharge[j]: continue
			if not t.Electron_cutBased[j] >= 4: continue #cambio
			if ord(t.Electron_lostHits[j]) > 1: continue #cambio 
			if not t.Electron_convVeto[j]: continue 
			if not t.Electron_pfRelIso03_all[j] < 0.15: continue # Tight ISO, RelIso04 < 0.15 (para los eletrones es 03)
			self.leptones.append(fun.lepton(v,t.Electron_charge[j],11))
			self.obj['Ptelec'].Fill(pt,self.peso)
			
		
		leps = self.leptones #ordena por el pt
		pts  = [lep.Pt() for lep in leps]
		self.leptones = [lep for _,lep in sorted(zip(pts,leps))]
		self.leptones.reverse()
		
		#jets 
		self.jets=[]
		for i in range(t.nJet): 
			q=TLorentzVector()
			q.SetPtEtaPhiM(t.Jet_pt[i], t.Jet_eta[i], t.Jet_phi[i],t.Jet_mass[i])
			jetid=t.Jet_jetId[i]
			if not jetid >1: continue 
			if q.Pt() <25 or abs(q.Eta()) > 2.4: continue
			#if  t.Jet_btagDeepFlavB[i] <0.3: continue #b jets
			Jets=fun.jet(q)
			if not Jets.IsClean(self.leptones, 0.4): continue #quita los jets que están cerca de un leptón en un radio de 0.4 #quita muchos sucesos de 3 jets
			'''
			isClean = True
			for lep in self.leptones:
				if lep.jetId == i: isClean = False
			if not isClean: continue
			'''
			self.jets.append(Jets)
			njet=t.nJet
		if len(self.leptones)<2: return
		ElMu= True if self.leptones[0].pdgid+self.leptones[1].pdgid==24 else False
		MuMu=True if self.leptones[0].pdgid+self.leptones[1].pdgid==26 else False
		ElEl=True if self.leptones[0].pdgid+self.leptones[1].pdgid==22 else False
		if self.isData:
			if   self.outname == 'HighEGJet':
				if   ElEl: passTrig = t.HLT_HIEle17_WPLoose_Gsf
				elif ElMu: passTrig = t.HLT_HIEle17_WPLoose_Gsf and not t.HLT_HIMu17 
				else:                passTrig = False
			elif self.outname == 'SingleMuon':
				if   MuMu: passTrig = t.HLT_HIMu17 
				elif ElMu: passTrig = t.HLT_HIMu17 
				else:                passTrig = False
			
		self.jets=fun.SortByPt(self.jets) #ordena los jets por su Pt
		MET=TLorentzVector()
		MET.SetPtEtaPhiM(t.MET_pt,0,t.MET_phi,0) #Energía faltante transversa 
		#prueba MET
		ptm=t.MET_pt
		self.obj['METpt'].Fill(ptm,self.peso)
		
		#selección de sucesos
		if not passTrig: return
		if len(self.leptones) ==2: 
			#if len(self.jets)< 2: return 
			invmass=fun.InvMass(self.leptones[0], self.leptones[1]) 
			if invmass <20: return 
			if self.leptones[0].charge*self.leptones[1].charge >0: return
			self.pt=self.leptones[0].Pt() #pt del leading lepton
			self.pt2=self.leptones[1].Pt() #pt del subleading lepton
			if len(self.jets)>=1: self.ptjet=self.jets[0].Pt() #pt del leading jet
			self.obj['InvMasslep'].Fill(invmass,self.peso)
			self.obj['InvMasslep'].Sumw2(0)
			
			if self.leptones[0].pdgid+self.leptones[1].pdgid==24:#mu + e
				if len(self.jets)==0:
					self.obj['cnjets'].Fill(0,self.peso) #esto es para comparar con DY, que solo salen 0 y 1 jets
				if len(self.jets)==1:
					self.obj['cnjets'].Fill(1,self.peso)
				if len(self.jets)==2: 
					self.obj['nsucjets'].Fill(2,self.peso) 
					self.obj['cnjets'].Fill(2,self.peso)
				if len(self.jets)==3:
					self.obj['nsucjets'].Fill(3,self.peso)
					self.obj['cnjets'].Fill(3,self.peso)
				if len(self.jets)==4:
					self.obj['nsucjets'].Fill(4,self.peso)
					self.obj['cnjets'].Fill(4,self.peso)
				if len(self.jets)==5:
					self.obj['nsucjets'].Fill(5,self.peso)
					self.obj['cnjets'].Fill(5,self.peso)
				if len(self.jets)>=6:
					self.obj['nsucjets'].Fill(6,self.peso)
					self.obj['cnjets'].Fill(6,self.peso)

				
				self.obj['InvMassemulep'].Fill(invmass,self.peso)
				self.obj['InvMassemulep'].Sumw2(0)
				self.obj['Ptlep'].Fill(self.pt,self.peso)
				self.obj['Ptlep'].Sumw2(0)
				
				masaT=fun.MT(self.leptones[0],MET) #no sé si funciona así
				self.obj['MT'].Fill(masaT,self.peso)
				self.obj['MT'].Sumw2(0)
				masaTT=fun.MT(self.leptones[0],self.jets[0]) if len(self.jets)>0 else 0 #no sé si funciona así
				self.obj['MTttbar'].Fill(masaTT,self.peso)
				self.obj['MTttbar'].Sumw2(0)
				
				if len(self.jets)>=2:
					self.obj['canales'].Fill(0,self.peso) 
					self.obj['canales'].Sumw2(0)
					self.obj['Ptlep2jets'].Fill(self.pt,self.peso)
					self.obj['Ptlep2jets'].Sumw2(0)
					self.obj['jetpt'].Fill(self.ptjet,self.peso)
					self.obj['jetpt'].Sumw2(0)
					self.obj['Pt2lep'].Fill(self.pt2,self.peso)
					self.obj['Pt2lep'].Sumw2(0)
			if self.leptones[0].pdgid+self.leptones[1].pdgid==26: # mu+mu
				if invmass < 105 and invmass> 75: return
				#if ptm <40: return #cambio
				if t.MET_sumEt<40: return #cambio
				self.obj['InvMassmumulep'].Fill(invmass,self.peso)
				self.obj['InvMassmumulep'].Sumw2(0)

				if len(self.jets)==0:
					self.obj['cnjetsmumu'].Fill(0,self.peso) #esto es para comparar con DY, que solo salen 0 y 1 jets
				if len(self.jets)==1:
					self.obj['cnjetsmumu'].Fill(1,self.peso)
				if len(self.jets)==2: 
					self.obj['nsucjetsmumu'].Fill(2,self.peso) 
					self.obj['cnjetsmumu'].Fill(2,self.peso)
				if len(self.jets)==3:
					self.obj['nsucjetsmumu'].Fill(3,self.peso)
					self.obj['cnjetsmumu'].Fill(3,self.peso)
				if len(self.jets)==4:
					self.obj['nsucjetsmumu'].Fill(4,self.peso)
					self.obj['cnjetsmumu'].Fill(4,self.peso)
				if len(self.jets)==5:
					self.obj['nsucjetsmumu'].Fill(5,self.peso)
					self.obj['cnjetsmumu'].Fill(5,self.peso)
				if len(self.jets)>=6:
					self.obj['nsucjetsmumu'].Fill(6,self.peso)
					self.obj['cnjetsmumu'].Fill(6,self.peso)
				self.obj['Ptlepmumu'].Fill(self.pt,self.peso)
				self.obj['Ptlepmumu'].Sumw2(0)
				
				if len(self.jets)>=2:
					self.obj['canales'].Fill(1,self.peso) 
					self.obj['canales'].Sumw2(0)
					self.obj['Ptlep2jetsmumu'].Fill(self.pt,self.peso)
					self.obj['jetptmumu'].Fill(self.ptjet,self.peso)
					self.obj['Pt2lepmumu'].Fill(self.pt2,self.peso)

				
			if self.leptones[0].pdgid+self.leptones[1].pdgid==22: #e+e
				if invmass < 105 and invmass> 75: return
				#if ptm<40: return #cambio
				if t.MET_sumEt<40: return #cambio
				self.obj['InvMasseelep'].Fill(invmass,self.peso)
				self.obj['InvMasseelep'].Sumw2(0)
				
				if len(self.jets)==0:
					self.obj['cnjetsee'].Fill(0,self.peso) #esto es para comparar con DY, que solo salen 0 y 1 jets
				if len(self.jets)==1:
					self.obj['cnjetsee'].Fill(1,self.peso)
				if len(self.jets)==2: 
					self.obj['nsucjetsee'].Fill(2,self.peso) 
					self.obj['cnjetsee'].Fill(2,self.peso)
				if len(self.jets)==3:
					self.obj['nsucjetsee'].Fill(3,self.peso)
					self.obj['cnjetsee'].Fill(3,self.peso)
				if len(self.jets)==4:
					self.obj['nsucjetsee'].Fill(4,self.peso)
					self.obj['cnjetsee'].Fill(4,self.peso)
				if len(self.jets)==5:
					self.obj['nsucjetsee'].Fill(5,self.peso)
					self.obj['cnjetsee'].Fill(5,self.peso)
				if len(self.jets)>=6:
					self.obj['nsucjetsee'].Fill(6,self.peso)
					self.obj['cnjetsee'].Fill(6,self.peso)
				self.obj['Ptlepee'].Fill(self.pt,self.peso)
				self.obj['Ptlepee'].Sumw2(0)
				
				if len(self.jets)>=2:
					self.obj['canales'].Fill(2,self.peso)
					self.obj['canales'].Sumw2(0)
					self.obj['Ptlep2jetsee'].Fill(self.pt,self.peso)
					self.obj['Ptlep2jetsee'].Sumw2(0)
					self.obj['jetptee'].Fill(self.ptjet,self.peso)
					self.obj['jetptee'].Sumw2(0)
					self.obj['Pt2lepee'].Fill(self.pt2,self.peso)
					self.obj['Pt2lepee'].Sumw2(0)

		
		#se rellenan los histogramas con variables para calcular el peso (o relacionadas con él)
		self.obj['peso'].Fill(self.EventWeight)
		self.obj['sucesos'].Fill(self.nEvents)
		self.obj['sumpesos'].Fill(self.nSumOfWeights)

	
	
