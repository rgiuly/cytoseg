
import sys
import logging
import default_path


originalStdout = sys.stdout
originalStderr = sys.stderr

class LogFile(object):
    """File-like object to log text using the `logging` module."""

    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def write(self, msg, level=logging.INFO):
        originalStdout.write(msg)
        self.logger.log(level, msg)

    def flush(self):
        originalStdout.flush()
        for handler in self.logger.handlers:
            handler.flush()

#logging.basicConfig(level=logging.DEBUG, filename='log.txt')

# Redirect stdout and stderr
sys.stdout = LogFile('stdout')
sys.stderr = LogFile('stderr')


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

        if len(sys.argv) > 6:
            self.param['configFile'] = sys.argv[6]

        print self.param

        # set global variables
        default_path.defaultTemporaryFolder = self.param['cytosegDataFolder']
        default_path.cytosegDataFolder = self.param['cytosegDataFolder']
        default_path.contourOutputTemporaryFolder = self.param['cytosegDataFolder']
        default_path.defaultOutputPath = self.param['cytosegDataFolder']
