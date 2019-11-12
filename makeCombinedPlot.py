import ROOT
from ROOT import *
from array import array
import argparse

parser =  argparse.ArgumentParser(description='ETL Filter Study')
parser.add_argument('-p', '--plot', dest='plot', required=True, type=str)
parser.add_argument('-n', '--name', dest='name', required=True, type=str)

opt = parser.parse_args()
plot = opt.plot
name = opt.name

file = []
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151201/','Bias Voltage = 100 V',kRed])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151202/','Bias Voltage = 105 V',kBlue])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151203/','Bias Voltage = 110 V',kGreen])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151204/','Bias Voltage = 115 V',kMagenta])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151205/','Bias Voltage = 120 V',kOrange+2])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151206/','Bias Voltage = 125 V',kGreen-2])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151209/','Bias Voltage = 140 V',kBlack])
file.append(['../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151216/','Bias Voltage = 175 V',kOrange])

# plots = ['TimRes_vs_Freq_Beta.root','BaselineRMS_vs_Freq_Beta.root','dVdT_vs_Freq_Beta.root']
# colors = [kRed,kBlack,kGreen,kOrange,kBlue]
#
# for p in plots:
#     grs = []
#     for f in file:
#         temp_file = TFile(f[0]+p)
#         grs.append(temp_file.Get('Graph'))
#     c = TCanvas()
#     for g,gr in enumerate(grs):
#         gr.SetLineColor(colors[g])
#         gr.Draw("same")
#         c.SaveAs("test_combined.pdf")
dummy = TFile("dummy.root", "RECREATE")
grs = []
c = TCanvas()
leg = TLegend(0.6, 0.7, 0.89, 0.89)
# leg = TLegend(0.156642, 0.693295, 0.447368, 0.883024)
leg.SetLineWidth(0)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
for f in file:
    temp_file = TFile(f[0]+plot)
    print temp_file
    tempgr = temp_file.Get("Graph")
    dummy.cd()
    tempgr.SetLineColor(f[2])
    tempgr.SetMarkerColor(f[2])
    tempgr.Write()
    grs.append([tempgr, f[1]])

print len(grs)
c = TCanvas()
for ig, g in enumerate(grs):
    if ig==0:
        g[0].Draw("AP")
        g[0].GetYaxis().SetRangeUser(20, 170)
        c.Update()
    else:
        g[0].Draw("P same")
    c.Update()
    leg.AddEntry(g[0],g[1],"lp")

leg.Draw("same")
c.SaveAs(name+".pdf")
