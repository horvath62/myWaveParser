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

    plot1.set_xlim([int(slider1.val), int(slider2.val)])
    plot1.set_ylim([min(chan1+chan2), max(chan1+chan2)])
    if (slider2.val-slider1.val) < 100:
        plot1.set_xticks(np.arange(int(slider1.val), int(slider2.val), 10))
    else:
        plot1.set_xticks(np.arange(int(slider1.val), int(slider2.val), int(10**(int(np.log10(slider2.val-slider1.val))))//2))

    zcrosslist1 = zerocrossing(x1, chan1, slider1.val, slider2.val)
    #zcrosslist2 = zerocrossing(x1, chan2, slider1.val, slider2.val))

    print(zcrosslist1)

    print(chan1[slider1.val:slider2.val])


    plot2.cla()
    plot3.cla()

    yfft1 = fft(chan1[slider1.val:slider2.val])
    yfft2 = fft(chan2[slider1.val:slider2.val])
    xfft = fftfreq(slider2.val-slider1.val+1)

    #slider4.set(xfft[-1])

    #print(len(xfft), len(yfft1), len(yfft2))
    #print(xfft)
    #print("#### abs yfft1 ###")
    #print(np.abs(yfft1))
    #print("#### abs yfft2 ###")
    #print(np.abs(yfft2))

    [fftline1] = plot2.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2), abs(yfft1[0:len(xfft) // 2]), label='fft1')
    [fftline2] = plot2.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2), abs(yfft2[0:len(xfft) // 2]), label='fft2')

    [angleline1] = plot3.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2), 57.2975 * np.angle(yfft1[0:len(xfft) // 2]), label='fft1')
    [angleline2] = plot3.plot(np.linspace(0, len(xfft) // 2 - 1, len(xfft) // 2), 57.2975 * np.angle(yfft2[0:len(xfft) // 2]), label='fft1')

    plt.show()


def fftslider_on_changed(val):

    print("FFT Slider", fftslider1.val, fftslider2.val)

    plot2.set_xlim([int(fftslider1.val), int(fftslider2.val)])
    plot3.set_xlim([int(fftslider1.val), int(fftslider2.val)])
    yfft1min = np.min(np.abs(yfft1[fftslider1.val:fftslider2.val]))
    yfft2min = np.min(np.abs(yfft2[fftslider1.val:fftslider2.val]))
    yfft1max = np.max(np.abs(yfft1[fftslider1.val:fftslider2.val]))
    yfft2max = np.max(np.abs(yfft2[fftslider1.val:fftslider2.val]))
    yfftmin = np.min([yfft1min,yfft2min])
    yfftmax = np.max([yfft1max,yfft2max])

    yfft1temp = 0
    yfft2temp = 0
    for i in range(0, len(xfft)//2-1):
        if np.abs(yfft1[i]) > yfft1temp:
            yfft1temp = np.abs(yfft1[i])
        if np.abs(yfft2[i]) > yfft2temp:
            yfft2temp = np.abs(yfft2[i])
        print(format(i,'5d'), format(xfft[i],'7.5f'),
              "#1#", format(np.abs(yfft1[i]),'10.2f'), format(yfft1temp,'10.2f'),
              "#2#", format(np.abs(yfft2[i]),'10.2f'), format(yfft2temp,'10.2f'))

    #yfft2min = min(np.abs(yfft2[fftslider1.val:fftslider2.val]))
    #yfft2max = max(np.abs(yfft2[fftslider1.val:fftslider2.val]))

    plot2.set_ylim([yfftmin, yfftmax])

    print("###YLIM###:", plot2.get_ylim(), " #MIN# ", yfft1min,yfft2min, yfftmin, "#MAX#", yfft1max, yfft2max, yfftmax)

    plt.show()


# DATA above this level is not noise
NOISETHRESHOLD = 2
PREDATA = True
datacount = 0
GRAPHX = 2000
chan1 = np.array([])
chan2 = np.array([])
x1 = np.array([])

####################
# SELECT FILE      #
####################
'''
root = tk.Tk()
root.withdraw()
myFile = filedialog.askopenfile()

WaveFile = myFile.name
'''

'''
### AUTO SELECT FILE DURING DEBUG
'''
WaveFile = "C:/synth_samples/Rhodes_C4_session.wav"
'''
#####################################


'''
print("File selected:", WaveFile)

# OPEN FILE
f = open(WaveFile, "rb")
content = f.read()
print("WAVE FILE LENGTH =", len(content), " bytes")

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

        # No longer noise, so process data, put into channel arrays
        if not PREDATA:
            datacount += 1
            if datacount < GRAPHX:
                chan1 = np.append(chan1, [(signedint16(content[i] + 0x100 * content[i + 1]))])
                chan2 = np.append(chan2, [(signedint16(content[i + 2] + 0x100 * content[i + 3]))])
                x1 = np.append(x1, [datacount])

    print("NONE ZERO DATA STARTS AT BYTE LOCATION:", NONZERODATA)
    print("NOISE (NONE ZERO DATA) THRESHOLD:", NOISETHRESHOLD)
    print("DATA SAMPLES PROCESSED", datacount, GRAPHX, chan1.size, x1.size)

else:
    print("NO DATA FOUND")

print()
print('###CHAN1###')
print(chan1)



################################
#       CALCULATIONS           #
################################


yfft1 = fft(chan1)
yfft2 = fft(chan2)
xfft = fftfreq(x1.size)

# PLOT
fig = plt.figure(1, figsize=(8,10),dpi=100)



####################
# PLOT 1  (TIME)  ##
####################

#add_axes[left, bottom, width, height]
plot1 = fig.add_axes([0.1, 0.7, 0.6, 0.3])
plot1.grid()
#plot1.set_title("Wave File")
#plot1.set_ylabel("amplitude")
#plot1.set_xlabel("time")
plot1.set_xlim([0, GRAPHX])
plot1.set_ylim([-32768, 32768])
[chanline1] = plot1.plot(x1, chan1, label='time1', linewidth=2, color='green')
[chanline2] = plot1.plot(x1, chan2, label='time2', linewidth=2, color='red')

slider1ax = fig.add_axes([0.1, 0.6, 0.6, 0.03])
slider1 = Slider(slider1ax, 'start', 0, GRAPHX, valinit=0, valstep=1)
slider2ax = fig.add_axes([0.1, 0.55, 0.6, 0.03])
slider2 = Slider(slider2ax, 'width', 0, GRAPHX, valinit=GRAPHX, valstep=1)

slider1.on_changed(timeslider_on_changed)
slider2.on_changed(timeslider_on_changed)

fig.text(0.72, 0.975, "WAVEFILE ANALYZER:" )
fig.text(0.72, 0.95, "SAMPLING FREQ:" + format(SAMPLEFREQ,'7.0f'))
fig.text(0.72, 0.925, "SAMPLE INT:"+ format(1/SAMPLEFREQ*1e6,'6.2f')+'us' )
fig.text(0.72, 0.90, "CHANNELS:"+format(NUMCHANNELS, '1d'))
fig.text(0.72, 0.875, "BITS PER SAMPLE:"+format(BITSPERSAMPLE, '2d'))
fig.text(0.72, 0.85, "SAMPLES:"+format(DATACHUNKSIZE,'8d'))
fig.text(0.72, 0.825, "FUND. FREQ:"+format(0,'5.2f') )

# Create the scatter plot
# plt.scatter(x=x, y=y)



# PLOT 2 (FFT)  #################

'''
print()
print("FFT freq range:", xfft[0], " to ", xfft[len(xfft)//2-1])
print("   number of freq:", len(xfft), )
print(xfft)
for i in range(0, len(xfft)//2):
    print(i, " ", format(xfft[i],'5.3f'), " ",x1[i])
'''
'''
print()
print("Chan 1: first FFT amp:", yfft1[0], "last FFT amp:", yfft1[len(xfft)//2], "max:", max(yfft1))
print("Chan 2: first FFT amp:", yfft2[0], "last FFT amp:", yfft2[len(xfft)//2], "max:", max(yfft1))
print()
'''

plot2 = fig.add_axes([0.1, 0.4, 0.6, 0.1])
plot2.set_xlim([0, len(xfft)//2])
plot2.set_ylim([min(np.abs(yfft1) + np.abs(yfft2)), max(np.abs(yfft1) + np.abs(yfft2))])

'''
print("### abs yfft1 ####")
print(np.abs(yfft1[0:len(xfft)//2]))
print("MAX:",np.amax(np.abs(yfft1[0:len(xfft)//2])))
print("### abs yfft2 ####")
print(np.abs(yfft2[0:len(xfft)//2]))
print("MAX:",np.amax(np.abs(yfft2[0:len(xfft)//2])))
'''

[fftline1] = plot2.plot(np.linspace(0, len(xfft)//2-1, len(xfft)//2), abs(yfft1[0:len(xfft)//2]), label='fft1')
[fftline2] = plot2.plot(np.linspace(0, len(xfft)//2-1, len(xfft)//2), abs(yfft2[0:len(xfft)//2]), label='fft2')

plot3 = fig.add_axes([0.1, 0.2, 0.6, 0.1])
plot3.set_xlim([0, len(xfft//2)])
[angleline1] = plot3.plot(np.linspace(0, len(xfft)//2-1, len(xfft)//2), 57.2975*np.angle(yfft1[0:len(xfft)//2]), label='fft1')
[angleline2] = plot3.plot(np.linspace(0, len(xfft)//2-1, len(xfft)//2), 57.2975*np.angle(yfft2[0:len(xfft)//2]), label='fft1')

'''
print(chanline1.get_data())
print(chanline1.get_path())
print(chanline2)
print(fftline1.get_data())
print(fftline1.get_path())
print(fftline2)
'''

fftslider1ax = fig.add_axes([0.1, 0.1, 0.8, 0.03])
fftslider1 = Slider(fftslider1ax, 'start', 0, len(xfft)//2, valinit=0, valstep=1)
fftslider2ax = fig.add_axes([0.1, 0.05, 0.8, 0.03])
fftslider2 = Slider(fftslider2ax, 'width', 0, len(xfft)//2, valinit=len(xfft)//2, valstep=1)

#fftslider_on_changed(fftslider1)
fftslider1.on_changed(fftslider_on_changed)
fftslider2.on_changed(fftslider_on_changed)

plt.show()

