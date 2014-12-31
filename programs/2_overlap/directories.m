% DIRECTORY NAMES

% PROGDIR
% Set this directory to the one in which you place "correlation.m" and
% "correlation_vars.m", and "directories.m" (this file).
progdir=[rootdir '/programs/2_correlation'];

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

% NUMDECOR
% This is the directory for the matrices giving the time-step and number of
% decorrelated pixels for each of the baseline series.
numdecor = [rootdir '/files/' runtitle '/correlation_output/number_decorrelated'];

% SCALECOR
% This is the directory for the scaled correlation matrices.
scalecor = [rootdir '/files/' runtitle '/correlation_output/correlation_scaled'];

% SCALECOR_ZERO
% This is the directory for scalled correlation data when the initial
% time-step is set to 0.
scalecor_zero = [rootdir '/files/' runtitle '/correlation_output/correlation_scaled_zeroed'];

% SCALECOR_ZERO_ONELIST
% This is the directory for the single matrix of all of the scaled
% correlation data when the initial time-step for each run is set to 0.
% This is the final matrix that will be used with the MATLAB curve fitting
% toolbox to create and export a channel mobility / floodplain re-working
% curve.
scalecor_zero_onelist = [rootdir '/files/' runtitle '/correlation_output/correlation_scaled_zeroed_together'];
