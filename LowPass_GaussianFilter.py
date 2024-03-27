def GaussianLowPassFilter(currentsweep, start_index, end_index, abf):
    '''
    Take each current sweep data as input and apply a low pass gaussian filter to the data. 
    The filter is only applied to the selected time range IV data extraction.
    
    Parameters: 
        current data for each sweep. 
        the IV_start_time and IV_end_time in the function of IV_Relationships.
        abf file itself for the sampling rate.
        
    Return:
        filtered current data within the time range(filtered signal).
        modifified current data (with filtered current data being inserted into the raw sweep data) for the plotting purposes.
    '''
    
    # Extract the segment of interest
    segment = currentsweep[start_index:end_index+1]
    # Use the Fast Fourier Tranform (FFT) to convert a signal to the frequency domain
    signal_fft = scipy.fftpack.fft(segment)
    #Apply a Gaussian filter as a mask
    frequency = np.fft.fftfreq(segment.size, d=1/abf.dataRate)
    cutoff_frequency = 50  # Define your cutoff frequency in Hz
    gaussian_mask = np.exp(-frequency**2 / (2 * cutoff_frequency**2))
    filtered_fft = signal_fft * gaussian_mask
    # IFFT to convert back to time domain
    filtered_signal = np.real(scipy.fftpack.ifft(filtered_fft))
    # Copy the original signal to not modify it directly
    modified_signal = np.copy(currentsweep)
    # Replace the segment in the copied signal with the filtered segment
    modified_signal[start_index:end_index+1] = filtered_signal
    
    return filtered_signal ,modified_signal
