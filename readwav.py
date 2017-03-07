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

######################################################################
# Degree to which a fingerprint can be paired with its neighbors --
# higher will cause more fingerprints, but potentially better accuracy.
DEFAULT_FAN_VALUE = 15

######################################################################
# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

######################################################################
# Number of cells around an amplitude peak in the spectrogram in order
# for Dejavu to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 200


def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    params = w.getparams()
    print params
    nchannels, sampwidth, framerate, nframes = params[:4]
    print nchannels, sampwidth, framerate, nframes

    n=60*framerate
    print n

    str_data = w.readframes(n)
    w.close()

    wav_data = np.fromstring(str_data, dtype=np.short)
    wav_data.shape = -1, 2
    wav_data = wav_data.T

    return wav_data, n, params

def spectrum(wav_data, n, params, fan_value=DEFAULT_FAN_VALUE,
                amp_min=DEFAULT_AMP_MIN, plot=False):

    time = np.arange(0, n) * (1.0 / params[2])

    if plot:
        pl.figure()
        pl.subplot(211)
        pl.plot(time, wav_data[0])
        pl.subplot(212)
        pl.plot(time, wav_data[1], c="g")
        pl.xlabel("time (seconds)")
        pl.savefig('%s_pylab.png' %wav_file)

    plt.figure()
    arr2D = plt.specgram(wav_data[0], NFFT=NFFT, Fs=Fs, window=mlab.window_hanning, noverlap=900)[0] # generate spectogram
    plt.savefig('%s_k.png' %wav_file)

    arr2D = 10 * np.log10(arr2D)
    arr2D[arr2D == -np.inf] = 0  # replace infs with zeros

    # find local maxima
    local_maxima = get_2D_peaks(arr2D, plot=True, amp_min=amp_min)

    return local_maxima
    #return generate_hashes(local_maxima, fan_value=fan_value)
    # plt.figure()
    # plt.specgram(wav_data[1], NFFT=NFFT, Fs=Fs, noverlap=900)[0] # generate spectogram
    # plt.savefig('%s_2.png' %wav_file)

def get_2D_peaks(arr2D, plot=False, amp_min=DEFAULT_AMP_MIN):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max - eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    if plot:
        # scatter of the peaks
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(time_idx, frequency_idx)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        ax.axis('normal')
        plt.gca().invert_yaxis()
        plt.savefig('200_peak.png')

    return zip(frequency_idx, time_idx)


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
            (wav_data, n, params) = read_wav(wav_file)

            print wav_data, n, params

            spectrum(wav_data, n, params, plot=False)
        except:
            continue