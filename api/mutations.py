from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import ToDo

@convert_kwargs_to_snake_case
def create_todo_resolver(obj, info, title, description, image_url):
    try:
        user_id = info.context['user_id']
        todo = ToDo(
            title=title,
            description=description,
            author_id=user_id,
            image_url=image_url
        )
        db.session.add(todo)
        db.session.commit()
        return {
            "success": True,
            "errors": [],
            "todo": todo.to_dict()
        }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)],
            "todo": None
        }

@convert_kwargs_to_snake_case
def delete_todo_resolver(obj, info, id):
    try:
        user_id = info.context['user_id']
        todo = db.session.query(ToDo).filter_by(id=id).first()
        if todo.author_id != user_id:
            raise Exception("You are not authorized to delete this todo")
        db.session.delete(todo)
        db.session.commit()
        return {
            "success": True,
            "errors": [],
            "todo": todo.to_dict()
        }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)],
            "todo": None
        }

@convert_kwargs_to_snake_case
def update_todo_resolver(obj, info, id, title, description, image_url):
    try:
        user_id = info.context['user_id']
        todo = db.session.query(ToDo).filter_by(id=id).first()
        if todo.author_id != user_id:
            raise Exception("You are not authorized to update this todo")
        todo.title = title
        todo.description = description
        todo.image_url = image_url
        db.session.commit()
        return {
            "success": True,
            "errors": [],
            "todo": todo.to_dict()
        }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)],
            "todo": None
        }