% This module of repeat.m captures and saves a screenshot of the starting 
% image.

%display image
imagesc(img); axis image; axis off;

% make the area that is '0' in mask, transparent in the current image
alpha(mask)

%Capture the image.
    image=getframe(gca);
    cd(imageoutdir)
    imwrite(image.cdata,[imname], imouttype);
    
cd(moduledir)