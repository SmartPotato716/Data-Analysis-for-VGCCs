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

def CheckforSSI(abf):
    '''
    Check if the abf file is an SSI recording and if the recording is complete. 
    
    Parameters: abf meta data. 
    
    Returns:
        -bool: True if the file is an SSI recording and is complete, False if otherwise.
    '''
    abf.setSweep(0, channel = 0)
    time1 = abf.sweepX
    voltage1 = abf.sweepC
    
    try: 
        if len(time1) != 25000:
            return False
        
        # Check if we are steping the voltage back to -30 after long-term inactivation.
        # Using round() to round the value and then compare
        if round(voltage1[21000]) != -30:
            return False
        
        # Check if the total number of sweeps is 18
        if len(abf.sweepList) != 18:
            return False
        
        # If all conditions are met
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False
