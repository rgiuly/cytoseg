
import sys
import default_path

class CommandReader:

    def __init__(self):

        self.param = {}

        # each volume is a stack of 8 bit tiff images


        # full input volume
        self.param['originalImageFilePath'] = sys.argv[1]

        # training data image volume
        self.param['voxelTrainingImageFilePath'] = sys.argv[2]

        # training data labels
        # this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
        self.param['voxelTrainingLabelFilePath'] = sys.argv[3]

        # output volume
        self.param['blobImageStackOutputFolder'] = sys.argv[4]

        self.param['cytosegDataFolder'] = sys.argv[5]

        print self.param

        # set global variables
        default_path.defaultTemporaryFolder = self.param['cytosegDataFolder']
        default_path.cytosegDataFolder = self.param['cytosegDataFolder']
        default_path.contourOutputTemporaryFolder = self.param['cytosegDataFolder']
        default_path.defaultOutputPath = self.param['cytosegDataFolder']
