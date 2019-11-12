import ROOT
from ROOT import *
from plotterTools import *
import math
from array import array
import argparse

parser =  argparse.ArgumentParser(description='ETL Filter Study')
parser.add_argument('-s', '--sensor', dest='sensor', required=True, type=str)
parser.add_argument('-c', '--cfdLGAD', dest='cfdLGAD', required=True, type=str)
parser.add_argument('-a', '--ampCut', dest='ampCut',required=True, type=str)
parser.add_argument('-phoMin','--photekMinCut',dest='photekMinCut',required=True,type=str)
parser.add_argument('-phoMax','--photekMaxCut',dest='photekMaxCut',required=True,type=str)
parser.add_argument('-min','--min',dest='min',required=True,type=str)
parser.add_argument('-max','--max',dest='max',required=True,type=str)
parser.add_argument('-Ch','--Ch',dest='Ch',required=True,type=str)
parser.add_argument('-Out','--Out',dest='Out',required=True,type=str)

opt = parser.parse_args()
sensor = opt.sensor
cfd_lgad = opt.cfdLGAD
ampCut = opt.ampCut
photekMinCut = opt.photekMinCut
photekMaxCut = opt.photekMaxCut
Ch = opt.Ch
print opt.min
print opt.max
hMin = float(str(opt.min)+'e-9')
hMax = float(str(opt.max)+'e-9')
print hMin
print hMax
runs = []
if sensor == 'Pre-rad_UCSC_160':
    runs = runs_1
if sensor == 'Pre-rad_FNAL_195':
    runs = runs_2
if sensor == 'Beta':
    runs = runs_3

outputLoc = opt.Out
# outputLoc = '../ETL_Agilent_MSO-X-92004A/Plotter/BetaSetup/151216/'

sigma_arr, sigma_err_arr = array( 'd' ), array( 'd' )
baselineRMS_arr, baselineRMS_err_arr = array( 'd' ), array( 'd' )
slewrate_arr, slewrate_err_arr = array( 'd' ), array( 'd' )
freq_arr, freq_err_arr = array( 'd' ), array( 'd' )
risetime_arr, risetime_err_arr = array( 'd' ), array( 'd' )
mpv,mpv_err = array('d'),array('d')
min_cfdLGAD = array('d')
## cfd scan for photek
nfreq = len(freq)

gROOT.SetBatch(kTRUE)

for f in freq:
    ch = TChain('pulse')
    for run in runs:
        for r in run:
            # ch.Add('root://cmseos.fnal.gov//store/group/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v1/run_scope_dat2root_'+str(r)+'_converted.root')
            ch.Add('root://cmseos.fnal.gov//store/user/twamorka/FilterStudy/dat2Root_Filter/run_scope_dat2root_'+str(r)+'_'+str(f)+'.root')
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
        hname_photek = str(f)+'_'+str(c)
        # h_photek = TH1F(hname_photek,hname_photek,100,-4e-9,-2e-9)
        h_photek = TH1F(hname_photek,hname_photek,100,hMin,hMax)
        # ch.Draw('LP2_'+str(cfd_lgad)+'[2] - LP2_'+str(c)+'[3]>>' +hname_photek,TCut('LP2_'+str(cfd_lgad)+'[2]!=0&&LP2_'+str(c)+'[3]!=0&&amp[2]>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))

        # print 'LP2_'+str(cfd_lgad)+'['+str(Ch)+'] - LP2_'+str(c)+'[3]>>' +hname_photek,TCut('LP2_'+str(cfd_lgad)+'['+str(Ch)+']!=0&&LP2_'+str(c)+'[3]!=0&&amp[0]>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut))
        ch.Draw('LP2_'+str(cfd_lgad)+'['+str(Ch)+'] - LP2_'+str(c)+'[3]>>' +hname_photek,TCut('LP2_'+str(cfd_lgad)+'['+str(Ch)+']!=0&&LP2_'+str(c)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
        c0 = TCanvas('c0','c0',800,600)
        gausFit = h_photek.Fit('gaus','S')
        timePhotek_res.append((gausFit.Parameters()[2])/1e-12)
        timePhotek_res_err.append((gausFit.Errors()[2])/1e-12)
        cfd_arr.append(c)
        cfd_err_arr.append(0)
        h_photek.Draw()
        c0.SaveAs(outputLoc+'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_Photekcfd_'+str(c)+'.pdf')
        c0.SaveAs(outputLoc+'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_Photekcfd_'+str(c)+'.png')
    npoints = len(cfd_arr)
    MakeGraphErrors(npoints,array('d',cfd_arr),array('d',timePhotek_res),array('d',cfd_err_arr),array('d',timePhotek_res_err),'Photek CFD','Time Resolution [ps]',outputLoc,'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_vs_Photekcfd'+str(sensor))

    min_photek_cfd = cfd_arr[min(xrange(len(timePhotek_res)), key=timePhotek_res.__getitem__)]
# # ## cfd scan for LGAD
    for c in cfd:
        hname_lgad = str(f)+'_2_'+str(c)
        h_lgad = TH1F(hname_lgad,hname_lgad,100,hMin,hMax)

        ch.Draw('LP2_'+str(c)+'['+str(Ch)+'] - LP2_'+str(min_photek_cfd)+'[3]>>' +hname_lgad,TCut('LP2_'+str(c)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
        gausFit2 = h_lgad.Fit('gaus','S')
        timeLGAD_res.append((gausFit2.Parameters()[2])/1e-12)
        timeLGAD_res_err.append((gausFit2.Errors()[2])/1e-12)
        h_lgad.Draw()
        c0.SaveAs(outputLoc+'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_LGADcfd_'+str(c)+'.pdf')
        c0.SaveAs(outputLoc+'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_LGADcfd_'+str(c)+'.png')
    min_lgad_cfd = cfd_arr[min(xrange(len(timeLGAD_res)), key=timeLGAD_res.__getitem__)]
    min_cfdLGAD.append(min_lgad_cfd)
    MakeGraphErrors(npoints,array('d',cfd_arr),array('d',timeLGAD_res),array('d',cfd_err_arr),array('d',timeLGAD_res_err),'LGAD CFD','Time Resolution [ps]',outputLoc,'freq_'+str(f)+'_lgadcfd'+str(cfd_lgad)+'_vs_LGADcfd'+str(sensor))

    hname = 'dummy_hist'
    print "min lgad cfd ", min_lgad_cfd
    h1 = TH1F(hname,hname,100,hMin,hMax)
    ch.Draw('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+'] - LP2_30[3] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
    c = TCanvas('c','c',800,600)
    gausFit = h1.Fit('gaus','S')
    h1.Draw()
    c.SaveAs(outputLoc+'freq_'+str(f)+'.pdf')
    c.SaveAs(outputLoc+'freq_'+str(f)+'.png')
    sigma_arr.append((gausFit.Parameters()[2])/1e-12)
    sigma_err_arr.append((gausFit.Errors()[2])/1e-12)
    freq_arr.append(f)
    freq_err_arr.append(0)

    h2 = TH1F(hname,hname,100,0,100)
    ch.Draw('baseline_RMS['+str(Ch)+'] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
    baselineRMS_arr.append(h2.GetMean())
    baselineRMS_err_arr.append(h2.GetMeanError())

    h3 = TH1F(hname,hname,100,-3000,100)
    # ch.Draw('risetime['+str(Ch)+']/1e9 >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
    ch.Draw('risetime['+str(Ch)+']/1e12 >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
    slewrate_arr.append(abs(h3.GetMean()))
    slewrate_err_arr.append(abs(h3.GetMeanError()))

    h4 = TH1F(hname,hname,100,0,800)
    ch.Draw('amp['+str(Ch)+'] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
    lanFit = h4.Fit('landau','S')
    h4.Draw()
    c.SaveAs(outputLoc+'freq_mpv'+str(f)+'.pdf')
    c.SaveAs(outputLoc+'freq_mpv'+str(f)+'.png')
    mpv.append(lanFit.Parameters()[1])
    mpv_err.append(lanFit.Errors()[1])

    h5 = TH1F(hname,hname,100,-100,100)
    ch.Draw('amp['+str(Ch)+']*1e9/risetime['+str(Ch)+'] >>' +hname,TCut('LP2_'+str(min_lgad_cfd)+'['+str(Ch)+']!=0&&LP2_'+str(min_photek_cfd)+'[3]!=0&&amp['+str(Ch)+']>'+str(ampCut)+'&&amp[3]>'+str(photekMinCut)+'&&amp[3]<'+str(photekMaxCut)))
    risetime_arr.append(abs(h5.GetMean()))
    risetime_err_arr.append(abs(h5.GetMeanError()))


print baselineRMS_arr
print slewrate_arr
jitter = [float(ai)/bi for ai,bi in zip(baselineRMS_arr,slewrate_arr)]
mpv_over_noise = [float(ai)/bi for ai,bi in zip(mpv,baselineRMS_arr)]

MakeGraphErrors(nfreq,freq_arr,sigma_arr,freq_err_arr,sigma_err_arr,'Filter Frequency [MHz]','Time Resolution [ps]',outputLoc,'TimRes_vs_Freq_'+str(sensor))
MakeGraphErrors(nfreq,freq_arr,baselineRMS_arr,freq_err_arr,baselineRMS_err_arr,'Filter Frequency [MHz]','Baseline RMS',outputLoc,'BaselineRMS_vs_Freq_'+str(sensor))
MakeGraphErrors(nfreq,freq_arr,slewrate_arr,freq_err_arr,slewrate_err_arr,'Filter Frequency [MHz]','Slew Rate (dV/dt)',outputLoc,'dVdT_vs_Freq_'+str(sensor))
MakeGraphErrors(nfreq,freq_arr,mpv,freq_err_arr,mpv_err,'Filter Frequency [MHz]','Amplitude [mV]',outputLoc,'Amp_vs_Freq_'+str(sensor))
MakeGraphErrors(nfreq,freq_arr,risetime_arr,freq_err_arr,risetime_err_arr,'Filter Frequency [MHz]','Rise time [ns]',outputLoc,'Risetime_vs_Freq_'+str(sensor))
# MakeGraph(nfreq,freq_arr,array('d',jitter),'Filter Frequency [MHz]','Jitter [ns]',outputLoc,'Jitter_vs_Freq_'+str(sensor))
MakeGraph(nfreq,freq_arr,array('d',jitter),'Filter Frequency [MHz]','Expected Jitter [ps]',outputLoc,'Jitter_vs_Freq_'+str(sensor))
MakeGraph(nfreq,freq_arr,min_cfdLGAD,'Filter Frequency [MHz]','Min. LGAD cfd',outputLoc,'MinLGAD_vs_Freq_'+str(sensor))
MakeGraph(nfreq,freq_arr,array('d',mpv_over_noise),'Filter Frequency [MHz]','MPV/Baseline RMS',outputLoc,'MPVoverNoise_Freq_'+str(sensor))
