from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
from joblib import load

app = Flask(__name__)

# Load dataset once at the start
csv_file_path = "../dataset/filtered_data.csv"
dataset = pd.read_csv(csv_file_path)
MODEL_PATH = "../model/shipping_fee_model.joblib"
shipping_fee_model = load(MODEL_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/input_data", methods=["GET"])
def input_data():
    try:
        # Randomly select a row
        random_row = dataset.sample(n=1).iloc[0]

        # Prepare data as dictionary
        row_data = {
            "weight": round(random_row["weight"], 2),
            "item_price": random_row["item_price"],
            "shipment_method_id": random_row["shipment_method_id"],
            "seller_id": random_row["seller_id"],
            "quantity": random_row["quantity"],
            "b2c_c2c": random_row["b2c_c2c"],
            "declared_handling_days": random_row["declared_handling_days"],
            "zip_distance": random_row["zip_distance"],
            "category_id": random_row["category_id"],
        }

        return jsonify({"success": True, "data": row_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect input data
        weight = float(request.form["weight"])
        item_price = float(request.form["item_price"])
        shipment_method_id = int(request.form["shipment_method_id"])
        seller_id = int(request.form["seller_id"])
        quantity = int(request.form["quantity"])
        b2c_c2c = int(request.form["b2c_c2c"])
        declared_handling_days = int(request.form["declared_handling_days"])
        zip_distance = float(request.form["zip_distance"])
        category_id = int(request.form["category_id"])

        # Prepare features
        features = [
            [
                weight,
                item_price,
                shipment_method_id,
                seller_id,
                quantity,
                b2c_c2c,
                declared_handling_days,
                zip_distance,
                category_id,
            ]
        ]

        # Predict using the model
        prediction = shipping_fee_model.predict(features)[0]

        return jsonify({"success": True, "shipping_fee": round(prediction, 2)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
