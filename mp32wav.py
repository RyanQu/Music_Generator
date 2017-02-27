import subprocess
import wave
import struct
import numpy
import csv
import sys
import os
from pydub import *
 
def compute_chunk_features(mp3_file):
    """Return feature vectors for two chunks of an MP3 file."""
    # Extract MP3 file to a mono, 10kHz WAV file
    song = AudioSegment.from_mp3(mp3_file)
    db = song.dBFS
    song.export('temp.wav', format="wav")

    # We'll cover how the features are computed in the next section!
    return db
 
# Main script starts here
# =======================
 
for path, dirs, files in os.walk('/Users/RyanQu/Documents/Workspace/Git/Music_Generator/mp3/'):
    for f in files:
        if not f.endswith('.mp3'):
            # Skip any non-MP3 files
            continue
        mp3_file = os.path.join(path, f)
        # Extract the track name (i.e. the file name) plus the names
        # of the two preceding directories. This will be useful
        # later for plotting.
        tail, track = os.path.split(mp3_file)
        
        try:
            db = compute_chunk_features(mp3_file)
        except:
            continue