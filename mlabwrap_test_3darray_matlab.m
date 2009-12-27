%function out = mlabwrap_test_3darray_matlab(array)
function mlabwrap_test_3darray_matlab(array)

%function out = mlabwrap_test_3darray_matlab(array)

    for x=1:3
        for y=1:3
            for z=1:3
                %matlabArray(x,y,z) = 10000 +  x*100 + y*10 + z
                matlabArray(x,y,z) = x*100 + y*10 + z

            end
        end
    end


    reshapedArray = reshape(array,3,3,3)
    fid = fopen('temp_output.txt', 'wt');
    fprintf(fid, num2str(matlabArray));
    fprintf(fid, '----------------------\n');
    fprintf(fid, num2str(reshapedArray));

    %out = reshapedArray;
    fclose(fid);