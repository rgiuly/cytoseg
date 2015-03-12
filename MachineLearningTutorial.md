If cytoseg is not installed, follow these instructions:

http://code.google.com/p/cytoseg/wiki/Installation

Download the neuropil segmentation example data at:

http://cytoseg.googlecode.com/files/machine_learning_tutorial.zip

You need to be in the cytoseg/testing folder to run:
```
python machine_learning_command.py ...
```


---


# Running with Example Data #

Unzip machine\_learning\_tutorial.zip and note where the a, a\_membranes, and b folders are located.

The suggested folder to unzip into is C:\temp

The unzipped folder will have the following image stacks:
  * b
    * ![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/b.png](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/b.png)
  * a
    * ![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/a.png](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/a.png)
  * a\_membranes
    * ![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/a_membranes.png](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/a_membranes.png)

Enter this line at your operating system's command prompt:

```
python machine_learning_command.py C:\temp\machine_learning_tutorial\b C:\temp\machine_learning_tutorial\a C:\temp\machine_learning_tutorial\a_membranes c:\temp c:\temp
```

(If you are not using C:\temp, you will need to adjust this appropriately.)

It will take some time for this to finish running. (20 minutes or so)


When the processing is complete, you will see this output text:
<pre>
c:\temp\membranes\output000.tif<br>
c:\temp\membranes\output001.tif<br>
c:\temp\membranes\output002.tif<br>
c:\temp\membranes\output003.tif<br>
c:\temp\membranes\output004.tif<br>
c:\temp\membranes\output005.tif<br>
c:\temp\membranes\output006.tif<br>
c:\temp\membranes\output007.tif<br>
c:\temp\membranes\output008.tif<br>
</pre>

These are the files that make up the output stack, you can now view them.

The first and last 3 images of the output will always be blank.

Here's an example from the output, output003.tif:

![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/output003.png](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/output003.png)


---


# Running with Your Data #

Here's the meaning of the command:

```
python machine_learning_command.py input training_data training_labels output temporary
```

  * input: Image stack folder that contains raw data input that you want to process.
  * training\_data: Image stack used for training. This can be the same as input but it doesn't have to be.
  * training\_labels: Image stack of labels, this marks voxels with a number to identify the type of object. This dataset must match [training\_data](training_data.md) exactly in dimensions.
  * output: Output folder
  * temporary: Folder for storing temporary files


To test things out, here's how you can classify training data.

Crop out an image stack with dimensions 175x175x9
Put it in a folder, for example my\_input

Create a label volume that also has dimensions 175x175x9
You'll need to paint the voxel where the objects of interest are with nonzero values.
Put this in a folder, for example, my\_seg

Then run the following command:

```
python machine_learning_command.py my_input my_input my_seg c:\temp c:\temp
```