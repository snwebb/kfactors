import ROOT
import sys
from math import sqrt
fin = ROOT.TFile.Open(sys.argv[1])
ROOT.gStyle.SetOptStat(0)

di="kfactors_shape"
bins = ["200_500","500_1000","1500_5000"]
uncerts = ["","_Renorm_Up","_Renorm_Down","_Fact_Up","_Fact_Down","_PDF_Up","_PDF_Down"]

base = "kfactor_vbf_mjj_"
cols = [1,2,4]
fcol=[ROOT.kGray,ROOT.kRed-9,ROOT.kAzure+6]

haxis = ROOT.TH1D("base",";Boson p_{T} GeV;NLO/LO k-factor",1,0,1000)
haxis.GetXaxis().SetTitle("Boson p_{T} GeV")
haxis.GetYaxis().SetTitle("NLO/LO k-factor")
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
haxis.SetMaximum(2.0)
haxis.SetMinimum(0.5)

leg = ROOT.TLegend(0.5,0.6,0.87,0.87)
leg.SetBorderSize(0)

def calculateUncertainty(lists):
    
    for i in range(3):
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
        
  #loop over bins edges again
  #get the up hists, take the difference to nominal and add to a clone of the original
  #same for the down

  #  append to the correct list

  

  
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

for uncert in uncerts:
  temp = []
  for i,c in enumerate(cols): 


    h = fin.Get("%s%s/%s%s"%(di,uncert,base,bins[i]))
    h.SetLineColor(c)
    h.SetMarkerColor(c)
    h.SetMarkerSize(1)
    h.SetMarkerStyle(21)
    temp.append(h)
    # suminQuad([h,fin.Get("kfactors_shape_Renorm_Down/%s%s"%(base,bins[i])),fin.Get("kfactors_shape_Fact_Down/%s%s"%(base,bins[i]))])
 
    h.SetFillColorAlpha(fcol[i],0.5)
    # h.Draw("PE2Lsame")
    # h.Draw("PLsame")

    # labs1,labs2 = bins[i].split("_")[0], bins[i].split("_")[1]
    # leg.AddEntry(temp[-1],"%s < m_{jj} < %s GeV"%(labs1,labs2),"fpel")
  allh.append(temp)

#Calculate uncertainty, and create "Scale Up" and "Scale Down" hists

calculateUncertainty(allh)



for i,hist in enumerate(allh[0]):
  
    labs1,labs2 = bins[i].split("_")[0], bins[i].split("_")[1]
    leg.AddEntry(hist,"%s < m_{jj} < %s GeV"%(labs1,labs2),"fpel")

    total = True;
    up = 7
    down = 8
    if ( total ):
        up = 9
        down = 10

    allh[up][i].Draw("HISTsame")
    hist.Draw("PSAME")
    allh[down][i].SetFillColor(10)
    allh[down][i].Draw("HISTsame")

  
  # allh[7][i].SetFillColorAlpha(fcol[i],0.6)
  # allh[8][i].SetFillColorAlpha(fcol[i],0.6)
  # allh[9][i].SetFillColorAlpha(fcol[i],0.3)
#  allh[7][i].Draw("HISTsame")
#  allh[7][i].Draw("HISTsame")
#  hist.Draw("PSAME")

#  allh[8][i].Draw("HISTsame")
#  allh[8][i].SetFillColor(10)
#  allh[8][i].Draw("HISTsame")
  #hist.Draw("PE2Lsame")
  #hist.Draw("PLsame")
   
leg.Draw()
can.SetTicky()
can.SetTickx()
can.RedrawAxis()
can.SaveAs("%s.pdf"%fin.GetName())

