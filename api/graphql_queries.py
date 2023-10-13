
graphql_url = "http://localhost:5000/graphql"

query_allToDo = """
query Alltodo {
    listTodos {
        success
        errors
        todos {
            id
            title 
            description
            created_at
            pro_license
            image_url
            author_id
        }
    }
}
"""
def mutation_createToDo(title, description, image_url):
    query_create =f"""
        mutation CreateTodo {{
            createToDo(
                title: "{title}"
                description: "{description}"
                image_url: "{image_url}"
            ) {{
                success
                errors
                todos {{
                    id
                    title
                    description
                    created_at
                    pro_license
                    image_url
                    author_id
                }}
            }}
        }}
    """

    return query_create

def mutation_deleteToDo(id):
    query_delete = f"""
        mutation DeleteTodo {{
            deleteToDo(
                id: "{id}"
            ) {{
                success
                errors
                todos {{
                    id
                    title
                    description
                    created_at
                    pro_license
                    image_url
                    author_id
                }}
            }}
        }}
    """

    return query_delete

def mutation_updateToDo(id, title, description, image_url):
    query_update = f"""
        mutation UpdateTodo {{
            updateToDo(
                id: "{id}"
                title: "{title}"
                description: "{description}"
                image_url: "{image_url}"
            ) {{
                success
                errors
                todos {{
                    id
                    title
                    description
                    created_at
                    pro_license
                    image_url
                    author_id
                }}
            }}
        }}
    """

    return query_update


if __name__ == "__main__":
    mutation_createToDo = mutation_createToDo.format(
        "title",
        "description",
        "image_url",
        "user_id"
    )

    print(mutation_createToDo)

