% This program loads the binary channel-map file for each image, selects a
% baseline, and finds the number of changed pixels between images N and
% N+1, with N being the baseline.

% This program requires the correlation profiles to be found first.

% Human-entered variables and directory names
changerate_clean_vars %This is the file that needs to be edited for each run.
directories %This is automated based on selections in correlation_vars.m.

% Select input directory and create a list of files contained within
cd(numdecor)
files=dir('*.mat');

%Create final output matrices
pixels=zeros((numel(files)-1),2);
meters=zeros((numel(files)-1),2);
meters_timescaled=zeros((numel(files)-1),1);

% Calculate changed pixels
for z=1:numel(files)-1
    file=load(files(z).name);
    file=file.npix_decor_outmat;
    npix_changed=file(z+1,2)-file(z,2);
    area_changed=npix_changed*pixel_to_meter_scale;
    % Time unit is given in correlation file
    time_differential=file(z+1,1)-file(z,1);
    
    pixels(z,1)=time_differential;
    pixels(z,2)=npix_changed;
    
    meters(z,1)=time_differential;
    meters(z,2)=area_changed;
    
    meters_timescaled(z)=area_changed/time_differential;
    
end

% Save the matrices
cd(outdir)
save('time_pixels', 'pixels');
save('time_meters^2', 'meters');
save('meters^2scaledtotime', 'meters_timescaled');


cd(progdir)