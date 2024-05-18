from flask import Flask, render_template,url_for,request,jsonify
import pandas as pd
import json
import numpy as np
import pickle
from datetime import datetime as dt
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
pf=pd.read_csv("Merged_One.csv")


def filter_dataframe(df, district=None, unit=None, crimetype=None, month=None, year=None):
    filtered_df = df.copy()
    if unit:
        filtered_df = filtered_df[filtered_df['UnitName'] == unit]
        district=None
    if district:
        filtered_df = filtered_df[filtered_df['District_Name'] == district]
    if crimetype:
        crity=df['CrimeGroup_Name'].value_counts().head().index
        if(crimetype=='Others'):
            ss=~filtered_df['CrimeGroup_Name'].isin(crity)
            filtered_df=filtered_df[ss]
        else:
            filtered_df = filtered_df[filtered_df['CrimeGroup_Name'] == crimetype]
    if year:
        year=int(year)
        filtered_df = filtered_df[filtered_df['Year'] == year]
        month=None   
    if month:
        month=int(month)
        filtered_df = filtered_df[filtered_df['Month'] == month]
    filtered_df=filtered_df.reset_index()
    filtered_df['Offence_From_Date']=pd.to_datetime(filtered_df['Offence_From_Date'])
    filtered_df['Offence_Date']=filtered_df['Offence_From_Date'].dt.date
    filtered_df['Offence_Time']=filtered_df['Offence_From_Date'].dt.time
    names=filtered_df.District_Name
    lati=filtered_df.latitude
    longi=filtered_df.longitude
    crime=filtered_df.CrimeGroup_Name
    date=filtered_df.Offence_Date
    time=filtered_df.Offence_Time
    village=filtered_df.Village_Area_Name
    crr1=filtered_df['CrimeGroup_Name'].iloc[:]
    # print('crr',crr)
    # print('crr unique',crr.unique())
    crr=crr1.value_counts().head().index.to_list()
    crr.append('Others')
    crime_count=crr1.value_counts().head().values.tolist()
    ll=sum(crr1.value_counts().values)-sum(crime_count)
    crime_count.append(ll)
    map=list()
    lis=list()
    len1=2000
    if(len(crr1)<len1):
        len1=len(crr1)
    for i in range(len1):
        dic=dict() 
        dic['name']=names.iloc[i]
        dic['coordinates']=[lati.iloc[i],longi.iloc[i]] 
        dic['crime']=1
        lis.append([crime.iloc[i],time.iloc[i],date.iloc[i],village.iloc[i]])
        map.append(dic)
    # print("Qqqaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    # print(lis)
    # print("Qqqaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    # print(filtered_df[['District_Name','UnitName','Village_Area_Name','Offence_Date','Offence_Time']].iloc[:250,:])
    ss=len(map)
    # print(map,lis,ss,crr)
    # print('aa',crr)
    print(crime_count)
    return map,lis,ss,crr,crime_count
 

app=Flask(__name__)

# print(filter_dataframe(pf)[0])



 
districts = pf['District_Name'].unique()
# occupation=pf['Profession'].unique()

# Ask user for district input
dir=list(districts)
# occup=list(occupation)

profession=pf["Profession_x"].unique()
prof=list(profession)

cast=pf['Caste_x'].unique()
cast=list(cast)

occupation=pf['Occupation'].unique()
occup=list(occupation)




def crimeTypeList(df, district=None, unit=None):
    filtered_df = df.copy()
    if unit:
        filtered_df = filtered_df[filtered_df['UnitName'] == unit]
        district=None
    if district:
        filtered_df = filtered_df[filtered_df['District_Name'] == district]

    a=filtered_df['CrimeGroup_Name'].iloc[:250]
    # print('unique',a.unique())
    a=a.value_counts().head().index.to_list()
    a.append('Others')
    # print('a',a)
    return a
 



@app.route('/')
def combined_route():
#     data = [
#     {'name': 'Bagalkot', 'coordinates': [15.8929852, 75.6571751], 'crime': 1},
#     {'name': 'Bagalkot', 'coordinates': [15.9111875, 75.5029201], 'crime': 1}
# ]

# # Convert data to GeoDataFrame
#     geometry = [Point(xy) for xy in [(d['coordinates'][1], d['coordinates'][0]) for d in data]]
#     crimes = [d['crime'] for d in data]
#     gdf = gpd.GeoDataFrame({'crime': crimes}, geometry=geometry)

    all = filter_dataframe(pf)
    totalCrimes = all[2]
    second_route_data = all[0]
    mapLatLong = all[0] # Example data, replace with your actual data 
    # print(totalCrimes) 
    # print("**************************************************************************************************************")
    # # print(mapLatLong)
    # print(all[4])

    # Convert int64 objects to Python int before serialization
    crime_count = [int(count) for count in all[4]]

    # Convert numpy int64 objects to Python int before serialization
    crime_count = [int(count) if isinstance(count, np.int64) else count for count in all[4]]

    # Now you can serialize crime_count to JSON
    crime_count_json = json.dumps(crime_count)

    crime=[[count] for count in all[3]]
    crime = [int(count) if isinstance(count, np.int64) else count for count in all[3]]

    
    crime=json.dumps(crime)


    return render_template("index.html", districts=dir, crime=all[3], crimeCount=sum(all[4]), crime_list=all[1],crime5=all[4], data=second_route_data,points=mapLatLong,chart=crime_count_json,crimeBar=crime)

 
s={}
# Iter
# 
# te over unique districts
for district in districts:
    # Group by district and count occurrences of UnitName
    unit_counts = pf[pf['District_Name'] == district]['UnitName'].value_counts().index
    li=list(unit_counts)
    ui={district:li}
    s.update(ui)
 

@app.route('/process_data', methods=['POST']) 
def process_data():
    selected_option = request.json['selectedOption'] 
    # Simulate pagination: return only a portion of the data
    page_number = request.args.get('page', default=1, type=int)
    page_size = 100000  # Adjust page size as needed
    start_index = (page_number - 1) * page_size 
    end_index = start_index + page_size
    data = s.get(selected_option, [])
    
    data_subset = data[start_index:end_index]
    return jsonify(data_subset) 


@app.route('/process_crimeType_data1', methods=['POST'])
def process_crimeType_data1():
    selected_option = request.json['selectedOption'] 
    crime_types =  crimeTypeList(pf, selected_option)
    # print(selected_option)
    # print(crime_types)
    return jsonify(crime_types) 

@app.route('/process_crimeType_data2', methods=['POST'])
def process_crimeType_data2():
    selected_option = request.json['selectedOption'] 
    # print(selected_option)
    # print(" **************************************************************************************")
 
    district,place=selected_option.split(",")
    # print(district,place)
    crime_types = crimeTypeList(pf, district,place)
    # print(crime_types)
    # print(selected_option)
    return jsonify(crime_types) 
 
 
 
@app.route('/', methods=['POST'])
def crimeType():
    district_name = request.form['district']
    place_name = request.form['places']
    place=''
    places=''
    crime_types=request.form['crimeType']
    if(district_name==""):
        district_name=None

    if(crime_types==""):
        crime_types=None

    if(place_name==""):
        place=None
    else:
        places=place_name.split(',')
        place=places[1]
    # print("District:", district_name)
    # print("Places:", place)
    # print("Crime Types:", crime_types)
    print("***************************************************************************************")
    all=filter_dataframe(pf,district_name,place,crime_types)

    # print(all)    

    # Convert int64 objects to Python int before serialization
    crime_count = [int(count) for count in all[4]]

    # Convert numpy int64 objects to Python int before serialization
    crime_count = [int(count) if isinstance(count, np.int64) else count for count in all[4]]

    # Now you can serialize crime_count to JSON 
    crime_count_json = json.dumps(crime_count)

    print("!!!!!!!!!!!!!!!!!!!!!!!",all[3],"!!!!!!!!!!!!!!!!!!!")


    crime=[[count] for count in all[3]]
    crime = [int(count) if isinstance(count, np.int64) else count for count in all[3]]

    crime=json.dumps(crime)
    print(crime)
    
    return render_template("index.html", districts=dir,crime=all[3],crimeBar=crime, crimeCount=sum(all[4]),crime_list=all[1],crime5=all[4],points=all[0],chart=crime_count_json)

import pandas as pd 
import numpy as np
import json
from flask import Flask, render_template

@app.route('/AccusedAnalysis')
def accusedAnalysis():
    ss = pf.loc[:,['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month','AccusedName', 'Person_Name', 'age_x',
            'Caste_x', 'Profession_x', 'Sex_x', 'PresentCity_x', 'PresentState_x',
            'Person_No', 'Arr_ID_x', 'agegrp','crime_no']]
    ss = ss.reset_index(drop=True)

    # Get the top 20 caste counts and convert them to a list
    caste = ss['Caste_x'].value_counts().iloc[:10]
    caste_counts=caste.values.tolist()
    caste_name=caste.index.to_list()
    print(caste_counts)
    print(caste_name)
    casteCount=[int(count) for count in caste_counts]
    casteCount = [int(count) if isinstance(count, np.int64) else count for count in caste_counts]
    # Now you can serialize crime_count to JSON 
    caste_count_json = json.dumps(casteCount)
    casteName=[[count] for count in caste_name] 
    casteName = [int(count) if isinstance(count, np.int64) else count for count in caste_name]


    age=ss.agegrp.value_counts().iloc[:10] 
    ageidx=age.index.tolist()
    ageval=age.values.tolist()
    print(ageidx,ageval)
    age_idx=[count for count in ageidx]
    age_idx = [count if isinstance(count, np.int64) else count for count in ageidx]
    age_idx_json=json.dumps(age_idx)
    age_val=[count for count in ageval]
    age_val=[count if isinstance(count, np.int64) else count for count in ageval]
    age_val_json=json.dumps(age_val)


    profession=ss.Profession_x.value_counts().iloc[:10]
    professionidx=profession.index.tolist()
    professionval=profession.values.tolist()
    print(professionidx,professionval)
    profession_idx=[count for count in professionidx]
    profession_idx = [count if isinstance(count, np.int64) else count for count in professionidx]
    # profession_idx_json=json.dumps(profession_idx)
    profession_val=[int(count) for count in professionval]
    profession_val=[int(count) if isinstance(count, np.int64) else count for count in professionval]
    profession_val_json=json.dumps(profession_val)


    # Pass the points variable to the HTML template
    return render_template("accusedAnalysis.html",casteCount=caste_count_json,casteName=casteName,ageIdx=age_idx_json,ageVal=age_val_json,professionVal=profession_val_json,professionIdx=profession_idx,districts=dir)
 

@app.route('/AccusedAnalysis', methods=['POST'])
def accusedAnalysis1():
    ss = pf.loc[:,['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month','AccusedName', 'Person_Name', 'age_x',
            'Caste_x', 'Profession_x', 'Sex_x', 'PresentCity_x', 'PresentState_x',
            'Person_No', 'Arr_ID_x', 'agegrp','crime_no']]
    dt = request.form['district']
    place = request.form['places']
    if(place==""):
        place=None
    else:
        place=place.split(',')[1]
    def function(df,dt=None,unit=None):
        if dt:
            df=df[df['District_Name']==dt]
        if(unit):
            df=df[df['UnitName']==unit]
        return df
    ss=function(ss,dt,place)
    print(ss)
    # Get the top 20 caste counts and convert them to a list
    caste = ss['Caste_x'].value_counts().iloc[:10]
    caste_counts=caste.values.tolist()
    caste_name=caste.index.to_list()
    # print(caste_counts)
    # print(caste_name)
    casteCount=[int(count) for count in caste_counts]
    casteCount = [int(count) if isinstance(count, np.int64) else count for count in caste_counts]
    # Now you can serialize crime_count to JSON 
    caste_count_json = json.dumps(casteCount)
    casteName=[[count] for count in caste_name] 
    casteName = [int(count) if isinstance(count, np.int64) else count for count in caste_name]


    age=ss.agegrp.value_counts().iloc[:10] 
    ageidx=age.index.tolist()
    ageval=age.values.tolist()
    # print(ageidx,ageval)
    age_idx=[count for count in ageidx]
    age_idx = [count if isinstance(count, np.int64) else count for count in ageidx]
    age_idx_json=json.dumps(age_idx)
    age_val=[count for count in ageval]
    age_val=[count if isinstance(count, np.int64) else count for count in ageval]
    age_val_json=json.dumps(age_val)


    profession=ss.Profession_x.value_counts().iloc[:10]
    professionidx=profession.index.tolist()
    professionval=profession.values.tolist()
    # print(professionidx,professionval)
    profession_idx=[count for count in professionidx]
    profession_idx = [count if isinstance(count, np.int64) else count for count in professionidx]
    # profession_idx_json=json.dumps(profession_idx)
    profession_val=[int(count) for count in professionval]
    profession_val=[int(count) if isinstance(count, np.int64) else count for count in professionval]
    profession_val_json=json.dumps(profession_val)


    # Pass the points variable to the HTML template
    return render_template("accusedAnalysis.html",casteCount=caste_count_json,casteName=casteName,ageIdx=age_idx_json,ageVal=age_val_json,professionVal=profession_val_json,professionIdx=profession_idx,districts=dir)
 


@app.route("/vitcimAnalysis")
def victimAnalysis():
    ls=pf[['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'VictimName']]
    sex_distribution = pf['Sex'].value_counts()
    print("***************")
    print(sex_distribution)
    print("******************")



    sexval=sex_distribution.values.tolist() 
    sexidx=sex_distribution.index.to_list() 
 
    sex_val=[int(count) for count in sexval]
    sex_val = [int(count) if isinstance(count, np.int64) else count for count in sexval]
    # Now you can serialize crime_count to JSON 
    sex_val_json = json.dumps(sex_val)

    sex_idx=[[count] for count in sexidx] 
    sex_idx = [int(count) if isinstance(count, np.int64) else count for count in sexidx]

    print(sex_val) 
    print(sex_idx)


    prof=pf.Profession_x.value_counts().iloc[:10]

    profval=prof.values.tolist() 
    profidx=prof.index.to_list() 
 
    prof_val=[int(count) for count in profval]
    prof_val = [int(count) if isinstance(count, np.int64) else count for count in profval]
    # Now you can serialize crime_count to JSON 
    prof_val_json = json.dumps(prof_val)

    prof_idx=[[count] for count in profidx] 
    prof_idx = [int(count) if isinstance(count, np.int64) else count for count in profidx]




    cas=pf.Caste.value_counts().iloc[:10]

    casval=cas.values.tolist() 
    casidx=cas.index.to_list() 
 
    cas_val=[int(count) for count in casval]
    cas_val = [int(count) if isinstance(count, np.int64) else count for count in casval]
    # Now you can serialize crime_count to JSON 
    cas_val_json = json.dumps(cas_val)

    cas_idx=[[count] for count in casidx] 
    cas_idx = [int(count) if isinstance(count, np.int64) else count for count in casidx]



    unitname=pf.UnitName.value_counts().iloc[:10]
    
    unitval=unitname.values.tolist() 
    unitidx=unitname.index.tolist()
 
    unit_val=[int(count) for count in unitval]
    unit_val = [int(count) if isinstance(count, np.int64) else count for count in unitval]
    # Now you can serialize crime_count to JSON 
    unit_val_json = json.dumps(unit_val)

    unit_idx=[[count] for count in unitidx] 
    unit_idx = [int(count) if isinstance(count, np.int64) else count for count in unitidx]

    print(unit_idx)
    print(unit_val)



    dist=pf.District_Name.value_counts().iloc[:10]
    distval=dist.values.tolist() 
    distidx=dist.index.tolist()
 
    dist_val=[int(count) for count in distval]
    dist_val = [int(count) if isinstance(count, np.int64) else count for count in distval]
    # Now you can serialize crime_count to JSON 
    dist_val_json = json.dumps(dist_val)

    dist_idx=[[count] for count in distidx] 
    dist_idx = [int(count) if isinstance(count, np.int64) else count for count in distidx]

    print(dist_idx)
    print(dist_val)



 

    data=pf
    data['Crime_Count'] = data.groupby('District_Name')['FIRNo'].transform('count')
    data['Average_Severity'] = data.groupby('District_Name')['Arrested Count\tNo.'].transform('mean')
    high_risk_threshold = np.percentile(data['Crime_Count'], 50)
    print(high_risk_threshold)
    data['High_Risk_Area'] = (data['Crime_Count'] >= high_risk_threshold).astype(int)


    highrisk = data[data['High_Risk_Area']==1]
    highrisk=highrisk.drop_duplicates(subset=['Crime_Count','District_Name','UnitName'])
    # print(highrisk.loc[:,['latitude']])
    # print('*'*100)
    print(highrisk.columns)
    lati=highrisk.latitude.tolist()
    longi=highrisk.longitude.tolist()
    name=highrisk.Village_Area_Name.tolist()
    print('*'*100)
    print(name)
    ls=[]
    for i in range(len(lati)):
        dic=dict() 
        dic['coordinates']=[lati[i],longi[i]] 
        dic['crime']=1
        dic['name']=name[i]




        # a=lll.iloc[i,0]
        # b=lll.iloc[i,1]
        ls.append(dic)
    print("*******************************************************************************")
    print(ls)

    points=ls
    print(points)


    print("*******************************************************************************")
  


 
    return render_template("victimAnalysis.html",sexVal=sex_val_json,sexIdx=sex_idx,profVal=prof_val_json,profIdx=prof_idx,casVal=cas_val_json,casIdx=cas_idx,unitVal=unit_val_json,unitIdx=unit_idx,distVal=dist_val_json,distIdx=dist_idx,points=points,districts=dir)

 

@app.route("/vitcimAnalysis",methods=['POST'])
def victimAnalysis1():
    ls=pf[['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'VictimName', 'age_y', 'Caste_y','Profession_y', 'Sex_y', 'PresentCity_y', 'PresentState_y','crime_no','PersonType', 'InjuryType', 'Arr_ID_y', 'Victim_ID']]
    ls=ls.drop_duplicates()
    sex_distribution = ls['Sex_y'].value_counts()
    print("***************")
    print(sex_distribution)
    print("******************") 

    district = request.form['district']
    place = request.form['places']
    if(not place==""):
        place=place.split(',')[1]
    def function(df,dt=None,unit=None):
        if dt:
            df=df[df['District_Name']==dt]
        if(unit):
            df=df[df['UnitName']==unit]
        return df
    

    ls=function(ls,district,place)



    sexval=sex_distribution.values.tolist() 
    sexidx=sex_distribution.index.to_list() 
 
    sex_val=[int(count) for count in sexval]
    sex_val = [int(count) if isinstance(count, np.int64) else count for count in sexval]
    # Now you can serialize crime_count to JSON 
    sex_val_json = json.dumps(sex_val)

    sex_idx=[[count] for count in sexidx] 
    sex_idx = [int(count) if isinstance(count, np.int64) else count for count in sexidx]

    print(sex_val) 
    print(sex_idx)


    prof=ls.Profession_y.value_counts().iloc[:10]

    profval=prof.values.tolist() 
    profidx=prof.index.to_list() 
 
    prof_val=[int(count) for count in profval]
    prof_val = [int(count) if isinstance(count, np.int64) else count for count in profval]
    # Now you can serialize crime_count to JSON 
    prof_val_json = json.dumps(prof_val)

    prof_idx=[[count] for count in profidx] 
    prof_idx = [int(count) if isinstance(count, np.int64) else count for count in profidx]




    cas=ls.Caste_y.value_counts().iloc[:10]

    casval=cas.values.tolist() 
    casidx=cas.index.to_list() 
 
    cas_val=[int(count) for count in casval]
    cas_val = [int(count) if isinstance(count, np.int64) else count for count in casval]
    # Now you can serialize crime_count to JSON 
    cas_val_json = json.dumps(cas_val)

    cas_idx=[[count] for count in casidx] 
    cas_idx = [int(count) if isinstance(count, np.int64) else count for count in casidx]



    unitname=ls.UnitName.value_counts().iloc[:10]
    
    unitval=unitname.values.tolist() 
    unitidx=unitname.index.tolist()
 
    unit_val=[int(count) for count in unitval]
    unit_val = [int(count) if isinstance(count, np.int64) else count for count in unitval]
    # Now you can serialize crime_count to JSON 
    unit_val_json = json.dumps(unit_val)

    unit_idx=[[count] for count in unitidx] 
    unit_idx = [int(count) if isinstance(count, np.int64) else count for count in unitidx]

    print(unit_idx)
    print(unit_val)



    dist=ls.District_Name.value_counts().iloc[:10]
    distval=dist.values.tolist() 
    distidx=dist.index.tolist()
 
    dist_val=[int(count) for count in distval]
    dist_val = [int(count) if isinstance(count, np.int64) else count for count in distval]
    # Now you can serialize crime_count to JSON 
    dist_val_json = json.dumps(dist_val)

    dist_idx=[[count] for count in distidx] 
    dist_idx = [int(count) if isinstance(count, np.int64) else count for count in distidx]

    print(dist_idx)
    print(dist_val)



 

    data=pf
    data['Crime_Count'] = data.groupby('District_Name')['FIRNo'].transform('count')
    data['Average_Severity'] = data.groupby('District_Name')['Arrested Count\tNo.'].transform('mean')
    high_risk_threshold = np.percentile(data['Crime_Count'], 50)
    print(high_risk_threshold)
    data['High_Risk_Area'] = (data['Crime_Count'] >= high_risk_threshold).astype(int)


    highrisk = data[data['High_Risk_Area']==1]
    highrisk=highrisk.drop_duplicates(subset=['Crime_Count','District_Name','UnitName'])
    # print(highrisk.loc[:,['latitude']])
    # print('*'*100)
    print(highrisk.columns)
    lati=highrisk.latitude.tolist()
    longi=highrisk.longitude.tolist()
    name=highrisk.Village_Area_Name.tolist()
    print('*'*100)
    print(name)
    ls=[]
    for i in range(len(lati)):
        dic=dict() 
        dic['coordinates']=[lati[i],longi[i]] 
        dic['crime']=1
        dic['name']=name[i]




        # a=lll.iloc[i,0]
        # b=lll.iloc[i,1]
        ls.append(dic)
    print("*******************************************************************************")
    print(ls)

    points=ls


    print("*******************************************************************************")
  


 
    return render_template("victimAnalysis.html",sexVal=sex_val_json,sexIdx=sex_idx,profVal=prof_val_json,profIdx=prof_idx,casVal=cas_val_json,casIdx=cas_idx,unitVal=unit_val_json,unitIdx=unit_idx,distVal=dist_val_json,distIdx=dist_idx,points=points,districts=dir)



@app.route("/TimeSeries")
def timeSeries():
    # with open('arima.pkl','rb') as file:
    #     result=pickle.load(file)
    
    pf['Date'] = pd.to_datetime(pf[['Year', 'Month']].assign(day=1))
    crime_count=pf.groupby('Date').size()
    # prediction=result.forecast(steps=10)
    # dateidx=prediction.index.date.tolist()
    dateidx=crime_count.index.date
    dataval=crime_count.values.tolist()
    print('*'*100)
    print(dateidx)
    dateidx=[[(dateidx[i].strftime('%Y-%m')),dataval[i]] for i in range(len(dateidx))]
    print(dateidx)


    dateYear=dateidx
    # dateMonth=dateidx[1]
    # print(dateYear)
    # print(dateMonth)


    # def get_month_number(year, month):
    #     start_year = 2024
    #     start_month = 4

    #     # Calculate the number of months from the starting year and month
    #     months_passed = (year - start_year) * 12 + (month - start_month) + 1

    #     return months_passed

    # # Example usage:
    # for i in range(len(dateidx)):
    #     year = int(dateidx[i][0])
    #     month = int(dateidx[i][1])
    #     result = get_month_number(year, month)
    #     print("Number of months passed since the starting date:", result)



    dateYear_val_json = json.dumps(dateidx)

    # print(prediction)
    return render_template("timeSeries.html",data=dateYear_val_json)





@app.route("/TimeSeries", methods=['POST'])
def TimeSeries1():
    # Check if the 'date' key exists in the form data
    date = request.form.get('date')
    date = date.split("-")
    month = date[1]
    year = date[0]
    if date is None:
        return jsonify({'error': 'Date not found in form data'}), 400
    
    def get_month_number(year, month):
        start_year = 2024
        start_month = 4

        # Calculate the number of months from the starting year and month
        months_passed = (year - start_year) * 12 + (month - start_month) + 1

        return months_passed
    months=get_month_number(int(year),int(month))
    with open('arima.pkl','rb') as file:
        result=pickle.load(file)
    predict=result.forecast(steps=months)
    ss=predict.index.to_list()
    ss=[i.strftime('%Y-%m') for i in ss]
    predict=[int(i) for i in predict.values]
    # print(predict,ss)
    # print('*'*100)
    dateidx=[[ss[i],predict[i]] for i in range(len(ss))]
    print("***********************************************************")
    print(dateidx)
    print("***********************************************************")



    # Assuming you have fetched the predicted data and stored it in the 'dateidx' variable
    dateidx = dateidx

    # Convert the predicted data to JSON format
    dateYear_val_json = json.dumps(dateidx)

    return render_template("timeSeries.html", data=dateYear_val_json)


@app.route("/accusedAnalysisModel")
def AccusedAnalysisModel():
    output=""
    return render_template("accusedAnalysisModel.html",districts=dir,profession=prof,cast=cast,occupation=occup,output=output)

@app.route("/accusedAnalysisModel", methods=['POST'])
def AccusedAnalysisModel1():
    dt = request.form['district']
    place = request.form['places']
    pn=place.split(',')[1]
    cn=request.form['cast']
    an=request.form['age']
    gn=request.form['gender']
    pro=request.form['profession']
    print(dt,pn,cn,an,gn,pro) 
    dataset=pf
    le1 = LabelEncoder().fit(dataset['District_Name'])
    le2 = LabelEncoder().fit(dataset['UnitName'])
    le3 = LabelEncoder().fit(dataset['Caste_x'])
    le4 = LabelEncoder().fit(dataset['Sex_x'])
    le5 = LabelEncoder().fit(dataset['Profession_x'])
    scaler=MinMaxScaler().fit(dataset[['age_x']])
    with open('logistic.pkl','rb') as file:
        model=pickle.load(file)

    a=le1.transform([dt])
    b=le2.transform([pn])
    c=le3.transform([cn])
    d=le4.transform([gn])
    e=le5.transform([pro])
    f=scaler.transform([[an]])
    print('*'*100)
    print(a,b,c,d,e,f)
    dataframe=pd.DataFrame({'District_Name':a[0],'UnitName':b[0],'age_x':f[0],'Caste_x':c[0],'Profession_x':e[0],'Sex_x':d[0]})
    prediction=model.predict(dataframe)
    output=""
    if(prediction[0]==1):
        print('hi will commit into the crime')
        output="will commit into the crime"
    else:
        print('He will not commit into the crime .')
        output="will not commit into the crime "
    if(gn=='FEMALE'):
        output='She '+output
    elif(gn=='MALE'):
        output='He '+output
    print(gn)
    return render_template("accusedAnalysisModel.html",districts=dir,profession=prof,cast=cast,occupation=occup,output=output)


 





if(__name__=="__main__"):
    app.run(debug=True,port=200,host='0.0.0.0')  