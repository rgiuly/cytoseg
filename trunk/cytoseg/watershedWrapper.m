function labelMatrix1D = watershedWrapper(volume1D,d1,d2,d3,connectivity)
    % volume1D is the 3D volume array flattened into a 1D array.
    % dimensions d1,d2,d3 are the dimensions of the original 3D array.
    % a 1D array is used because mlabwrap currently does not support 3D
    % arrays.
    % d1, d2, d3 are dimensions of the 3D array
    
    volume = reshape(volume1D, d1,d2,d3);

    labelMatrix = watershed(volume, connectivity);
    sliceView(labelMatrix);
    labelMatrix1D = labelMatrix(:);
    
    
    
    
    