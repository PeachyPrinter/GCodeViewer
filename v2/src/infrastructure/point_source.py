import os
import wave
import struct
import numpy as np
from domain.source import PointSource

class WavFolderPointSource(PointSource):
    def __init__(self, path):
        self._validate_path(path)
        self._load_wav_files(path)

    def get_points(self):
        for fle in self.wav_files:
            for point in self._get_points_from_file(fle):
                yield point

    def _get_points_from_file(self, wave_file):
        wav = wave.open(wave_file, 'r')
        z = float(wave_file.split('_')[1])
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
        if nchannels != 2:
            raise Exception("Wave must be stereo")
        left, right = self._get_wave_data(nframes, wav.getnframes(nframes))
        for x,y in self._peaks(left, right):
            yield (float(x) / 32767.0, float(y) / 32767.0, z)

    def _get_wave_data(self, nframes, frames):
        out = struct.unpack_from("%dh" % nframes * 2, frames)
        left = np.array(out[0::2])
        right = np.array(out[1::2])
        return left, right

    def _peaks(self, left, right):
        return [(left[i], right[i]) for i in range(1, len(left) - 1) if left[i] > left[i - 1] and left[i] > left[i + 1]]

    def _validate_path(self, path):
        if not os.path.exists(path):
            raise Exception('Folder specified doesn\'t exist')

    def _load_wav_files(self, path):
        self.wav_files = [fle for fle in os.listdir(path) if fle[-4:] == '.wav']
        if not self.wav_files:
            raise Exception('Directory Specified contains no wave files')
