% TIME

% This converts a filename timestamp into a number of a preferred unit of
% time.

% Use one section of those below and comment out the other. Insert the
% numerical locations of the time-stamps of the various classes in the
% parentheses after ".name". (e.g. for dd_hh_mm_ss, ss would be 10:11).


% DAYS HOURS MINUTES SECONDS (typically for experiments)

% days = str2double(files(L).name());
 hours = str2double(files(L).name(13:14));
 minutes = str2double(files(L).name(15:16));
 seconds = str2double(files(L).name(17:18));
%seconds = str2double(files(L).name(9:15)); %(XES02) 
%timestamp=seconds;
timestamp = seconds + 60*minutes + 3600*hours;
%timestamp = seconds + 60*minutes + 3600*hours + 86400*days;



% YEARS (e.g., 1986; typically for field-scale rivers)

% timestamp = str2double(files(L).name(1:4));


% OTHER

%timestamp = 120*(str2double(files(L).name(9:11))-1);
