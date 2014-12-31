% Build a stack of all of the outputs for visualization.
% This has been superceded by the programs that create the full scatter plots, 
% with running means and all data. But I have kept it around in case it is 
% useful and to show my thought process back in 2006.

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
