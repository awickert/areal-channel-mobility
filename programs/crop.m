% crop images to speed analysis

system_name='XES02_slow_bl_rise';

indir=['/Volumes/My Book/decor4/files/' system_name '/channelmap_input/images_precrop'];
outdir=['/Volumes/My Book/decor4/files/' system_name '/channelmap_input/images'];

cd(indir);
files=dir('*.jpg');
for n=1:numel(files);
    % Set up for XES02 slow rise w/ fewer time-steps
    cd(indir);
    img=importdata(files(n).name);
    img(:,1:60,:)=[];
    img(:,421:end,:)=[];
    %img(1:125,:,:)=[];
    %img(326:end,:,:)=[];
    cd(outdir);
    imwrite(img, files(n).name, 'JPG')
end