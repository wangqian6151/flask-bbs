from models import Model


class Mail(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('sender_id', str, 0),
            ('receiver_name', str, ''),
        ]
        return names
