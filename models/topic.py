from models import Model
from models.user import User
from models.reply import Reply
from models.board import Board

class Topic(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', str, 0),
            ('board_id', str, 0),
        ]
        return names

    @classmethod
    def find(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        ms = Reply.all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.one(id=self.board_id)
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def recent_topic(cls, id):
        ms = Topic.all(user_id=id)
        number = 5
        if len(ms) < number:
            recent_topic = reversed(ms)
        else:
            recent_topic = reversed(ms[-number:])
        return recent_topic

    @classmethod
    def recent_reply(cls, id):
        ms = Reply.all(user_id=id)
        recent_reply = []
        number = 5
        if len(ms) < number:
            ms = reversed(ms)
        else:
            ms = reversed(ms[-number:])
        for m in ms:
            t = Topic.one(id=m.topic_id)
            if t is not None:
                recent_reply.append(t)
        return recent_reply

