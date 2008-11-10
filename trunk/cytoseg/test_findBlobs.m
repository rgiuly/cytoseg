function test_findBlobs

    a = ones(5,5,5) * 100;
    a(2,2,2)=1;
    a(2,3,2)=1;
    a(4,4,4)=1;

    [c,a] = findBlobs(a,6,5,5,5);
    c
    a
    
    
    
    