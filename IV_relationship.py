def CheckforIV (abf):
    """
    Check if the abf file is an IV recording and if the recordinging is complete.
    
    Parameters: abf meta data.
    
    Returns: 
        -bool: True if the file is an IV recording and is complete, False otherwise.
    """
    
    abf.setSweep(0, channel = 0)
    time1 = abf.sweepX
    voltage1 = abf.sweepC
    
    try: 
        if len(time1) != 6000:
            return False
        
        # Check if the voltage at a specific point is approximately -100
        # Using round() to round the value and then compare
        if round(voltage1[2000]) != -100:
            return False
        
        # Check if the total number of sweeps is 18
        if len(abf.sweepList) != 18:
            return False
        
        # If all conditions are met
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False

  def IV_relationship(filepath, start_time, end_time):
    '''
    Perform batch analysis of abf files in a input filepath, generating IV data and plots. 
    
    Parameters: 
        filepath that containing files to be analyzed. 
        Timeframe (start and end time point) for choosing the peak current. 
    
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
        
        
        if CheckforIV(abf) == False:
            continue
        
        voltage_steps = []
        peak_currents = []

        for sweepnumber in abf.sweepList:  # loop through the sweeps

            # Extract the voltage data
            abf.setSweep(sweepnumber, channel = 1)
            voltage = abf.sweepY # IN3 Readout
            time = abf.sweepX
            # Find indices corresponding to the time range
            start_index = np.where(time >= start_time)[0][0]
            end_index = np.where(time <= end_time)[0][-1]

            voltage_steps.append(round(np.mean(voltage[start_index:end_index+1])))

            # Extract the current data
            abf.setSweep(sweepnumber, channel=2)  # select the sewwp number
            current = abf.sweepY # sweep data 
            
            
            ### --- Applying Gaussian Low pass filter with cut off frequency @100Hz within the voltage step for IV
            filtered_signal, modified_signal = GaussianLowPassFilter(current, start_index, end_index, abf)

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
    output.to_csv(f"{BatchExportPath}/BatchIV_{Batchlabel}.csv", index = False)
    plt.savefig(f"{BatchExportPath}/BatchIV_{Batchlabel}.png", dpi=300)
    
    return 
