from infrastructure.point_source import WavFolderPointSource
from infrastructure.display_list_builder import DisplayListBuilder


class Loader(object):

    def displayListFromWaves(self, folder):
        wfps = WavFolderPointSource(folder)
        points = wfps.get_points()
        dlb = DisplayListBuilder()
        return dlb.get_list_id(points)


