import subprocess
import wave
import struct
import scipy
import numpy as np
import pylab as pl
import csv
import os
import matplotlib.pyplot
from pydub import *

NFFT = 1024       # the length of the windowing segments
dt = 0.001
Fs = int(1.0/dt)  # the sampling frequency

def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    params = w.getparams()
    print params
    nchannels, sampwidth, framerate, nframes = params[:4]
    print nchannels, sampwidth, framerate, nframes

    n=nframes/2
    print n

    str_data = w.readframes(n)
    w.close()

    wav_data = np.fromstring(str_data, dtype=np.short)
    wav_data.shape = -1, 2
    wav_data = wav_data.T
    time = np.arange(0, n) * (1.0 / framerate)

    pl.figure()
    pl.subplot(211)
    pl.plot(time, wav_data[0])
    pl.subplot(212)
    pl.plot(time, wav_data[1], c="g")
    pl.xlabel("time (seconds)")
    pl.savefig('%s_pylab.png' %wav_file)

    matplotlib.pyplot.figure()
    matplotlib.pyplot.specgram(wav_data[0], NFFT=NFFT, Fs=Fs, noverlap=900) # generate spectogram
    matplotlib.pyplot.savefig('%s_1.png' %wav_file)

    matplotlib.pyplot.figure()
    matplotlib.pyplot.specgram(wav_data[1], NFFT=NFFT, Fs=Fs, noverlap=900) # generate spectogram
    matplotlib.pyplot.savefig('%s_2.png' %wav_file)

    return wav_data

for path, dirs, files in os.walk('/Users/RyanQu/Documents/Workspace/Git/Music_Generator/wav/'):
    for f in files:
        if not f.endswith('.wav'):
            # Skip any non-MP3 files
            continue

        wav_file = os.path.join(path, f)
        print wav_file
        # Extract the track name (i.e. the file name) plus the names
        # of the two preceding directories. This will be useful
        # later for plotting.
        tail, track = os.path.split(wav_file)
        
        try:
            wav_data = read_wav(wav_file)
        except:
            continue