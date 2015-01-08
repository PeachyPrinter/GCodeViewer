import wave
import sys
import os
import struct
import numpy as np
from os import listdir
from os.path import isfile, join

sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..', '..','src'))

from domain.PG_objects import *


class Wav2PGObject(object):
    def process(self,afile):
        self.z = float(afile.split('_')[1])
        wav = None
        try:
            wav = wave.open(afile, 'r')
            x,y = self.wavLoad(wav)
            points = self.wave_to_points(x, y)
            # print points
        finally:
            if wav:
                wav.close()

    def wavLoad (self,wav):
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
        frames = wav.readframes (nframes * nchannels)
        out = struct.unpack_from ("%dh" % nframes * nchannels, frames)

    # Convert 2 channles to numpy arrays
        if nchannels == 2:
            left = np.array(out[0::2])
            right = np.array(out[1::2])
        else:
            left = np.arrayf(out)
            right = left
        return left, right

    def wave_to_points(self,x,y):
        sample_since_last = 0
        peak_values = []
        last_value = 32768
        current_value = 32768
        print(len(x))

        for index in range(0, len(x)):
            last_last_value = last_value
            last_value = current_value
            current_value =  x[index]
            # print('%s < %s > %s' % (last_last_value,last_value,current_value))
            sample_since_last += 1 
            if (last_last_value < last_value and last_value  > current_value):
                # print('%s < %s > %s' % (last_last_value,last_value,current_value))
                if sample_since_last > 6:
                    move = True
                else:
                    move = False
                peak_values.append([x[index-1],y[index-1],self.z, move ])
                sample_since_last = 0
        return peak_values




class folder2PGOjects(object):
    def __init__(self, folder):
        self._files = [ afile for files in listdir(folder) if isfile(join(mypath,afile)) and afile.endswith(".wav") ]
        self._current_file_index = 0
        self._max_index = (len(self.files))
        self._wave_to_object = Wav2PGObject()

    def __iter__(self):
        return self

    def next(self):
        if self._current_file_index < self._max_index:
            self._current_file_index += 1
            return process(self._files[self._current_file_index - 1 ])
        else:
            raise StopIteration()

    def process(self,afile):
        wav = None
        

if __name__ == '__main__':
        w2pg = Wav2PGObject()
        w2pg.process('/opt/git/peachyprintertools/tmp/layer_0.0_.wav')
