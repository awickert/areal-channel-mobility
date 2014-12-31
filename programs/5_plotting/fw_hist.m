% Started Christmas Eve, 2011
% Histograms of wetted fractions!

exportfigs=1; % 1 to export, 0 to not

%rootpath = '/Users/awickert/Documents/decor4/files/';
rootpath = '/home/awickert/Desktop/decor4/files/';
fwpath = '/channelmap_output/timesteps_pixelcount/timestamp_pixdist.mat';
explist = {'XES02_bl_const' 'XES02_slow_bl_fall' 'XES02_slow_bl_rise' 'XES02_rapid_bl_fall' 'XES02_rapid_bl_rise' 'DB03-1_02_04' 'DB03-2_1400-end' 'tal_sand' 'tal_veg'};
descriptive_titles = {'XES02: base level constant' 'XES02: slow base level fall' 'XES02: slow base level rise' 'XES02: rapid base level fall' 'XES02: rapid base level rise' 'DB03-1' 'DB03-2'  'BV-1 (nonvegetated)' 'BV-2 (vegetated)'};

%x = -1:.01:1;
x = 0:.01:2;

for experiment=1:length(explist)
    
    % pixmat
    load([rootpath explist{experiment} fwpath]);

    % Create a fit to the histogram
    [N,X] = hist((pixmat(:,3) - mean(pixmat(:,3)))/mean(pixmat(:,3))+1,20);
    %X = X+1;
    %N = N / (sum(N) * mean(diff(X)));
    [fitobject, gof] = fit(X',N','gauss1');
    
    if experiment == 1
        histogram = figure('position',[101 -500 1100 1100]);
    end

    figure(histogram)
    subplot(3,3,experiment);
    hold on
    bar(X,N,1)
    %hist((pixmat(:,3) - mean(pixmat(:,3)))/mean(pixmat(:,3))+1,20);
    xlim([0 2])
    %h(1) = plot(fitobject);
    plot(x, fitobject.a1 * exp(-((x-fitobject.b1)./fitobject.c1).^2), 'k-', 'LineWidth', 2 )
    % R squared in text on plot
    yl = ylim;
    text(1.3, 0.9 * yl(2), ['R^2 = ' num2str(gof.rsquare)], 'Color', 'k');
    
    %tickValues = get(gca,'XTick');
    %newLabels = arrayfun(@(value)(sprintf('%.1f $b$',value)), tickValues, 'UniformOutput',false);
    %set(gca, 'XTickLabel', newLabels);
    
    % LaTeX support
    [hx,hy] = format_ticks(gca,'$\bar{b}$','');

    
    hold off
    h = findobj(gca,'Type','patch');
    %set(h,'FaceColor',[.3 .3 .3],'EdgeColor','k')
    set(h,'FaceColor',[.6 .6 .6],'EdgeColor',[.6 .6 .6])
    title(descriptive_titles{experiment})
end

if exportfigs
    % export_fig '/Users/awickert/Documents/geology_docs/papers/Working copies/Channel mobility - methods/figures/fw_hist.png' -jpg -m2
    %saveas(histogram,'/Users/awickert/Documents/geology_docs/papers/Working copies/Channel mobility - methods/figures/fw_hist.eps')
    saveas(histogram,'/home/awickert/Documents/geology_docs/papers/Submitted copies/Channel_mobility/Revising2012/figures/fw_hist_withcurves.eps')
end
