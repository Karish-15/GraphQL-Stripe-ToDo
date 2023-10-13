from .models import ToDo
from api import db

def resolve_all_todos(obj, info):
    try:
        # use info to get the user_id)
        user_id = info.context['user_id']
        todos = db.session.query(ToDo).all()
        todos_dicts = [todo.to_dict() for todo in todos if todo.author_id == user_id]
        
        return {
            "success": True,
            "errors": [],
            "todos": todos_dicts
        }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)],
            "todos": []
        }




