% LOADMASK
% This script is a subroutine of "channelmap.m". It loads a black (0) and
% white (1) binary matrix which chooses which parts of the image are to be
% examined. Only the parts marked in white (1) will be examined; the parts
% marked in black (0) will be disregarded.

% Load the mask.
cd(maskdir);
mask=logical(imread(maskname))+0;

%Find the total size of the active floodplain.
active_floodplain_size = sum(sum(mask));


