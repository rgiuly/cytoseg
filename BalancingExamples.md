To refine your results with Cytoseg, check the number of "mitochondria" (positive) examples and "other" (negative) examples. The program shows the counts to you pretty much first thing when it starts running. You can adjust it with the voxel weight parameter. A good rule of thumb is about 1000 mito examples and about 1500 of the other examples.

For example:
--voxelWeights=0.0130,0.00064

The first number is proportional to the mito example count and the second is proportional to the "other" count.

You'll see the difference it makes in the voxel output.