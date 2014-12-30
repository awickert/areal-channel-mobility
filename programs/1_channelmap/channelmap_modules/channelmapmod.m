% This program changes a depthmap into a defined set of channels. 1 is
% "wet" or "channel", and 0 is "dry" or "active floodplain".

% This is NOT STAND-ALONE. Run by running "repeat.m".

% channel_unmasked = ((depth(1:rc,1:cc) > 0.6)); %DB03-2
% channel_unmasked =((depth(1:rc,1:cc) == 3)); %(XES02)
% channel_unmasked =((depth(1:rc,1:cc) == 1)); %(White R., Allier R., R. Beni, Big Blue R., R. Severn)
channel_unmasked =((depth(1:rc,1:cc) > .22)); %(DB03-1)

channel = channel_unmasked.*mask;

cd(moduledir)


