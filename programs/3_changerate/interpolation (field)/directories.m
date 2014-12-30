% DIRECTORY NAMES

% PROGDIR
% Set this directory to the one in which you place "changerate_fuzzy.m" and
% "changerate_vars.m", and "directories.m" (this file).
progdir=[rootdir '/programs/3_changerate/interpolation (field)'];

% REALCHANNELS
% This is the directory for the matrices giving the real channelmaps.
realchannels = [rootdir '/files/' runtitle '/channelmap_output/real_channels'];

% INTERPOLATEDCHANNELS
% This is the directory for the matrices giving the interpolated
% channelmaps.
interpolatedchannels = [rootdir '/files/' runtitle '/channelmap_output/channelmaps'];

% OUTDIR
% This is the directory for the output matrices of pixel / square meter
% change and time-difference in-between time-steps.
outdir = [rootdir '/files/' runtitle '/changerate_output/interpolation'];