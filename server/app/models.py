# -*- coding: utf-8 -*-

from typing import Union, Type, Optional
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from slugify import slugify
from flask import Flask, json, url_for, current_app
from flask.helpers import get_env
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

from .helpers import get_unix_time_tuple

db: SQLAlchemy = SQLAlchemy()

tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)

DEFAULT_SETTINGS = {
    "locale": "en",
    "name": "Blog",
    "cover_url": "/static/images/cover.jpg",
    "avatar": "/static/images/avatar.jpeg",
    "description": "A simple blog powered by Flask",
}

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(11), default=get_unix_time_tuple())
    last_modified = db.Column(db.String(11), default=get_unix_time_tuple(), onupdate=get_unix_time_tuple())
    image = db.Column(db.String(400))
    lang = db.Column(db.String(20))
    content = db.Column(db.Text())
    comment = db.Column(db.Boolean(), default=True)
    description = db.Column(db.String(400))
    author = db.Column(db.String(50))
    tags = db.relationship("Tag", secondary=tags, backref="posts")
    slug = db.Column(db.String(100))
    is_draft = db.Column(db.Boolean(), default=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")

    def __init__(self, **kwargs) -> None:
        if isinstance(kwargs.get("category"), str):
            kwargs["category"] = Category.get_one_or_new(kwargs["category"])
        tags = kwargs.get("tags")
        if tags and isinstance(tags[0], str):
            kwargs["tags"] = [Tag.get_one_or_new(tag) for tag in tags]
        kwargs.pop("date", None)
        kwargs.pop("last_modified", None)
        super().__init__(**kwargs)

    def to_dict(self, ensure_text: bool = False) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "image": self.image,
            "category": self.category if not ensure_text else str(self.category),
            "lang": self.lang,
            "comment": self.comment,
            "description": self.description,
            "author": self.author,
            "tags": self.tags if not ensure_text else [str(tag) for tag in self.tags],
            "slug": self.slug,
            "content": self.content,
            "last_modified": self.last_modified,
            "is_draft": self.is_draft,
        }

    def __repr__(self) -> str:
        return "<Post: %s>" % self.title


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean(), default=False)
    settings = db.Column(db.Text())
    link = db.Column(db.String(128))
    picture = db.Column(db.String(512))
    u_type = db.Column(db.String(16))
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("username", "email", name="_username_email"),)

    def __init__(self, **kwargs) -> None:
        password = kwargs.pop("password", None)
        if password:
            password = generate_password_hash(password)
        if not kwargs.get('username') and kwargs.get('name'):
            kwargs['username'] = slugify(kwargs['name'])

        super(User, self).__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def display_name(self):
        return self.name or self.username

    @classmethod
    def get_admin(cls) -> "User":
        rv: Union[User, None] = cls.query.filter_by(is_admin=True).first()
        if not rv:
            rv = cls(
                username="admin",
                email=current_app.config["ADMIN_EMAIL"],
                password=current_app.config["DEFAULT_ADMIN_PASSWORD"],
                is_admin=True,
            )
            db.session.add(rv)
            db.session.commit()
        return rv

    @property
    def avatar(self) -> str:
        if self.picture:
            return self.picture
        email_hash = hashlib.md5(
            (self.email or self.username).strip().lower().encode()
        ).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"

    def generate_token(self, expiration=24 * 60 * 60) -> bytes:
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    @classmethod
    def verify_auto_token(cls, token) -> Union[None, "User"]:
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return None
        user = cls.query.get(data["id"])
        return user

    def read_settings(self) -> dict:
        return json.loads(self.settings or json.dumps(DEFAULT_SETTINGS))

    def write_settings(self, data: dict) -> None:
        self.settings = json.dumps(data)
        db.session.commit()

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "avatar": self.avatar,
            "display_name": self.display_name
        }

class GetOrNewMixin:
    @classmethod
    def get_one_or_new(cls, text: str):
        record = cls.query.filter_by(text=text).first()
        if not record:
            record = cls(text=text)
        return record

class Tag(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(50), unique=True)
    url = db.Column(db.String(50))

    def __init__(self, **kwargs) -> None:
        with current_app.test_request_context():
            kwargs["url"] = url_for("tag", text=slugify(kwargs["text"]))
        super(Tag, self).__init__(**kwargs)

    def __repr__(self) -> str:
        return "<Tag: {}>".format(self.text)

    def __str__(self) -> str:
        return self.text


class Category(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), unique=True)
    posts = db.relationship("Post", backref="category", lazy="dynamic")

    def __repr__(self) -> str:
        return "<Category: {}>".format(self.text)

    def __str__(self) -> str:
        return self.text


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    floor = db.Column(db.Integer)
    content = db.Column(db.Text())
    html = db.Column(db.Text())
    create_at = db.Column(db.String(11), default=get_unix_time_tuple())
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    replies = db.relationship("Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("post_id", "floor", name="post_id_floor"),)

    @property
    def children(self):
        queue = self.replies.all()
        rv = []
        while queue:
            node = queue.pop(0)
            rv.append(node)
            queue.extend(node.replies or [])
        return sorted(rv, key=lambda x: x.create_at)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "autor": self.author.to_dict(),
            "post": {"title": self.post.title, "url": self.post.url},
            "floor": self.floor,
            "content": self.content,
            "html": self.html,
            "create_at": self.create_at,
        }

def init_app(app: Flask)-> None:
    db.init_app(app)
    Migrate(app, db)