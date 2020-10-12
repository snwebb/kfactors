#!/usr/bin/env python3
import ROOT
import sys
import os
from math import sqrt
import subprocess

filelist = []
outdir = "plots/" + sys.argv[2] + "/"
subprocess.call("mkdir -p " + outdir,shell=True)

#fin = ROOT.TFile.Open(sys.argv[1])
ROOT.gStyle.SetOptStat(0)

#di="kfactors_shape"
uncerts = ["Corr-Renorm-Up","Corr-Renorm-Down","Corr-Fact-Up","Corr-Fact-Down","Uncorr-Renorm-Up","Uncorr-Renorm-Down","Uncorr-Fact-Up","Uncorr-Fact-Down"]
#cols = [1,1,2,2,4,4,6,6]
cols = [1,2,4,6]
base = "WZRatio"

#fcol=[ROOT.kGray,ROOT.kGray,ROOT.kRed-9,ROOT.kRed-9,ROOT.kAzure+6,ROOT.kAzure+6,ROOT.kMagenta+2,ROOT.kMagenta+2]
fcol=[ROOT.kGray,ROOT.kRed-9,ROOT.kAzure+6,ROOT.kMagenta+2]

# haxis = ROOT.TH1D("base",";Boson p_{T} GeV; W/Z ratio [syst] / W/Z ratio[nominal]",1,0,1000)
# haxis.SetTitle("")
# haxis.Draw("axis")


can = ROOT.TCanvas("c","c",800,600)
# haxis.Draw("axis")


def loadHists(infile,allhists,bins):

    filelist.append(ROOT.TFile.Open(sys.argv[1]+"/"+infile + ".root","READ"))
    fin = filelist[-1]
    
    for i,uncert in enumerate(uncerts):
        h2d = fin.Get("%s"%(uncert))
        temp = []
        for b,binn in enumerate(bins):
            h = h2d.ProjectionX("proj_" + str(binn) + "_" + uncert ,binn,binn )
            h.SetLineColor(cols[i])
            h.SetMarkerColor(cols[i])
            h.SetMarkerSize(1)
            h.SetMarkerStyle(21)
            #h.SetFillColorAlpha(fcol[i],0.5)
            temp.append(h)


        allhists.append(temp)
            
def plotUncertainty(allhists,bins,name,maxi=None,mini=None,logy=False,plotsum=False):

    allhists_swap = list(zip(*allhists))
    leg = ROOT.TLegend(0.5,0.6,0.87,0.87)
    leg.SetBorderSize(0)

    for b,hists in enumerate(allhists_swap):

        FirstDrawn = 0
        Sum = hists[0].Clone("Sum_"+hists[0].GetName())
        Sum.Reset()
        for hist in hists:
            Sum.Add(hist)
        for i,hist in enumerate(hists):
            
            #labs1,labs2,labs3 = uncerts[i].split("-")[1], uncerts[i].split("-")[2], uncerts[i].split("-")[0]
            #labs1,labs2 = uncerts[i].split("-")[0], uncerts[i].split("-")[1]
            labs1,labs2 = uncerts[i].split("/")[0], uncerts[i].split("/")[1]
            leg.AddEntry(hist,"%s %s"%(labs1,labs2),"pl")
            if (i==0):
                FirstDrawn = hist
                hist.Draw("HIST")
            else:hist.Draw("HISTSAME")
            if maxi != None:
                FirstDrawn.SetMaximum(maxi)
            else:
                FirstDrawn.SetMaximum(hist.GetBinContent(hist.GetMaximumBin())*10)
            if mini != None:
                FirstDrawn.SetMinimum(mini)

            hist.SetTitle(";Boson p_{T} GeV;W/Z ratio [syst] / W/Z ratio[nominal]")

            ROOT.gPad.SetLogy(logy)

        if ( plotsum ):
            Sum.Draw("HISTSAME")
        leg.Draw()
        can.SetTicky()
        can.SetTickx()
        can.RedrawAxis()

        can.SaveAs(outdir + name + "_flav_"+bins[b]+".pdf")
        can.SaveAs(outdir + name + "_flav_"+bins[b]+".png")
        can.Clear()
        leg.Clear()


#Calculate uncertainty, and create "Scale Up" and "Scale Down" hists

# allh = []
# infile = "2D-wz-ratio-uncertainty"
# bins_vbf= ["200_500","500_1000","1500_5000"]
# bins = [2,3,5]
# loadHists(infile,allh,bins)
# plotUncertainty(allh,bins_vbf,"standard")

infile = "2D-wz-ratio-uncertainty-split"
bins_vbf= ["200_500","500_1000","1500_5000"]
bins = [2,3,5]

allh = []
uncerts = ["light/WZRatioFlavourSep-Renorm-Up","light/WZRatioFlavourSep-Renorm-Down","light/WZRatioFlavourSep-Fact-Up","light/WZRatioFlavourSep-Fact-Down"]
loadHists(infile,allh,bins)
plotUncertainty(allh,bins_vbf,"light",maxi=1.1,mini=0.95)

allh = []
uncerts = ["heavy-w/WZRatioFlavourSep-Renorm-Up","heavy-w/WZRatioFlavourSep-Renorm-Down","heavy-w/WZRatioFlavourSep-Fact-Up","heavy-w/WZRatioFlavourSep-Fact-Down"]
loadHists(infile,allh,bins)
plotUncertainty(allh,bins_vbf,"heavy-w",maxi=1.1,mini=0.95)

allh = []
uncerts = ["heavy-z/WZRatioFlavourSep-Renorm-Up","heavy-z/WZRatioFlavourSep-Renorm-Down","heavy-z/WZRatioFlavourSep-Fact-Up","heavy-z/WZRatioFlavourSep-Fact-Down"]
loadHists(infile,allh,bins)
plotUncertainty(allh,bins_vbf,"heavy-z",maxi=1.1,mini=0.95)





#infile = "FlavourScaleUncertainty"
# allh = []
# uncerts = ["z-heavy/Z-Nominal","z-light/Z-Nominal"]
# loadHists(infile,allh,bins)
# plotUncertainty(allh,bins_vbf,"z",logy=True,plotsum=True)
# allh = []
# uncerts = ["w-heavy/W-Nominal","w-light/W-Nominal"]
# loadHists(infile,allh,bins)
# plotUncertainty(allh,bins_vbf,"w",logy=True,plotsum=True)




# allh = []
# uncerts = ["FlavourSep-Fact-Up","FlavourSep-Fact-Down","Corr-Fact-Up","Corr-Fact-Down","Uncorr-Fact-Up","Uncorr-Fact-Down","Wup-Fact-Up","Wup-Fact-Down"]
# loadHists(infile,allh,bins)
# plotUncertainty(allh,bins_vbf,"fact",maxi=1.2,mini=0.9)


#Draw Plots

