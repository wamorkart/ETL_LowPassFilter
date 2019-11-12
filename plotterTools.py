import ROOT
from ROOT import *
freq = [300,325,350,400,425,450,500,525,550,575,600,625,650,675,700,800,900,1000,1200,1400,1600,1800,2000]
# freq = [300,325,350,400,425,450,500,525,550,575,600,625,650,675,700]
# freq =  [500,525,550,575,600,625,650,675,700,750,800]
# freq = [600,650]
# freq = [300]
# freq = [525,550,575,600,625,650,675,700,800,900,1000,1200,1400,1600,1800,2000]
## HPK Pre-rad 3.1 4x4 Pre-rad UCSC board (160V)
## 6636, 6640, 6642, 6643, 6644, 6656, 6657, 6658, 6659, 6660 --> for filter frequencies (300 to 2000 MHz)
# runs_1 = []
# runs_1.append([6636,6640,6642,6643,6644,6656,6657,6658,6659,6660]) ## HPK 3.1 4x4 Pre-rad UCSC board (160V)

# runs_2 = []
# runs_2.append([12395, 12397, 12401, 12403, 12407]) ## HPK 3.1 4x4 Pre-rad FNAL board (195 V)
# runs_2.append([12395,12403])

runs_3 = []
runs_3.append([151216]) ## 15 and 11-35
var = []
var.append(['LP2_30[0]-LP2_30[3]',100,-2.8e-9,-1.8e-9])
var.append(['baseline_RMS[0]',100,0,100])
var.append(['risetime[0]',100,-170e9,0])
var.append(['amp[0]',100,0,200])


cfd = [5,10,15,20,25,30,35,40,45,50,55,60]


def MakeGraphErrors(npoints,array_x,array_y,array_y_err,array_x_err,x_title,y_title,outputLoc,name):
    gr = TGraphErrors(npoints,array_x,array_y,array_y_err,array_x_err)
    c = TCanvas()
    gr.SetMarkerStyle(20)
    gr.SetMarkerColor(kBlack)
    gr.SetTitle(';'+str(x_title)+';'+str(y_title))
    gr.Draw('AP')
    c.SaveAs(outputLoc+str(name)+'.pdf')
    c.SaveAs(outputLoc+str(name)+'.png')
    c.SaveAs(outputLoc+str(name)+'.root')
    gr.SaveAs(outputLoc+str(name)+'.root')
    return 1

def MakeGraph(npoints,array_x,array_y,x_title,y_title,outputLoc,name):
    gr = TGraph(npoints,array_x,array_y)
    c = TCanvas()
    gr.SetMarkerStyle(20)
    gr.SetMarkerColor(kBlack)
    gr.SetTitle(';'+str(x_title)+';'+str(y_title))
    gr.Draw('AP')
    c.SaveAs(outputLoc+str(name)+'.pdf')
    c.SaveAs(outputLoc+str(name)+'.png')
    c.SaveAs(outputLoc+str(name)+'.root')
    gr.SaveAs(outputLoc+str(name)+'.root')
    return 1
