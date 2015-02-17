import os
import wave
import struct
import numpy as np
from math import pow
from domain.source import PointSource
from domain.point import Point


class WavFolderPointSource(PointSource):
    def __init__(self, path):
        self._validate_path(path)
        self._wave_files = self._load_wav_files(path)
        self._height_scale = self._get_z_scale(self._wave_files)

    def get_points(self):
        for fle in self._wave_files:
            for point in self._get_points_from_file(fle):
                yield point

    def mod_range(self, number, min_val, max_val):
        old_range = float(max_val - min_val)
        dest_range = 2.0
        return (((number - min_val) * dest_range) / old_range) - 1.0

    def _get_points_from_file(self, wave_file):
        wav = wave.open(wave_file, 'r')
        z = self._file_height(wave_file) * self._height_scale
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
        max_value = pow(2, (8 * sampwidth) - 1)
        min_value = max_value / 4
        if nchannels != 2:
            raise Exception("Wave must be stereo")
        left, right = self._get_wave_data(nframes, wav.readframes(nframes))
        for x, y, state in self._peaks(left, right):
            yield Point(
                self.mod_range(float(x), min_value, max_value),
                self.mod_range(float(y), min_value, max_value),
                z,
                state)

    def _get_wave_data(self, nframes, frames):
        out = struct.unpack_from("%dh" % nframes * 2, frames)
        left = np.array(out[0::2])
        right = np.array(out[1::2])
        return left, right

    def _is_peak(self, array, index):
        return array[index] > array[index - 1] and array[index] > array[index + 1]

    def _diffrences(self, indexes):
        diffs = [indexes[i] - indexes[i-1] for i in range(1, len(indexes)-1)]
        values = list(set(diffs))
        return values

    def _get_hi_modulation_samples(self, data):
        index = 0
        gaps = []

        for index in range(1, len(data) - 1):
            if self._is_peak(data, index):
                if gaps:
                    gaps.append(index)
                    diffs = self._diffrences(gaps)
                    if len(diffs) == 2:
                        return min(diffs)
                else:
                    gaps = [index]
            index += 1
        return None

    def _peaks(self, left, right):
        peaks = []
        min_gap = self._get_hi_modulation_samples(left)
        last_peak_index = 0

        for index in range(1, len(left) - 1):
            if self._is_peak(left, index):
                if min_gap and index - last_peak_index > min_gap:
                    peaks.append((left[index], right[index], False))
                else:
                    peaks.append((left[index], right[index], True))
                last_peak_index = index
        return peaks

    def _validate_path(self, path):
        if not os.path.exists(path):
            raise Exception('Folder specified doesn\'t exist')

    def _file_height(self, file_name):
        file_only = os.path.split(file_name)[-1]
        return float(file_only.split('_')[1])

    def _load_wav_files(self, path):
        files = [os.path.join(path, fle) for fle in os.listdir(path) if fle[-4:] == '.wav']
        if not files:
            raise Exception('Directory Specified contains no wave files')
        return sorted(files, key=self._file_height)

    def _get_z_scale(self, files):
        height = self._file_height(files[-1])
        return 1.0 / float(height)
        
