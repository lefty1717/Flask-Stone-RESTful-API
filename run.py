from flask import Flask, jsonify, request, render_template
from flask_restful import Api
from werkzeug.wrappers import Response

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return "Hello World!"

app_info: dict = {
        'id': '412346098',
        'name': 'flask-test',
        'version': '1.0.1',
        'author': 'Finn'
    }

@app.route("/page/", methods=["GET"])
def page():
    return render_template("page.html", text="Flask", appInfo=app_info)

store = []
@app.get("/store")
def get_store():
    return jsonify(store)

@app.post("/store")
def add_store():
    request_data = request.get_json()
    new_item = {
        "name": request_data["name"],
        "price": request_data["price"]
    }
    store.append(new_item)
    return jsonify(new_item)

@app.put("/store/<string:name>")
def update_store(name):
    request_data = request.get_json()
    for item in store:
        if item["name"] == name:
            item["price"] = request_data["price"]
            return jsonify(item)
    return jsonify({"message": "Item not found"})

@app.delete("/store/<string:name>")
def delete_store(name):
    for item in store:
        if item["name"] == name:
            store.remove(item)
            return Response(status=204)
    return Response(status=404, response="Item not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)