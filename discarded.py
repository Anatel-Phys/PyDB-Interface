#peut-être griser à la place de discard
discarded = ["Y. Wang2019_T_Haze"]

def pop_discarded(spectrum):
    discarded_list = []
    for key in spectrum.keys():
        if key in discarded:
            discarded_list.append(key)
    
    for key in discarded_list:
        print("Discarding " + key + "...") 
        spectrum.pop(key)

def split_discarded(spectrum):
    data = {}
    discarded_data = {}

    return data, discarded_data
    
    
        
        