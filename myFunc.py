import numpy as np
import math


# Convert a signed 16-bit value to signed integer (i.e. 0xffff => -1)
def signedint16(value):
    if value >= 0x8000:
        value -= 0x10000
    return value


# Returns musical note and cents from frequency
def freqnote(freq):
    notes = (["C ", "C#", "D ", "D#", "E ", "F ", "F#", "G ", "G#", "A ", "A#", "B "])
    ratio = freq / 16.35  # C0 frequency
    notenumber = math.log(ratio, 2) * 12
    octave = notenumber // 12
    notemod = notenumber % 12
    noteint = round(notemod)
    notecent = 100 * (notemod - noteint)
    if noteint > 11:   #because of rounding it can round up to 12
        noteint = noteint - 12
        octave = octave + 1
        # print("over11")

    # print(noteint)
    note = notes[noteint]

    # print(format(freq,'+5.2f'), format(ratio, '+5.2f'),
    # format(notenumber, '-7.2f'), format(octave, '-6.2f'), format(notemod, '-6.2f'),
    # format(noteint, '-6.2f'), format(notecent, '-6.2f'), "   ", '{0}{1:1.0f} {2:+2.0f} cents'.format(note, octave,

    return '{0}{1:1.0f} {2:+2.0f} cents'.format(note, octave, notecent)


def zerocrossing (xdata, ydata, starti, endi):
    YPOSITIVE = False
    zcross = False
    indexlist = []
    if (np.abs(ydata[starti]) >= 0 ):
        YPOSITIVE = True

    for i in range(starti + 1, endi - starti -1):
        if (ydata[i] < 0) and (YPOSITIVE):
            #print("i:", i, "ydata[i]<0:", ydata[i], YPOSITIVE)
            zcross = True
            YPOSITIVE = False

        elif (ydata[i] >= 0) and (not YPOSITIVE):
            #print("i:", i, "ydata[i]>0:", ydata[i], YPOSITIVE)
            zcross = True
            YPOSITIVE = True
        #else:
            #print("ELSE: i:",i, ydata[i])

        if zcross == True:
            deltay = ydata[i]-ydata[i-1]
            ratio = np.abs(ydata[i-1]/deltay)
            zc = (i-1) + ratio
            indexlist.append(zc)
            zcross = False
            #print("###i:",i, "ydata:", ydata[i-1], ydata[i], "calc:" ,deltay, ratio, zc)

    return indexlist


'''
############################
#     iplt                 #
############################
xtemp=[0,1,2]
ytemp=[3,2,1]


fig2 = plt.figure(2)
plot4 = fig2.add_axes([0.1, 0.5, 0.8, 0.4])
controls = iplt.plot(xtemp,ytemp, tau=(1,3,1), beta=(1,10,100), label="f1")
iplt.plot(xtemp, ytemp, controls=controls, label="f2")
'''
'''
plot3 = fig.add_subplot(313)
[fftline1] = plot3.plot(xfft, yfft1.real)
[fftline2] = plot3.plot(xfft, yfft2.real)
#plt.plot(xfft, yfft1.real)
#plt.plot(xfft, yfft2.real)
'''

'''
plt.subplot(413)
plt.plot(xfft, 2/N*np.abs(yfft[0:N//2].imag))

plt.subplot(414)
plt.plot(xfft, 2/N*np.abs(ywfft[0:N//2]))
'''
