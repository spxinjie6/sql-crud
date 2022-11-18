from flask import Flask
from flask import request

import models
from libs.demo import Demo

app = Flask(__name__)
models.init(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/insert", methods=["POST"])
def insert_demo():
    Demo.create(**request.json)
    return 'done'


@app.route("/bulk/insert", methods=["POST"])
def bulk_insert_demo():
    Demo.bulk_create(*request.json)
    return "done"


@app.route("/update", methods=["PUT"])
def update_demo():
    _id = request.json.pop("id", 0)
    Demo.update(_id, **request.json)
    return "done"


@app.route("/bulk/update", methods=["PUT"])
def bulk_update_demo():
    Demo.bulk_update(*request.json)
    return "done"


@app.route("/query", methods=["GET"])
def query_demo():
    name = request.args.get("name", "")
    data = []
    for instance in Demo.query(name=name).all():
        data.append({
            "id": instance.id,
            "name": instance.name,
            "tag": instance.tag
        })
    print(data)
    return {"data": data}


@app.route("/delete/demo", methods=["delete"])
def delete_demo():
    id_list = request.json.get("ids", [])
    Demo.delete(id_list)
    return "done"


if __name__ == '__main__':
    app.run(debug=True)
