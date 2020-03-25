import ROOT
import sys, os
from math import sqrt
#fin = ROOT.TFile.Open("input/"+sys.argv[1])
outdir = "plots/"+sys.argv[2]
if os.path.exists(outdir) == False:
    os.mkdir(outdir) 

#fin_bu = ROOT.TFile.Open("2017_gen_v_pt_qcd_sf.root","READ")
fin_bu = ROOT.TFile.Open("2017_gen_v_pt_qcd_sf_20200122.root","READ")
fin_bu_component = ROOT.TFile.Open(" 2d_gen_vpt_mjj.root", "READ")
#fin_bu = ROOT.TFile.Open("2017_gen_v_pt_qcd_sf.root","READ")
#fin_component = ROOT.TFile.Open(sys.argv[1]+"/NLO_plots.root","READ")
filelist = []
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetImageScaling(3.)
analysis = "vbf"
di="kfactors_shape"
base = "kfactor_vbf_mjj_"
cols = [1,2,4,6]
fcol=[ROOT.kGray,ROOT.kRed-9,ROOT.kAzure+6,ROOT.kMagenta]

# if ( sys.argv[1].find("nonVBF")!=-1 ):
#     analysis = "nonvbf"

#if analysis == "nonvbf":
#    bins = ["boson_pt"]
#    bins = ["gen_jetp0"]
 #   base = "kfactor_nonvbf_"
#    cols = [2]
#    fcol=[ROOT.kRed-9]

uncerts = ["","_Renorm_Up","_Renorm_Down","_Fact_Up","_Fact_Down","_PDF_Up","_PDF_Down"]







# haxis = ROOT.TH1D("base",";Boson p_{T} GeV;NLO/LO k-factor",1,0,1000)
# haxis.GetXaxis().SetTitle("Boson p_{T} GeV")
# haxis.GetYaxis().SetTitle("NLO/LO k-factor")
# haxis.SetTitle("")
# haxis.Draw("axis")


allh_wbu = []
allh_zbu = []
allh_wbu_lo = []
allh_zbu_lo = []
allh_wbu_nlo = []
allh_zbu_nlo = []
allh_w_lo = []
allh_z_lo = []
allh_w_nlo = []
allh_z_nlo = []

def finaliseCanvas(canvas, haxis,maxplotted):    
    
    haxis.SetMaximum(maxplotted)
    haxis.Draw("same")
    return canvas

def setupCanvas(canvas, haxis, xtitle = "Boson p_{T} GeV", ytitle = "NLO/LO k-factor", ymax = None, ymin = None):

    haxis.GetXaxis().SetTitle(xtitle)
    haxis.GetYaxis().SetTitle(ytitle)
    haxis.SetTitle("")
    haxis.Draw("axis")
    if ymax is not None:
        haxis.SetMaximum(ymax)
    if ymin is not None:
        haxis.SetMinimum(ymin)


    canvas.SetTicky()
    canvas.SetTickx()
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
        colour = i;
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
    #    can = ROOT.TCanvas("c1","c",1600,1200)
    can = setupCanvas(can, haxis, ymin = 0.4, ymax = 2.0, xtitle = xaxis)
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

    #    can.SaveAs("plots/%s/%s.pdf"%(sys.argv[2],(sys.argv[1]).rsplit("/",1)[-1]))
    can.SaveAs("plots/%s/%s.pdf"%(sys.argv[2],plotname))
    can.SaveAs("plots/%s/%s.root"%(sys.argv[2],plotname))
    can.SaveAs("plots/%s/%s.png"%(sys.argv[2],plotname))
#    can.SaveAs("plots/%s/%s.png"%(sys.argv[2],(sys.argv[1]).rsplit("/",1)[-1]))

    can.Close()
    

def drawBUComparisonPlots(hists,bu,bins,plotname,ymin = None, ymax = None):

    maxplotted = 0
    can = ROOT.TCanvas("c1","c",800,600)

    leg = setupLegend()
    xaxis = "Boson p_{T} [GeV]"
    if ( bins[0] == "gen_jetp0" ):
        xaxis = "Leading jet p_{T} [GeV]"
    haxis = ROOT.TH1D("base",";"+xaxis+";NLO/LO k-factor",1,0,1000)

    
    for i,hist in enumerate(hists[0]):

        can.Clear()
        leg.Clear()
        can = setupCanvas(can, haxis, ymin = ymin, ymax = ymax, xtitle = xaxis)

        if ( analysis == "vbf" ):
            labs1,labs2 = bins[i].split("_")[0], bins[i].split("_")[1]
            leg.AddEntry(hist,"%s < m_{jj} < %s GeV"%(labs1,labs2),"fpel")

        # total = True;
        # up = 7
        # down = 8
        # if ( total ):
        #     up = 9
        #     down = 10

        #        hists[up][i].Draw("HISTsame")

        maxplotted = hist.GetMaximum()*1.2
        hist.Draw("PSAME0")
        #        hists[down][i].SetFillColor(10)
        #        hists[down][i].Draw("HISTsame")
        #        hist.Draw("PSAME0")
        bu[i].Draw("HISTSAME")

        if ( analysis == "vbf" ):
            leg.Draw()


        if (ymax is None):
            can = finaliseCanvas(can, haxis,maxplotted)
        can.RedrawAxis()

        can.SaveAs("plots/%s/comparison_%s_%s.pdf"%(sys.argv[2],bins[i],plotname))
        can.SaveAs("plots/%s/comparison_%s_%s.png"%(sys.argv[2],bins[i],plotname))
        can.SaveAs("plots/%s/comparison_%s_%s.root"%(sys.argv[2],bins[i],plotname))

#        can.Close()

    #for i,hist in enumerate(hists[0]):
        #hist.Draw("PSAME0")

    
def drawUncertaintyPlots(hists,bins,plotname):

#    default = list(zip(*hists))[0]
    leg = setupLegend()
    can = ROOT.TCanvas("c2","c",800,600)

    xaxis = "Boson p_{T} [GeV]"
    if ( bins[0] == "gen_jetp0" ):
        xaxis = "Leading jet p_{T} [GeV]"
    haxis = ROOT.TH1D("base",";"+xaxis+";NLO/LO k-factor",1,0,1000)
    can = setupCanvas(can, haxis, ytitle = "d#sigma/dp_{T} variation", ymin = 0.6, ymax = 1.3, xtitle = xaxis)
    #can = setupCanvas(can, haxis, ytitle = "d#sigma/dp_{T} variation", ymin = 0, ymax = 2.6)

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
        if (i==0):
            continue
        hist.Draw("HISTsame")
        leg.AddEntry(hist,"%s %s"%(uncerts[i].split("_")[1], uncerts[i].split("_")[2]),"pl")
        
    setLegendXY(leg,0.55,0.13,0.8,0.35) 
    leg.Draw()
    can.SaveAs("plots/%s/k-fac-uncert-%s.png"%(sys.argv[2],plotname))
    can.SaveAs("plots/%s/k-fac-uncert-%s.root"%(sys.argv[2],plotname))
    can.SaveAs("plots/%s/k-fac-uncert-%s.pdf"%(sys.argv[2],plotname))
    can.Close()
    
# def appendFittedUncertaintyToFile(hists):
# #
#  #   default = getUncertaintyRatios(hists,0)
    
#     for i,uncert in enumerate(bins):
#         ratios = getUncertaintyRatios(hists,i)
#         pol2 = ROOT.TF1("pol2","pol1",170,470)
#         for j,hist in enumerate(ratios):
#             if (j==0): continue
#             hist.Fit(pol2,"LRQ0")
#             for b in range(2,hist.GetNbinsX()+1):
#                 hist.SetBinContent(b,pol2.Eval(hist.GetBinCenter(b)))
#             hist.Multiply(ratios[0])
#             fin.cd("kfactors_shape" + uncerts[j])
#             hist.Write( base + uncert + "_fit")
#             fin.cd("..")
  
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

def loadGeneralHist(filename,histnames,outlist):
    filelist.append(ROOT.TFile.Open(sys.argv[1]+"/"+filename + ".root","READ"))
    
    for name in histnames:
        h = filelist[-1].Get(name)
        outlist.append(h)

    
def loadBUHists(bins):

    #Get BU Central Values    
    w_bu = (fin_bu.Get("2d_wjet_vbf"))
    z_bu = (fin_bu.Get("2d_dy_vbf"))

    w_bu_lo = (fin_bu_component.Get("wjet_lo_gen_vpt_mjj"))
    w_bu_nlo = (fin_bu_component.Get("wjet_nlo_gen_vpt_mjj"))
    z_bu_lo = (fin_bu_component.Get("dy_lo_gen_vpt_mjj"))
    z_bu_nlo = (fin_bu_component.Get("dy_nlo_gen_vpt_mjj"))

    inlist_w_lo=[]
    inlist_w_nlo=[]
    inlist_z_lo=[]
    inlist_z_nlo=[]
    #Form hist lists
    for b in bins:
        inlist_w_lo.append("W_Nominal_LO/VBF_MJJ_%s"%(b))
        inlist_w_nlo.append("W_Nominal_NLO/VBF_MJJ_%s"%(b))
        inlist_z_lo.append("Z_Nominal_LO/VBF_MJJ_%s"%(b))
        inlist_z_nlo.append("Z_Nominal_NLO/VBF_MJJ_%s"%(b))

    loadGeneralHist( "NLO_plots" , inlist_w_lo, allh_w_lo )
    loadGeneralHist( "NLO_plots" , inlist_w_nlo, allh_w_nlo )
    loadGeneralHist( "NLO_plots" , inlist_z_lo, allh_z_lo )
    loadGeneralHist( "NLO_plots" , inlist_z_nlo, allh_z_nlo )
        
    for hist in allh_w_lo:
        hist.Scale(1)
    for hist in allh_w_nlo:
        hist.Scale(1)
    for hist in allh_z_lo:
        hist.Scale(1)
    for hist in allh_z_nlo:
        hist.Scale(1)

    # for hist in allh_w_lo:
    #     hist.Scale(1/hist.Integral("width"))
    # for hist in allh_w_nlo:
    #     hist.Scale(1/hist.Integral("width"))
    # for hist in allh_z_lo:
    #     hist.Scale(1/hist.Integral("width"))
    # for hist in allh_z_nlo:
    #     hist.Scale(1/hist.Integral("width"))


        
    #for i in range (2,6):
    for i in range (1,6):
        allh_wbu.append( w_bu.ProjectionY("projw" + str(i),i,i) )
        allh_zbu.append( z_bu.ProjectionY("projz" + str(i),i,i) )

    for i in range (1,5):
        allh_wbu_nlo.append( w_bu_nlo.ProjectionY("projw_nlo" + str(i),i,i) )
        allh_zbu_nlo.append( z_bu_nlo.ProjectionY("projz_nlo" + str(i),i,i) )
        allh_wbu_lo.append( w_bu_lo.ProjectionY("projw_lo" + str(i),i,i) )
        allh_zbu_lo.append( z_bu_lo.ProjectionY("projz_lo" + str(i),i,i) )
        
    for hist in allh_wbu_lo:
        hist.Scale(1./41.,"width")
    for hist in allh_wbu_nlo:
        hist.Scale(1./41.,"width")
    for hist in allh_zbu_lo:
        hist.Scale(1./41.,"width")
    for hist in allh_zbu_nlo:
        hist.Scale(1./41.,"width")

    # for hist in allh_wbu_lo:
    #     print (hist.Integral())
    #     hist.Scale(1/hist.Integral(),"width")
    # for hist in allh_wbu_nlo:
    #     hist.Scale(1/hist.Integral(),"width")
    # for hist in allh_zbu_lo:
    #     hist.Scale(1/hist.Integral(),"width")
    # for hist in allh_zbu_nlo:
    #     hist.Scale(1/hist.Integral(),"width")

        
def loadHists(infile,allh,bins):
    #print (base)
    filelist.append(ROOT.TFile.Open(sys.argv[1]+"/"+infile + ".root","READ"))
    fin = filelist[-1]

    for uncert in uncerts:
        temp = []
        #    for i,c in enumerate(cols):
        h2d = fin.Get("%s%s/%s"%(di,uncert,base))

        #print ( "%s%s/%s"%(di,uncert,base) )
        for i,b in enumerate(bins): 
            # print ("%s%s/%s%s%s"%(di,uncert,base,b,histtype))


            h = h2d.ProjectionX("proj_" + str(b) + "_" + uncert ,b,b )
            #h = h1.Clone(h1.GetName()+"_2")
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
        # if (allf is not None):
        #     allf.append(f)




def main():

    name_nonvbf = "kfactor_nonVBF"
    name_vbf = "kfactor_VBF"
    name_vtr = "kfactor_VTR"


    global base,analysis
    
    #VBF W
    base = "kfactor_vbf"
    bins_index_vbf= [2,3,5]
    #bins_index_vbf= [2]
    #bins_index_vbf= [2,3,4,5]
    #bins_vbf= ["200_500"]
    bins_vbf= ["200_500","500_1000","1500_5000"]
    #    bins_vbf= ["1500_5000"]
        
    allh_vbf = []
    loadHists("2Dkfactor_VBF_wjet",allh_vbf,bins_index_vbf)
    calculateUncertainty(allh_vbf,bins_vbf)
    #drawUncertaintyPlots(allh_vbf,bins_vbf,"vbf_w")
    drawStandardKFactorPlots(allh_vbf,bins_vbf,"kfactor_VBF_wjet_born_default")
    
    #loadBUHists(bins_vbf)
    #drawBUComparisonPlots(allh_vbf,allh_wbu,bins_vbf,"vbf_w",ymin=0.4,ymax=2.0)

    # allh_vbf = []
    # loadHists("PtBinned_kfactor_VBF_wjet",allh_vbf,bins_vbf)
    # calculateUncertainty(allh_vbf,bins_vbf)
    # drawUncertaintyPlots(allh_vbf,bins_vbf,"ptbinned_vbf_w")
    # drawStandardKFactorPlots(allh_vbf,bins_vbf,"PtBinned_kfactor_VBF_wjet_born")



    # allh_vbf_lo = []
    # allh_vbf_lo.append(allh_w_lo)
    # drawBUComparisonPlots(allh_vbf_lo,allh_wbu_lo,bins_vbf,"vbf_w_lo")
    # allh_vbf_lo = []
    # allh_vbf_lo.append(allh_w_nlo)
    # drawBUComparisonPlots(allh_vbf_lo,allh_wbu_lo,bins_vbf,"vbf_w_nlo")

    #Z
    allh_vbf_z = []
    loadHists("2Dkfactor_VBF_zjet",allh_vbf_z,bins_index_vbf)
    calculateUncertainty(allh_vbf_z,bins_vbf)
    #drawUncertaintyPlots(allh_vbf_z,bins_vbf,"vbf_z")
    drawStandardKFactorPlots(allh_vbf_z,bins_vbf,"kfactor_VBF_zjet_born_default")

    #vbf_z
#    drawBUComparisonPlots(allh_vbf,allh_zbu,bins_vbf,"vbf_z",ymin=0.4,ymax=2.0)

    # allh_vbf = []
    # loadHists("PtBinned_kfactor_VBF_zjet",allh_vbf,bins_vbf)
    # calculateUncertainty(allh_vbf,bins_vbf)
    # drawUncertaintyPlots(allh_vbf,bins_vbf,"ptbinned_vbf_z")
    # drawStandardKFactorPlots(allh_vbf,bins_vbf,"PtBinned_kfactor_VBF_zjet_born")



    # allh_vbf_lo = []
    # allh_vbf_lo.append(allh_z_lo)
    # drawBUComparisonPlots(allh_vbf_lo,allh_zbu_lo,bins_vbf,"vbf_z_lo")
    # allh_vbf_lo = []
    # allh_vbf_lo.append(allh_z_nlo)
    # drawBUComparisonPlots(allh_vbf_lo,allh_zbu_lo,bins_vbf,"vbf_z_nlo")


    #ZNUNU
    allh_vbf_znn = []
    loadHists("2Dkfactor_VBF_znn",allh_vbf_znn,bins_index_vbf)
    calculateUncertainty(allh_vbf_znn,bins_vbf)
    #drawUncertaintyPlots(allh_vbf,bins_vbf,"vbf_w")
    drawStandardKFactorPlots(allh_vbf_znn,bins_vbf,"kfactor_VBF_znn_born_default")
    allh_vbf_znn_zll = []
    loadHists("2Dkfactor_VBF_znn_zll",allh_vbf_znn_zll,bins_index_vbf)
    calculateUncertainty(allh_vbf_znn_zll,bins_vbf)
    #drawUncertaintyPlots(allh_vbf,bins_vbf,"vbf_w")
    drawStandardKFactorPlots(allh_vbf_znn_zll,bins_vbf,"kfactor_VBF_znn_zll_born_default")

    for i in range (3):
        can = ROOT.TCanvas("c1","c",800,600)
        can = setupCanvas(can, allh_vbf_z[0][i], ymin = 0.4, ymax = 2.0)
        allh_vbf_z[0][i].SetFillColor(0)
        allh_vbf_znn[0][i].SetFillColor(0)
        allh_vbf_znn_zll[0][i].SetFillColor(0)
        allh_vbf_z[0][i].SetLineColor(1)
        allh_vbf_znn[0][i].SetLineColor(2)
        allh_vbf_znn_zll[0][i].SetLineColor(4)
        allh_vbf_z[0][i].Draw("HIST")
        print (i,allh_vbf_z[0][i].GetName())
        allh_vbf_znn[0][i].Draw("HISTsame")
        allh_vbf_znn_zll[0][i].Draw("HISTsame")
        can.SaveAs("plots/%s/%s_%s.png"%(sys.argv[2],"znn_comparison",bins_vbf[i]))
        can.Close()

    

    #VTR
    
    bins_boson_pt = ["boson_pt"]
    base = "kfactor_VTR"
    analysis = "vtr"
    allh_vbf = []
    bins_index_vtr= [1]
    bins_vtr= ["900_5000"]
    loadHists("2Dkfactor_VTR_wjet",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    #drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_w")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_wjet_born_default")
    allh_vbf = []
    loadHists("2Dkfactor_VTR_zjet",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    #drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_z")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_zjet_born_default")
    allh_vbf = []
    loadHists("2Dkfactor_VTR_znn",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    #drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_z")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_znn_born_default")
    allh_vbf = []
    loadHists("2Dkfactor_VTR_znn_zll",allh_vbf,bins_index_vtr)
    calculateUncertainty(allh_vbf,bins_vtr)
    #drawUncertaintyPlots(allh_vbf,bins_vtr,"vtr_z")
    drawStandardKFactorPlots(allh_vbf,bins_vtr,"kfactor_VTR_znn_zll_born_default")



    
    # # #NON VBF 
    # ####global base
    # base = "kfactor_nonvbf_"

    # bins_jetpt = ["gen_jetp0"]

    # #W
    # allh_nonvbf = []
    # loadHists("kfactor_nonVBF_wjet",allh_nonvbf,bins_boson_pt)
    # calculateUncertainty(allh_nonvbf,bins_boson_pt)    
    # drawStandardKFactorPlots(allh_nonvbf,bins_boson_pt,"nonvbf_bosonpt_w")
    # allh_nonvbf = []
    # loadHists("kfactor_nonVBF_wjet",allh_nonvbf, bins_jetpt)
    # calculateUncertainty(allh_nonvbf,bins_jetpt)    
    # drawStandardKFactorPlots(allh_nonvbf,bins_jetpt,"nonvbf_jetpt_w")
    # #Z
    # allh_nonvbf = []
    # loadHists("kfactor_nonVBF_zjet",allh_nonvbf,bins_boson_pt)
    # calculateUncertainty(allh_nonvbf,bins_boson_pt)    
    # drawStandardKFactorPlots(allh_nonvbf,bins_boson_pt,"nonvbf_bosonpt_z")
    # allh_nonvbf = []
    # loadHists("kfactor_nonVBF_zjet",allh_nonvbf, bins_jetpt)
    # calculateUncertainty(allh_nonvbf,bins_jetpt)    
    # drawStandardKFactorPlots(allh_nonvbf,bins_jetpt,"nonvbf_jetpt_z")






    

    
    #        drawUncertaintyPlots(allh_nonvbf_boson,bins_boson_pt)
    # calculateUncertainty(allh_nonvbf_jet,bins_jetpt)
    # drawStandardKFactorPlots(allh_nonvbf_jet,bins_boson_pt)
    #        drawUncertaintyPlots(allh_nonvbf_jet,bins_jetpt)


    # #appendFittedUncertaintyToFile(allh)

#    loadHists("kfactor_nonVBF_zjet",allh_nonvbf_jet,bins_jetpt)

main()

