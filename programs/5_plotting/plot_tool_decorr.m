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

a = 0.5691;
b = 1.905;
c = 0.1445;

% Load file
load(['/home/awickert/Desktop/decor4/files/' system '/correlation_output/correlation_scaled_zeroed_together/scalecor_zero_all.mat']);

% Define time
    % Years to hours for field case, seconds to hours for lab case
    % conversion = 365.25*24;
    conversion = 1/3600;
time = corr_zero_onelist(:,1)*conversion;
time_bankfull  = time*I;

% Make fitting equation

maximum= 1.05*max(time_bankfull);
times = 0:maximum/1000:maximum;
fit_curve = (a-c)*exp(-b*times)+c;

% Plot
figure(1);
plot(time_bankfull,corr_zero_onelist(:,2),'.','color',([0.31 0.31 0.31]),'markersize',marker_size);
hold on
plot(times,fit_curve,'k','LineWidth',2);
xlim([0 maximum]); ylim([-.2 1.00001]);
title(rivername,'FontSize',24,'Interpreter','latex');
hold off

% Save
cd('/home/awickert/Desktop/decor4/files/plotting/decor_plots')
%saveas(1,[system '.jpg'],'jpg')

% Go back to running directory
cd('/home/awickert/Desktop/decor4/programs/5_plotting')



