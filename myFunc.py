

# Convert a signed 16-bit value to signed integer (i.e. 0xffff => -1)
def signedint16(value):
    if value >= 0x8000:
        value -= 0x10000
    return value


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
