import ROOT
import sys, os
from math import sqrt

outdir = "plots/"+sys.argv[2]
if os.path.exists(outdir) == False:
    os.mkdir(outdir) 

filelist = []
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetImageScaling(3.)

analysis = "vbf"
di="kfactors_shape"
base = "kfactor_vbf_mjj_"
cols = [1,2,4,8]
fcol=[ROOT.kGray,ROOT.kRed-9,ROOT.kAzure+6,ROOT.kGreen-9]

uncerts = ["","_Renorm_Up","_Renorm_Down","_Fact_Up","_Fact_Down","_PDF_Up","_PDF_Down"]

allh_w_lo = []
allh_z_lo = []
allh_w_nlo = []
allh_z_nlo = []

def finaliseCanvas(canvas, haxis,maxplotted):    
    
    haxis.SetMaximum(maxplotted)
    haxis.Draw("same")
    return canvas

def setupCanvas(canvas, haxis, xtitle = "Boson p_{T} GeV", ytitle = "NLO/LO k-factor", ymax = None, ymin = None, gridx = False, gridy = False):

    haxis.GetXaxis().SetTitle(xtitle)
    haxis.GetYaxis().SetTitle(ytitle)
    haxis.SetTitle("")
    haxis.Draw("axis")
    if ymax is not None:
        haxis.SetMaximum(ymax)
    if ymin is not None:
        haxis.SetMinimum(ymin)

    if (gridy):
        canvas.SetGridy()
    if (gridx):
        canvas.SetGridx()
    
    canvas.SetTicky()
    canvas.SetTickx()

    haxis.Draw("axigsame")
    
    return canvas

def setupLegend():
    leg = ROOT.TLegend(0.5,0.6,0.87,0.87)
    leg.SetBorderSize(0)
    return leg
   
def setLegendXY(leg,x1,y1,x2,y2):
    leg.SetX1(x1)
    leg.SetX2(x2)
    leg.SetY1(y1)
    leg.SetY2(y2)
    return leg

def calculateUncertainty(lists,bins):

    scaleup = []
    pdfup = []
    totalup = []
    scaledown = []
    pdfdown = []
    totaldown = []
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
    #   for i in range (1,7):
    for i in range (7):
        uncert = default[i].Clone("uncert"+str(i))
        if (i != 0):
            uncert.Divide(default[0])
        uncert.SetFillColor(0)
        colour = (i+1)//2;
        if ( colour == 5 ):
            colour = 9
        uncert.SetLineColor(colour)
        uncert.SetMarkerColor(colour)
        ratios.append(uncert)

    return ratios
    
  
#Draw standard k-factor plots
def drawStandardKFactorPlots(hists,bins,plotname="plot"):

    leg = setupLegend()
    xaxis = "Boson p_{T} [GeV]"
    if ( bins[0] == "gen_jetp0" ):
        xaxis = "Leading jet p_{T} [GeV]"
    maximum = 1000
    if (analysis == "vtr"):
        maximum = 400
    haxis = ROOT.TH1D("base",";"+xaxis+";NLO/LO k-factor",1,0,maximum)

    can = ROOT.TCanvas("c1","c",800,600)
    can = setupCanvas(can, haxis, ymin = 0.4, ymax = 4.2, xtitle = xaxis)

    for i,hist in enumerate(hists[0]):
        if ( analysis == "vbf" ):
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

    if ( analysis == "vbf" ):
        leg.Draw()
    can.RedrawAxis()

    can.SaveAs("plots/%s/%s.pdf"%(sys.argv[2],plotname))
    can.SaveAs("plots/%s/%s.root"%(sys.argv[2],plotname))
    can.SaveAs("plots/%s/%s.png"%(sys.argv[2],plotname))

    can.Close()
    

    
def drawUncertaintyPlots(hists,bins,plotname):

    legend_entries = ["Renormalisation Scale","Renormalisation Scale","Factorisation Scale","Factorisation Scale","PDF","PDF"]
    xaxis = "Boson p_{T} [GeV]"
    if ( bins[0] == "gen_jetp0" ):
        xaxis = "Leading jet p_{T} [GeV]"


    for j,b in enumerate(bins): 
        haxis = ROOT.TH1D("base"+str(j),";"+xaxis+";NLO/LO k-factor",1,0,1000)

        ratios = getUncertaintyRatios(hists,j)

        can = ROOT.TCanvas("c"+str(j),"c",800,600)
        can = setupCanvas(can, haxis, ytitle = "d#sigma/dp_{T} variation", ymin = 0.65, ymax = 1.25, xtitle = xaxis, gridx = True, gridy = True)
        leg = setupLegend()

        
        for i,hist in enumerate(ratios):
            if (i==0):
                continue            
            hist.Draw("HISTsame")
            if ( i%2 == 0 ):
                leg.AddEntry(hist,"%s"%(legend_entries[i-1]),"pl")
        
        setLegendXY(leg,0.55,0.13,0.89,0.4) 
        leg.Draw()
        can.SaveAs("plots/%s/k-fac-uncert-%s-%s.png"%(sys.argv[2],plotname,b))
        can.SaveAs("plots/%s/k-fac-uncert-%s-%s.root"%(sys.argv[2],plotname,b))
        can.SaveAs("plots/%s/k-fac-uncert-%s-%s.pdf"%(sys.argv[2],plotname,b))
        can.Close()

def suminQuad(lists): 
  h0 = lists[0]
  v = [0 for b in range(h0.GetNbinsX())]
  for h in lists[1:]:
     for b in range(h0.GetNbinsX()): 
       v[b]+=(abs(h.GetBinContent(b+1)-h0.GetBinContent(b+1)))**2
  
  v = [vv**0.5 for vv in v]
  for b in range(h0.GetNbinsX()): 
      h0.SetBinContent(b+1,h0.GetBinContent(b+1)+v[b])

def loadGeneralHist(filename,histnames,outlist):
    filelist.append(ROOT.TFile.Open(sys.argv[1]+"/"+filename + ".root","READ"))
    
    for name in histnames:
        h = filelist[-1].Get(name)
        outlist.append(h)

    
        
def loadHists(infile,allh,bins):
    #print (base)
    filelist.append(ROOT.TFile.Open(sys.argv[1]+"/"+infile + ".root","READ"))
    fin = filelist[-1]

    for uncert in uncerts:
        temp = []
        h2d = fin.Get("%s%s/%s"%(di,uncert,base))

        for i,b in enumerate(bins): 

            h = h2d.ProjectionX("proj_" + str(b) + "_" + uncert ,b,b )
            h.SetLineColor(cols[i])
            for f in h.GetListOfFunctions():
                f.SetLineColor(cols[i])
                f.SetBit(ROOT.TF1.kNotDraw);
            h.SetMarkerColor(cols[i])
            h.SetMarkerSize(1)
            h.SetMarkerStyle(21)
            temp.append(h)
            h.SetFillColorAlpha(fcol[i],0.5)

            if (uncert==0):
                f = fin.Get("%s%s/%s%s%s"%(di,uncert,base,b,"_fitfunc"))

        allh.append(temp)

def main():

    name_nonvbf = "kfactor_nonVBF"
    name_vbf = "2Dkfactor_VBF"
    name_vtr = "2Dkfactor_VTR"

    global base,analysis

    ##    MTR    ##
    
    base = "kfactor_vbf"
    bins_index_vbf= [2,3,4,6]
    bins_vbf= ["200_500","500_1000","1000_1500","2000_5000"]

    #VBF W
    allh_vbf = []
    # load the relevant 2D k-factor histograms
    loadHists(name_vbf+"_wjet",allh_vbf,bins_index_vbf) 
    # calculate the uncertainty
    calculateUncertainty(allh_vbf,bins_vbf) 
    # draw the note uncertainty plots
    drawUncertaintyPlots(allh_vbf,bins_vbf,"vbf_w") 
    # draw k-factor plots, where the k-factor in each mjj bin is plotted on the same 1D plot vs boson pT
    drawStandardKFactorPlots(allh_vbf,bins_vbf,"kfactor_VBF_wjet_born_default") 
    
    #VBF DY
    allh_vbf_z = []
    loadHists(name_vbf+"_zjet",allh_vbf_z,bins_index_vbf)
    calculateUncertainty(allh_vbf_z,bins_vbf)
    drawUncertaintyPlots(allh_vbf_z,bins_vbf,"vbf_z")
    drawStandardKFactorPlots(allh_vbf_z,bins_vbf,"kfactor_VBF_zjet_born_default")


    #VBF ZNN
    allh_vbf_znn = []
    loadHists(name_vbf+"_znn",allh_vbf_znn,bins_index_vbf)
    calculateUncertainty(allh_vbf_znn,bins_vbf)
    drawUncertaintyPlots(allh_vbf_znn,bins_vbf,"vbf_znn")
    drawStandardKFactorPlots(allh_vbf_znn,bins_vbf,"kfactor_VBF_znn_born_default")

    for i in range (3):
        can = ROOT.TCanvas("c1","c",800,600)
        can = setupCanvas(can, allh_vbf_z[0][i], ymin = 0.4, ymax = 2.0)
        allh_vbf_z[0][i].SetFillColor(0)
        allh_vbf_znn[0][i].SetFillColor(0)
        allh_vbf_z[0][i].SetLineColor(1)
        allh_vbf_znn[0][i].SetLineColor(2)
        allh_vbf_z[0][i].Draw("HIST")
        allh_vbf_znn[0][i].Draw("HISTsame")
        can.SaveAs("plots/%s/%s_%s.png"%(sys.argv[2],"znn_comparison",bins_vbf[i]))
        can.Close()

    ##    MTR    ##

    bins_boson_pt = ["boson_pt"]
    base = "kfactor_VTR"
    analysis = "vtr"
    allh_vbf = []
    bins_index_vtr= [1]
    bins_vtr= ["900_5000"]

    loadHists(name_vtr+"_wjet",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_w")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_wjet_born_default")
    allh_vbf = []
    loadHists(name_vtr+"_zjet",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_z")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_zjet_born_default")
    allh_vbf = []
    loadHists(name_vtr+"_znn",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_znn")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_znn_born_default")

main()

