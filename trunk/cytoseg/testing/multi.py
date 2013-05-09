
import subprocess
import os



import os
step = 200
for i in range(800, 1200, step):
	lower = i
	upper = i + step
	path = "/home/rgiuly/temp/coyote/output%d" % i
	print "output path", path
	if not(os.path.isdir(path)):
		os.mkdir(path)
	subprocess.Popen(["python", "run_pipeline.py", "/home/rgiuly/images/CoyoteSampleData/DataX2", path, "--trainingImage=/home/rgiuly/images/CoyoteSampleData/DataX2", "--trainingSeg=/home/rgiuly/images/CoyoteSampleData/SegX2", "--voxelTrainingLowerBound=945,%d,0"%lower,  "--voxelTrainingUpperBound=1227,%d,8"%upper, "--voxelProcessingLowerBound=900,750,15", "--voxelProcessingUpperBound=1277,1500,19", "--contourTrainingLowerBound=*,*,*", "--contourTrainingUpperBound=*,*,*", "--contourProcessingLowerBound=*,*,*", "--contourProcessingUpperBound=*,*,*", "--accuracyCalcLowerBound=*,*,*", "--accuracyCalcUpperBound=*,*,*", "--labelConfigFile=settings2.py", "--voxelWeights=0.08,0.15", "--contourListWeights=7,1", "--contourListThreshold=0.8", "--step1"])


