clear all; close all;

% Plots for reworking

% System
system = 'DB03-1_01_23_deepscour';

% Labels
rivername = 'DB03-1';
marker_size = 1;

% Define intermittency: to hours at bankfull
I = 1;

% Define equation used to fit

a = 0.9315;
b = 0.3606;
c = 0.1043;

% Load file
load(['/Volumes/MY BOOK/decor4/files/' system '/rework_output/notvisited_zeroed_onelist/notvisited_notinitial_zero_all.mat']);

% Define time
    % Years to hours for field case, seconds to hours for lab case
    % conversion = 365.25*24;
    conversion = 1/3600;
time = notvisited_notinitial_zero_all(:,1)*conversion;
time_bankfull  = time*I;

% Make fitting equation

maximum= 1.05*max(time_bankfull);
times = 0:maximum/1000:maximum;
fit_curve = (a-c)*exp(-b*times)+c;

% Plot
figure(1);
plot(time_bankfull,notvisited_notinitial_zero_all(:,2),'.','color',([0.31 0.31 0.31]),'markersize',marker_size);
hold on
plot(times,fit_curve,'k','LineWidth',2);
xlim([0 maximum]); ylim([0 1]);
title(rivername,'FontSize',24,'Interpreter','latex');
hold off

% Save
cd('/Volumes/MY BOOK/decor4/files/plotting/rw_plots')
saveas(1,[system '.jpg'],'jpg')

% Go back to running directory
cd('/Volumes/MY BOOK/decor4/programs/5_plotting')



