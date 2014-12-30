close all; clear all;

% This program removes every channelmap outside of 1/2 standard deviation
% from the mean wetted area in the DB03-2 aggrading phase.

cd('/Volumes/My Book/decor4/files/DB03-2_1400-end/channelmap_output/timesteps_pixelcount');
load timestamp_pixdist.mat;

cd('/Volumes/My Book/decor4/files/DB03-2_1400-end/channelmap_output/channelmaps_pre_SD');

files=dir('*.mat');

n2=1;

for n=1:numel(files)
    cd('/Volumes/My Book/decor4/files/DB03-2_1400-end/channelmap_output/channelmaps_pre_SD');
    if pixmat(n,3) <.2577 && pixmat(n,3) >.1109;
        pixmat2(n2,:)=pixmat(n,:);
        n2=n2+1;
        %channelmap_name = files(n).name;
        %load(channelmap_name);
        %cd('/Volumes/My Book/decor4/files/DB03-2_1400-end/channelmap_output/channelmaps2');
        %save(channelmap_name, 'channel')
    end
end

    
    
    