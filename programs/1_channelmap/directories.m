% DIRECTORIES - EDIT ONLY IF YOU DO NOT WANT TO USE THE PREFORMATTED
% FILESYSTEM.


% REQUIRED DIRECTORIES

% PROGDIR
% Set this directory to the one in which you place "channelmap.m",
% "channelmap_vars.m", and "directories.m" (this file).
progdir=[rootdir '/programs/1_channelmap'];

% MODULEDIR
% Set this to the directory containing the MATLAB m-files of the
% subroutines.
moduledir=[rootdir '/programs/1_channelmap/channelmap_modules'];

% IMINDIR
% This is the directory of the input images, either overhead photos of
% experiments or aerial photos with well-defined color differences between
% channel and active floodplain.
imindir=[rootdir '/files/' runtitle '/channelmap_input/images'];

% MASKDIR
% Place the mask file in this directory. The mask is a binary matrix (0,1)
% which defines with "0" the area which will not be included in the
% analysis. This allows a non-rectangular active floodplain to be analyzed.
% This area will be shown as transparent in the images and will receive a
% value of "0" in the matrix. Although this value is the same as that of
% the unoccupied active floodplain, it will not be counted in the analysis.
maskdir=[rootdir '/files/' runtitle '/channelmap_input/mask'];

% CHANNELMAPOUTDIR
% Set this to the directory you have slated to receive the output binary
% channelmap matrices.
channelmapoutdir=[rootdir '/files/' runtitle '/channelmap_output/channelmaps'];

% TIME_PIXEL_OUTDIR
% Set this directory to receive the output matrix with the timestamps and
% pixel counts.
time_pixel_outdir=[rootdir '/files/' runtitle '/channelmap_output/timesteps_pixelcount'];



% OPTIONAL DIRECTORIES

% IMAGEOUTDIR *OPTIONAL*
% Set this to the directory you have slated to receive the output images
% (screen-shots) of the original image, if desired. These can be used for
% purposes of comparison and quality-control with the depth-maps and the
% channel-maps.
imageoutdir=[rootdir '/files/' runtitle '/channelmap_output/screenshots/image'];

% DEPTHOUTDIR *OPTIONAL*
% Set this to the directory you have slated to receive the output images
% (screen-shots) of the depth-map, if desired. These can be used for
% purposes of comparison and quality-control with the original images and
% the channel-maps.
depthoutdir=[rootdir '/files/' runtitle '/channelmap_output/screenshots/depthmap'];

% CHANNELOUTDIR *OPTIONAL*
% Set this to the directory you have slated to receive the output images
% (screen-shots) of the channel-map, if desired. These can be used for
% purposes of comparison and quality-control with the original images and
% depth-maps.
channeloutdir=[rootdir '/files/' runtitle '/channelmap_output/screenshots/channelmap'];



