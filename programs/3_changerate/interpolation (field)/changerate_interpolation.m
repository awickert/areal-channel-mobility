clear all; close all;

% This program uses the channel maps of the real channels and the
% interpolated channels to give the amount of area re-worked between two
% images. Unlike the others, this is the reworked area, not the changed
% area, and must *not* be divided by 2. (Even if this weren't the case, it
% shouldn't be divided by 2 because the area re-worked is often more than 
% a channel width.)

% It also requires a folder, real_channels, containing the actual channel
% maps (not the interpolated ones) in the channelmap_output folder.

% Human-entered variables and directory names
changerate_interpolation_vars %This is the file that needs to be edited for each run.
directories %This is automated based on selections in correlation_vars.m.

% Select input directories and create lists of files contained within
cd(realchannels)
files=dir('*.mat');

%Create final output matrix
pixels=zeros((numel(files)-1),2);

% Calculate changed pixels
for z=1:numel(files)-1
    cd(realchannels);
    channelmap_real=load(files(z).name);
    channelmap_real=channelmap_real.channel;
    cd(interpolatedchannels);
    channelmap_interpolated=load(files(z+1).name);
    channelmap_interpolated=channelmap_interpolated.channel;
    figure; imagesc(channelmap_interpolated-2*channelmap_real);
    %
    %timestep=files(z+1).name;
    %prechannel=channelmap_interpolated
    pix_rework=sum(sum(channelmap_interpolated-channelmap_real));
    time_differential=(str2double(files(z+1).name(timestamp)))-(str2double(files(z).name(timestamp)));
    
    pixels(z,1)=time_differential;
    pixels(z,2)=pix_rework;
    
end

% Save the matrices
cd(outdir)
save('time_pixrw', 'pixels');

cd(progdir)