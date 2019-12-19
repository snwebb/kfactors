import ROOT
import sys, os
from math import sqrt
#fin = ROOT.TFile.Open("input/"+sys.argv[1])
outdir = "plots/"+sys.argv[2]
if os.path.exists(outdir) == False:
    os.mkdir(outdir) 
fin = ROOT.TFile.Open(sys.argv[1],"READ")

ROOT.gStyle.SetOptStat(0)

di="kfactors_shape"
bins = ["200_500","500_1000","1500_5000"]
#bins = ["200_500"]
uncerts = ["","_Renorm_Up","_Renorm_Down","_Fact_Up","_Fact_Down","_PDF_Up","_PDF_Down"]
cols = [1,2,4]
base = "kfactor_vbf_mjj_"


fcol=[ROOT.kGray,ROOT.kRed-9,ROOT.kAzure+6]

# haxis = ROOT.TH1D("base",";Boson p_{T} GeV;NLO/LO k-factor",1,0,1000)
# haxis.GetXaxis().SetTitle("Boson p_{T} GeV")
# haxis.GetYaxis().SetTitle("NLO/LO k-factor")
# haxis.SetTitle("")
# haxis.Draw("axis")

allh = []
scaleup = []
pdfup = []
totalup = []
scaledown = []
pdfdown = []
totaldown = []

#can = ROOT.TCanvas("c","c",800,600)
def setupCanvas(canvas, haxis, xtitle = "Boson p_{T} GeV", ytitle = "NLO/LO k-factor", ymax = 2.0, ymin = 0.4):

    haxis.GetXaxis().SetTitle(xtitle)
    haxis.GetYaxis().SetTitle(ytitle)
    haxis.SetTitle("")
    haxis.Draw("axis")
    haxis.SetMaximum(ymax)
    haxis.SetMinimum(ymin)
    canvas.SetTicky()
    canvas.SetTickx()
    return canvas

leg = ROOT.TLegend(0.5,0.6,0.87,0.87)
leg.SetBorderSize(0)

def setLegendXY(leg,x1,y1,x2,y2):
    leg.SetX1(x1)
    leg.SetX2(x2)
    leg.SetY1(y1)
    leg.SetY2(y2)
    return leg

def calculateUncertainty(lists):
    
    for i in range(len(bins)):
        uncert = list(zip(*lists))[i]
        scale_up = uncert[0].Clone()
        scale_down = uncert[0].Clone()
        total_up = uncert[0].Clone()
        total_down = uncert[0].Clone() 
        for b in range(uncert[0].GetNbinsX()+1):

            v_nom = uncert[0].GetBinContent(b)
            v_r_up = uncert[1].GetBinContent(b)
            v_r_down = uncert[2].GetBinContent(b)
            v_f_up = uncert[3].GetBinContent(b)
            v_f_down = uncert[4].GetBinContent(b)
            v_p_up = uncert[5].GetBinContent(b)
            v_p_down = uncert[6].GetBinContent(b)
            
            v_scale_down = sqrt( (v_r_up-v_nom)**2 + (v_f_up-v_nom)**2 )
            v_scale_up = sqrt( (v_r_down-v_nom)**2 + (v_f_down-v_nom)**2 )#down causes the k-factor to reduce, so swap arbitrary meaning

            v_total_up = sqrt( (v_p_up-v_nom)**2 + (v_scale_down)**2 )
            v_total_down = sqrt( (v_p_down-v_nom)**2 + (v_scale_up)**2 )
                          
            scale_up.SetBinContent( b, v_nom + v_scale_up )
            scale_down.SetBinContent( b, v_nom - v_scale_down )
            total_up.SetBinContent( b, v_nom + v_total_up )
            total_down.SetBinContent( b, v_nom - v_total_down )

        scaleup.append ( scale_up )
        scaledown.append ( scale_down )
        totalup.append ( total_up )
        totaldown.append ( total_down )

    lists.append(scaleup)
    lists.append(scaledown)
    lists.append(totalup)
    lists.append(totaldown)
        

def getUncertaintyRatios(hists,region):

    default = list(zip(*hists))[region]
    ratios = []
#    for i in range (1,7):
    for i in range (7):
        uncert = default[i].Clone("uncert"+str(i))
        if (i != 0):
            uncert.Divide(default[0])
        uncert.SetFillColor(0)
        colour = i;
        if ( colour == 5 ):
            colour = 9
        uncert.SetLineColor(colour)
        uncert.SetMarkerColor(colour)
        ratios.append(uncert)

    return ratios
    
  
#Draw standard k-factor plots
def drawStandardKFactorPlots(hists):

    haxis = ROOT.TH1D("base",";Boson p_{T} GeV;NLO/LO k-factor",1,0,1000)
    can = ROOT.TCanvas("c","c",800,600)
    can = setupCanvas(can, haxis, ymin = 0.4, ymax = 2.0)
    for i,hist in enumerate(hists[0]):
  
        labs1,labs2 = bins[i].split("_")[0], bins[i].split("_")[1]
        leg.AddEntry(hist,"%s < m_{jj} < %s GeV"%(labs1,labs2),"fpel")

        total = True;
        up = 7
        down = 8
        if ( total ):
            up = 9
            down = 10

        hists[up][i].Draw("HISTsame")
        hist.Draw("PSAME0")
        hists[down][i].SetFillColor(10)
        hists[down][i].Draw("HISTsame")
        hist.Draw("PSAME0")

    for i,hist in enumerate(hists[0]):
        hist.Draw("PSAME0")


    leg.Draw()
    can.RedrawAxis()

    can.SaveAs("plots/%s/%s.pdf"%(sys.argv[2],(sys.argv[1]).rsplit("/",1)[-1]))
    can.SaveAs("plots/%s/%s.png"%(sys.argv[2],(sys.argv[1]).rsplit("/",1)[-1]))

def drawUncertaintyPlots(hists):

#    default = list(zip(*hists))[0]
    leg.Clear()
    can = ROOT.TCanvas("c","c",800,600)

    haxis = ROOT.TH1D("base",";Boson p_{T} GeV;NLO/LO k-factor",1,0,1000)
    can = setupCanvas(can, haxis, ytitle = "d#sigma/dp_{T} variation", ymin = 0.6, ymax = 1.3)

 #   uncert_list = []
    # for i in range (1,7):
    #     uncert = default[i].Clone("uncert"+str(i))
    #     uncert.Divide(default[0])
    #     uncert.SetFillColor(0)
    #     colour = i;
    #     if ( colour == 5 ):
    #         colour = 9
    #     uncert.SetLineColor(colour)
    #     uncert.SetMarkerColor(colour)
    #     uncert_list.append(uncert)

    ratios = getUncertaintyRatios(hists,0)
    
    for i,hist in enumerate(ratios):
        if (i==0): continue
        hist.Draw("HISTsame")
        leg.AddEntry(hist,"%s %s"%(uncerts[i+1].split("_")[1], uncerts[i+1].split("_")[2]),"pl")
        
    setLegendXY(leg,0.55,0.13,0.8,0.35) 
    leg.Draw()
    can.SaveAs("plots/%s/k-fac-uncert.png"%sys.argv[2])
    can.SaveAs("plots/%s/k-fac-uncert.pdf"%sys.argv[2])

def appendFittedUncertaintyToFile(hists):
#
 #   default = getUncertaintyRatios(hists,0)
    
    for i,uncert in enumerate(bins):
        ratios = getUncertaintyRatios(hists,i)
        pol2 = ROOT.TF1("pol2","pol1",170,470)
        for j,hist in enumerate(ratios):
            if (j==0): continue
            hist.Fit(pol2,"LRQ0")
            for b in range(2,hist.GetNbinsX()+1):
                hist.SetBinContent(b,pol2.Eval(hist.GetBinCenter(b)))
            hist.Multiply(ratios[0])
            fin.cd("kfactors_shape" + uncerts[j])
            hist.Write( base + uncert + "_fit")
            fin.cd("..")
  
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

histtype = "_fit"
#histtype = ""
cols = cols[:len(bins)]
for uncert in uncerts:
    temp = []
    print (uncert)
    for i,c in enumerate(cols): 
        print (i) 
        print ("%s%s/%s%s%s"%(di,uncert,base,bins[i],histtype))
        h = fin.Get("%s%s/%s%s%s"%(di,uncert,base,bins[i],histtype))
        
        h.SetLineColor(c)
        h.SetMarkerColor(c)
        h.SetMarkerSize(1)
        h.SetMarkerStyle(21)
        temp.append(h)
        h.SetFillColorAlpha(fcol[i],0.5)

    allh.append(temp)


  
#Calculate uncertainty, and create "Scale Up" and "Scale Down" hists

calculateUncertainty(allh)
#drawUncertaintyPlots(allh)
drawStandardKFactorPlots(allh)




#appendFittedUncertaintyToFile(allh)

