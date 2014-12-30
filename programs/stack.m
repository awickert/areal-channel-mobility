% Change file names from name number

% Directories

indir='/Volumes/My Book/decor4/files/tal_veg/channelmap_input/images';

% Program

cd(indir);
files=dir([indir '/' '*.jpg']);
for n=1:numel(files);   
A=importdata(files(n).name);
if n==1
    B=A;
else
    B=[B+A];
end
end
