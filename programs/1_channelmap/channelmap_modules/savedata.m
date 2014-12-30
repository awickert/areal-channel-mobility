% This program first saves the channel-map as a *.MAT file. Then, it saves
% the timestep and pixel-occupation matrix as a *.MAT file.

% Save the channelmap as a variable filename depending its original
% timestamped name.
cd (channelmapoutdir)
save (imname(1:filenamelength), 'channel');

% Save the timestamp and pixel-occupation matrix.
cd (time_pixel_outdir)
save timestamp_pixdist pixmat;

cd(moduledir)