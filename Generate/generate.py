import numpy
import scipy.io.wavfile
import matplotlib.pyplot
import random
import wave
import scipy.stats as stats

doremi = [523.0, 587.0, 659.0, 698.0, 784.0] # C,D,E,F,G or Do,Re,Mi,Fa,So
temp=stats.norm.pdf(numpy.arange(-5,5,0.1),0,10)
for i in range(5,100):
    # temp=random.random()
    # if (int(100*temp) % 2 == 0):
    #     doremi.append(doremi[i-1]*(1+0.4*temp))
    # else:
    #     doremi.append(doremi[i-1]*(1-0.4*temp))
    doremi.append(temp[i]*5000)

NFFT = 1024       # the length of the windowing segments
dt = 0.0005
Fs = int(1.0/dt)  # the sampling frequency

amplitude = 65536.0/4.0
sampling_rate = 44100.0 # sampling rate
duration = 0.3 # 0.5 seconds
sample = sampling_rate * duration
t = numpy.arange(sample) 
t = t/sample # scale each element for normalization
print t
song = numpy.array([])
for freq in doremi:
    wav = numpy.sin(2*numpy.pi*freq*t)*amplitude
    song = numpy.concatenate([song, wav])

print song
print type(song)
#print type(song.tolist())

w = wave.open('doremi.wav','wb')
w.setparams((2, 2, sampling_rate, 11323008, 'NONE', 'not compressed'))
w.writeframesraw(song.astype(numpy.int16))
# scipy.io.wavfile.write('doremi.wav', sampling_rate, song.astype(numpy.int16))

w.close()

matplotlib.pyplot.specgram(song, NFFT=NFFT, Fs=Fs, noverlap=900) # generate spectogram
matplotlib.pyplot.savefig('doremi.png')

