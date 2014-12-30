% DIRECTORY NAMES

% PROGDIR
% Set this directory to the one in which you place "correlation.m" and
% "correlation_vars.m", and "directories.m" (this file).
progdir=[rootdir '/programs/4_rework'];

% CHANNELMAPINDIR
% This is the directory for the input channel-maps that are used in the
% pixel-overlap/correlation analysis here. This is the same directory as
% the channel-map output from the program "channelmap.m".
channelmapindir = [rootdir '/files/' runtitle '/channelmap_output/channelmaps'];

% TIMEPIXINDIR
% This is the directory for the matrix which contains the timesteps and
% numbers of channel and active floodplain and total pixals in each
% channe-map.
timepixindir = [rootdir '/files/' runtitle '/channelmap_output/timesteps_pixelcount'];

% MASKDIR
% This is the location of the mask, to find the size of the active
% floodplain.
maskdir = [rootdir '/files/' runtitle '/channelmap_input/mask'];

% TOT_NPIX_VISITED
% This is the directory for the matrices giving the time-step and number of
% visited pixels on the active floodplain for each of the baseline series.
tot_npix_visited = [rootdir '/files/' runtitle '/rework_output/tot_npix_visited'];

% NOTVISITED
% This is the directory for the proportion of not visited pixels in the
% time-series.
notvisited = [rootdir '/files/' runtitle '/rework_output/notvisited'];

% NOTVISITED_NOTINITIAL
% This is the directory for the proportion of not visited pixels in the
% time-series that are also not part of the original channel.
notvisited_notinitial = [rootdir '/files/' runtitle '/rework_output/notvisited_notinitial'];

% NOTVISITED_ZERO
% This is the directory for the proportion of not visited pixels in the
% time-series when the initial time-step is set to 0.
notvisited_zero = [rootdir '/files/' runtitle '/rework_output/notvisited_zero'];

% NOTVISITED_NOTINITIAL_ZERO
% This is the directory for the proportion of not visited pixels in the
% time-series that are also not part of the original channel when the initial
% time-step is set to 0.
notvisited_notinitial_zero = [rootdir '/files/' runtitle '/rework_output/notvisited_notinitial_zero'];

% NOTVISITED_ZERO_ONELIST
% This is the directory for the single matrix of all of the data from both
% the plain not-visited matrix and the notinitial one when the initial 
% time-step for each run is set to 0.
% This is the final matrix that will be used with the MATLAB curve fitting
% toolbox to create and export a channel mobility / floodplain re-working
% curve.
notvisited_zero_onelist = [rootdir '/files/' runtitle '/rework_output/notvisited_zeroed_onelist'];


