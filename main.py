import tkinter as tk
from tkinter import filedialog

from scipy.fft import fft, fftfreq, rfft, ifft
#from scipy.signal import blackman
import matplotlib.pyplot as plt
import numpy as np



# Convert a signed 16-bit value to signed integer (i.e. 0xffff => -1)
def signedint16(value):
    if value >= 0x8000:
        value -= 0x10000
    return value


# Print a line of data (file byte position, hex value and integer values)
def printbytes(i, desc, bytes):
    print(" ", format(i, '#04x'), "(", i, ") : ", desc, end='')
    if bytes == 4:
        print(" ", format(content[i], '#04x'), format(content[i + 1], '#04x'), end='')
        print(" ", format(content[i + 2], '#04x'), format(content[i + 3], '#04x'), end='')
        print(":", format(content[i] + 0x100 * content[i + 1] + 0x10000 * content[i + 2] + 0x1000000 * content[i + 3],
                          '10d'), end='')
        print(":", format(signedint16(content[i] + 0x100 * content[i + 1]), '6d'), end='')
        print(":", format(signedint16(content[i + 2] + 0x100 * content[i + 3]), '6d'))

    elif bytes == 2:
        print(" ", format(content[i], '#04x'), format(content[i + 1], '#04x'), end='')
        print("           :", content[i] + 0x100 * content[i + 1])

    else:
        print("")


# DATA above this level is not noise
NOISETHRESHOLD = 2
PREDATA = True
datacount = 0
GRAPHX = 1000
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
print("WAVE FILE LENGTH =", len(content))

#ENDDATA = (len(content) // 4) * 4 - 4
ENDDATA = 110000


for i in range(0, len(content)):
    # print("%3d %s" % (content[i], chr(content[i])))
    # print(chr(content[i]))
    if chr(content[i]) == "R" and chr(content[i + 1]) == "I" and chr(content[i + 2]) == "F" and chr(
            content[i + 3]) == "F":
        print("RIFF@", i, hex(i))
    if chr(content[i]) == "W" and chr(content[i + 1]) == "A" and chr(content[i + 2]) == "V" and chr(
            content[i + 3]) == "E":
        print("WAVE@", i, hex(i))
    if chr(content[i]) == "f" and chr(content[i + 1]) == "m" and chr(content[i + 2]) == "t" and chr(
            content[i + 3]) == " ":
        printbytes(i, "fmt            ", 4)
        printbytes(i + 4, "Sub-chunk size ", 4)
        printbytes(i + 8, "Audio Format   ", 2)
        printbytes(i + 10, "Num of Channels", 2)
        printbytes(i + 12, "Sample rate    ", 4)
        printbytes(i + 16, "Byte rate      ", 4)
        printbytes(i + 20, "Block Align    ", 2)
        printbytes(i + 22, "Bits per sample", 2)

        NUMCHANNELS = content[i+10] + 0x100 * content[i + 11]
        SAMPLEFREQ = content[i+12] + 0x100 * content[i + 13] + 0x10000 * content[i + 14] + 0x1000000 * content[i + 15]
        BITSPERSAMPLE = content[i+22] + 0x100 * content[i + 23]

    if chr(content[i]) == "d" and chr(content[i + 1]) == "a" and chr(content[i + 2]) == "t" and chr(
            content[i + 3]) == "a":
        print("Data@", i, hex(i))
        STARTDATA = i + 8
        printbytes(i + 4, "data chunk size", 4)
        printbytes(i + 8, "data:          ", 4)
        printbytes(i + 12, "data:          ", 4)
        printbytes(i + 16, "data:          ", 4)
        printbytes(i + 20, "data           ", 4)
        printbytes(i + 24, "data:          ", 4)
        printbytes(i + 28, "data:          ", 4)
        printbytes(i + 32, "data:          ", 4)

    if i == 64:
        break



print()
print("SAMPLE FREQ:", SAMPLEFREQ)
print("NUM OF CHANNELS", NUMCHANNELS)
print("BITS PER SAMPLE",BITSPERSAMPLE)
print("WAVE FILE DATA PROCESSED IN BYTE LOCATIONS", STARTDATA, " to ", ENDDATA)



# GOING THROUGH 2 channel data (each channel 2 bytes)

for i in range(STARTDATA, ENDDATA, 4):
    # checking if data is below noise threshold
    if (signedint16(content[i] + 0x100 * content[i + 1]) > NOISETHRESHOLD or
            signedint16(content[i] + 0x100 * content[i + 1]) < -NOISETHRESHOLD or
            signedint16(content[i + 2] + 0x100 * content[i + 3]) > NOISETHRESHOLD or
            signedint16(content[i + 2] + 0x100 * content[i + 3]) < -NOISETHRESHOLD):
        PREDATA = False
        NONEZEROLOC = i

    # No longer noise, so process data, put into channel arrays
    if PREDATA == False:
        datacount += 1
        if datacount < GRAPHX:
            chan1 = np.append(chan1, [(signedint16(content[i] + 0x100 * content[i + 1]))])
            chan2 = np.append(chan2, [(signedint16(content[i+2] + 0x100 * content[i + 3]))])
            x1 = np.append(x1, [datacount])

print("NONE ZERO DATA STARTS AT BYTE LOCATION:", NONEZEROLOC)
print("NOISE THRESHOLD (NONE ZERO DATA) ",NOISETHRESHOLD)
print("DATA SAMPLES PROCESSED", datacount, GRAPHX, chan1.size, x1.size)
'''
    if PREDATA == False:
            # printbytes(i, "data:          ", 4)
'''


# FFT CALCULATION
yfft = fft(chan1)
xfft = fftfreq(x1.size)



# PLOT


plt.figure(1)

plt.subplot(211)
plt.axis([0, GRAPHX, -32768, 32768])
plt.plot(x1, chan1)
plt.plot(x1, chan2)
plt.xlabel('samples')
plt.ylabel('value')

plt.subplot(212)
plt.plot(xfft, yfft)

'''
plt.subplot(413)
plt.plot(xfft, 2/N*np.abs(yfft[0:N//2].imag))

plt.subplot(414)
plt.plot(xfft, 2/N*np.abs(ywfft[0:N//2]))
'''
plt.show()
