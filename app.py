from flask import Flask, jsonify,  request, render_template
import joblib
from werkzeug.utils import secure_filename
import numpy as np
import pickle
import pandas as pd

import flask

# # Create the application.
app = Flask(__name__)
#model_load = joblib.load("./pickle/Recommendation.pkl")
model_load = pickle.load(open("Recommendation.pkl", "rb"))


@app.route('/')
def index():
    return flask.render_template('input.html')

@app.route("/predict", methods=['POST'])
def predict():
    if (request.method == 'POST'):
         user = [x for x in request.form.values()]
         ratings = pd.read_csv('ratings.csv')
         username=ratings[ratings.reviews_username_2.apply(lambda x:x==user[0])].reviews_username.tolist()[0]
         d = model_load.loc[(username)].sort_values(ascending=False)[0:20]
         list = d.to_frame().reset_index().id.to_list()
         ratings_top=ratings[ratings['id'].apply(lambda x:x in list)]
         ratings_top.user_sentiment_pred=ratings_top.user_sentiment_pred.apply(lambda x:0 if x=='Negative' else 1)
         count(ratings_top,list,ratings_top)
         temp=d.to_frame()
         temp['Sentiment_percent']=list_perc
         top5_list = temp.Sentiment_percent.sort_values(ascending=False)[0:5].to_frame().reset_index().id.to_list()
         product_recommended=set(ratings_top[ratings_top['id'].apply(lambda x:x in top5_list)].name.tolist())
         return render_template('input.html', prediction_text='Recommended product {}'.format(product_recommended))
    else :
         return render_template('index.html')



@app.route("/predict_api", methods=['POST', 'GET'])
def predict_api():
    print(" request.method :",request.method)
    if (request.method == 'POST'):
        data = request.get_json()
        #return jsonify(data)
        #return jsonify(model_load.predict([np.array(list(data.values()))]).tolist())
        return jsonify(model_load.loc[19327].sort_values(ascending=False)[0:20].tolist())
        #return jsonify(model_load.predict([np.array(list(data.values()))]).tolist())

    else:
        return render_template('index.html')

list_perc=[]
list_perc.clear()
def count(df,list,ratings_top):
  for x in list:
    list2=[x]
    dummy_frame=ratings_top[ratings_top.id.apply(lambda x:x  in list2)]
    deno=len(dummy_frame)
    num=dummy_frame.user_sentiment_pred.sum()
    list_perc.append(round(num/deno,3))


if __name__ == '__main__' :
    app.run(debug=True )  # this command will enable the run of your flask app or api