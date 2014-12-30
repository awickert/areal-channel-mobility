% This program will calculate the depth of an experimental channel
% by using substrate color vs. background color based on user inputs in
% channelmap_vars.m.

% This is NOT STAND-ALONE. Run by running "chanelmap.m".

% Separate into R,G,B
%separate into H,S,V
rgb=double(img);
hsv=rgb2hsv(rgb);

%R=rgb(:,:,1);
%G=rgb(:,:,2);
%B=rgb(:,:,3);
%H=hsv(:,:,1);
S=hsv(:,:,2);
%V=hsv(:,:,3);

% Specify the equation that is to be used to determine the depth map in
% terms of R, G, B, H, S, V. 
% Optional: to speed processing, comment out the color parameters that will
% not be used in your analysis (above).
% depth=(H>.45)+(H<.6)+(S>.15); %(XES02)
% depth=S+V/(3*255); (DB03-2)
% depth=img; % (White R., Big Blue R., R. Severn, Sacramento R., Luangwa R.)
% depth = (R<50) - (V<50); % (Allier)
% depth=1-img; % (Beni)
 depth=S; % DB03-1
cd(moduledir)
