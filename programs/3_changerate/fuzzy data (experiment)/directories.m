% DIRECTORY NAMES

% PROGDIR
% Set this directory to the one in which you place "changerate_fuzzy.m" and
% "changerate_vars.m", and "directories.m" (this file).
progdir=[rootdir '/programs/3_changerate/fuzzy data (experiment)'];

% NUMDECOR
% This is the directory for the matrices giving the time-step and number of
% decorrelated pixels for each of the baseline series.
numdecor = [rootdir '/files/' runtitle '/correlation_output/number_decorrelated'];

% OUTDIR
% This is the directory for the output matrices of pixel / square meter
% change and time-difference in-between time-steps.
outdir = [rootdir '/files/' runtitle '/changerate_output/2_3 (fuzzy)'];