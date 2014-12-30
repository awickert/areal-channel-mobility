close all; clear all;

% For re-working, we simply cut out everything above 1/2 SD on the high
% end, as we need more time-step density and the low end doesn't cause the
% error that the high end would.

cd('/Volumes/My Book/decor4/files/DB03-2_1400-end_rework/channelmap_output/timesteps_pixelcount');
load timestamp_pixdist.mat;

cd('/Volumes/My Book/decor4/files/DB03-2_1400-end_rework/channelmap_output/channelmaps_pre_SD');

files=dir('*.mat');

n2=1;

for n=1:numel(files)
    cd('/Volumes/My Book/decor4/files/DB03-2_1400-end_rework/channelmap_output/channelmaps_pre_SD');
    if pixmat(n,3) <.2577;
        pixmat2(n2,:)=pixmat(n,:);
        n2=n2+1;
        channelmap_name = files(n).name;
        load(channelmap_name);
        cd('/Volumes/My Book/decor4/files/DB03-2_1400-end_rework/channelmap_output/channelmaps_prefilter');
        save(channelmap_name, 'channel')
    end
end

    
    
    