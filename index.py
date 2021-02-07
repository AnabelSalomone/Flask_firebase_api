import firebase_admin
from firebase_admin import credentials, db
from decouple import config
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

# Initializes a Flask app
app = Flask(__name__)
# Initializes a restful api
api = Api(app)

# Fetch the service account key JSON file contents
cred = credentials.Certificate(config('GOOGLE_APPLICATION_CREDENTIALS'))

# Initialize the app with a service account
firebase_admin.initialize_app(cred, {
    'databaseURL': config("DATABASE_URL")
})


def abort_action_if_id_exists(id):
    data = db.reference().get("")
    if id in data:
        abort(409, "Id already exists")


class GetData(Resource):
     def get(self):
        # Access the database and copies it
        data = db.reference().get("")
        return data


class GetByAuthor(Resource):
    def get(self, author):
        data = db.reference().get("")
        return [item for item in data if item.get('author') == author]

class AddBook(Resource):
    def put(self):
        abort_action_if_id_exists(id)
        book_args = reqparse.RequestParser()
        book_args.add_argument("author", type=str, required=True)
        book_args.add_argument("title", type=str, required=True)

        args = book_args.parse_args()

        ref = db.reference()
        ref.push().set(args)

        data = db.reference().get("")
        return data, 201


api.add_resource(GetData, "/getdata")
api.add_resource(GetByAuthor, "/getdata/<string:author>")
api.add_resource(AddBook, "/addbook")

# Initializes de server
if __name__ == "__main__":
    app.run(debug=True)
