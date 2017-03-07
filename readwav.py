import subprocess
import wave
import struct
import scipy
import numpy as np
import pylab as pl
import csv
import os

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import hashlib
from operator import itemgetter
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

    return wav_data, n

def spectrum(wav_data, plot=False, n):

    time = np.arange(0, n) * (1.0 / framerate)

    if plot:
        pl.figure()
        pl.subplot(211)
        pl.plot(time, wav_data[0])
        pl.subplot(212)
        pl.plot(time, wav_data[1], c="g")
        pl.xlabel("time (seconds)")
        pl.savefig('%s_pylab.png' %wav_file)

    plt.figure()
    arr2D = plt.specgram(wav_data[0], NFFT=NFFT, Fs=Fs, noverlap=900)[0] # generate spectogram
    plt.savefig('%s_1.png' %wav_file)

    # plt.figure()
    # plt.specgram(wav_data[1], NFFT=NFFT, Fs=Fs, noverlap=900)[0] # generate spectogram
    # plt.savefig('%s_2.png' %wav_file)
    return arr2D



for path, dirs, files in os.walk('/Users/RyanQu/Documents/Workspace/Git/Music_Generator/wav/'):
    for f in files:
        if not f.endswith('temp.wav'):
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