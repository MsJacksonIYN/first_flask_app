from flask import Flask, request, render_template
import pickle
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.model_selection import RandomizedSearchCV
# from xgboost import XGBClassifier


app = Flask(__name__)

d = pickle.load( open( "encoder.pkl", "rb" ) )
poly = pickle.load( open("interaction_maker.pkl", "rb"))
mod = pickle.load( open("xgboost_model.pkl", "rb"))

@app.route('/predict', methods = ['POST'])
def make_preds():
    animal = {'Type':[request.form.get('Type')],
        'Sex':[request.form.get('Sex')],
        'Size':[request.form.get('Size')],
        'Intake Type':[request.form.get('Intake Type')],
        'Intake Jurisdiction':[request.form.get('Intake Jurisdiction')],
        'PredomBreed':[request.form.get('Breed')],
        'PredomColor':[request.form.get('Color')]}

    animal_df = pd.DataFrame.from_dict(animal, orient='columns')
    animal_transformed = animal_df.apply(lambda x: d[x.name].transform(x))
    features = pd.DataFrame(poly.transform(animal_transformed), columns=poly.get_feature_names(input_features=animal_transformed.columns))
    prediction = mod.best_estimator_.predict(features)
    
    if prediction[0]==0:
        return 'ADOPTION'
    elif prediction[0]==1:
        return 'EUTHANIZE'
    elif prediction[0]==2:
        return 'RETURN TO OWNER'
    elif prediction[0]==3:
        return 'TRANSFER'

@app.route('/predict', methods = ['GET'])
def render_html():
    return render_template('dropdown.html')