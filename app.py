import numpy as np
import pandas as pd

from flask import *  


app = Flask(__name__)  
 

@app.route('/',methods = ['GET','POST'])  
def home():
    if request.method == 'GET':
        return render_template("upload_file.html", data=[],status=False)
    if request.method == 'POST':  
        f = request.files['file']  
        f.save('TS_MM012.xlsx')  
 
        file_path = 'TS_MM012.xlsx'

        df = pd.read_excel(file_path,header=None)
        df = df.rename(columns=df.iloc[1])
        df = df.drop(0)
        df = df.drop(1)
        df = df.loc[:, ~df.columns.duplicated()]

        our_locations = [
            '742-630-01-01 - PLOT NO. 1/G1, SIPCOT IT PARK (742-630-01-01)',
            '739-630-01-01 - GACHIBOWLI,SERI LINGAMPALLY,RANGA REDDY (739-630-01-01)',
            '743-617-11-01 - EXPLORER BUILDING (743-617-11-01)',
            '739-814-06-00 - PLOT 54, 1 & 2 FL INTERSIL BLDG (739-814-06-00)',
            '739-814-02-00 - PLOT 54, 1 & 2 FL INTERSIL BLDG (739-814-02-00)',
            '739-645-14-01 - BUILDING 15A, ZONE 01, GIFT SEZ (739-645-14-01)',
            '739-000-00-00 - NON BAC ADDRESS (739-000-00-00)',
        ]
        def locationAssign(location):
            if location == '742-630-01-01 - PLOT NO. 1/G1, SIPCOT IT PARK (742-630-01-01)':
                return 'Chennai'
            elif location == '739-630-01-01 - GACHIBOWLI,SERI LINGAMPALLY,RANGA REDDY (739-630-01-01)':
                return 'Hyderabad'
            elif location == '743-617-11-01 - EXPLORER BUILDING (743-617-11-01)':
                return 'Bangalore'
            elif location == '739-814-06-00 - PLOT 54, 1 & 2 FL INTERSIL BLDG (739-814-06-00)':
                return 'Mumbai'
            elif location == '739-814-02-00 - PLOT 54, 1 & 2 FL INTERSIL BLDG (739-814-02-00)':
                return 'Mumbai'
            elif location == '739-645-14-01 - BUILDING 15A, ZONE 01, GIFT SEZ (739-645-14-01)':
                return 'Gandhinagar'
            elif location == '739-000-00-00 - NON BAC ADDRESS (739-000-00-00)':
                return 'Gandhinagar'
            else:
                return 'No Data'

        df['Location'] = df['Resource Mailcode'].apply(locationAssign) 

        def locationFilter(location):
            if location in our_locations:
                return True
            else:
                return False

        df = df[ df['Resource Mailcode'].apply(locationFilter) ]


        our_supervisor = [
            'Sebolt, Dave',
            'Rusch, Brant',
            'Sonthi, Ravi'
        ]
        def supervisorFilter(name):
            if name in our_supervisor:
                return True
            else:
                return False
        df = df[ df['Worker: Worker Supervisor'].apply(supervisorFilter) ]


        df = df[['Worker','Email' ,'Location','Time Sheet Start Date','Time Sheet End Date','Net Billable Hours','Time Sheet Status']]


        df = df.groupby(['Worker','Email','Location','Time Sheet Status','Net Billable Hours', ],as_index=False).sum()


        totalEmployeesCount = len(df)

        data = []
        draft_zero = 0
        draft_non_zero = 0
        submitted = 0

        for i in range(0,totalEmployeesCount):
            temp = {
                'Sr_No':0,
                'Employee_Name':'',
                'Email':'',
                'Location':'',
                'Time_Sheet_Status':'',
                'Net_Billable_Hours':-1
            }
            temp['Sr_No']=i+1
            temp['Employee_Name']=df.iloc[i].at['Worker']
            temp['Email']=df.iloc[i].at['Email']
            temp['Location']=df.iloc[i].at['Location']
            temp['Time_Sheet_Status']=df.iloc[i].at['Time Sheet Status']
            temp['Net_Billable_Hours']=df.iloc[i].at['Net Billable Hours']
            if temp['Time_Sheet_Status']=='Draft':
                if temp['Net_Billable_Hours']==0:
                    draft_zero+=1
                else:draft_non_zero+=1
            else:
                submitted+=1
            data.append(temp)
        return render_template("upload_file.html",status=True, data = data, draft_zero=draft_zero, draft_non_zero=draft_non_zero, submitted=submitted) 

if __name__ == '__main__':  
    app.run(debug = True)  