from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

orders = {}

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data or "product" not in data:
        return jsonify({"error": "Product is required"}), 400

    order_id = str(uuid.uuid4())

    orders[order_id] = {
        "product": data["product"],
        "quantity": data.get("quantity", 1),
        "status": "Processing"
    }

    return jsonify({
        "order_id": order_id,
        "status": "Processing"
    }), 201


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = orders.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "order_id": order_id,
        "product": order["product"],
        "quantity": order["quantity"],
        "status": order["status"]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)