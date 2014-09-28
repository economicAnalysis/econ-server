import fred
import datetime
import calendar
import matplotlib
import matplotlib.pyplot as plt
import pprint
import json
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)

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


    pce_avghr_series = [{'average_hour_value': avghr_yoy_d[date], \
                   'pce_value': pce_yoy_d[date], \
                   'date': date} \
                   for date in pce_dates[14:]]

    month_year_value = time.strftime("%m_%Y")
    year_value = time.strftime("%Y")
    month_value = time.strftime("%m").lstrip("0").replace(" 0", "")

    economic_series_for_date = {'month_year': month_year_value, 'pce_avghr': pce_avghr_series}

    # database economic_data
    db = client.economic_data
    # economic 
    document = db.economic_series_by_date.find_one({'month_year':month_year_value})
  
    # write_pce_avghr runs first and should create the document if the document
    # hasn't already been created and insert the document if the documents
    # hasn't already been inserted
    if not document or 'pce_avghr' not in document:
      db.economic_series_by_date.insert(economic_series_for_date)


    date_document = db.observation_dates.find_one()
    if not date_document:
      date_document = {
        year_value: {month_value: True}
      }
      db.observation_dates.insert(date_document) 
    elif year_value not in date_document:
      date_document[year_value] = {month_value: True}
      db.observation_dates.save(date_document)
    elif month_value not in date_document[year_value]:
      date_document[year_value][month_value] = True
      db.observation_dates.save(date_document)


def write_pce_govrt(pce_yoy_d,govrt_yoy_d,pce_dates):
    """code to call the matplotlib libraries and generate charts"""
    
 
    pce_government_rate_series = [{'govrt_rate_value': govrt_yoy_d[date], \
               'pce_value': pce_yoy_d[date], \
               'date': date} \
               for date in pce_dates[14:]]

    date_value = time.strftime("%m_%Y")

    # database economic_data
    db = client.economic_data
    # economic 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    if 'pce_government_rate' not in document:
      document['pce_government_rate'] = pce_government_rate_series 
      economic_series_by_date.save(document)
    
    
def write_avghr(avghr_yoy_d,navghr_yoy_d,pcedef_yoy_d,avghr_dates):
    """generates nominal versus deflated average hour data"""
 
    nominal_vs_deflated_avghr_series = [{'deflated_avghr_value': avghr_yoy_d[date], \
               'nominal_avghr_value': navghr_yoy_d[date], \
               'pce_deflator_value': pcedef_yoy_d[date], \
               'date': date} \
               for date in avghr_dates[14:]]

    date_value = time.strftime("%m_%Y")

    db = client.economic_data
    # get the economic_series_by_date collection
    # 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    #if 'deflated_vs_nominal_avghr' not in document:
    if 'deflated_vs_nominal_avghr' not in document:
      document['deflated_vs_nominal_avghr'] = nominal_vs_deflated_avghr_series 
      economic_series_by_date.save(document)


    

def write_dscrt(pcedef_yoy_d,govrt_d,plot_dates):
    """code to call the matplotlib libraries and generate charts"""
    
    pcedef_val = [pcedef_yoy_d[date] for date in plot_dates]
    govrt_val = [govrt_d[date] for date in plot_dates]
    x_axis = [datetime.datetime.strptime(date,"%Y-%m-%d") for date in plot_dates]

    federal_funds_vs_pce_deflator_series = [{'pce_deflator_value': pcedef_yoy_d[date], \
     'govrt_rate_value': govrt_d[date], \
     'date': date} \
     for date in plot_dates[14:]]

    date_value = time.strftime("%m_%Y")

    db = client.economic_data
    # get the economic_series_by_date collection
    # 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    #if 'deflated_vs_nominal_avghr' not in document:
    if 'federal_funds_vs_pce_deflator' not in document:
      document['federal_funds_vs_pce_deflator'] = federal_funds_vs_pce_deflator_series 
      economic_series_by_date.save(document)

def write_unemployment_rate(pce_yoy_d,unemployment_rate_d,pce_dates):
    """code to write the unemployment rate to the database"""
    
    unemployment_vs_pce_series = [{'pce_value': pce_yoy_d[date], \
     'unemployment_rate_value': unemployment_rate_d[date], \
     'date': date} \
     for date in pce_dates[14:]]

    date_value = time.strftime("%m_%Y")

    db = client.economic_data
    # get the economic_series_by_date collection
    # 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    #if 'deflated_vs_nominal_avghr' not in document:
    if 'unemployment_vs_pce' not in document:
      document['unemployment_vs_pce'] = unemployment_vs_pce_series 
      economic_series_by_date.save(document)        
  

def write_employment(pce_yoy_d,employment_yoy_d,pce_dates):
    """code to write the emploment versus pce series to the database"""
    
 
    employment_vs_pce_series = [{'pce_value': pce_yoy_d[date], \
     'employment_rate_value': employment_yoy_d[date], \
     'date': date} \
     for date in pce_dates[14:]]

    date_value = time.strftime("%m_%Y")

    db = client.economic_data
    # get the economic_series_by_date collection
    # 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    #if 'deflated_vs_nominal_avghr' not in document:
    if 'employment_vs_pce' not in document:
      document['employment_vs_pce'] = employment_vs_pce_series 
      economic_series_by_date.save(document)       


def write_domestic_debt(domestic_debt_yoy_d,treasury_10yr_d,domestic_debt_dates):
    """code to write the domestic debt versus 10YR treasury yield to the database"""
    
  
    domestic_debt_vs_treasury_series = [{'domestic_debt_value': domestic_debt_yoy_d[date], \
     'treasury_10yr_value': treasury_10yr_d[date], \
     'date': date} \
     for date in domestic_debt_dates[5:]]

    date_value = time.strftime("%m_%Y")

    db = client.economic_data
    # get the economic_series_by_date collection
    # 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    #if 'deflated_vs_nominal_avghr' not in document:
    if 'domestic_debt_vs_treasury' not in document:
      document['domestic_debt_vs_treasury'] = domestic_debt_vs_treasury_series 
      economic_series_by_date.save(document)   

    
def write_prime(domestic_debt_yoy_d,prime_d,domestic_debt_dates):
    """code to call the matplotlib libraries and generate charts"""
 
    domestic_debt_vs_prime_series = [{'domestic_debt_value': domestic_debt_yoy_d[date], \
     'prime_rate_value': prime_d[date], \
     'date': date} \
     for date in domestic_debt_dates[5:]]

    date_value = time.strftime("%m_%Y")

    db = client.economic_data
    # get the economic_series_by_date collection
    # 
    economic_series_by_date = db.economic_series_by_date
    document = economic_series_by_date.find_one({'month_year': date_value})
    #if 'deflated_vs_nominal_avghr' not in document:
    if 'domestic_debt_vs_prime' not in document:
      document['domestic_debt_vs_prime'] = domestic_debt_vs_prime_series 
      economic_series_by_date.save(document)   

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
    write_unemployment_rate(pce_yoy_d,unrate_d,pce_dates)
    write_employment(pce_yoy_d,emply_yoy_d,pce_dates)
    write_domestic_debt(dmdebt_yoy_d,trsy_10yr_d,dmdebt_dates)
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

if __name__ == "__main__":
  test()
