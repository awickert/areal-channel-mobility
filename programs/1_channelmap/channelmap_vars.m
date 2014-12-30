% channelmap_vars.m

% ABOUT channelmap_vars.m
% This file contains an editable list of variables and directories for
% program "channelmap.m", which uses color analysis to turn images of
% fluvial systems with bimodally-colored land and water into binary
% matrices of active floodplain (0) and channel (1). (As a note, "0" is
% also used in the matrices for area within the rectangle of the analysis,
% but outside the active floodplain. This redundancy does not impair the
% program's function.)

% For more information on this program, read "reference.txt" in the root
% folder.


% -----------

% DIRECTORY DEFINITIONS

% Set the root directory: this is the location of the "programs" and
% "files" folder. Do not include the final backslash.
rootdir='/Volumes/My Book/decor4';

% Set the title of the run. This is the name of the folder within the
% "files" folder that contains the filesystem for the data that is to be
% manipulated. Do not include any slashes or backslashes.
runtitle='DB03-1_02_04';


% -----------

% TECHNICAL DEFINITIONS: CHANNELMAP (MAIN PROGRAM)

% Set the filetype for the images to be analyzed. (i.e., *.jpg)
filetype = '*.jpg';

% Set these variables to the number of pixels in your image (rc = row-count
% = Y-AXIS-PIXEL-COUNT; cc = column-count = X-AXIS-PIXEL-COUNT).
rc=690; % Height
cc=750; % Width


% TECHNICAL DEFINITIONS: LOADMASK

% Specify the mask filename. I typically use a 2-bit binary bitmap image.
maskname = 'mask.bmp';


% TECHNICAL DEFINITIONS: x-CAPTURE

% Specify the desired output image (screenshot) type (i.e., 'jpg').
imouttype = 'jpg';


% TECHNICAL DEFINITIONS: DEPTHMAP

% Edit the equation that defines "depth" in the module "depthmap" to choose
% the weighting of color values that will create the map.


% TECHNICAL DEFINITIONS: CHANNELMAPMOD

% Set the threshold value between "channel" and "land in the modlue
% "channelmapmod".


% TECHNICAL DEFINITIONS: TIME

% Edit module "time" to choose the conversion from the time-stamp in the
% file to a set number of seconds in a matrix.


% TECHNICAL DEFINITIONS: SAVEDATA

% Please write the number of characters in each time-stamp filename, before
% the file extension.
filenamelength = 18;

