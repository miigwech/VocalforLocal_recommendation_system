from flask import Flask,render_template,request,jsonify
import pandas as pd
import pickle
import numpy as np
import os

#pic = os.path.join('static','images')

#app.config['UPLOAD_FOLDER'] = picFolder

pdata_df = pickle.load(open('pdata.pkl','rb'))
indices = pickle.load(open('indices.pkl','rb'))
loaded_data = np.load('cosine_sim.npz')
cosine_sim = loaded_data['arr_0']


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           product_name = list(pdata_df['product'].values),
                           brand_name = list(pdata_df['brand'].values),
                           pr_price = list(pdata_df['sale_price'].values),
                           ratings = list(pdata_df['rating'].values),
                           descrip = list(pdata_df['description'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/about')
def about_ui():
    #pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'sarvesh.jpg')
    return render_template('about.html')

@app.route('/recommend_products',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    idx = indices[user_input]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    recommended_products = pdata_df.iloc[movie_indices][['product','brand','sale_price','rating','description']].to_dict('records')

    print(recommended_products)

    return render_template('recommend.html', recommended_products=recommended_products)
    
    #return pdata_df.iloc[movie_indices][['product','brand','sale_price','rating']]

    #return jsonify(pdata_df.iloc[movie_indices][['product','brand','sale_price','rating']].to_dict())

    #return str(user_input)

if __name__=='__main__':
    app.run(debug=True)