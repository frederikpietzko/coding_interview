from flask import Flask, request
from dataclasses import dataclass, asdict
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@dataclass
class User:
    id: int
    name: str
    age: int


@dataclass
class Post:
    id: int
    title: str
    content: str
    userId: int


@dataclass
class Comment:
    id: int
    content: str
    userId: int
    postId: int


users: list[User] = []
posts: list[Post] = []
comments: list[Comment] = []


@app.route("/user", methods=["POST"])
def create_user():
    req = request.get_json()
    if len(users) == 0:
        max_user_id = 1
    else:
        max_user_id = max(map(lambda user: user.id, users))
    user = User(id=max_user_id + 1, name=req["name"], age=req["age"])
    users.append(user)
    return json.dumps(asdict(user))


@app.route("/users")
def get_users():
    return json.dumps([asdict(user) for user in users])


@app.route("/post", methods=["POST"])
def create_post():
    req = request.get_json()
    if len(posts) == 0:
        max_id = 1
    else:
        max_id = max(map(lambda post: post.id, posts))
    post = Post(
        id=max_id + 1, title=req["title"], content=req["content"], userId=req["userId"]
    )
    posts.append(post)
    return json.dumps(asdict(post))


@app.route("/posts")
def get_posts():
    return json.dumps([asdict(post) for post in posts])


@app.route("/posts/<int:id>", methods=["GET", "DELETE", "PUT"])
def get_post(id: int):
    if request.method == "GET":
        post = list(filter(lambda post: post.id == id, posts))[0]
        return json.dumps(asdict(post))
    elif request.method == "DELETE":
        post = list(filter(lambda post: post.id == id, posts))[0]
        posts.remove(post)
        return json.dumps(asdict(post))
    elif request.method == "PUT":
        req = request.get_json()
        post = list(filter(lambda post: post.id == id, posts))[0]
        post.title = req["title"]
        post.content = req["content"]
        return json.dumps(asdict(post))


@app.route("/posts/<int:id>/user")
def get_post_user(id: int):
    post = list(filter(lambda post: post.id == id, posts))[0]
    user = list(filter(lambda user: user.id == post.userId, users))[0]
    return json.dumps(asdict(user))


@app.route("/comment", methods=["POST"])
def create_comment():
    req = request.get_json()
    if len(comments) == 0:
        max_id = 1
    else:
        max_id = max(map(lambda comment: comment.id, comments))
    comment = Comment(
        id=max_id + 1,
        content=req["content"],
        userId=req["userId"],
        postId=req["postId"],
    )
    comments.append(comment)
    return json.dumps(asdict(comment))


@app.route("/comments")
def get_comments():
    return json.dumps([asdict(comment) for comment in comments])


@app.route("/comments/<int:id>", methods=["GET", "DELETE", "PUT"])
def get_comment(id: int):
    if request.method == "GET":
        comment = list(filter(lambda comment: comment.id == id, comments))[0]
        return json.dumps(asdict(comment))
    elif request.method == "DELETE":
        comment = list(filter(lambda comment: comment.id == id, comments))[0]
        comments.remove(comment)
        return json.dumps(asdict(comment))
    elif request.method == "PUT":
        req = request.get_json()
        comment = list(filter(lambda comment: comment.id == id, comments))[0]
        comment.content = req["content"]
        return json.dumps(asdict(comment))
