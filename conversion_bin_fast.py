import struct  #struct unpack result - tuple
import numpy as np
import matplotlib.pyplot as plt
import ROOT
from ROOT import *
import time
import optparse
import argparse
import os

from scipy import signal
from scipy.signal import butter,sosfilt,sosfreqz,lfilter,filtfilt

parser = argparse.ArgumentParser(description='Creating a root file from Binary format')

parser.add_argument('--Run',metavar='Run', type=str, help='Run Number to process',required=True)
parser.add_argument('--Freq',metavar='Freq', type=str, help='Filter cutoff',required=True)
args = parser.parse_args()
run = args.Run
freq = args.Freq
#RawDataPath = '/home/daq/2019_04_April_CMSTiming/KeySightScope/KeySightScopeMount/'
RawDataPath = '/home/daq/FilterStudy/binFiles/'
RawDataLocalCopyPath = '/home/daq/2019_04_April_CMSTiming/KeySightScope/RawData/'
#OutputFilePath = '/home/daq/2019_04_April_CMSTiming/KeySightScope/RecoData/ConversionRECO/'
#OutputFilePath = '/home/daq/2019_04_April_CMSTiming/KeySightScope/RecoData/Test_LowPassFilter/'
OutputFilePath = '/home/daq/FilterStudy/reco_LocalTest/'
Debug=False

def keysight_get_points(filepath_in):
    my_file = open(filepath_in, 'rb')
    b_cookie = my_file.read(2) #char
    b_version = my_file.read(2) #char
    b_size = struct.unpack('i', my_file.read(4)) #int32 - i
    b_nwaveforms = struct.unpack('i', my_file.read(4)) #int32 - i ## number of events (or segments)
    b_header = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = b_header[0] - 4
    # print " remaining = ", remaining
    b_wavetype = struct.unpack('i', my_file.read(4)) #int32 - i
    # print "b_wavetype = ", b_wavetype
    remaining = remaining - 4
    b_wavebuffers = struct.unpack('i', my_file.read(4)) #int32 - i
    # print " b_wavebuffers = ", (b_wavebuffers[0])
    remaining = remaining - 4
    b_points = struct.unpack('i', my_file.read(4)) #int32 - i
    # my_file.close()
    return b_points


def fast_Keysight_bin(filepath_in, index_in,n_points):
    global x_axis, y_axis, remaining
    x_axis = []
    y_axis = []

    # read from file
    my_index = index_in
    # start = time.time()
    my_file = open(filepath_in, 'rb')

    b_cookie = my_file.read(2) #char
    b_version = my_file.read(2) #char
    b_size = struct.unpack('i', my_file.read(4)) #int32 - i
    b_nwaveforms = struct.unpack('i', my_file.read(4)) #int32 - i ## number of events (or segments)
    # end = time.time()

    if my_index <= b_nwaveforms[0]:
        my_index = my_index
    else:
        my_index = 1
    counter = 0

    nBytesPerEvent = 140+12+(4*n_points)
    # print nBytesPerEvent
    # nBytesPerEvent = 16152 ##-- 140+12+16000
    my_file.seek( (nBytesPerEvent)*(my_index-1) ,1)
    b_header = struct.unpack('i', my_file.read(4)) #int32 - i
    # if b_header[0]!=140:
    #     print "bad event, skipping"
    #     x_axis = np.linspace(0, 1000, n_points)
    #     y_axis = np.linspace(0, 1000, n_points)
    #     return [x_axis,y_axis]
    #print " b_header = ", (b_header)
    remaining = b_header[0] - 4
    #print " remaining = ", remaining
    b_wavetype = struct.unpack('i', my_file.read(4)) #int32 - i
    #print "b_wavetype = ", b_wavetype
    remaining = remaining - 4
    b_wavebuffers = struct.unpack('i', my_file.read(4)) #int32 - i
    #print " b_wavebuffers = ", (b_wavebuffers[0])
    remaining = remaining - 4
    b_points = struct.unpack('i', my_file.read(4)) #int32 - i
    #print " b_point =", (b_points)
    remaining = remaining - 4
    b_count = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_x_disp_range = struct.unpack('f', my_file.read(4)) #float32 - f
    remaining = remaining - 4
    b_x_disp_orig = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_x_inc = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_x_orig = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_x_units = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_y_units = struct.unpack('i', my_file.read(4)) #int32 - i
    remaining = remaining - 4
    b_date =  my_file.read(16)
    remaining = remaining - 16
    b_time =  my_file.read(16)
    remaining = remaining - 16
    b_frame =  my_file.read(24)
    remaining = remaining - 24
    b_wave_string =  my_file.read(16)
    remaining = remaining - 16
    b_time_tag = struct.unpack('d', my_file.read(8)) #double - d
    remaining = remaining - 8
    b_segment_index = struct.unpack('I', my_file.read(4)) #unsigned int - I
    remaining = remaining - 4
    # print " remaining is now = ", remaining

    #print " x origin = ", b_x_orig[0]
    #print " x inc = ", b_x_inc[0]
    #print b_points[0]

    x_axis = b_x_orig[0] + b_x_inc[0] * np.linspace(0, b_points[0]-1, b_points[0])
 
   # j loop on buffers - only returns the last buffer
    for j in range(0,b_wavebuffers[0]):
        counter += 1
        #header size - int 32
        b_header = struct.unpack('i' , my_file.read(4)) #int32 - i
       # print 'buffer header size: ' ,( str(b_header[0]))
        remaining = b_header[0] - 4
        #buffer type - int16
        b_buffer_type = struct.unpack('h' , my_file.read(2)) #int16 - h
        # print 'buffer type: ' ,( str(b_buffer_type[0]))
        remaining = remaining - 2
        #bytes per point - int16
        b_bytes_per_point = struct.unpack('h' , my_file.read(2)) #int16 - h
        #print 'bytes per point: ' ,( str(b_bytes_per_point[0]) )
        remaining = remaining - 2
        #buffer size - int32
        b_buffer_size = struct.unpack('i' , my_file.read(4)) #int32 - i
        #print 'buffer size: ' ,( str(b_buffer_size[0]) )
        remaining = remaining - 4
        # create y axis for voltage vector
        # currently ONLY standard voltage -  float32 - Buffer Type 1 / 2 / 3
        # print  " buffer size = ", (b_buffer_size[0])
        b_y_data = my_file.read(b_buffer_size[0])
        y_axis = struct.unpack("<"+str(b_points[0])+"f", b_y_data)
    return_array = [x_axis,y_axis]
    # print " counter = ", (counter)
    #print len(return_array[0])
    # print (return_array[1])
    # my_file.close()
    return return_array, b_nwaveforms, b_points, b_x_inc[0]

#def butter_lowpass(lowcut, fs, order=3):
    #nyq = 0.5 * fs
    #low = lowcut / nyq
    #high = highcut / nyq
    #b, a = butter(order, [low, high], analog=False,btype='band',output='sos')
    #sos = butter(order, [low], analog=False,btype='low',output='sos')
    #return sos

#def butter_lowpass_filter(data, lowcut, fs, order=3):
    #sos = butter_lowpass(lowcut, fs, order=order)
    #y = lfilter(b, a, data)
    #y = sosfilt(sos, data)
    #return y

def butter_lowpass(lowcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b,a = butter(order, low, analog=False,btype='low')
    return b,a
def butter_lowpass_filter(data, lowcut, fs, order=3):
    b,a = butter_lowpass(lowcut,fs,order=order)
    y = filtfilt(b, a, data)
    return y

#b, a = signal.butter(4, 100, 'low', analog=True)
#w,h = signal.freqs(b,a)
#sos = signal.butter(10,15,'lp',1000,output='sos')

#### Copy files locally, and if successful, move them to "to_delete" directory

print "Copying files locally."
rawFiles = RawDataPath + 'Wavenewscope_CH*_'+run+'.bin'
#os.system('rsync -z -v %s %s && mv %s %s' % (rawFiles,RawDataLocalCopyPath,rawFiles,RawDataPath+"/to_delete/"))
os.system('cp %s %s && mv %s %s' % (rawFiles,RawDataLocalCopyPath,rawFiles,RawDataPath+"/to_delete/"))
print "Starting conversion."
## read the input files
print "file1"
#inputFile1 = RawDataLocalCopyPath + 'Wavenewscope_CH1_'+run+'.bin'
#inputFile1 = 'Wavenewscope_CH1_'+run+'.bin'
print "file2"
#inputFile2 = RawDataLocalCopyPath + 'Wavenewscope_CH2_'+run+'.bin'
#inputFile2 = 'Wavenewscope_CH2_'+run+'.bin'
print "file3"
#inputFile3 = RawDataLocalCopyPath + 'Wavenewscope_CH3_'+run+'.bin'
#inputFile4 = RawDataLocalCopyPath + 'Wavenewscope_CH4_'+run+'.bin'
inputFile1 = 'Wavenewscope_CH1_'+run+'.bin'
inputFile2 = 'Wavenewscope_CH1_'+run+'.bin'
inputFile3 = 'Wavenewscope_CH1_'+run+'.bin'
inputFile4 = 'Wavenewscope_CH1_'+run+'.bin'
#inputFile1 = '/home/daq/fnal_tb_18_11/AgilentMount/Wavenewscope_CH1_test_4000events.bin'
# inputFile2 = '/home/daq/fnal_tb_18_11/AgilentMount/Wavenewscope_CH2_test_4000events.bin'
# inputFile3 = '/home/daq/fnal_tb_18_11/AgilentMount/Wavenewscope_CH3_test_4000events.bin'
# inputFile4 = '/home/daq/fnal_tb_18_11/AgilentMount/Wavenewscope_CH4_test_4000events.bin'

n_points = keysight_get_points(inputFile1)[0]
print n_points
#inputFile1 = 'Wavenewscope_CH3_Apr2_87.bin'
# inputFile2 = 'Wavenewscope_CH3_Apr2_87.bin'
# inputFile3 = 'Wavenewscope_CH3_Apr2_87.bin'
# inputFile4 = 'Wavenewscope_CH3_Apr2_87.bin'
# print "HERE 1"
input1 = fast_Keysight_bin(inputFile1,1,n_points) ## to get the number of segments/events and points

n_events = list (input1[1])[0] ## number of events/segments
n_points = list(input1[2])[0] ## number of points acquired for each event/segment
print "n_events = ", n_events
print "n_points = ", n_points
print "here" ,input1[3]
## prepare the output files
outputFile = '%srun_scope%s_%s.root' % (OutputFilePath, run, freq)
outRoot = TFile(outputFile, "RECREATE")
outTree = TTree("pulse","pulse")

i_evt = np.zeros(1,dtype=np.dtype("u4"))
channel_old = np.zeros([4,n_points],dtype=np.float32)
time = np.zeros([1,n_points],dtype=np.float32)
channel = np.zeros([4,n_points],dtype=np.float32)
filtered = np.zeros([4,n_points],dtype=np.float32)

outTree.Branch('i_evt',i_evt,'i_evt/i')
outTree.Branch('channel_old', channel_old, 'channel_old[4]['+str(n_points)+']/F' )
outTree.Branch('time', time, 'time[1]['+str(n_points)+']/F' )
outTree.Branch('channel', channel, 'channel[4]['+str(n_points)+']/F' )

#fs = 5000000000 
#fs = 1./(2.5e-11) ## for run 12504
#fs = 1./(2e-11)
#fs = 1./(n_points)
#fs = 40000000000
fs = 1./(input1[3])
print fs
#lowcut = 1000000000
#lowcut = 0.0002 
#highcut = 500000000
#lowcut = 750000000
lowcut = float(freq)*1000000
print lowcut
print "cut off frequency", lowcut
## get voltage values for each event/segment (return array gives voltage and time values for each segment. number of entries in the time and voltage arrays are equal to number of points)
#print "HERE 1"
if Debug: n_events=10
for i in range(n_events):
    if i%1000==0:
        print "Processing event %i" % i
    #channel[0] = fast_Keysight_bin(inputFile1, i+1, n_points)[0][1]
    #channel[1] = fast_Keysight_bin(inputFile2, i+1, n_points)[0][1]
    #channel[2] = fast_Keysight_bin(inputFile3, i+1, n_points)[0][1]
    #channel[3] = fast_Keysight_bin(inputFile4, i+1, n_points)[0][1]
    time[0] = fast_Keysight_bin(inputFile4, i+1, n_points)[0][0]
    i_evt[0] = i
    channel[0] = butter_lowpass_filter(fast_Keysight_bin(inputFile1, i+1, n_points)[0][1], lowcut, fs, order=6)
    channel[1] = butter_lowpass_filter(fast_Keysight_bin(inputFile2, i+1, n_points)[0][1], lowcut, fs, order=6)
    channel[2] = butter_lowpass_filter(fast_Keysight_bin(inputFile3, i+1, n_points)[0][1], lowcut, fs, order=6)
    channel[3] = fast_Keysight_bin(inputFile4, i+1, n_points)[0][1]
    #channel[3] = butter_lowpass_filter(fast_Keysight_bin(inputFile4, i+1, n_points)[0][1], lowcut, fs, order=6)
    #channel_old[0] = butter_lowpass_filter(channel[0], lowcut, fs, order=6)
    #channel_old[1] = butter_lowpass_filter(channel[1], lowcut, fs, order=6)
    #channel_old[2] = butter_lowpass_filter(channel[2], lowcut, fs, order=6)
    #channel_old[3] = butter_lowpass_filter(channel[3], lowcut, fs, order=6)

    outTree.Fill()

print "done filling the tree"
outRoot.cd()
outTree.Write()
outRoot.Close()
