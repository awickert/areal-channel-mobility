% PIXDIST
% This program is a module of channelmap.m.
% It outputs a 4-column matrix of [Timestamp (seconds), Active floodplain
% size (pixels, fraction of channel pixels, fraction of active floodplain
% pixels.

pixmat(L,1) = timestamp;
pixmat(L,2) = active_floodplain_size;
pixmat(L,3) = sum(sum(channel))/pixmat(L,2);
pixmat(L,4) = (1-pixmat(L,3));


