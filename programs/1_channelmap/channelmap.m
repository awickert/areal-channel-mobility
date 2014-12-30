clear all; close all;

% channelmap.m

% ABOUT channelmap.m
% This is the script that calls the subroutines which use color analysis
% to turn images of fluvial systems with bimodally-colored land and water
% into binary matrices of active floodplain (0) and channel (1).


% Load variables
channelmap_vars;
directories;

% Select the image directory and load the image file matrix.
cd(imindir);
files = dir(filetype);
numfiles = numel(files);

% Load the mask (constant, and therefore not part of the "for" loop) and
% determine its size.
cd(moduledir);
loadmask

% Create the output matrix for numbers of channel and active floodplain
% pixels and time-stamps.
pixmat = zeros(numfiles,4);

% Run the images through the modules

% Set the number after the colon to the number of images you plan to
% process.
for L = 1:numfiles;
   
    
    % Define the image directory and load/loop through the image names.
    cd (imindir)
    imname=files(L).name;
    img=imread(imname);
    
    % Change directory to the location of the modules.
    cd (moduledir)
    
    % These are the modules that are to be run, in order.
    time
    imagecapture %OPTIONAL
    depthmap
    depthcapture %OPTIONAL
    channelmapmod
    channelcapture %OPTIONAL
    pixdist
    savedata
    
    cd (progdir)

end

    
   