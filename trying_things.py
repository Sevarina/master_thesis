def make_mask(data, direct, index):
        #make a mask to filter out everything that is useless
    try:
        mask = open_df(direct,"exclude")
    except:
        shape = (len(index),8)
        dummy_data = np.ones(shape = shape)
        columns = ["Loadcells","Accelerometer","Laser sensor",	"Crack area",	 "Opening angle",	"High speed camera", "Additional accelerometer vertical","Additional accelerometer horizontal"]
        mask = pd.DataFrame(data = dummy_data, index = index, columns = columns)
        
    mask = mask.astype(bool)

    #mask to latex
    excl_accl = mask[["Additional accelerometer vertical","Additional accelerometer horizontal"]]
    excl = mask.drop(["Opening angle","Crack area","Additional accelerometer vertical","Additional accelerometer horizontal"], axis = 1)
    excl_format = [ex_in_clude] * len(excl.columns)
    excl_accl_format = [ex_in_clude] * len(excl_accl.columns)
    
    excl.to_latex(direct + "\\tables\\exclude.tex",formatters = excl_format, escape = False,na_rep=" ")
    excl_accl.to_latex(direct + "\\tables\\exclude_accel.tex",formatters = excl_accl_format, escape = False,na_rep=" ")
    
    return mask