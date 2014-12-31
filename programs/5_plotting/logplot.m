% Written 12/22/11 by ADW
% Finds curve fits and generates logarithmic plots for my outputs

%% Setup

rootpath = '/Users/awickert/Documents/decor5/files/';
%rootpath = '/home/awickert/Desktop/decor5/files/';
rwpath = '/rework_output/notvisited_zeroed_onelist/notvisited_notinitial_zero_all.mat';
overlappath = '/correlation_output/correlation_scaled_zeroed_together/scalecor_zero_all.mat';

exportfigs=1; % 1 to export, 0 to not

% First, identify the experiments in which time steps really should be
% constant and need to be fixed.
% In fact, I am going to set all of them to dt
% CAN'T: TAL SAND HAS UNEVEN TIME STEPS (NOT ALL ACCOUNTED-FOR!!!)
explist = {'XES02_bl_const' 'XES02_slow_bl_fall' 'XES02_slow_bl_rise' 'XES02_rapid_bl_fall' 'XES02_rapid_bl_rise' 'DB03-1_02_04' 'DB03-2_1400-end' 'tal_sand' 'tal_veg'};
dtlist = [120 120 120 120 120 15 1800 30 30];
startrmv_list = [0 0 0 0 0 0 0 172 0]; % Remove these from the beginning of the data set
                                       % Tal nonveg discontinuity of
                                       % unknown length problem
                                       % Should be 175, but 172 b/c missing
                                       % first 3 entries
const_dt = [1 1 1 1 1 1 1 1 1]; % All but Tal nonveg have constant dt and can be stacked
                                % Wait - no! Is still even interval - and
                                % skipped are NaN, so are removed!
% max_t = [0 0 0 0 0 0 0 0.5 0]; % Look only at t < this; hours
descriptive_titles = {'XES02: base level constant' 'XES02: slow base level fall' 'XES02: slow base level rise' 'XES02: rapid base level fall' 'XES02: rapid base level rise' 'DB03-1' 'DB03-2'  'BV-1 (nonvegetated)' 'BV-2 (vegetated)'};

rw_output = zeros(length(dtlist),4);
overlap_output = zeros(length(dtlist),4);
                        
% Second, identify experiments in which we should pick only a subset of the
% avaiable data points for analysis.

% Third, choose the text positions
xrel_lin = .55;
yrel_lin = .8;
xrel_log = .05;
yrel_log = .1;
% BV-2 (Tal Veg) will always use the "log" versions

%% Loop start
generate_plots=1; % switch
for experiment=1:length(dtlist)
    %% Select experiments and get their characteristics
    expname = explist{experiment};
    expdt = dtlist(experiment);
    startrmv = startrmv_list(experiment);

    %% Reworking 
    % Import data
    % Replace experiment name with vector of names in the end
    load([rootpath expname rwpath]);
    nnza = notvisited_notinitial_zero_all;

    % Find length of data set
    % Number of elements to the first NaN
    nframes = find(isnan(nnza(:,1)), 1 ) - 1; % more efficient than: min(find(isnan(nnza(:,1))));
    nts = nframes - startrmv; % should be equal unless we have problems with the data and 
                   % need to remove some

    % Select frames to remove, if necessary
    nnza(1:nframes*startrmv,:) = [];

    % Remove required number of cells from the start of each set
    t = nnza(:,1);
    rw = nnza(:,2);
    for i=1:nts
        startpoint = (i-1) * nframes + 1;
        t(startpoint : startpoint + startrmv - 1) = -9999; % A "remove me" value
    end
    rw(t == -9999) = [];
    t(t == -9999) = [];
    nnza = [t rw]; % Make it square again, so to speak.
                   % Same number of time steps as number of image frames

    % Recalculate nframes
    nframes = find(isnan(nnza(:,1)), 1 ) - 1; % more efficient than: min(find(isnan(nnza(:,1))));
    
    if const_dt(experiment)
        %plot(nnza(:,1),nnza(:,2),'k.')

%         % If I want to cap the time that is taken into account
%         % to focus on the early transience
%         % that is done here
%         if max_t(experiment)
%             t = nnza(:,1);
%             rw = nnza(:,2);
%             rw = rw(t < max_t(experiment)*3600);
%             t = t(t < max_t(experiment)*3600);
%             nnza = [t rw];
%         end
        
        % Use dt [s] to rewrite the time array
        dt_seconds = expdt; % REPLACE
        dt = dt_seconds/3600; % convert to hours

        teven = 0:dt:(nframes-1)*dt;
        for i=1:nframes
            startpoint = (i-1) * nframes + 1;
            endpoint = i * nframes;
            nnza(startpoint:endpoint,1) = teven(1:end);
            % scoot up teven with a NaN at start
            teven(2:end) = teven(1:end-1);
            teven(1) = NaN;
        end
        
        % Stack
        teven = 0:dt:(nframes-1)*dt; % Restore teven
        rwstack = (zeros(size(teven)))'; % For size
        normalizer = rwstack; % Number of non-NaN entries you see
        %nnza_0nan = nnza;
        %nnza_0nan(isnan(nnza_0nan)) = 0;
        for i=1:nframes
            startpoint = (i-1) * nframes + 1;
            endpoint = i * nframes;
            rwstack(1:end+1-i) = rwstack(1:end+1-i) + nnza(startpoint+i-1:endpoint,2);
            %normalizer = normalizer + (1 - isnan(nnza(startpoint:endpoint,2)));
            normalizer(1:end+1-i) = normalizer(1:end+1-i) + 1;
        end
        rwstack = rwstack ./ normalizer;
    end
    if const_dt(experiment)
        t = nnza(:,1);
    else
        % Uneven data.
        % C onvert to hours
        t = t/3600;
    end
    
    %rw = nnza(:,2);
    % For DB03-2
    %rwexp = 0.9676 * exp(-0.03948 * teven) + 0.003674;

    % Remove all nan entries - won't plot anyway.
    % Ordering will be funky - but we have everything in order at this point
    % So just need this for plotting / curve fitting

    rw(isnan(t)) = [];
    t(isnan(t)) = [];
    
    % Curve fit
    % Define custom fit
    f = fittype( @(a, p, R, t) (a-p) * exp(-R*t) + p, 'independent', 't');
    % coeffnames(f) = a p R, as entered above, so will set start points in that
    % order
    startpoints = [1 0 .1];
    [c,gof] = fit(t,rw,f,'StartPoint',startpoints); % ,'Lower',[mean(rw(t*3600 == dtlist(experiment))) 0 0]
    % Then adjust the plotted curves to go along with this
    % (a-p) is the height of the function, a is the y-intercept, and p is the
    % asymptote
    % So we want to take the whole function, subtract out the asymptote so this
    % becomes 0) and then divide by the function height (so this becomes 1).
    % In reality, this should make the data point at 0 be >1, but this is OK.
    rwnorm = (rw - c.p)/(c.a-c.p);
    if const_dt(experiment)
        rwstack_norm = (rwstack - c.p)/(c.a-c.p);
    end
        
    % Also create curve fit
    if const_dt(experiment)
        rwexp = (c.a-c.p) * exp(-1*c.R*teven) + c.p;
        resid = rwstack-rwexp';
    end
    
    rw_output(experiment,:) = [c.a c.R c.p gof.rsquare];

    %% Overlap

    % Import data
    % Replace experiment name with vector of names in the end
    load([rootpath expname overlappath]);
    czo = corr_zero_onelist;

    % Find length of data set
    % Number of elements to the first NaN
    nframes = find(isnan(czo(:,1)), 1 ) - 1; % more efficient than: min(find(isnan(czo(:,1))));
    nts = nframes - startrmv; % should be equal unless we have problems with the data and 
                   % need to remove some

    % Select frames to remove, if necessary
    czo(1:nframes*startrmv,:) = [];
    
    % Remove required number of cells from the start of each set
    tc = czo(:,1);
    o = czo(:,2);
    for i=1:nts
        startpoint = (i-1) * nframes + 1;
        tc(startpoint : startpoint + startrmv - 1) = -9999; % A "remove me" value
    end
    o(tc == -9999) = [];
    tc(tc == -9999) = [];
    czo = [tc o]; % Make it square again, so to speak.
                   % Same number of time steps as number of image frames

    % Recalculate nframes
    nframes = find(isnan(czo(:,1)), 1 ) - 1; % more efficient than: min(find(isnan(czo(:,1))));

    % Use dt [s] to rewrite the time array
    if const_dt(experiment)
        dt_seconds = expdt; % REPLACE
        dt = dt_seconds/3600; % convert to hours

        teven = 0:dt:(nframes-1)*dt;
        for i=1:nframes
            startpoint = (i-1) * nframes + 1;
            endpoint = i * nframes;
            czo(startpoint:endpoint,1) = teven(1:end);
            % scoot up teven with a NaN at start
            teven(2:end) = teven(1:end-1);
            teven(1) = NaN;
        end
    end

    %plot(czo(:,1),czo(:,2),'k.')

%     % If I want to cap the time that is taken into account
%     % to focus on the early transience
%     % that is done here
%     if max_t(experiment)
%         tc = czo(:,1);
%         o = czo(:,2);
%         o = o(tc < max_t(experiment)*3600);
%         tc = tc(tc < max_t(experiment)*3600);
%         czo = [tc o];
%     end
    
    % Stack
    if const_dt(experiment)
        teven = 0:dt:(nframes-1)*dt; % Restore teven
        ostack = (zeros(size(teven)))'; % For size
        normalizer = ostack; % Number of non-NaN entries you see
        %czo_0nan = czo;
        %czo_0nan(isnan(czo_0nan)) = 0;
        for i=1:nframes
            startpoint = (i-1) * nframes + 1;
            endpoint = i * nframes;
            ostack(1:end+1-i) = ostack(1:end+1-i) + czo(startpoint+i-1:endpoint,2);
            %normalizer = normalizer + (1 - isnan(czo(startpoint:endpoint,2)));
            normalizer(1:end+1-i) = normalizer(1:end+1-i) + 1;
        end
        ostack = ostack ./ normalizer;
    end
    
    if const_dt(experiment)
        tc = czo(:,1);
    else
        % Uneven data.
        % C onvert to hours
        tc = tc/3600;
    end
    
    %o = czo(:,2);
    % For DB03-2
    %oexp = 0.9676 * exp(-0.03948 * teven) + 0.003674;

    % Remove all nan entries - won't plot anyway.
    % Ordering will be funky - but we have everything in order at this point
    % So just need this for plotting / curve fitting
    o(isnan(tc)) = [];
    tc(isnan(tc)) = [];


    % Curve fit
    % Define custom fit
    f = fittype( @(a, p, M, t) (a-p) * exp(-M*t) + p, 'independent', 't');
    %options = fitoptions(f);
    %set(options,'Lower',[0 0 0]) % DB03-2 - not a permanent solution, but this is the only instance for which I need it
    % coeffnames(f) = a p R, as entered above, so will set start points in that
    % order
    startpoints = [.4 .4 1];
    [co,gof] = fit(t,o,f,'StartPoint',startpoints); %,'Lower',[0 0 0] %mean(o(tc*3600 == dtlist(experiment))) for 1st coeff lower
    % Then adjust the plotted curves to go along with this
    % (a-p) is the height of the function, a is the y-intercept, and p is the
    % asymptote
    % So we want to take the whole function, subtract out the asymptote so this
    % becomes 0) and then divide by the function height (so this becomes 1).
    % In reality, this should make the data point at 0 be >1, but this is OK.
    onorm = (o - co.p)/(co.a-co.p);
    if const_dt(experiment)
        ostack_norm = (ostack - co.p)/(co.a-co.p);
    end
    % Also create curve fit
    if const_dt(experiment)
        oexp = (co.a-co.p) * exp(-1*co.M*teven) + co.p;
        resid_o = ostack-oexp';
    end
    overlap_output(experiment,:) = [co.a co.M co.p gof.rsquare];

    %% Plot (group)
    if generate_plots
        rwfig = figure('position',[101 -500 1100 1100]);
        overlapfig = figure('position',[101 -500 1100 1100]);
        %rwlog = figure('position',[101 -500 1100 1100]);
        %overlaplog = figure('position',[101 -500 1100 1100]);
        rwlog_norm = figure('position',[101 -500 1100 1100]);
        %overlaplog_norm = figure('position',[101 -500 1100 1100]);
        generate_plots=0; % switch off
    end

    % Text
    textstrR = ['R = ', num2str(c.R, 4)];
    textstrM = ['M = ', num2str(co.M, 4)];
    
    figure(rwfig)
    subplot(3,3,experiment)
    hold on
    plot(t,rw,'k.','MarkerSize',4,'MarkerEdgeColor',[.8 .8 .8]) % Points
    if const_dt(experiment)
        plot(teven,rwstack, 'Color', [.4 .4 .4], 'LineWidth', 3) % Line
        plot(teven,rwexp, 'Color', [0 0 0], 'LineWidth', 3)
    end
    ylim([0 1])
    % text
    xlim([0 ceil(max(t))])
    xl = xlim;
    yl = ylim;
    if all(descriptive_titles{experiment}(1:4) == 'BV-2')
        xt_pos_lin = .1*(abs(diff(xlim))) + xl(1);
        yt_pos_lin = .2*(abs(diff(ylim))) + yl(1);
    else
        xt_pos_lin = xrel_lin*(abs(diff(xlim))) + xl(1);
        yt_pos_lin = yrel_lin*(abs(diff(ylim))) + yl(1);
    end
    text(xt_pos_lin,yt_pos_lin,textstrR, 'FontSize', 18)
    hold off
    title(descriptive_titles{experiment}, 'FontSize', 18)
    set(gca,'FontSize',18) % tick labels
    
    figure(overlapfig)
    subplot(3,3,experiment)
    hold on
    plot(t,o,'k.','MarkerSize',4,'MarkerEdgeColor',[.8 .8 .8]) % Points
    if const_dt(experiment)
        plot(teven,ostack, 'Color', [.4 .4 .4], 'LineWidth', 3) % Line
        plot(teven,oexp, 'Color', [0 0 0], 'LineWidth', 3)
    end
    yl = ylim;
%    ylim([yl(1), 1])
    ylim([-.5 1])
    xlim([0 ceil(max(t))])
    xl = xlim;
    yl = ylim;
    if all(descriptive_titles{experiment}(1:4) == 'BV-2')
        xt_pos_lin = .1*(abs(diff(xlim))) + xl(1);
        yt_pos_lin = .2*(abs(diff(ylim))) + yl(1);
    else
        xt_pos_lin = xrel_lin*(abs(diff(xlim))) + xl(1);
        yt_pos_lin = yrel_lin*(abs(diff(ylim))) + yl(1);
    end
    text(xt_pos_lin,yt_pos_lin,textstrM, 'FontSize', 18)
    hold off
    title(descriptive_titles{experiment}, 'FontSize', 18)
    set(gca,'FontSize',18) % tick labels
    
%     figure(rwlog)
%     subplot(3,3,experiment)
%     semilogy(t,rw,'k.','markers',4) % Points
%     hold on
%     semilogy(teven,rwstack) % Line
%     semilogy(teven,rwexp,'r-')
%     hold off
%     title(descriptive_titles{experiment})
    
%     figure(overlaplog)
%     subplot(3,3,experiment)
%     semilogy(t,o,'k.','markers',4) % Points
%     hold on
%     semilogy(teven,ostack) % Line
%     semilogy(teven,oexp,'r-')
%     hold off
%     title(descriptive_titles{experiment})

    figure(rwlog_norm)
    subplot(3,3,experiment)
    semilogy(t,rwnorm,'k.','MarkerSize',4,'MarkerEdgeColor',[.8 .8 .8]) % Points
    ylim([1E-3 1])
    hold on
    if const_dt(experiment)
        semilogy(teven,rwstack_norm, 'Color', [.4 .4 .4], 'LineWidth', 3) % Line
        semilogy(teven,exp(-1*c.R*teven), 'Color', [0 0 0], 'LineWidth', 3)
    end
    xlim([0 ceil(max(t))])
    xl = xlim;
    yl = ylim;
    if all(descriptive_titles{experiment}(1:4) == 'BV-2')
        xt_pos_lin = .1*(abs(diff(xlim))) + xl(1);
        yt_pos_log = 5E-3;
    else
        xt_pos_lin = xrel_lin*(abs(diff(xlim))) + xl(1);
        yt_pos_log = .5;
    end
    text(xt_pos_lin,yt_pos_log,textstrR, 'FontSize', 18)
    hold off
    title(descriptive_titles{experiment}, 'FontSize', 18)
    set(gca,'FontSize',18) % tick labels

%     figure(overlaplog_norm)
%     subplot(3,3,experiment)
%     semilogy(t,onorm,'k.','markers',4) % Points
%     hold on
%     semilogy(teven,ostack_norm) % Line
%     semilogy(teven,exp(-1*co.M*teven),'r-')
%     hold off
%     title(descriptive_titles{experiment})

end


output = [overlap_output rw_output]

%getenv('HOME')
if exportfigs
    figure(rwfig)
    export_fig '/Users/awickert/Documents/geology_docs/papers/Submitted copies/Channel_mobility/Revising2012/figures/rework_lin.png' -png -transparent -m2
    figure(overlapfig)
    export_fig '/Users/awickert/Documents/geology_docs/papers/Submitted copies/Channel_mobility/Revising2012/figures/overlap_lin.png' -png -transparent -m2
    figure(rwlog_norm)
    export_fig '/Users/awickert/Documents/geology_docs/papers/Submitted copies/Channel_mobility/Revising2012/figures/rework_log.png' -png -transparent -m2
end
