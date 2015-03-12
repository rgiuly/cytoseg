#How to use bounds options in the cytoseg command line

# Using bounds to from the command line #

One way to process only parts of data is to crop it before processing, but cytoseg gives you some bounds parameters that you can use to only process certain regions. The format is lower bounds X,Y,Z and upper bounds X,Y,Z. These specify two corners of the box you which to process (or where training will occur). You can use ImageJ to get the exact coordinates you would want to use here. X and Y come directly from ImageJ. The Z values is the number of slice. Note that slice numbers start on 0. When you use asterisks like this:

**,**,

For a boundary it uses the smallest (for lower) or largest (for upper) bounds. You can have mixtures like for example, **,**,6 in a lower bound would mean lowest possible bound for X, lowest possible bound for y, and 6 as the lower bound for Z.

