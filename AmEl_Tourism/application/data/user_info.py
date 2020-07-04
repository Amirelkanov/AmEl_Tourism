from ..extensions.init_models import db


class TGUserInfo(db.Model):
    """ TG User info model initialization class """

    __tablename__ = 'tg_user_info'
    tg_user_id = db.Column(db.Integer, primary_key=True)
    tg_user_coords = db.Column(db.String, nullable=True)
    tg_user_page = db.Column(db.Integer, nullable=False, default=1)


class VKUserInfo(db.Model):
    """ VK User info model initialization class """

    __tablename__ = 'vk_user_info'
    vk_user_id = db.Column(db.Integer, primary_key=True)
    vk_user_coords = db.Column(db.String, nullable=True)
    vk_user_page = db.Column(db.Integer, nullable=False, default=1)
