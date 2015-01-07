import unittest
import os
import sys
from mock import patch, MagicMock
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.point_source import WavFolderPointSource


class WavFolderPointSourceTest(unittest.TestCase):
    def setUp(self):
        self.default_nchannels = 2
        self.default_sampwidth = 2
        self.default_framerate = 48000
        self.default_nframes = 4
        self.default_comptype = None
        self.default_compname = None
        self.default_params = (self.default_nchannels,
                               self.default_sampwidth,
                               self.default_framerate,
                               self.default_nframes,
                               self.default_comptype,
                               self.default_compname)

    def _to_frame(self, values):
            return  values.astype(np.dtype('<i2')).tostring()

    def test_init_raises_exception_if_folder_doesnt_exist(self):
        with self.assertRaises(Exception):
            WavFolderPointSource('ERRR')

    def test_init_returns_if_valid_folder(self):
        WavFolderPointSource('test_data')

    def test_init_raises_exception_if_valid_folder_but_no_wav_files(self):
        with self.assertRaises(Exception):
            WavFolderPointSource('.')

    @patch('infrastructure.point_source.wave')
    def test_get_points_raises_exception_given_non_stereo_wav_file(self, mock_wave):
        wave_file = MagicMock()
        mock_wave.open.return_value = wave_file
        wave_file.getparams.return_value(1,
                                         self.default_sampwidth,
                                         self.default_framerate,
                                         self.default_nframes,
                                         self.default_comptype,
                                         self.default_compname
                                         )
        wfps = WavFolderPointSource('test_data')
        with self.assertRaises(Exception):
            points = wfps.get_points()
            points.next()
        mock_wave.open.assert_called_with('layer_69.88_.wav', 'r')

    @patch('infrastructure.point_source.wave.open')
    def test_get_points_returns_expected_point(self, mock_open):
        mock_wave = MagicMock()
        mock_open.return_value = mock_wave
        mock_wave.getparams.return_value = self.default_params
        l = np.array((-32768, 0, 32767, 0))
        data = np.column_stack((l, l))
        wave_data = data.astype(np.dtype('<i2')).tostring()
        mock_wave.getnframes.return_value = wave_data
        wfps = WavFolderPointSource('test_data')

        points = wfps.get_points()
        point = points.next()

        self.assertEqual(point, (1.0, 1.0, 69.88))


if __name__ == '__main__':
    unittest.main()
