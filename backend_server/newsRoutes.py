from flask import request,jsonify
from globals import *
from sqlalchemy import desc
import json

from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis
from rediesConnecter import rd
from Web_Crawler_news import return_10_news


from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
api = Namespace('news', description='news operations')

# dictionary to json
def exportNews(news):
    return {
        "newsId":0,
        "newsTitle":news['title'],
        "newsDate":news['date'],
        "newsUrl": news['link'],
        "newsImg":news['img_bo'],
        "newsStandfirst":news['standfirst']
    }

#return a list of news
class NewsList(Resource):
    @api.doc(description="get a list of news")
    def get(self):
        result = []
        try:
            #lists = News.query.order_by(desc(News.newsDate)).all()
            #for news in lists:
            #    result.append(exportNews(news))
            dic = return_10_news()
            for k in dic.keys():
                result.append(exportNews(dic[k]))


        except:
            return {"message": "bad payload"}, 400
        return result,200
api.add_resource(NewsList, '')
