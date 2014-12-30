clear all;
close all;

channel_system='DB03-1_02_04';

indir=['/Volumes/My Book/decor4/files/' channel_system '/channelmap_output/channelmaps_prefilter'];
outdir=['/Volumes/My Book/decor4/files/' channel_system '/channelmap_output/channelmaps_bmp'];
chars = 18; % number of characters in filename, not including extension

cd(indir);

files=dir('*.mat');

for z=1:numel(files);
    cd(indir)
    A=files(z).name;
    B=load(A);
    C=B.channel;
    cd(outdir)
    imwrite(C, [A(1:chars) '.bmp'], 'BMP');
end