from api import db
import datetime

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    time_now = datetime.datetime.utcnow().strftime('%d-%m-%Y')
    created_at = db.Column(db.String, default=time_now)
    pro_license = db.Column(db.Boolean, default = False)
    image_url = db.Column(db.String, default = "")
    author_id = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at if self.created_at else "N/A"),
            "image_url": self.image_url, 
            "pro_license": self.pro_license,
            "author_id": self.author_id
        }

class UserPro(db.Model):
    id = db.Column(db.String, primary_key=True)
    pro_license = db.Column(db.Boolean, default = False)

    
