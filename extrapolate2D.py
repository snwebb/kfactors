import ROOT
import sys, os



def main():

    infiles_vbf = [ "2Dkfactor_VBF_zjet", "2Dkfactor_VBF_wjet"]
    infiles_vtr = [ "2Dkfactor_VTR_zjet", "2Dkfactor_VTR_wjet"]
    infiles_nonvbf = [ "2Dkfactor_nonvbf_zjet", "2Dkfactor_nonvbf_wjet"]
    regionnames = ["vbf", "VTR", "nonvbf"]
    infiles = []
    filelist = []

    for region in regionnames:

        if (region == "vbf"):
            infiles = infiles_vbf
        elif (region == "VTR"):
            infiles = infiles_vtr
        elif (region == "nonvbf"):
            infiles = infiles_nonvbf
    
        for f in infiles:
            nominal = []
            Systs = []

            filelist.append(ROOT.TFile.Open(sys.argv[1] + "/" + f + ".root","UPDATE"))
            fin = filelist[-1]


            h = fin.Get("kfactors_shape/kfactor_" + region)
            ru = fin.Get("kfactors_shape_Renorm_Up/kfactor_" + region)
            rd = fin.Get("kfactors_shape_Renorm_Down/kfactor_" + region)
            fu = fin.Get("kfactors_shape_Fact_Up/kfactor_" + region)
            fd = fin.Get("kfactors_shape_Fact_Down/kfactor_" + region)
            pu = fin.Get("kfactors_shape_PDF_Up/kfactor_" + region)
            pd = fin.Get("kfactors_shape_PDF_Down/kfactor_" + region)
            nominal.append(h)

            Systs.append(ru)
            Systs.append(rd)
            Systs.append(fu)
            Systs.append(fd)
            Systs.append(pu)
            Systs.append(pd)

            #Take correction from bin 6

            origdir = filelist[-1].GetDirectory("/")
            filelist[-1].GetDirectory("/kfactors_shape/").cd()
            for n,nom in enumerate(nominal):
                       
                if (region == "vbf"):
                    for x in range(1,nom.GetNbinsX()+1):
                        nom.SetBinContent(x,1,nom.GetBinContent(x,2))#to account for events with mjj < 200
                elif (region == "nonvbf"):
                    for x in range(1,5):
                        for y in range(1,nom.GetNbinsY()+1):
                            nom.SetBinContent(x,y,nom.GetBinContent(5,y))#to account for events with boson pt < 160
                nom.Write("kfactor_" + region ,ROOT.TObject.kOverwrite )

            origdir.cd()

            dirlist = ["Renorm_Up/" ,"Renorm_Down/" , "Fact_Up/", "Fact_Down/",  "PDF_Up/", "PDF_Down/"]
            for d,direc in enumerate(dirlist):
                filelist[-1].GetDirectory("/kfactors_shape_" + direc).cd()

                syst = Systs[d]
                
                #                for n,syst in enumerate(Systs):
                binchoice = 6
                #loop over mjj bins
                for y in range(1,syst.GetNbinsY()+1):
                    correction = syst.GetBinContent(binchoice,y)-nominal[0].GetBinContent(binchoice,y)
                    for b in range(1,6):
                        syst.SetBinContent(b, y, correction + nominal[0].GetBinContent(b,y))

                if (region == "vbf"):
                    for x in range(1,syst.GetNbinsX()+1):
                        syst.SetBinContent(x,1,syst.GetBinContent(x,2))
                if (region == "nonvbf"):
                    for x in range(1,5):
                        for y in range(1,syst.GetNbinsY()+1):
                            syst.SetBinContent(x,y,syst.GetBinContent(5,y))
                syst.Write("kfactor_" + region,ROOT.TObject.kOverwrite )

                origdir.cd()

            fin.Close()


    
            
main()
