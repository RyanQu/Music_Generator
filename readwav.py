import subprocess
import wave
import struct
import numpy
import csv
import sys
import os
from pydub import *
 
def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    n = 60 * 10000
    # if w.getnframes() < n * 2:
    #     raise ValueError('Wave file too short')
    frames = w.readframes(n)
    print type(frames)
    wav_data = struct.unpack('%dh' % n, frames)
    print type(wav_data)
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