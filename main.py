import tkinter as tk
from tkinter import filedialog

from scipy.fft import fft, fftfreq, rfft, ifft
# from scipy.signal import blackman
import matplotlib.pyplot as plt
import numpy as np


# Convert a signed 16-bit value to signed integer (i.e. 0xffff => -1)
def signedint16(value):
    if value >= 0x8000:
        value -= 0x10000
    return value


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


# DATA above this level is not noise
NOISETHRESHOLD = 2
PREDATA = True
datacount = 0
GRAPHX = 500
chan1 = np.array([])
chan2 = np.array([])
x1 = np.array([])

# SELECT FILE

'''
root = tk.Tk()
root.withdraw()
myFile = filedialog.askopenfile()

WaveFile = myFile.name

'''
WaveFile = "C:/synth_samples/Rhodes_C4_session.wav"

print("File selected:", WaveFile)

# OPEN FILE
f = open(WaveFile, "rb")
content = f.read()
print("WAVE FILE LENGTH =", len(content), " bytes")

# ENDDATA = (len(content) // 4) * 4 - 4
# ENDDATA = 110000

'''
for i in range(0, 64):
    printbytes(i, "==>", 4)
'''

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

###################################
#       FFT CALCULATION           #
###################################
yfft1 = fft(chan1)
yfft2 = fft(chan2)
xfft = fftfreq(x1.size)

# PLOT
plt.figure(1)

plt.subplot(311)
plt.axis([0, GRAPHX, -32768, 32768])
plt.plot(x1, chan1)
plt.plot(x1, chan2)
plt.xlabel('samples')
plt.ylabel('value')

plt.subplot(312)
plt.plot(xfft, yfft1.real)
plt.plot(xfft, yfft2.real)

plt.subplot(313)
plt.plot(xfft[0:100], np.abs(yfft1[0:100]))


'''
plt.subplot(413)
plt.plot(xfft, 2/N*np.abs(yfft[0:N//2].imag))

plt.subplot(414)
plt.plot(xfft, 2/N*np.abs(ywfft[0:N//2]))
'''
plt.show()
