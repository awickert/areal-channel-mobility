% This module of channelmap.m captures and saves a screenshot of the 
% channel-map.

% display image
imagesc(channel); axis image; colormap gray; axis off;

% make the area that is '0' in mask, transparent in the current image
alpha(mask)

%Capture the image.
    image=getframe(gca);
    cd(channeloutdir)
    imwrite(image.cdata,[imname], imouttype);
    
cd(moduledir)