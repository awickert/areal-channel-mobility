clear all;
close all;

system_name='DB03-1_02_04';

indir=['/Volumes/My Book/decor4/files/' system_name '/channelmap_output/channelmaps_bmp_filtered'];

cd(indir)

files=dir('*.bmp');

cd(['/Volumes/My Book/decor4/files/' system_name '/channelmap_input/mask']);
premask=importdata('mask.bmp');
mask=premask.cdata;

for z=(numel(files)/2+1):numel(files);
    cd(indir)
    A=files(z).name;
    B=importdata(A);
    B2=B.cdata;
    C=1-B2;
    channel=C.*mask;
    cd(['/Volumes/My Book/decor4/files/' system_name '/channelmap_output/channelmaps'])
    save([A(1:18) '.mat'], 'channel')
end