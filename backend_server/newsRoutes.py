from flask import request,jsonify
from globals import *
from sqlalchemy import desc
import json

from flask_restplus import Api, Resource, fields, Namespace
from forms import *
import redis
from rediesConnecter import rd


from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt,
)
api = Namespace('news', description='news operations')

def exportNews(news):
    return {
        "newsId":news.newsId,
        "newsTitle":news.newsTitle,
        "newsDate":news.newsDate,
        "newsUrl": news.newsUrl,
        "newsStandfirst":news.newsStandfirst
    }


class NewsList(Resource):
    @api.doc(description="get a list of news")
    def get(self):
        result = []
        try:
            lists = News.query.order_by(desc(News.newsDate)).all()
            for news in lists:
                result.append(exportNews(news))

        except:
            return {"message": "bad payload"}, 400
        return result,200
api.add_resource(NewsList, '')
