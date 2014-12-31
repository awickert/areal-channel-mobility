% Started Christmas Eve, 2011
% Histograms of wetted fractions!

exportfigs=1; % 1 to export, 0 to not

rootpath = '/Users/awickert/Documents/decor4/files/';
fwpath = '/channelmap_output/timesteps_pixelcount/timestamp_pixdist.mat';
explist = {'XES02_bl_const' 'XES02_slow_bl_fall' 'XES02_slow_bl_rise' 'XES02_rapid_bl_fall' 'XES02_rapid_bl_rise' 'DB03-1_02_04' 'DB03-2_1400-end' 'tal_sand' 'tal_veg'};
descriptive_titles = {'XES02: base level constant' 'XES02: slow base level fall' 'XES02: slow base level rise' 'XES02: rapid base level fall' 'XES02: rapid base level rise' 'DB03-1' 'DB03-2'  'BV-1 (nonvegetated)' 'BV-2 (vegetated)'};

for experiment=1:length(explist)
    
    % pixmat
    load([rootpath explist{experiment} fwpath]);

    if experiment == 1
        histogram = figure('position',[101 -500 1100 1100]);
    end

    figure(histogram)
    subplot(3,3,experiment)
    hist((pixmat(:,3) - mean(pixmat(:,3)))/mean(pixmat(:,3)),20);
    xlim([-1 1])
    h = findobj(gca,'Type','patch');
    set(h,'FaceColor',[.3 .3 .3],'EdgeColor','k')
    title(descriptive_titles{experiment})
end

if exportfigs
    % export_fig '/Users/awickert/Documents/geology_docs/papers/Working copies/Channel mobility - methods/figures/fw_hist.png' -jpg -m2
    saveas(histogram,'/Users/awickert/Documents/geology_docs/papers/Working copies/Channel mobility - methods/figures/fw_hist.eps')
end
