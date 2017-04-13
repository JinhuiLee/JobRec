from flask import Flask, request
from flask_restful import Resource, Api
from nlp import Rec
from nlpIntern import RecIntern
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

rec = Rec()
recIntern = RecIntern()
todos = {}

class Recommend(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        doc = request.form['data']
        print doc
        return rec.recommend(doc)

class RecommendIntern(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        doc = request.form['data']
        print doc
        return recIntern.recommend(doc)

api.add_resource(Recommend, '/api/recommend')
api.add_resource(RecommendIntern, '/api/recommendIntern')
if __name__ == '__main__':
    app.run(debug=True)