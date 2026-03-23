# app.py
"""
Calculator REST API.

Calculator sinifini HTTP API olarak sunan Flask uygulamasi.

Calistirma:
    python src/app.py

Endpoints:
    POST /api/calculate    → Hesaplama yap
    GET  /api/history      → Islem gecmisini getir
    DELETE /api/history     → Gecmisi temizle
    GET  /api/health       → Saglik kontrolu
"""
from flask import Flask, request, jsonify, render_template
from calculator import Calculator

app = Flask(__name__)
calc = Calculator()


@app.route("/")
def index():
    """Calculator web arayuzu — Playwright E2E testleri icin."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Saglik kontrolu endpoint'i."""
    return jsonify({"status": "healthy", "service": "calculator-api"})


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """Hesaplama endpoint'i.

    Request Body:
        {
            "operation": "add|subtract|multiply|divide|power|percentage|average|absolute|factorial",
            "a": <number>,           # Ilk operand (average haric)
            "b": <number>,           # Ikinci operand (average haric)
            "numbers": [<numbers>]   # Sadece average icin
        }

    Response:
        {"result": <number>, "operation": "<op>"}
        veya
        {"error": "<message>"}, 400/422
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    operation = data.get("operation")
    if not operation:
        return jsonify({"error": "Operation is required"}), 400

    try:
        if operation == "average":
            numbers = data.get("numbers")
            if numbers is None:
                return jsonify({"error": "'numbers' field is required for average"}), 400
            result = calc.average(numbers)

        elif operation == "absolute":
            a = data.get("a")
            if a is None:
                return jsonify({"error": "'a' field is required"}), 400
            result = calc.absolute(a)

        elif operation == "factorial":
            a = data.get("a")
            if a is None:
                return jsonify({"error": "'a' field is required"}), 400
            if not isinstance(a, int):
                raise TypeError("Factorial only works with integers!")
            result = calc.factorial(a)

        else:
            a = data.get("a")
            b = data.get("b")
            if a is None or b is None:
                return jsonify({"error": "'a' and 'b' fields are required"}), 400

            operations = {
                "add": calc.add,
                "subtract": calc.subtract,
                "multiply": calc.multiply,
                "divide": calc.divide,
                "power": calc.power,
                "percentage": calc.percentage,
            }

            if operation not in operations:
                return jsonify({"error": f"Unknown operation: {operation}"}), 400

            result = operations[operation](a, b)

        return jsonify({"result": result, "operation": operation})

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 422


@app.route("/api/history", methods=["GET"])
def get_history():
    """Islem gecmisini dondurur."""
    history = calc.get_history()
    return jsonify({"history": history, "count": len(history)})


@app.route("/api/history", methods=["DELETE"])
def clear_history():
    """Islem gecmisini temizler."""
    calc.clear_history()
    return jsonify({"message": "History cleared"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)