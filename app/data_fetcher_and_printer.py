import fred
import datetime
import calendar
import matplotlib
import matplotlib.pyplot as plt
import pprint
import json

###what we'll do is calculate all the lists and dictionaries once
###and then pass them to the relevant fucntions   

def make_dict(obs_list):
    return dict((obs['date'],float(obs['value'])) for obs in obs_list)

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.datetime(year,month,day)

def make_index(start_date, end_date,increment = 1):
    """parameters input in as a string in the format
    YYYY-MM-DD. make index returns a list of type datetime dates"""
    
    dates = datetime.datetime.strptime(start_date,"%Y-%m-%d")

    strp_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")

    date_index = []
    while dates <= strp_date:
        date_index.append(dates.strftime("%Y-%m-%d"))
        dates = add_months(dates,increment)
        
    return date_index

def make_avg(date, val_dict):
    """make average takes a string date and a
    dictionary of date:value pairs and returns
    the trailing 3 month average"""

    date_val = datetime.datetime.strptime(date,"%Y-%m-%d")
    mo_0 = add_months(date_val,-2).strftime("%Y-%m-%d")
    mo_1 = add_months(date_val,-1).strftime("%Y-%m-%d")
    return (val_dict[mo_0]+val_dict[mo_1]+val_dict[date])/3.0

def make_yoy_dict(dates, val_dict):
    """make yoy dict takes a string date and a dictionary
    of date:value pairs and returns the YoY change"""
    ##dates are in string format. The function converts dates
    ##to datetime type, subtracts 12 months, and then converts
    ##the date back to a string

    return dict((date,100*(val_dict[date]/\
                val_dict[add_months(datetime.datetime.strptime(date,"%Y-%m-%d"),-12).\
                strftime("%Y-%m-%d")]-1)) for date in dates)

	
def get_fred(id_str):
    """get_fred takes the FRED key for a series as a parameter e.g. 'PCE96' for real 
    consumer spending, and returns a list of dictionaries. There is a dictionary
    for each date. Dictionary keys are date, realtime_start, realtime_end, value""" 	
	
    fred_key1 = "observations"
    fred_key2 = "observation"
    return fred.observations(id_str)[fred_key1]


    
def write_pce_avghr(pce_yoy_d,avghr_yoy_d,pce_dates):
    """code to generate the series and """

    avghr_val = [avghr_yoy_d[date] for date in pce_dates[14:]]
    pce_val = [pce_yoy_d[date] for date in pce_dates[14:]]
    pce_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in pce_dates[14:]]

    fo = open('tmp.txt');
    fo.write(json.dumps(avghr_val));
    fo.write()


    avghr_line = ax.plot(pce_axis,avghr_val,color='r',lw=2,label="YoY change in Real Average Hourly Earnings")
    pce_line = ax.plot(pce_axis,pce_val,color='k',label="YoY change in Real PCE")
    ax.grid(axis="both")
    ax.legend(loc="upper center",bbox_to_anchor=(0.5,1.2))
    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("Real Hourly Earnings leading indicator of change in Real PCE",y=1.175)

    plt.show()

def make_pce_govrt(pce_yoy_d,govrt_yoy_d,pce_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    pce_val = [pce_yoy_d[date] for date in pce_dates[14:]]
    pce_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in pce_dates[14:]]
    govrt_val = [govrt_yoy_d[date] for date in pce_dates[14:]]

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax2 = ax1.twinx()
    ax2.invert_yaxis()
    ax2.set_ylim(3,-5)
    pce_line = ax1.plot(pce_axis,pce_val,color='k',label="YoY change in Real PCE")
    govrt_line = ax2.plot(pce_axis,govrt_val,color='r',lw=2,label="YoY change in Fed Funds Rate")
    
    ax1.grid(axis="both")
    ax1.legend(loc="upper center",bbox_to_anchor=(0.5,1.2))
    ax2.legend(loc="upper center",bbox_to_anchor=(0.5,1.12))
    
    box = ax1.get_position()
    ax1.set_position([box.x0,box.y0,box.width,box.height*0.8])
    box2 = ax2.get_position()
    ax2.set_position([box2.x0,box2.y0,box2.width,box2.height*0.8])
    plt.title("Fed Funds Rate leading indicator of change in Real PCE",y=1.175)

    plt.show()
    
def make_avghr(avghr_yoy_d,navghr_yoy_d,pcedef_yoy_d,avghr_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    davghr_val = [avghr_yoy_d[date] for date in avghr_dates[14:]]
    navghr_val = [navghr_yoy_d[date] for date in avghr_dates[14:]]
    pcedef_val = [pcedef_yoy_d[date] for date in avghr_dates[14:]]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in avghr_dates[14:]]

    fig = plt.figure()
    ax = plt.subplot(111)

    navghr_line = ax.plot(x_axis,navghr_val,color='b',lw=2,label="YoY change in Nominal Average Hourly Earnings")
    davghr_line = ax.plot(x_axis,davghr_val,color='r',lw=2,label="YoY change in Real Average Hourly Earnings")
    pce_line = ax.plot(x_axis,pcedef_val,color='k',label="YoY change in PCE Deflator")
    
    ax.grid(axis="both")
    ax.legend(loc="upper center",bbox_to_anchor=(0.5,1.275))
    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("How Inflation Effects Real Avg. Hourly Earnings",y=1.25)
    
    plt.show()    

def make_dscrt(pcedef_yoy_d,govrt_d,plot_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    pcedef_val = [pcedef_yoy_d[date] for date in plot_dates]
    govrt_val = [govrt_d[date] for date in plot_dates]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in plot_dates]

    fig = plt.figure()
    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()

    pcedef_line = ax1.plot(x_axis,pcedef_val,color='r',lw=2,label="YoY change in PCE deflator (3 month average)")
    govrt_line = ax2.plot(x_axis,govrt_val,color='k',lw=2,label="Federal Fund (Discount Rate prior to 2000)")
    
    ax1.grid(axis="both")
    ax1.legend(loc="upper center",bbox_to_anchor=(0.5,1.22))
    ax2.legend(loc="upper center",bbox_to_anchor=(0.5,1.12))
    box = ax1.get_position()
    ax1.set_position([box.x0,box.y0,box.width,box.height*0.8])
    ax2.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("Inflation Drives Interest Rates",y=1.25)

    plt.show()    


def make_unrate(pce_yoy_d,unrate_d,pce_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    pce_val = [pce_yoy_d[date] for date in pce_dates[14:]]
    unrate_val = [unrate_d[date] for date in pce_dates[14:]]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in pce_dates[14:]]
        
    fig = plt.figure()
    ax1 = plt.subplot(111)
    ax1.set_ylim(-6,10)
    ax2 = ax1.twinx()
    ax2.set_ylim(12,1)

    pcedef_line = ax1.plot(x_axis,pce_val,color='r',lw=2,label="YoY change in Real PCE (3 month average)")
    govrt_line = ax2.plot(x_axis,unrate_val,color='k',lw=2,label="Unemployment Rate (Inverted)")
    
    ax1.grid(axis="both")
    ax1.legend(loc="upper center",bbox_to_anchor=(0.5,1.22))
    ax2.legend(loc="upper center",bbox_to_anchor=(0.5,1.12))
    box = ax1.get_position()
    ax1.set_position([box.x0,box.y0,box.width,box.height*0.8])
    ax2.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("Change in Real PCE drives Unemployment Rate",y=1.25)

    plt.show()    


def make_emply(pce_yoy_d,emply_yoy_d,pce_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    pce_val = [pce_yoy_d[date] for date in pce_dates[14:]]
    emply_val = [emply_yoy_d[date] for date in pce_dates[14:]]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in pce_dates[14:]]
        
    fig = plt.figure()
    ax1 = plt.subplot(111)
    ax1.set_ylim(-4,10)
    ax2 = ax1.twinx()
    ax2.set_ylim(-6,10)

    pcedef_line = ax1.plot(x_axis,pce_val,color='r',lw=2,label="YoY change in Real PCE (3 month average)")
    govrt_line = ax2.plot(x_axis,emply_val,color='k',lw=2,label="YoY change in Employment")
    
    ax1.grid(axis="both")
    ax1.legend(loc="upper center",bbox_to_anchor=(0.5,1.22))
    ax2.legend(loc="upper center",bbox_to_anchor=(0.5,1.12))
    box = ax1.get_position()
    ax1.set_position([box.x0,box.y0,box.width,box.height*0.8])
    ax2.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("Change in Real PCE drives Employment",y=1.25)

    plt.show()    

def make_dmdebt(dmdebt_yoy_d,trsy_10yr_d,dmdebt_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    dmdebt_val = [dmdebt_yoy_d[date] for date in dmdebt_dates[5:]]
    trsy_val = [trsy_10yr_d[date] for date in dmdebt_dates[5:]]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in dmdebt_dates[5:]]


    fig = plt.figure()
    ax1 = plt.subplot(111)
    
    dmdebt_line = ax1.plot(x_axis,dmdebt_val,color='r',lw=2,label="YoY change in Total Nonfinancial Domestic Debt")
    trsy_10yr_line = ax1.plot(x_axis,trsy_val,color='k',lw=2,label="10 Year Treasury Yield")
    
    ax1.grid(axis="both")
    ax1.legend(loc="upper center",bbox_to_anchor=(0.5,1.22))
    box = ax1.get_position()
    ax1.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("Increase in Total Domestic Nonfinancial Debt Drives 10 Year Treasury Yield",y=1.25)

    plt.show()    

    
def make_prime(dmdebt_yoy_d,prime_d,dmdebt_dates):
    """code to call the matplotlib libraries and generate charts"""
 
    dmdebt_val = [dmdebt_yoy_d[date] for date in dmdebt_dates[5:]]
    prime_val = [prime_d[date] for date in dmdebt_dates[5:]]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in dmdebt_dates[5:]]

    fig = plt.figure()
    ax1 = plt.subplot(111)
    
    dmdebt_line = ax1.plot(x_axis,dmdebt_val,color='r',lw=2,label="YoY change in Total Nonfinancial Domestic Debt")
    prime_line = ax1.plot(x_axis,prime_val,color='k',lw=2,label="Prime Rate")
    
    ax1.grid(axis="both")
    ax1.legend(loc="upper center",bbox_to_anchor=(0.5,1.22))
    box = ax1.get_position()
    ax1.set_position([box.x0,box.y0,box.width,box.height*0.8])
    plt.title("Increase in Total Domestic Nonfinancial Debt Drives Prime Rate",y=1.25)

    plt.show()    

def main_routine():
    fred.key('f412b494756f8cbd24c8310e01d14630')
        
    ##########data for real PCE vs average hourly earnings ##########

    ##get_fred returns a list of dictionaries
    pce_list = get_fred("PCEC96")
    avghr_list = get_fred("AHETPI")
    pcedef_list = get_fred("PCEPI")
        
    ##get the index for the last date in the series
    ##pce_list[-1] is the final dictionary in the series
    end_pce = pce_list[-1]
    ##retrieve the date value of the dictionary
    enddate_pce = end_pce['date']
    
    start_date_pce = "1999-01-01"
    pce_dates = make_index(start_date_pce,enddate_pce)

    ##find the position of the 1995-1-1 entry (entries prior to 1995-1-1 are zero)
    start_index = (i for i in range(len(pce_list)) if (pce_list[i])['date'] == start_date_pce).next()

    ##create a dictionary of PCE date:values
    ##Real PCE values start as of 1995-1-1, as per start_index
    pce_d = make_dict(pce_list[start_index:])

    ##calculate the trailing 3 month averages, start from index 2 (need 3 values to make a 3 month average) 
    pce_3mo_d = dict((date,make_avg(date,pce_d)) for date in pce_dates[2:])

    ##calculate the yoy change
    pce_yoy_d = make_yoy_dict(pce_dates[14:],pce_3mo_d)

    ########## avg hourly earnings #########
    ##process avg hourly earnings
    start_avghr, end_avghr = avghr_list[0],avghr_list[-1]
    start_date_avghr = start_avghr['date']
    enddate_avghr = end_avghr['date']
    avghr_dates = make_index(start_date_avghr,enddate_avghr)
    
    ##the pce deflator series is used in the govt rate vs. pce deflator. I'm more certain that the
    ##fedfunds rate will already be available
    fedfund_list = get_fred("FEDFUNDS")
    discrt_list = get_fred("MDISCRT")
    pcedef_govrt_end = (fedfund_list[-1])['date']

    ##these are the dates to be used for the plotting
    ##start from the max of the 14th entry of the pce deflator series
    ##or the discrt start. We need at least 14 data points to
    ##to generate the 3 month average and the YoY calculation
    pcedef_start = datetime.datetime.strptime((pcedef_list[14])['date'],"%Y-%m-%d")
    discrt_start = datetime.datetime.strptime((discrt_list[0])['date'],"%Y-%m-%d")
    pcedef_govrt_start = max(pcedef_start,discrt_start).strftime("%Y-%m-%d")

    ##generate the dates for the pce deflator series
    pcedef_govrt_dates = make_index(pcedef_govrt_start,pcedef_govrt_end)
        
    ##create a dictionary for avg hr date:value
    avghr_d = make_dict(avghr_list)
        
    ##create a dictionary for pce deflator date:value
    pcedef_d = make_dict(pcedef_list)
    ##if current month for pce deflator hasn't be reported, calculate an estimated value
    if pcedef_govrt_end not in pcedef_d or avghr_dates[-1] not in pcedef_d:
        prior1 = (pcedef_list[-1])['date']
        prior2 = add_months(datetime.datetime.strptime((pcedef_list[-1])['date'],"%Y-%m-%d"),-1).strftime("%Y-%m-%d")
        nextMonth = add_months(datetime.datetime.strptime((pcedef_list[-1])['date'],"%Y-%m-%d"),1).strftime("%Y-%m-%d")
        pcedef_d[nextMonth] = 2*pcedef_d[prior1] - pcedef_d[prior2]
        
    ##create the deflated average hourly earnings
    def_avghr_d = dict((key,100*avghr_d[key]/pcedef_d[key]) for key in avghr_d)            
  
    ##create the trailing 3 months 
    avghr_3mo_d = dict((date,make_avg(date,def_avghr_d)) for date in avghr_dates[2:])
    
    ##calculate avg hourly earnings yoy change
    avghr_yoy_d = make_yoy_dict(avghr_dates[14:],avghr_3mo_d)
 
    ##########data for real PCE vs dicount rate/fed funds rates ##########
    
    ##get the federal funds rate data
    ##switch from discount rate to federal funds rate as of 1-1-2000
    switch_date = datetime.datetime(2000,01,01)
    govrt_d = dict((each['date'],float(each['value'])) for each in fedfund_list if datetime.datetime.strptime(each['date'],"%Y-%m-%d")>= switch_date )

    for obs in discrt_list:
        if datetime.datetime.strptime(obs['date'],"%Y-%m-%d") < switch_date:
            govrt_d[obs['date']] = float(obs['value'])

    ##create an index of dates. Starts from index 12 since the calculation looks back 12 months
    govrt_yoy_dates = make_index((discrt_list[0])['date'],(fedfund_list[-1])['date'])[12:]
   
    ##make dictionary of the YoY change
    govrt_yoy_d = dict((date,govrt_d[date] - govrt_d[add_months(datetime.datetime.strptime(date,"%Y-%m-%d"),-12).strftime("%Y-%m-%d")]) for date in govrt_yoy_dates)
    
    ##########data for the effect of inflation on real average hourly wages #########        
    
    ##calculate the pce deflator trailing 3 month average
    if datetime.datetime.strptime(pcedef_govrt_dates[-1],"%Y-%m-%d") > datetime.datetime.strptime((pcedef_list[-1])['date'],"%Y-%m-%d"):
        suffix = [pcedef_govrt_dates[-1]]
    elif datetime.datetime.strptime(avghr_dates[-1],"%Y-%m-%d") > datetime.datetime.strptime((pcedef_list[-1])['date'],"%Y-%m-%d"):
        suffix = [avghr_dates[-1]]
    else:
        suffix = []
    pcedef_dates = [obs['date'] for obs in pcedef_list] + suffix
    pcedef_3mo_d = dict((date,make_avg(date,pcedef_d)) for date in pcedef_dates[2:])
    
    ##calculate the pce deflator YoY
    pcedef_yoy_d = make_yoy_dict(pcedef_dates[14:],pcedef_3mo_d)
        
    ##create the trailing 3 months (nominal)
    navghr_3mo_d = dict((date,make_avg(date,avghr_d)) for date in avghr_dates[2:])

    ##calculate avg hourly earnings (nominal) yoy change
    navghr_yoy_d = make_yoy_dict(avghr_dates[14:],navghr_3mo_d)

    ###########data for discount rate/fed funds rate vs pce deflator ##########
    ###########certain date calculations on line 401 ##########
    ###########all calculations done above as other series use same data ###########
    
    ##########data for the unemployment rate ##########    
    unrate_list = get_fred("UNRATE")

    ##make dictionary from unemployment rate observations
    unrate_d = make_dict(unrate_list)

    ##########data for the employment ##########
    emply_list = get_fred("CE16OV")

    ##get employment dates
    emply_dates = [obs['date'] for obs in emply_list]
    
    ##make dictionary from unemployment rate observations
    emply_d = make_dict(emply_list)

    ##calculate the 3 mo average
    emply_3mo_d = dict((date,make_avg(date,emply_d)) for date in emply_dates[2:])

    ##calculate the YoY value
    emply_yoy_d = make_yoy_dict(emply_dates[14:], emply_3mo_d) 

    ##########data for domestic debt and 10 year treasury #########
    dmdebt_list = get_fred("TCMDODNS")
    trsy_10yr_list = get_fred("GS10")

    dmdebt_start = '1952-01-01'
    start_index = (dmdebt_list.index(obs) for obs in dmdebt_list if obs['date'] == dmdebt_start).next()
    
    dmdebt_dates = make_index(dmdebt_start,(dmdebt_list[-1])['date'],3)

    ##make dictionary
    dmdebt_d = dict((obs['date'],float(obs['value'])) for obs in dmdebt_list[start_index:])

    ##calculate YoY change
    dmdebt_yoy_d = dict((date,100*(dmdebt_d[date]/ \
                        dmdebt_d[add_months(datetime.datetime.strptime(date,"%Y-%m-%d"),-12).strftime("%Y-%m-%d")]-1)) for date in dmdebt_dates[4:])

    ##make dictionary
    trsy_10yr_d = dict((obs['date'],float(obs['value'])) for obs in trsy_10yr_list)

    ########## date for domestic debt and prime rate##########
    prime_list = get_fred("MPRIME")

    ##make dictionary
    prime_d = dict((obs['date'],float(obs['value'])) for obs in prime_list)

        
    write_pce_avghr(pce_yoy_d,avghr_yoy_d,pce_dates)
    write_pce_govrt(pce_yoy_d,govrt_yoy_d,pce_dates)
    write_avghr(avghr_yoy_d,navghr_yoy_d,pcedef_yoy_d,avghr_dates)
    write_dscrt(pcedef_yoy_d,govrt_d,pcedef_govrt_dates)        
    write_unrate(pce_yoy_d,unrate_d,pce_dates)
    write_emply(pce_yoy_d,emply_yoy_d,pce_dates)
    write_dmdebt(dmdebt_yoy_d,trsy_10yr_d,dmdebt_dates)
    write_prime(dmdebt_yoy_d,prime_d,dmdebt_dates)

def test1():
    fred.key('f412b494756f8cbd24c8310e01d14630')
        
    pp = pprint.PrettyPrinter(indent=2)
    ##########data for real PCE vs average hourly earnings ##########

    ##get_fred returns a list of dictionaries
    pce_list = get_fred("PCEC96")

    pp.pprint(pce_list)

def test():
    main_routine()

__name__ == "__main__":
  test()
