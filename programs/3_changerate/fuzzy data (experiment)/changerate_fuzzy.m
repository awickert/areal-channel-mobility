clear all; close all;

% This program loads the binary channel-map file for each image, selects a
% baseline, and finds the number of changed pixels between images N+1 and
% N+2, with N being the baseline. The reason for this convoluted approach
% is to avoid values of changed pixels that are too high because of random
% variations; this method cancels out this because it compares the
% comparisons of N and N+1, and N and N+2.

% This program requires the correlation profiles to be found first.

% Human-entered variables and directory names
changerate_fuzzy_vars %This is the file that needs to be edited for each run.
directories %This is automated based on selections in correlation_vars.m.

% Select input directory and create a list of files contained within
cd(numdecor)
files=dir('*.mat');

%Create final output matrices
final_matrix_pixels=zeros((numel(files)-2),2);
final_matrix_meters=zeros((numel(files)-2),2);
final_matrix_meters_timescaled=zeros((numel(files)-2),1);

% Calculate changed pixels
for z=1:numel(files)-2
    file=load(files(z).name);
    file=file.npix_decor_outmat;
    npix_changed=file(z+2,2)-file(z+1,2);
    area_changed=npix_changed*pixel_to_meter_scale;
    % Time unit is given in correlation file
    time_differential=file(z+2,1)-file(z+1,1);
    
    final_matrix_pixels(z,1)=time_differential;
    final_matrix_pixels(z,2)=npix_changed;
    
    final_matrix_meters(z,1)=time_differential;
    final_matrix_meters(z,2)=area_changed;
    
    final_matrix_meters_timescaled(z)=area_changed/time_differential;
    
end

% Save the matrices
cd(outdir)
save('time_pixels', 'final_matrix_pixels');
save('time_meters^2', 'final_matrix_meters');
save('meters^2scaledtotime', 'final_matrix_meters_timescaled');


cd(progdir)