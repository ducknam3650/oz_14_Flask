from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint('posts', __name__, description='posts api', url_prefix='/posts')

    @posts_blp.route('/', methods=['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()
        if request.method == 'GET':
            sql = "SELECT * FROM posts"
            cursor.execute(sql)
            
            posts = cursor.fetchall()
            cursor.close()
            

            post_list = []

            for post_item in posts:
                post_list.append({
                    'id': post_item[0],
                    'title': post_item[1],
                    'content': post_item[2]
                })

            return jsonify(post_list)
        
        elif request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message="Title or Content can not be empty")

            sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
            mysql.connection.commit()
            cursor.close()
           
            return jsonify({"msg":"successfully created post data","title":title,"content":content}), 201



    @posts_blp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM posts WHERE id = {id}"
        cursor.execute(sql)
        post = cursor.fetchone()

        if request.method == 'GET':
            if not post:
                abort(404, "Not found post")
            return jsonify({
                    'id':post[0],
                    'title':post[1],
                    'content':post[2]
                    })
            
            
        elif request.method == 'PUT':
            title = request.json.get('title')
            content = request.json.get('content')

            if not post: # post가 없는 경우 404 반환
                abort(400, "Not found post")
            if not title or not content: # title 또는 content가 없는 경우 400 반환
                abort(404, message="Title or Content can not be empty")

            sql = "UPDATE posts SET title = %s, content = %s WHERE id = %s"
            cursor.execute(sql, (title, content, id))
            mysql.connection.commit()
            cursor.close()
            return jsonify({"msg":"Successfully updated post"})

        elif request.method == 'DELETE':
            if not post:
                abort(404, "Not found post")

            sql = "DELETE FROM posts WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()

            return jsonify({"msg":"Successfully deleted post"})


    return posts_blp