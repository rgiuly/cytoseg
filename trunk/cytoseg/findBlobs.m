function [centroids, areas] = findBlobs(volume1D,d1,d2,d3,threshold,showResults)
    % volume1D is the 3D volume array flattened into a 1D array.
    % dimensions d1,d2,d3 are the dimensions of the original 3D array.
    % a 1D array is used because mlabwrap currently does not support 3D
    % arrays.
    
    volume = reshape(volume1D, d1,d2,d3);
    if showResults
    	cytoseg_sliceView(volume);
    end
    thresholded = volume < threshold;
    labelMatrix = bwlabeln(thresholded);
    if showResults
    	cytoseg_sliceView(labelMatrix);
    end
    props = regionprops(labelMatrix,{'Area', 'Centroid'});
    for i=1:length(props)
        areas(i) = props(i).Area;
        centroids(i,:) = props(i).Centroid;
    end
    
    
    