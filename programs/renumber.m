% Change file names from name number

% Directories

indir='/Volumes/My Book/decor4/files/tal_veg/channelmap_input/F12-15_small';
outdir='/Volumes/My Book/decor4/files/tal_veg/channelmap_input/images';

% Program

files=dir([indir '/' '*.jpg']);
time=30*(1:numel(files));
for n=1:numel(files);   
    sourcename=files(n).name;
    destname=sprintf('%0.5d.jpg', time(n));
	copyfile([indir '/' sourcename], [outdir '/' destname]);
end
