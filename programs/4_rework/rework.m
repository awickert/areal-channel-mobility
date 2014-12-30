clear all; close all;

% This program loads the binary channel-map file for each image in turn,
% and calculates the amount of active channel area remaining un-visited
% over time, in order to define a floodplain re-working time-scale.


% Human-entered variables and directory names
rework_vars %This is the file that needs to be edited for each run.
directories %This is automated based on selections in correlation_vars.m.

% Channel-maps
cd(channelmapindir);
channelmaps = dir ('*.mat');

% Load matrix of time-steps and pixel occupancy and set a variable for
% number of pixels in the active floodplain (A).
cd(timepixindir);
timepixlist = dir ('*.mat');
timepix = load(timepixlist(1).name);
timepix = timepix.pixmat;
A = timepix(1,2);


% Analyze the data through four steps.

% Load each baseline.
for z=1:numel(channelmaps)
    
    % Load the *.mat channel-map files and specify the output filename.
    % (The specification of the output filename is set to be automated
    % based on the filename time-stamp, set through correlation_vars.m.
    cd(channelmapindir);
    baselinename=([channelmaps(z).name]);
    baseline=load(baselinename);
    baseline=baseline.channel;
    outputname=['base_', baselinename(timestampchars)];
    
    % Find the number of wet pixels in the baseline image-matrix.
    nwetpix_baseline = sum(sum(baseline));
    
    % Specify the number of entries in the output matrices, and create the
    % template output matries for the first three steps.
    time_z=timepix(z:end,1);
    template1=NaN*zeros((numel(channelmaps)),2);
    template2=template1;
    template2(z:end,1)=time_z;
    template3=template1;
    template3(z:end,1)=time_z-timepix(z,1);
    
    npix_visited_outmat=template2;
    notvisited_outmat=template2;
    notvisited_notinitial_outmat=template2;
    notvisited_zero_outmat=template3;
    notvisited_notinitial_zero_outmat=template3;
    
    % Set initial number of visited pixels to 0
    previsited=0;
    
    for f=z:(numel(channelmaps))
        
        % STEP 1: Find the number of visited pixels.
        cd(channelmapindir);
        transient=load(channelmaps(f).name);
        transient=transient.channel;
        visitedmap=transient+previsited;
        binaryvisitedmap=visitedmap>0;
        npix_visited=sum(sum(binaryvisitedmap));
        
        % Set new number of visited pixels;
        previsited=visitedmap;
        
        % In order to analyze the data, a single column matrix is made,
        % containing each of the sums.
        npix_visited_outmat(f,2)=npix_visited;
        
        
        % STEP 2: Load the mask from the making of the wet-dry maps in
        % order to find how many pixels are in the active floodplain. Make
        % sure that the active floodplain is denoted by a "1" in MATLAB in
        % the mask image-matrix
        cd(maskdir);
        mask=importdata('mask.bmp');
        floodplain=mask.cdata;
        npix_fp_total=sum(sum(floodplain));
        
        
        % STEP 3: create both scaled output matrices.
        
        % This output matrix gives the proportion of the total active
        % floodplain area not yet visited by the flow.
        notvisited_outmat(f,2) = 1 - (npix_visited / npix_fp_total);
        
        % This output matrix gives the proportion of the total active
        % floodplain, excluding the initial channel area, not yet visited
        % by the flow.
        notvisited_notinitial_outmat(f,2) = 1 - ((npix_visited-nwetpix_baseline) / (npix_fp_total-nwetpix_baseline));       
        
        
        % STEP 4: Set the baseline time-step to occur at t=0.
        notvisited_zero_outmat(f,2) = notvisited_outmat(f,2);
        notvisited_notinitial_zero_outmat(f,2) = notvisited_notinitial_outmat(f,2);
        
    end
    
    % Step 5: make the single 2-column list of time-steps and scaled
    % correlation with t=0 at each baseline.
    
    % For the basic not visited
    if z==1
        notvisited_zero_all=notvisited_zero_outmat;
    else
        notvisited_zero_all=[notvisited_zero_all; notvisited_zero_outmat];
    end

    % For the pixels not visited and not including the original channel
    % area
    if z==1 
        notvisited_notinitial_zero_all=notvisited_notinitial_zero_outmat;
    else
        notvisited_notinitial_zero_all=[notvisited_notinitial_zero_all; notvisited_notinitial_zero_outmat];
    end
    
    % Save the files from steps 1-4.
    cd(tot_npix_visited)
    save(outputname, 'npix_visited_outmat');
    
    cd(notvisited)
    save(outputname, 'notvisited_outmat');

    cd(notvisited_notinitial)
    save(outputname, 'notvisited_notinitial_outmat');
    
    cd(notvisited_zero)
    save(outputname, 'notvisited_zero_outmat');
    
    cd(notvisited_notinitial_zero)
    save(outputname, 'notvisited_notinitial_zero_outmat');
    
end

% Save the files from step 5.
cd(notvisited_zero_onelist)
save('notvisited_zero_all', 'notvisited_zero_all');
save('notvisited_notinitial_zero_all', 'notvisited_notinitial_zero_all');
time=notvisited_notinitial_zero_all(:,1);
save('time', 'time');
notvisited=notvisited_zero_all(:,2);
save('notvisited', 'notvisited');
notvisited_notinitial=notvisited_notinitial_zero_all(:,2);
save('notvisited_notinitial', 'notvisited_notinitial');

cd(progdir)