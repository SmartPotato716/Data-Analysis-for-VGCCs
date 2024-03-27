def SteadyStateInactivation(filepath, SSI_start_time, SSI_end_time):
    '''
    Perform Batch analysis to the abf files, parsing out the absolute peak currents within tail currents and plot the SSI.
    
    Parameters:
        filepath
        the time window that we choosed for the tail current
        
    Returns:
        .csv file of IV data
        initial plots for data inspection   
    '''
    
     # parse all the abf files from the filepath. 
    file_list = glob.glob(os.path.join(filepath, "*.abf"))
    # Initiate the output dataframe.
    voltage_steps = []
    output = pd.DataFrame({
    'Voltages': voltage_steps,
    })
    
    # loop through the files
    for file in file_list:
        print (file) 
        abf = pyabf.ABF(file) #Loading the data
        
        
        if CheckforSSI(abf) == False:
            continue
        
        voltage_steps = []
        peak_currents = []

        for sweepnumber in abf.sweepList:  # loop through the sweeps

            # Extract the voltage data
            abf.setSweep(sweepnumber, channel = 1)
            voltage = abf.sweepY # IN3 Readout
            time = abf.sweepX
            # Find indices corresponding to the time range for the voltage steps, here we are setting it to be between 0.5s to 1.5s.
            voltage_start_index = np.where(time >= 0.5)[0][0]
            voltage_end_index = np.where(time <= 1.5)[0][-1]

            voltage_steps.append(round(np.mean(voltage[voltage_start_index:voltage_end_index+1])))

            # Extract the current data
            abf.setSweep(sweepnumber, channel=2)  # select the sewwp number
            current = abf.sweepY # sweep data 
            # Find the indices for the tail current data.
            current_start_index = np.where(time >= SSI_start_time)[0][0]
            current_end_index = np.where(time <= SSI_end_time)[0][-1]            
            
            ### --- Applying Gaussian Low pass filter with cut off frequency @100Hz within the voltage step for IV
            filtered_signal, modified_signal = GaussianLowPassFilter(current, current_start_index, current_end_index, abf)

            # Find the index of the absolute maximum value
            index_of_max = np.argmax(np.abs(filtered_signal))
            #Find the absolute peak value within the filtered segments
            absolute_peak_value = filtered_signal[index_of_max]
            # print("The absolute peak value within the segment is:", absolute_peak_value)
            # Append the peak currents to the column
            peak_currents.append(absolute_peak_value)
            # print(len(peak_currents)
        
        
        filename = os.path.splitext(os.path.basename(file))[0]
        output['Voltages'] = voltage_steps
        output[filename] = peak_currents

        plt.plot(voltage_steps, peak_currents, label = filename)
        plt.axhline(y=0, color='k')  # Horizontal line (x-axis)
        plt.axvline(x=0, color='k')  # Vertical line (y-axis)
        plt.legend()
        # print(filename)
    Batchlabel = os.path.splitext(os.path.basename(file))[0][0:5]
    output.to_csv(f"{BatchExportPath}/BatchSSI_{Batchlabel}.csv", index = False)
    plt.savefig(f"{BatchExportPath}/BatchSST_{Batchlabel}.png", dpi=300)
    
    return 
