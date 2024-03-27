def exp_func(x, a, tau, c):
    return a*np.exp(-x/tau) + c

gmodel = Model(exp_func)
# print(f'parameter names: {gmodel.param_names}')
# print(f'independent variables: {gmodel.independent_vars}')
params = gmodel.make_params()
# print(params)

def expfit(start_index, end_index, time, current):
    
    x_data = time
    x_data = (x_data-x_data[0])*1000
    y_data = current
    
    p0 = [500, 0.02, -500]
    
    params, covariances = curve_fit(exp_func, x_data, y_data, p0)
    result = gmodel.fit(y_data, x = x_data, a = 500, tau = 50, c = -500)
    
    print(result.fit_report())
    
    plt.plot(x_data, y_data, 'o')
    plt.plot(x_data, result.init_fit, '--', label='initial fit')
    plt.plot(x_data, result.best_fit, '-', label='best fit')
    plt.legend()
    plt.show()

    a_fit, tau_fit, c_fit = params
    plt.plot(x_data, y_data)
    y_fit_data = exp_func(x_data, a_fit, tau_fit, c_fit)
    plt.plot(x_data, y_fit_data)
    plt.show()
    print (params)
    
    return tau_fit

def timeconstant(filepath, tau_starttime, tau_endtime):
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
        tau_ons = []
        tau_offs = []

        for sweepnumber in abf.sweepList:  # loop through the sweeps

            # Extract the voltage data
            abf.setSweep(sweepnumber, channel = 1)
            voltage = abf.sweepY # IN3 Readout
            time = abf.sweepX
            # Find indices corresponding to the time range for the voltage steps, here we are setting it to be between 0.5s to 1.5s.
            voltage_start_index = np.where(time >= 0.5)[0][0]
            voltage_end_index = np.where(time <= 1.5)[0][-1]
            
            # Filtering out the voltages steps between -50 to 0 mV.
            voltage_step = round(np.mean(voltage[voltage_start_index:voltage_end_index+1]))
            
            if voltage_step <-50 or voltage_step > 0:
                continue
            print (voltage_step)
            voltage_steps.append(voltage_step)

            # Extract the current data
            abf.setSweep(sweepnumber, channel=2)  # select the sewwp number
            current = abf.sweepY # sweep data 
            # Find the indices for the tail current data.
            current_start_index = np.where(time >= tau_starttime)[0][0]
            current_end_index = np.where(time <= tau_endtime)[0][-1]            
            current_new = current[current_start_index:current_end_index+1]
            
            ### --- Applying Gaussian Low pass filter with cut off frequency @100Hz within the voltage step for IV
            filtered_signal, modified_signal = GaussianLowPassFilter(current, current_start_index, current_end_index, abf)
            
            # plt.plot(filtered_signal)
            dI = dI_dt(filtered_signal)
            plt.plot(time[current_start_index: current_end_index+1], current_new)
            plt.show()
            # Find the index of the absolute maximum value
            index_of_max = np.argmax(np.abs(filtered_signal))
            
            time_on = time[current_start_index:current_start_index+index_of_max+1]
            current_on = current_new[0:index_of_max+1]
            
            time_off = time[current_start_index+index_of_max-1:current_end_index]
            current_off = current_new[index_of_max-1:-1]
            
            # print(index_of_max)
            # plt.plot(time_on, current_on)
            # plt.plot(time_off, current_off)
            
            tau_on = expfit(0, index_of_max, time_on, current_on)
            tau_off = expfit(index_of_max, -1, time_off, current_off)
            
            # Append the peak currents to the column
            tau_ons.append(tau_on)
            tau_offs.append(tau_off)
            # print(len(peak_currents)
        
        
        filename = os.path.splitext(os.path.basename(file))[0]
        
        output['Voltages'] = voltage_steps
        output['filename'] = filename
        output['tau_ons'] = tau_ons
        output['tau_offs'] = tau_offs
        

    Batchlabel = os.path.splitext(os.path.basename(file))[0][0:5]
    # output.to_csv(f"{BatchExportPath}/BatchSSI_{Batchlabel}.csv", index = False)
    print (output)
    return 

timeconstant("YangdongWang_24SpringRotationData/Ephys20240303", 0.093, 1.5)
