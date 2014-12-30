cd('/Volumes/My Book/decor4/files/DB03-2_1400-end/rework_output/notvisited_notinitial_zero');

files=dir('*.mat');

    A=importdata(files(1).name);
    notvisited_zero_all=A;

for z=2:numel(files)
    A=importdata(files(z).name);
    notvisited_zero_all=[notvisited_zero_all; A];
end