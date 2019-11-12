import ROOT
from ROOT import *
from plotterTools import *
import math
import argparse
from array import array
gROOT.SetBatch(kTRUE)

parser = argparse.ArgumentParser(description='unfiltered time resolution')
parser.add_argument('-a', '--ampCut', dest='ampCut',required=True, type=str)
parser.add_argument('-phoMin','--photekMinCut',dest='photekMinCut',required=True,type=str)
parser.add_argument('-phoMax','--photekMaxCut',dest='photekMaxCut',required=True,type=str)
parser.add_argument('-min','--min',dest='min',required=True,type=str)
parser.add_argument('-max','--max',dest='max',required=True,type=str)
parser.add_argument('-Ch','--Ch',dest='Ch',required=True,type=str)
parser.add_argument('-c', '--cfdLGAD', dest='cfdLGAD', required=True, type=str)


opt = parser.parse_args()
ampCut = opt.ampCut
photekMinCut = opt.photekMinCut
photekMaxCut = opt.photekMaxCut
hMin = float(str(opt.min)+'e-9')
hMax = float(str(opt.max)+'e-9')
Ch = opt.Ch
cfd_lgad = opt.cfdLGAD

outputLoc = '../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/Unfiltered/'

runs = [151201,151202,151203,151204,151205,151206,151209,151216]
cfd = [5,10,15,20,25,30,35,40,50,60]

min_cfdLGAD = array('d')
for run in runs:
     ch = TChain('pulse')
     ch.Add('root://cmseos.fnal.gov//store/user/twamorka/FilterStudy/UnfilteredFiles/run_scope'+str(run)+'.root')
     print ch.GetEntries()
     timePhotek_res = []
     timePhotek_res_err = []
     timeLGAD_res = []
     timeLGAD_res_err = []
     cfd_arr = []
     cfd_err_arr = []
     min_photek_cfd = 0
     min_lgad_cfd = 0
     for c in cfd:
         hname_photek = 'h_'+str(c)
         h_photek = TH1F(hname_photek,hname_photek,100,hMin,hMax)
         ch.Draw('LP2_'+str(cfd_lgad)+'['+str(Ch)+'] - LP2_'+str(c)+'[3]>>' +hname_photek,TCut('LP2_'+str(cfd_lgad)+'['+str(Ch)+']!=0&&LP2_'+str(c)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
         c0 = TCanvas('c0','c0',800,600)
         gausFit = h_photek.Fit('gaus','S')
         timePhotek_res.append((gausFit.Parameters()[2])/1e-12)
         timePhotek_res_err.append((gausFit.Errors()[2])/1e-12)
         cfd_arr.append(c)
         cfd_err_arr.append(0)
         h_photek.Draw()
         c0.SaveAs(outputLoc+'run_'+str(run)+'_lgadcfd'+str(cfd_lgad)+'_Photekcfd_'+str(c)+'.pdf')
         npoints = len(cfd_arr)
         min_photek_cfd = cfd_arr[min(xrange(len(timePhotek_res)), key=timePhotek_res.__getitem__)]

     for c in cfd:
         hname_lgad = 'h_2_'+str(c)
         h_lgad = TH1F(hname_lgad,hname_lgad,100,hMin,hMax)

         ch.Draw('LP2_'+str(c)+'['+str(Ch)+'] - LP2_'+str(min_photek_cfd)+'[3]>>' +hname_lgad,TCut('LP2_'+str(c)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
         gausFit2 = h_lgad.Fit('gaus','S')
         timeLGAD_res.append((gausFit2.Parameters()[2])/1e-12)
         timeLGAD_res_err.append((gausFit2.Errors()[2])/1e-12)
         h_lgad.Draw()
         c0.SaveAs(outputLoc+'run_'+str(run)+'_lgadcfd'+str(cfd_lgad)+'_LGADcfd_'+str(c)+'.pdf')
     min_lgad_cfd = cfd_arr[min(xrange(len(timeLGAD_res)), key=timeLGAD_res.__getitem__)]
     min_cfdLGAD.append(min_lgad_cfd)
     MakeGraphErrors(npoints,array('d',cfd_arr),array('d',timeLGAD_res),array('d',cfd_err_arr),array('d',timeLGAD_res_err),'CFD','Time Resolution [ps]',outputLoc,'run_'+str(run)+'_lgadcfd'+str(cfd_lgad)+'_vs_LGADcfd')
