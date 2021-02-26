#!/usr/bin/env python3
import ROOT
import sys
import os
from math import sqrt
import subprocess

filelist = []
outdir = "plots/" + sys.argv[2] + "/"
subprocess.call("mkdir -p " + outdir,shell=True)

ROOT.gStyle.SetOptStat(0)

di="kfactors_shape"
uncerts = ["Corr-Renorm-Up","Corr-Renorm-Down","Corr-Fact-Up","Corr-Fact-Down","Uncorr-Renorm-Up","Uncorr-Renorm-Down","Uncorr-Fact-Up","Uncorr-Fact-Down"]
cols = [1,1,2,2,4,4,6,6]
base = "WZRatio"

fcol=[ROOT.kGray,ROOT.kGray,ROOT.kRed-9,ROOT.kRed-9,ROOT.kAzure+6,ROOT.kAzure+6,ROOT.kMagenta+2,ROOT.kMagenta+2]

can = ROOT.TCanvas("c","c",800,600)

def loadHists(infile,allhists,bins):

    filelist.append(ROOT.TFile.Open(sys.argv[1]+"/"+infile + ".root","READ"))
    fin = filelist[-1]
    
    for i,uncert in enumerate(uncerts):
        
        h2d = fin.Get("%s/%s%s"%(di,base,uncert))
        temp = []
        for b,binn in enumerate(bins):
            h = h2d.ProjectionX("proj_" + str(binn) + "_" + uncert ,binn,binn )
            h.SetLineColor(cols[i])
            h.SetMarkerColor(cols[i])
            h.SetMarkerSize(1)
            h.SetMarkerStyle(21)
            temp.append(h)

        allhists.append(temp)
            
def plotUncertainty(allhists,bins,name,maxi=1.5,mini=0.7):

    allhists_swap = list(zip(*allhists))
    leg = ROOT.TLegend(0.5,0.6,0.87,0.87)
    leg.SetBorderSize(0)

    for b,hists in enumerate(allhists_swap):

        for i,hist in enumerate(hists):
            
            labs1,labs2,labs3 = uncerts[i].split("-")[1], uncerts[i].split("-")[2], uncerts[i].split("-")[0]
            if ( i%2 == 0):leg.AddEntry(hist,"%s %s"%(labs1,labs3),"pl")
            if (i==0):hist.Draw("HIST")
            else:hist.Draw("HISTSAME")
            hist.SetMaximum(maxi)
            hist.SetMinimum(mini)
            hist.SetTitle(";Boson p_{T} GeV;W/Z ratio [syst] / W/Z ratio[nominal]")


        leg.Draw()
        can.SetTicky()
        can.SetTickx()
        can.RedrawAxis()

        can.SaveAs(outdir + name + "_wz_"+bins[b]+".pdf")
        can.SaveAs(outdir + name + "_wz_"+bins[b]+".png")
        can.Clear()
        leg.Clear()


#Calculate uncertainty, and create "Scale Up" and "Scale Down" hists

# allh = []
# infile = "2D-wz-ratio-uncertainty"
# bins_vbf= ["200_500","500_1000","1500_5000"]
# bins = [2,3,5]
# loadHists(infile,allh,bins)
# plotUncertainty(allh,bins_vbf,"standard")

infile = "2D-wz-ratio-uncertainty"
bins_vbf= ["200_500","500_1000","1500_5000"]
bins = [2,3,5]
allh = []
uncerts = ["FlavourSep-Renorm-Up","FlavourSep-Renorm-Down","Corr-Renorm-Up","Corr-Renorm-Down","Uncorr-Renorm-Up","Uncorr-Renorm-Down","Wup-Renorm-Up","Wup-Renorm-Down"]
loadHists(infile,allh,bins)
plotUncertainty(allh,bins_vbf,"renorm",maxi=1.5,mini=0.7)

allh = []
uncerts = ["FlavourSep-Fact-Up","FlavourSep-Fact-Down","Corr-Fact-Up","Corr-Fact-Down","Uncorr-Fact-Up","Uncorr-Fact-Down","Wup-Fact-Up","Wup-Fact-Down"]
loadHists(infile,allh,bins)
plotUncertainty(allh,bins_vbf,"fact",maxi=1.2,mini=0.9)


#Draw Plots

