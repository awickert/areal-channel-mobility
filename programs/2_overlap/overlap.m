clear all; close all;

% This program loads the binary channel-map file for each image,
% finds the change between each image and a given baseline, and sums the
% change into a single value showing amount of decorrelation, or (as has been 
% more conservatively termed in the paper, loss of planform overlap (as opposed 
# to amount of remaining planform overlap, which is what the final graphs show).
% These single values are accumulated across the whole timeseries of data into 
% a new single DAT file, and a DAT file like this can be created for as many
% baselines as are specified.

% Variables are still named "corr" in memory of their previous naming as 
% "correlation" / "decorrelation" -- while this is not correlation in a strict 
% sense, it is analogous as a spatial overlap of patterns


% turns the DAT files for each of the images into single
% values, and then creates a graphable matrix of these values.
% Ta-da!


% Load data for the whole program.


% Human-entered variables and directory names
overlap_vars %This is the file that needs to be edited for each run.
directories %This is automated based on selections in overlap_vars.m.

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
    % based on the filename time-stamp, set through overlap_vars.m.
    cd(channelmapindir);
    baselinename=([channelmaps(z).name]);
    baseline=load(baselinename);
    baseline=baseline.channel;
    outputname=['base_', baselinename(timestampchars)];
    
    % Specify the number of entries in the output matrices, and create the
    % template output matries for the first three steps.
    time_z=timepix(z:end,1);
    template1=NaN*zeros((numel(channelmaps)),2);
    template2=template1;
    template2(z:end,1)=time_z;
    template3=template1;
    template3(z:end,1)=time_z-timepix(z,1);
    
    npix_decor_outmat=template2;
    corr_outmat=template2;
    corr_zero_outmat=template3;
    
    for f=z:(numel(channelmaps))
        
        % STEP 1: Find the number of decorrelated pixels.
        cd(channelmapindir);
        transient=load(channelmaps(f).name);
        transient=transient.channel;
        changedpix=sum(sum(abs(baseline-transient)));
        % Note: In the channel-maps, 0=active floodplain and 1=channel. So
        % in changedpix, 0=no change and 1=change. 
        
        % In order to analyze the data, a single column matrix is made,
        % containing each of the sums.
        npix_decor_outmat(f,2)=changedpix;
        
        
        % STEP 2: Build scaling parameters and apply the overlap.
        Phi=timepix(z,3)*timepix(f,4)+timepix(z,4)*timepix(f,3);
        corr_outmat(f,2)=1-changedpix/(Phi*A);
        
        
        % STEP 3: Set the baseline time-step to occur at t=0.
        corr_zero_outmat(f,2)=corr_outmat(f,2);
        
    end
    
    % Step 4: make the single 2-column list of time-steps and scaled
    % overlap with t=0 at each baseline.
    if z==1
        corr_zero_onelist=corr_zero_outmat;
    else
        corr_zero_onelist=[corr_zero_onelist; corr_zero_outmat];
    end
    
    % Save the files from steps 1-3.
    cd(numdecor)
    save(outputname, 'npix_decor_outmat');
    
    cd(scalecor)
    save(outputname, 'corr_outmat');
    
    cd(scalecor_zero)
    save(outputname, 'corr_zero_outmat');
    
end

% Save the file from step 4.
cd(scalecor_zero_onelist)
save('scalecor_zero_all', 'corr_zero_onelist');
time=corr_zero_onelist(:,1);
save('time', 'time');
corr=corr_zero_onelist(:,2);
save('corr', 'corr');

cd(progdir)
