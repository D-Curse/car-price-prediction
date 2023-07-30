from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import pickle, sklearn, json
# Create your views here.

model = pickle.load(open('./model/LinearRegressionModel.pkl', 'rb'))
car = pd.read_csv('./model/CLeaned_Car_data.csv')

def home(request):
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(),reverse=True) 
    fuel_type = car['fuel_type'].unique()
    
    companies.insert(0,'Select Company')   

    context = {
        'companies': companies,
        'car_models': car_models,
        'years': year,
        'fuel_types': fuel_type
    }
    
    return render(request, 'index.html', context)


def predict(request):
    
    if(request.method == 'POST'):
        company = request.POST.get('company')
        car_model = request.POST.get('car_models')
        year = request.POST.get('year')
        fuel_type = request.POST.get('fuel_type')
        kms_driven = request.POST.get('kms_driven')
        

        print(company,car_model,year,fuel_type,kms_driven)
        
        prediction = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                        data=np.array([car_model,company,year,kms_driven,fuel_type]).reshape(1,5)))
        
        print(prediction[0] )
        return HttpResponse(str(np.round(prediction[0], 2)))

    else:
        return "Invalid request method. Please use POST."