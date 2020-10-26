
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    def __init__(self, id, name, views, likes):
        self.id = id
        self.name = name
        self.views = views
        self.likes = likes

    def __repr__(self):
	    return f"Video{self.id}(name = {self.name}, views = {self.views}, likes = {self.likes})"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required.", required = True)
video_put_args.add_argument("likes", type=int, help="Likes on the video")
video_put_args.add_argument("views", type=int, help="Views on the video")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")
video_update_args.add_argument("views", type=int, help="Views on the video")

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
}

class Video(Resource):

    @marshal_with (resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="Video with that id doesn't exist...")
        return result

    @marshal_with (resource_fields) # so object gets serialized 
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel(id = video_id, name=args['name'], views = args['views'], likes = args['likes'])
        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409, message="Video already exists...")
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with (resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="Video doesn't exist...")
        if args['name']:
            result.name = args['name']
        if args['likes']:
            result.likes = args['likes']
        if args['views']:
            result.views = args['views']
        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="Video doesn't exist...")
        db.session.delete(result)
        db.session.commit()
        return '', 204

class VideoIndex(Resource):
    def get(self):
        return "Hello, Welcome to my API"

api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(VideoIndex, "/")

# @app.route('/')
# def index():
#     return "Welcome to my YouTube API."

if __name__ == "__main__":
    app.run(debug=True)