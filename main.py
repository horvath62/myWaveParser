import tkinter as tk
from tkinter import filedialog

from scipy.fft import fft, fftfreq, rfft, ifft
# from scipy.signal import blackman
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

from myFunc import *

import mpl_interactions.ipyplot as iplt
import time


# Print a line of data (file byte position, ascii description, and hex value and integer values at location i)
# pass in:  location, ascii description, number of bytes
def printbytes(i, desc, bytes):
    if i == -1:
        print("loc desc  bytes     dec")
    else:

        print(" ", format(i, '#04x'), "(", i, ") : ", desc, end='')
        if bytes == 4:
            print(" ", format(content[i], '#04x'), chr(content[i]), " ", format(content[i + 1], '#04x'),
                  chr(content[i + 1]), " ", end='')
            print(" ", format(content[i + 2], '#04x'), chr(content[i + 2]), " ", format(content[i + 3], '#04x'),
                  chr(content[i + 3]), end='')
            print(":",
                  format(content[i] + 0x100 * content[i + 1] + 0x10000 * content[i + 2] + 0x1000000 * content[i + 3],
                         '10d'), end='')
            print(":", format(signedint16(content[i] + 0x100 * content[i + 1]), '6d'), end='')
            print(":", format(signedint16(content[i + 2] + 0x100 * content[i + 3]), '6d'))

        elif bytes == 2:
            print(" ", format(content[i], '#04x'), chr(content[i + 1]), format(content[i], '#04x'), chr(content[i + 1]),
                  end='')
            print("           :", content[i] + 0x100 * content[i + 1])

        else:
            print("un supported variable in call")


def timeslider_on_changed(val):

    print("TIME SLIDER:", slider1.val, slider2.val)
    if slider2.val < slider1.val:
        slider2.set_val(slider1.val)

    global zcrosslist1
    global zcrosslist2
    global fftslider2val

    # plot1.set_title("Wave File")
    # plot1.set_ylabel("amplitude")
    # plot1.set_xlabel("time")
    # plot1.set_xlim([0, datacount - 1])
    # plot1.set_ylim([-32768, 32768])

    plot1.cla()

    [chanline1] = plot1.plot(x1[slider1.val:slider2.val], chan1[slider1.val:slider2.val], label='time1', linewidth=2, color='green')
    [chanline2] = plot1.plot(x1[slider1.val:slider2.val], chan2[slider1.val:slider2.val], label='time2', linewidth=2, color='red')

    plot1.set_xlim([int(slider1.val), int(slider2.val)])

    chan1min = np.min(chan1[slider1.val:slider2.val])
    chan2min = np.min(chan2[slider1.val:slider2.val])
    chan1max = np.max(chan1[slider1.val:slider2.val])
    chan2max = np.max(chan2[slider1.val:slider2.val])
    chanmin = np.min([chan1min,chan2min])
    chanmax = np.max([chan1max,chan2max])
    plot1.set_ylim([chanmin,chanmax])
    plot2.set_ylim(slider2.val-slider1.val)
    plot3.set_ylim(slider2.val-slider1.val)

    if (slider2.val-slider1.val) < 100:
        plot1.set_xticks(np.arange(int(slider1.val), int(slider2.val), 10))
    else:
        plot1.set_xticks(np.arange(int(slider1.val), int(slider2.val), int(10**(int(np.log10(slider2.val-slider1.val))))//2))

    # ZERO CROSSING LIST MADE FROM DATA
    zcrosslist1 = zerocrossing(x1, chan1, slider1.val, slider2.val)
    zcrosslist2 = zerocrossing(x1, chan2, slider1.val, slider2.val)
    # PLOT ZERO CROSSING
    zcross1 = plot1.scatter(x=zcrosslist1, y=[0]*len(zcrosslist1))
    zcross2 = plot1.scatter(x=zcrosslist2, y=[0]*len(zcrosslist2))

    '''
    print("zcross1,zcross2")
    print(zcross1.get_offsets())
    print(zcross2.get_offsets())
    '''

    # fftslider_on_changed(0)
    fftslider2.set_val(fftslider2val)

    plt.show()


def fftslider_on_changed(val):

    global fftslider2val
    global fftslider1val

    print("FFT Slider", fftslider1.val, fftslider2.val)

    # need to save slider value globally for next time this is called ( so it doesn't change)
    fftslider2val = fftslider2.val
    fftslider1val = fftslider1.val

    # IF END SLIDER IS LESS THAN START SLIDER, THATS ILLEGAL.  FORCE TO SAME
    if fftslider2.val < fftslider1.val:
        fftslider2val = fftslider1.val+1
        fftslider2.set_val(fftslider1.val+1)

    plot2.cla()
    plot3.cla()

    plot2.set_yscale("log")
    plot2.set_ylabel("FFT Amplitude")
    plot3.set_ylabel("Phase")


    # plot3.yaxis.set_major_locator(plot3.MultipleLocator(90))
    plot3.set_yticks((-180, -90, 0, 90, 180))

    # ############# FFT CALCULATIONS  #################### #
    yfft1 = fft(chan1[slider1.val:slider2.val])
    yfft2 = fft(chan2[slider1.val:slider2.val])
    xfft = fftfreq(slider2.val - slider1.val + 1)


    [fftline1] = plot2.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2), abs(yfft1[0:len(xfft) // 2]),
                            label='fft1')
    [fftline2] = plot2.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2), abs(yfft2[0:len(xfft) // 2]),
                            label='fft2')

    [angleline1] = plot3.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2),
                              57.2975 * np.angle(yfft1[0:len(xfft) // 2]), label='fft1')
    [angleline2] = plot3.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2),
                              57.2975 * np.angle(yfft2[0:len(xfft) // 2]), label='fft1')
    #############################################################

    plot2.set_xlim([int(fftslider1.val), int(fftslider2.val)])
    plot3.set_xlim([int(fftslider1.val), int(fftslider2.val)])
    yfft1min = np.min(np.abs(yfft1[fftslider1.val:fftslider2.val]))
    yfft2min = np.min(np.abs(yfft2[fftslider1.val:fftslider2.val]))
    yfft1max = np.max(np.abs(yfft1[fftslider1.val:fftslider2.val]))
    yfft2max = np.max(np.abs(yfft2[fftslider1.val:fftslider2.val]))
    yfftmin = np.min([yfft1min,yfft2min])
    yfftmax = np.max([yfft1max,yfft2max])

    plot2.set_ylim([yfftmin, yfftmax])

    plt.show()


def button1(event):
    fig2 = plt.figure(2, figsize=(8, 10), dpi=100)
    fig2.canvas.manager.set_window_title('WAVE FILE INFO   -  ' + WaveFile)
    fig2.text(0.05, 0.98, "WAVE FILE ZERO-CROSSING INTERVAL:")
    fig2.text(0.05, 0.96, "zcrosslist:" + format(zcrosslist1[0], '7.0f'))
    plot10 = fig2.add_axes([0.1,0.75,0.8,0.2])
    zeroslider1ax = fig2.add_axes([0.1, 0.70, 0.8, 0.03])
    zeroslider1 = Slider(zeroslider1ax, 'start', 0, len(zcrosslist1) - 1, valinit=0, valstep=1)
    zeroslider2ax = fig2.add_axes([0.1, 0.65, 0.8, 0.03])
    zeroslider2 = Slider(zeroslider2ax, 'end', 0, len(zcrosslist1) - 1, valinit=len(zcrosslist1)-1, valstep=1)

    freqlist1=[]
    freqlist2=[]

    #textbuf="ZERO CROSSING FREQUENCY and NOTE:\n" \
    textbuf = "Channel 1:\n"
    for i in range(1, len(zcrosslist1)-1):
        freq = SAMPLEFREQ/(zcrosslist1[i+1]-zcrosslist1[i-1])
        textbuf = textbuf + freqnote(freq) + "  " + format(freq, '8.2f') + "hz\n"
        freqlist1.append(freq)

    fig2.text(0.05, 0.6, textbuf, va="top")

    textbuf = "Channel 2:\n"
    for i in range(1, len(zcrosslist2) - 1):
        freq = SAMPLEFREQ / (zcrosslist2[i + 1] - zcrosslist2[i - 1])
        textbuf = textbuf + freqnote(freq) + "  " + format(freq, '8.2f') + "hz\n"
        freqlist2.append(freq)

    fig2.text(0.55, 0.6, textbuf, va="top")

    print(freqlist1)


    plot10.plot(np.linspace(0, len(freqlist1)-1, len(freqlist1)), freqlist1)
    plot10.plot(np.linspace(0, len(freqlist2)-1, len(freqlist2)), freqlist2)

    plt.show()


# DATA above this level is not noise
NOISETHRESHOLD = 2
PREDATA = True
datacount = 0
chan1 = np.array([])
chan2 = np.array([])
x1 = np.array([])
zcrosslist1 = []
zcrosslist2 = []

#############################################################################
# ####         SELECT, OPEN, READ and PROCESS WAVE FILE               ##### #
#############################################################################

# file selection dialog box
'''
root = tk.Tk()
root.withdraw()
myFile = filedialog.askopenfile()

WaveFile = myFile.name
'''

'''
### AUTO SELECT FILE DURING DEBUG
WaveFile = "C:/synth_samples/Rhodes_C4_session.wav"
'''
WaveFile = "C:/synth_samples/short_stereo_noerror.wav"

###########################################################################

print("File selected:", WaveFile)

f = open(WaveFile, "rb")
content = f.read()
print("WAVE FILE LENGTH =", len(content), " bytes")
f.close()

# ENDDATA = (len(content) // 4) * 4 - 4
# ENDDATA = 110000


if chr(content[0]) == "R" and chr(content[1]) == "I" and chr(content[2]) == "F" and chr(content[3]) == "F":
    print("RIFF FILE DETECTED in:", WaveFile)
else:
    print("NOT RIFF FILE in", WaveFile)

for i in range(5, 16):
    if (chr(content[i]) == "W" and chr(content[i + 1]) == "A" and chr(content[i + 2]) == "V" and chr(
            content[i + 3]) == "E" and
            chr(content[i + 4]) == "f" and chr(content[i + 5]) == "m" and chr(content[i + 6]) == "t"):
        print("WAVE FILE DETECTED:", WaveFile)
        printbytes(0, "RIFF", 4)
        printbytes(i, "WAVE", 4)
        printbytes(i + 4, "fmt ", 4)
        printbytes(i + 8, "Sub-chunk size ", 4)
        SUBCHUNKSIZE = content[i + 8] + 0x100 * content[i + 9] + 0x10000 * content[i + 10] + 0x1000000 * content[i + 11]
        print("SUB-CHuNK SIZE", SUBCHUNKSIZE)
        printbytes(i + 12, "Audio Format   ", 2)
        printbytes(i + 14, "Num of Channels", 2)
        printbytes(i + 16, "Sample rate    ", 4)
        printbytes(i + 20, "Byte rate      ", 4)
        printbytes(i + 24, "Block Align    ", 2)
        printbytes(i + 26, "Bits per sample", 2)

        NUMCHANNELS = content[i + 14] + 0x100 * content[i + 15]
        SAMPLEFREQ = content[i + 16] + 0x100 * content[i + 17] + 0x10000 * content[i + 18] + 0x1000000 * content[i + 19]
        BITSPERSAMPLE = content[i + 26] + 0x100 * content[i + 27]

        NOTWAVEFILE = False
        # print("check this:",NUMCHANNELS, SAMPLEFREQ, BITSPERSAMPLE)
        break

    else:
        NOTWAVEFILE = True

if NOTWAVEFILE:
    print("WAVE FILE NOT DETECTED in:", WaveFile)

DATAFOUND = False
for i in range(5, 64):
    if (chr(content[i]) == "d" and chr(content[i + 1]) == "a" and chr(content[i + 2]) == "t" and chr(
            content[i + 3]) == "a"):
        # data field found
        printbytes(i, "DATA", 4)
        DATAFOUND = True
        DATASTART = i + 8
        DATACHUNKSIZE = content[i + 4] + 0x100 * content[i + 5] + 0x10000 * content[i + 6] + 0x1000000 * content[i + 7]
        print("data chunk size", DATACHUNKSIZE)
        DATAEND = DATASTART + DATACHUNKSIZE
        break

if DATAFOUND:

    print("WAVE FILE DATA HAS", DATACHUNKSIZE, "BYTES IN LOCATIONS:", DATASTART, " to ", DATAEND)
    # print("check this:", DATASTART, DATAEND, DATASTART + DATACHUNKSIZE, len(content))

    datacount = 0
    predatacount = 0
    PREDATA = True
    for i in range(DATASTART, DATAEND, 4):

        # checking if data is below noise threshold
        if PREDATA:
            if (signedint16(content[i] + 0x100 * content[i + 1]) > NOISETHRESHOLD or
                    signedint16(content[i] + 0x100 * content[i + 1]) < -NOISETHRESHOLD or
                    signedint16(content[i + 2] + 0x100 * content[i + 3]) > NOISETHRESHOLD or
                    signedint16(content[i + 2] + 0x100 * content[i + 3]) < -NOISETHRESHOLD):
                PREDATA = False
                NONZERODATA = i
            else:
                predatacount += 1

        # No longer noise, so process data, put into channel arrays
        if not PREDATA:
            datacount += 1
            #if datacount < GRAPHX:
            if datacount > 0:
                #print("i:",i,"content[i]", content[i], "datacount",datacount)
                chan1 = np.append(chan1, [(signedint16(content[i] + 0x100 * content[i + 1]))])
                chan2 = np.append(chan2, [(signedint16(content[i + 2] + 0x100 * content[i + 3]))])
                x1 = np.append(x1, [datacount])

    print("NONE ZERO DATA STARTS AT BYTE LOCATION:", NONZERODATA)
    print("NOISE (NONE ZERO DATA) THRESHOLD:", NOISETHRESHOLD)
    print("DATA SAMPLES PROCESSED:", datacount, chan1.size, x1.size)

else:
    print("NO DATA FOUND")

print()
#print('###CHAN1###')
#print(chan1)


#######################################################################################
# ######                                   FIGURE                                #### #
#######################################################################################

fig = plt.figure(1, figsize=(8,10),dpi=100)

####################
# PLOT 1  (TIME)  ##
####################

plot1 = fig.add_axes([0.1, 0.7, 0.6, 0.3])
plot1.grid()

slider1ax = fig.add_axes([0.1, 0.6, 0.6, 0.03])
slider1 = Slider(slider1ax, 'start', 0, datacount-1, valinit=0, valstep=1)
slider2ax = fig.add_axes([0.1, 0.55, 0.6, 0.03])
slider2 = Slider(slider2ax, 'end', 0, datacount-1, valinit=datacount-1, valstep=1)

slider1.on_changed(timeslider_on_changed)
slider2.on_changed(timeslider_on_changed)

############
#  TEXT    #
############
fig.canvas.manager.set_window_title('WAVE FILE ANALYZER   -  '+ WaveFile)
fig.text(0.72, 0.98, "WAVE FILE HEADER:" )
fig.text(0.72, 0.96, "SAMPLING FREQ:" + format(SAMPLEFREQ,'7.0f'))
fig.text(0.72, 0.94, "SAMPLE INT:"+ format(1/SAMPLEFREQ*1e6,'6.2f')+'us' )
fig.text(0.72, 0.92, "CHANNELS:"+format(NUMCHANNELS, '1d'))
fig.text(0.72, 0.90, "BITS PER SAMPLE:"+format(BITSPERSAMPLE, '2d'))
fig.text(0.72, 0.88, "DATA BYTES:"+format(DATACHUNKSIZE,'8d'))
fig.text(0.72, 0.86, "SAMPLES:"+format(DATACHUNKSIZE/NUMCHANNELS/(BITSPERSAMPLE/8),'8.0f'))

fig.text(0.72, 0.83, "PROCESSING DATA")
fig.text(0.72, 0.81, "PROCESSED SAMPLES:"+format(datacount, '8d'))
fig.text(0.72, 0.79, "NOISE FLOOR:"+format(NOISETHRESHOLD, '8d'))
fig.text(0.72, 0.77, "LEADING BYTES:"+format(predatacount, '8d'))

#############
#  BUTTONS  #
#############
axBut1 = plt.axes([0.75,0.7,0.15,0.05])
btn1 = Button(axBut1, label="Zero Crossing",)
btn1.on_clicked(button1)



######################
# PLOT 2 and 3(FFT)  #
######################

# Setup location of fft amplitude and fft phase plots (axes)
plot2 = fig.add_axes([0.1, 0.3, 0.6, 0.2])
plot3 = fig.add_axes([0.1, 0.2, 0.6, 0.1])

# Need to get freq list to initialize the slider
xfft = fftfreq(x1.size)

# Setup Sliders
fftslider1ax = fig.add_axes([0.1, 0.1, 0.6, 0.03])
fftslider1 = Slider(fftslider1ax, 'start', 0, len(xfft)//2-1, valinit=0, valstep=1)
fftslider2ax = fig.add_axes([0.1, 0.05, 0.6, 0.03])
fftslider2 = Slider(fftslider2ax, 'end', 0, len(xfft)//2-1, valinit=len(xfft)//2, valstep=1)

# Set up event calls for changes to slider
fftslider1.on_changed(fftslider_on_changed)
fftslider2.on_changed(fftslider_on_changed)

# Call Slider routine to initialize the first loaded dataset
fftslider2val = len(xfft)//2
slider1.set_val(0)


plt.show()

