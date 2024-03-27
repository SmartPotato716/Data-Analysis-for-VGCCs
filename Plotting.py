filename = "YangdongWang_24SpringRotationData/Ephys20240303/24303011.abf"

def plottingVoltages(filename, start_time, end_time):
    
    abf = pyabf.ABF(filename)
    for sweepnumber in abf.sweepList:
        
        abf.setSweep(sweepnumber, channel = 1)
        current = abf.sweepY
        time = abf.sweepX
        
        start_index = np.where(time >= start_time)[0][0]
        end_index = np.where(time <= end_time)[0][-1]
        
        time = time[start_index:end_index+1]
        filtered_signal, modified_signal = GaussianLowPassFilter(current, 700, 1050, abf)
        current = current[start_index:end_index+1]
        modified_current = modified_signal[start_index:end_index+1]
        
        plt.plot(time, current, label = "IV_Protocal", color = 'k')
        # plt.plot(time, modified_current, color = 'red')

# plottingVoltages(filename, 0, 2.25)
        
# Step 1: Plotting the representative traces
IV_representative_path = 'YangdongWang_24SpringRotationData/BatchExport/WT_SSI_Rep_Trace.csv'  # Update this with your CSV file path
def plotRepreIV(file_path):
    data = pd.read_csv(file_path)

    # Set the first column as the index
    data.set_index(data.columns[0], inplace=True)

    # Plotting all columns against the first column
    plt.figure(figsize=(14, 8))
    for column in data.columns:
        plt.plot(data.index, data[column], color = 'k')

    plt.title('Plot of All Columns Against the First Column')
    plt.xlabel('First Column Values')
    plt.ylabel('Data Series Values')
    # plt.legend(loc='upper right', fontsize='small')
    # plt.grid(True)

    plt.show()
        
plotRepreIV(IV_representative_path)

def plotIV(Individual_IV_Path):
    df = pd.read_csv(Individual_IV_Path)
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 16))
    colors = {1: 'blue', 2: 'red'}
    groups = df.iloc[0, 1:].astype(int)  # Transfection values, as integers
    df_plot = df.drop(index=[0, 1]).reset_index(drop=True)
    df_plot['Voltages'] = df_plot['Voltages'].astype(float)  # Ensure 'Voltages' is float

    # Plotting individual traces on the first subplot
    for i, column in enumerate(df.columns[1:]):
        transfection_group = int(df.iloc[0, i+1])  # Adjusting for 'Voltages' column
        color = colors[transfection_group]
        norm = df_plot[column]/df.iloc[1, i+1]
        axs[0].plot(df_plot['Voltages'], norm, 'x', ls = '-', color=color, alpha=0.3, label=f'Transfection {transfection_group}')
    # Simplifying the legend for the first subplot
    handles, labels = axs[0].get_legend_handles_labels()
    by_label = dict(zip([f'Transfection {i}' for i in colors.keys()], handles[:2]))  # Taking only two handles for simplification
    # axs[0].legend(by_label.values(), by_label.keys())
    axs[0].set_title('Individual Normalized Traces over Voltage, Grouped by Transfection')
    axs[0].set_ylabel('Normalized Current (I/Cm)')

    # Plotting group averages on the second subplot, correcting the error in group handling
    for transfection_value in colors.keys():
        # Grouping the dataframe based on transfection value
        group_columns = df.columns[1:][(groups == transfection_value).values]
        group_df = df_plot[group_columns]
        
        # print (group_df)
        
        # Averaging over all columns in the group
        mean_values = group_df.mean(axis=1)
        sem_values = stats.sem(group_df, axis = 1)
        ci_95 = 1.96 * sem_values
        
        # print(sem_values)
        axs[1].plot(df_plot['Voltages'], mean_values, '.', ls = '-', color=colors[transfection_value], label=f'Transfection {transfection_value}')
        axs[1].fill_between(df_plot['Voltages'], mean_values - ci_95, mean_values + ci_95, color = colors[transfection_value], alpha=0.3)
        
    axs[1].set_title('Normalized Data over Voltage, Grouped by Transfection (Averages)')
    axs[1].set_xlabel('Voltage')
    axs[1].set_ylabel('Normalized Current (I/Cm)')
    # axs[1].legend()

    plt.tight_layout()
    plt.show()

# plotIV('YangdongWang_24SpringRotationData/BatchExport/BatchIV_24303 - copy.csv')

def plottc(tc_file):
    df = pd.read_csv(tc_file)
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 16))
    colors = {1: 'blue', 2: 'red'}
    groups = df.iloc[0, 1:].astype(int)  # Transfection values, as integers
    df_plot = df.drop(index=[0, 1]).reset_index(drop=True)
    df_plot['Voltages'] = df_plot['Voltages'].astype(float)  # Ensure 'Voltages' is float

    # Plotting individual traces on the first subplot
    for i, column in enumerate(df.columns[1:]):
        transfection_group = int(df.iloc[0, i+1])  # Adjusting for 'Voltages' column
        # print(df.iloc[18, i+1])
        color = colors[transfection_group]
        df_plot[column] = df_plot[column]/df.iloc[18, i+1]
        axs[0].plot(df_plot['Voltages'], df_plot[column], 'x', ls = '-', color=color, alpha=0.3, label=f'Transfection {transfection_group}')
        
    # Simplifying the legend for the first subplot
    handles, labels = axs[0].get_legend_handles_labels()
    by_label = dict(zip([f'Transfection {i}' for i in colors.keys()], handles[:2]))  # Taking only two handles for simplification
    # axs[0].legend(by_label.values(), by_label.keys())
    axs[0].set_title('Individual Normalized Traces over Voltage, Grouped by Transfection')
    axs[0].set_ylabel('Normalized Current (I/Cm)')

    # Plotting group averages on the second subplot, correcting the error in group handling
    for transfection_value in colors.keys():
        # Grouping the dataframe based on transfection value
        group_columns = df.columns[1:][(groups == transfection_value).values]
        group_df = df_plot[group_columns]
        
        # print (group_df)
        
        # Averaging over all columns in the group
        mean_values = group_df.mean(axis=1)
        sem_values = stats.sem(group_df, axis = 1)
        ci_95 = 1.96 * sem_values
        
        # print(sem_values)
        axs[1].plot(df_plot['Voltages'], mean_values, '.', ls = '-', color=colors[transfection_value], label=f'Transfection {transfection_value}')
        axs[1].fill_between(df_plot['Voltages'], mean_values - ci_95, mean_values + ci_95, color = colors[transfection_value], alpha=0.3)
        
    axs[1].set_title('Normalized Data over Voltage, Grouped by Transfection (Averages)')
    axs[1].axhline(y=0.5, ls = ':',color='k')  # Horizontal line (x-axis)
    axs[1].set_xlabel('Voltage')
    axs[1].set_ylabel('Normalized Current (I/Cm)')
    # axs[1].legend()

    plt.tight_layout()
    plt.show()
# plottc('YangdongWang_24SpringRotationData/BatchExport/BatchTailCurrents_24303 - Copy.csv')

def plotSSI(SSI_file):
    df = pd.read_csv(SSI_file)
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 16))
    colors = {1: 'blue', 2: 'red'}
    groups = df.iloc[0, 1:].astype(int)  # Transfection values, as integers
    df_plot = df.drop(index=[0, 1]).reset_index(drop=True)
    df_plot['Voltages'] = df_plot['Voltages'].astype(float)  # Ensure 'Voltages' is float

    # Plotting individual traces on the first subplot
    for i, column in enumerate(df.columns[1:]):
        transfection_group = int(df.iloc[0, i+1])  # Adjusting for 'Voltages' column
        # print(df.iloc[1, i+1])
        color = colors[transfection_group]
        df_plot[column] = df_plot[column]/df.iloc[1, i+1]
        axs[0].plot(df_plot['Voltages'], df_plot[column], 'x', ls = '-', color=color, alpha=0.3, label=f'Transfection {transfection_group}')
        
    # Simplifying the legend for the first subplot
    handles, labels = axs[0].get_legend_handles_labels()
    by_label = dict(zip([f'Transfection {i}' for i in colors.keys()], handles[:2]))  # Taking only two handles for simplification
    # axs[0].legend(by_label.values(), by_label.keys())
    axs[0].set_title('Individual Normalized Traces over Voltage, Grouped by Transfection')
    axs[0].set_ylabel('Normalized Current (I/Cm)')

    # Plotting group averages on the second subplot, correcting the error in group handling
    for transfection_value in colors.keys():
        # Grouping the dataframe based on transfection value
        group_columns = df.columns[1:][(groups == transfection_value).values]
        group_df = df_plot[group_columns]
        
        # print (group_df)
        
        # Averaging over all columns in the group
        mean_values = group_df.mean(axis=1)
        sem_values = stats.sem(group_df, axis = 1)
        ci_95 = 1.96 * sem_values
        
        # print(sem_values)
        axs[1].plot(df_plot['Voltages'], mean_values, '.', ls = '-', color=colors[transfection_value], label=f'Transfection {transfection_value}')
        axs[1].fill_between(df_plot['Voltages'], mean_values - ci_95, mean_values + ci_95, color = colors[transfection_value], alpha=0.3)
        
    axs[1].set_title('Normalized Data over Voltage, Grouped by Transfection (Averages)')
    axs[1].axhline(y=0.5, ls = ':',color='k')  # Horizontal line (x-axis)
    axs[1].set_xlabel('Voltage')
    axs[1].set_ylabel('Normalized Current (I/Cm)')
    # axs[1].legend()

    plt.tight_layout()
    plt.show()
    
# plotSSI('YangdongWang_24SpringRotationData/BatchExport/BatchSSI_24303 - Copy.csv')
