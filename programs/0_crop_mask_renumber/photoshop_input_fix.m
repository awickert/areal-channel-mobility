% Get rid of hidden files from photoshop

clear all;
close all;

channel_system='luangwa_rework';
chars = 4; % number of characters in filename, without the extension
filetypein='bmp';
filetypeout='bmp';
%if crop
%infile='/channelmap_input/images_photoshop';
%outfile='/channelmap_input/images';

%if smooth
infile='/channelmap_input/images_photoshop';
outfile='/channelmap_input/images';

indir=['/Volumes/My Book/decor4/files/' channel_system infile];
outdir=['/Volumes/My Book/decor4/files/' channel_system outfile];

cd(indir);

files=dir(['*.' filetypein]);

for z=numel(files)/2+1:numel(files);
    cd(indir)
    A=files(z).name;
    B=importdata(A);
    C=B.cdata;
    D=[A(1:chars) ['.' filetypeout]];
    cd(outdir)
    imwrite(C, D, filetypeout);
end