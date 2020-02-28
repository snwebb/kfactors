#!/usr/bin/env python3
import ROOT
import sys
from math import sqrt
fin = ROOT.TFile.Open(sys.argv[1])
ROOT.gStyle.SetOptStat(0)

di="kfactors_shape"
#bins = ["200_500","500_1000","1500_5000"]
#uncerts = ["","_Renorm_Up","_Renorm_Down","_Fact_Up","_Fact_Down","_PDF_Up","_PDF_Down"]
uncerts = ["Corr-Renorm-Up","Corr-Renorm-Down","Corr-Fact-Up","Corr-Fact-Down","Uncorr-Renorm-Up","Uncorr-Renorm-Down","Uncorr-Fact-Up","Uncorr-Fact-Down"]

#uncerts = ["Wup-Renorm-Up","Wup-Renorm-Down","Wup-Fact-Up","Wup-Fact-Down","Zup-Renorm-Up","Zup-Renorm-Down","Zup-Fact-Up","Zup-Fact-Down"]
cols = [1,1,2,2,4,4,6,6]
base = "WZRatio"

fcol=[ROOT.kGray,ROOT.kGray,ROOT.kRed-9,ROOT.kRed-9,ROOT.kAzure+6,ROOT.kMagenta+2,ROOT.kMagenta+2]

haxis = ROOT.TH1D("base",";Boson p_{T} GeV; W/Z ratio [syst] / W/Z ratio[nominal]",1,0,1000)
#haxis.GetXaxis().SetTitle("Boson p_{T} GeV")
#haxis.GetYaxis().SetTitle("NLO/LO k-factor")
haxis.SetTitle("")
haxis.Draw("axis")

allh = []
scaleup = []
pdfup = []
totalup = []
scaledown = []
pdfdown = []
totaldown = []


can = ROOT.TCanvas("c","c",800,600)
haxis.Draw("axis")
haxis.SetMaximum(1.5)
haxis.SetMinimum(0.7)

leg = ROOT.TLegend(0.5,0.6,0.87,0.87)
leg.SetBorderSize(0)

  
def suminQuad(lists): 
  h0 = lists[0]
  v = [0 for b in range(h0.GetNbinsX())]
  for h in lists[1:]:
     for b in range(h0.GetNbinsX()): 
       v[b]+=(abs(h.GetBinContent(b+1)-h0.GetBinContent(b+1)))**2
  
  v = [vv**0.5 for vv in v]
  for b in range(h0.GetNbinsX()): 
#    h0.SetBinError(b+1,v[b])
      h0.SetBinContent(b+1,h0.GetBinContent(b+1)+v[b])

#cols = cols[:len(bins)]
for i,uncert in enumerate(uncerts):

    h = fin.Get("%s/%s%s"%(di,base,uncert))
    h.SetLineColor(cols[i])
    h.SetMarkerColor(cols[i])
    h.SetMarkerSize(1)
    h.SetMarkerStyle(21)
#    h.SetFillColorAlpha(fcol[i],0.5)
    allh.append(h)

#Calculate uncertainty, and create "Scale Up" and "Scale Down" hists
  
    labs1,labs2,labs3 = uncerts[i].split("-")[1], uncerts[i].split("-")[2], uncerts[i].split("-")[0]
    leg.AddEntry(h,"%s %s %s"%(labs1,labs2,labs3),"pl")

for i,hist in enumerate(allh):
    hist.Draw("HISTSAME")
#    hist.GetXaxis().SetRangeUser(180,1000)
       
leg.Draw()
can.SetTicky()
can.SetTickx()
can.RedrawAxis()
#can.SaveAs("%s.pdf"%fin.GetName())

can.SaveAs("wz_1.pdf")
can.SaveAs("wz_1.png")
# can.SaveAs("wz_2.pdf")
# can.SaveAs("wz_2.png")
# can.SaveAs("%s.pdf"%sys.argv[1])
# can.SaveAs("%s.png"%sys.argv[1])

