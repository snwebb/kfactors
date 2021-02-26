import ROOT
import sys, os

def main():

    infiles_vbf = [ "kfactor_VBF_zjet", "kfactor_VBF_wjet"]
    infiles_vtr = [ "kfactor_VTR_zjet", "kfactor_VTR_wjet"]
    infiles_nonvbf = [ "kfactor_VBF_zjet", "kfactor_VBF_wjet"]
    bins_vbf= ["200_500","500_1000","1000_1500","1500_5000"]
    bins_vtr = ["boson_pt"]
    bins_nonvbf = ["boson_pt","gen_jetp0"]
    bins = []
    infiles = []
    filelist = []

    for region in range(2):

        if (region == 0):
            bins = bins_vbf
            infiles = infiles_vbf
        elif (region == 1):
            bins = bins_vtr
            infiles = infiles_vtr
    
        for f in infiles:
            nominal = []
            RenormUp = []
            RenormDown = []
            FactUp = []
            FactDown = []
            PDFUp = []
            PDFDown = []

            filelist.append(ROOT.TFile.Open(sys.argv[1] + "/" + f + ".root","UPDATE"))
            fin = filelist[-1]
            for b in bins: 
                if (region == 0):
                    h = fin.Get("kfactors_shape/kfactor_vbf_mjj_" + b)
                    ru = fin.Get("kfactors_shape_Renorm_Up/kfactor_vbf_mjj_" + b)
                    rd = fin.Get("kfactors_shape_Renorm_Down/kfactor_vbf_mjj_" + b)
                    fu = fin.Get("kfactors_shape_Fact_Up/kfactor_vbf_mjj_" + b)
                    fd = fin.Get("kfactors_shape_Fact_Down/kfactor_vbf_mjj_" + b)
                    pu = fin.Get("kfactors_shape_PDF_Up/kfactor_vbf_mjj_" + b)
                    pd = fin.Get("kfactors_shape_PDF_Down/kfactor_vbf_mjj_" + b)
                    nominal.append(h)
                    RenormUp.append(ru)
                    RenormDown.append(rd)
                    FactUp.append(fu)
                    FactDown.append(fd)
                    PDFUp.append(pu)
                    PDFDown.append(pd)

                elif (region == 1):
                    h = fin.Get("kfactors_shape/kfactor_VTR_" + b)
                    ru = fin.Get("kfactors_shape_Renorm_Up/kfactor_VTR_" + b)
                    rd = fin.Get("kfactors_shape_Renorm_Down/kfactor_VTR_" + b)
                    fu = fin.Get("kfactors_shape_Fact_Up/kfactor_VTR_" + b)
                    fd = fin.Get("kfactors_shape_Fact_Down/kfactor_VTR_" + b)
                    pu = fin.Get("kfactors_shape_PDF_Up/kfactor_VTR_" + b)
                    pd = fin.Get("kfactors_shape_PDF_Down/kfactor_VTR_" + b)
                    nominal.append(h)
                    RenormUp.append(ru)
                    RenormDown.append(rd)
                    FactUp.append(fu)
                    FactDown.append(fd)
                    PDFUp.append(pu)
                    PDFDown.append(pd)


            #Take correction from bin 5
            origdir = filelist[-1].GetDirectory("/")
            filelist[-1].GetDirectory("/kfactors_shape_Renorm_Up/").cd()
            for n,renorm in enumerate(RenormUp):
                binchoice = 6
                correction = renorm.GetBinContent(binchoice)-nominal[n].GetBinContent(binchoice)
                for b in range(1,6):
                    renorm.SetBinContent(b, correction + nominal[n].GetBinContent(b))
                if (region == 0):
                    renorm.Write("kfactor_vbf_mjj_" + bins[n],ROOT.TObject.kOverwrite )
                elif (region == 1):
                    renorm.Write("kfactor_VTR_" + bins[n],ROOT.TObject.kOverwrite )

            origdir.cd()
            filelist[-1].GetDirectory("/kfactors_shape_Renorm_Down/").cd()
            for n,renorm in enumerate(RenormDown):
                binchoice = 6
                correction = renorm.GetBinContent(binchoice)-nominal[n].GetBinContent(binchoice)
                for b in range(1,6):
                    renorm.SetBinContent(b, correction + nominal[n].GetBinContent(b))
                if (region == 0):
                    renorm.Write("kfactor_vbf_mjj_" + bins[n],ROOT.TObject.kOverwrite )
                elif (region == 1):
                    renorm.Write("kfactor_VTR_" + bins[n],ROOT.TObject.kOverwrite )

            origdir.cd()
            filelist[-1].GetDirectory("/kfactors_shape_Fact_Up/").cd()
            for n,fact in enumerate(FactUp):
                binchoice = 6
                correction = fact.GetBinContent(binchoice)-nominal[n].GetBinContent(binchoice)
                print("corr = ",	correction)
                for b in range(1,6):
                    fact.SetBinContent(b, correction + nominal[n].GetBinContent(b))
                if (region == 0):
                    fact.Write("kfactor_vbf_mjj_" + bins[n],ROOT.TObject.kOverwrite )
                elif (region == 1):
                    fact.Write("kfactor_VTR_" + bins[n],ROOT.TObject.kOverwrite )

            origdir.cd()
            filelist[-1].GetDirectory("/kfactors_shape_Fact_Down/").cd()
            for n,fact in enumerate(FactDown):
                binchoice = 6
                correction = fact.GetBinContent(binchoice)-nominal[n].GetBinContent(binchoice)
                print("corr = ",	correction)
                for b in range(1,6):
                    fact.SetBinContent(b, correction + nominal[n].GetBinContent(b))
                if (region == 0):
                    fact.Write("kfactor_vbf_mjj_" + bins[n],ROOT.TObject.kOverwrite )
                elif (region == 1):
                    fact.Write("kfactor_VTR_" + bins[n],ROOT.TObject.kOverwrite )

            origdir.cd()
            filelist[-1].GetDirectory("/kfactors_shape_PDF_Up/").cd()
            for n,pdf in enumerate(PDFUp):
                binchoice = 6
                correction = pdf.GetBinContent(binchoice)-nominal[n].GetBinContent(binchoice)
                print("corr = ",	correction)
                for b in range(1,6):
                    pdf.SetBinContent(b, correction + nominal[n].GetBinContent(b))
                if (region == 0):
                    pdf.Write("kfactor_vbf_mjj_" + bins[n],ROOT.TObject.kOverwrite )
                elif (region == 1):
                    pdf.Write("kfactor_VTR_" + bins[n],ROOT.TObject.kOverwrite )

            origdir.cd()
            filelist[-1].GetDirectory("/kfactors_shape_PDF_Down/").cd()
            for n,pdf in enumerate(PDFDown):
                binchoice = 6
                correction = pdf.GetBinContent(binchoice)-nominal[n].GetBinContent(binchoice)
                print("corr = ",	correction)
                for b in range(1,6):
                    pdf.SetBinContent(b, correction + nominal[n].GetBinContent(b))
                if (region == 0):
                    pdf.Write("kfactor_vbf_mjj_" + bins[n],ROOT.TObject.kOverwrite )
                elif (region == 1):
                    pdf.Write("kfactor_VTR_" + bins[n],ROOT.TObject.kOverwrite )

            fin.Close()


    
            
main()
