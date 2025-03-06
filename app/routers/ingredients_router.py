from flask import Flask, jsonify, request
from app.classifier import process_ingredients

app = Flask(__name__)

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = process_ingredients()
    return jsonify(ingredients)

if __name__ == '__main__':
    app.run(debug=True)
