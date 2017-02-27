import numpy
import scipy.io.wavfile
import matplotlib.pyplot

doremi = [523.0, 587.0, 659.0, 698.0, 784.0] # C,D,E,F,G or Do,Re,Mi,Fa,So
NFFT = 1024       # the length of the windowing segments
dt = 0.0005
Fs = int(1.0/dt)  # the sampling frequency

amplitude = 65536.0/4.0
sampling_rate = 44100.0 # sampling rate
duration = 0.5 # 0.5 seconds
sample = sampling_rate * duration
t = numpy.arange(sample) 
t = t/sample # scale each element for normalization
song = numpy.array([])
for freq in doremi:
    wav = numpy.sin(2*numpy.pi*freq*t)*amplitude
    song = numpy.concatenate([song, wav])

print song
print type(song)
#print type(song.tolist())


scipy.io.wavfile.write('doremi.wav', sampling_rate, song.astype(numpy.int16))
matplotlib.pyplot.specgram(song, NFFT=NFFT, Fs=Fs, noverlap=500) # generate spectogram
matplotlib.pyplot.savefig('doremi.png')