from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__)

# Define variable for equations
x = sp.symbols('x')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    expr = data.get("expression")

    try:
        expr = expr.lower()

        # -------------------------
        # BASIC NLP REPLACEMENTS
        # -------------------------
        replacements = {
            "plus": "+",
            "minus": "-",
            "multiply": "*",
            "into": "*",
            "divide": "/",
            "by": "/",
            "power": "**"
        }

        for word, symbol in replacements.items():
            expr = expr.replace(word, symbol)

        expr = expr.replace("square root of", "sqrt")
        expr = expr.replace("root", "sqrt")

        # -------------------------
        # SOLVE EQUATION
        # -------------------------
        if "solve" in expr:
            expr = expr.replace("solve", "").strip()
            result = sp.solve(expr, x)
            return jsonify({"result": str(result)})

        # -------------------------
        # NORMAL CALCULATION
        # -------------------------
        result = sp.sympify(expr)
        result = sp.N(result)

        # Convert to float
        result_float = float(result)

        # Remove unnecessary decimals
        if result_float.is_integer():
            result = int(result_float)
        else:
            result = round(result_float, 6)

        return jsonify({"result": str(result)})

    except:
        return jsonify({"result": "Error"})

# Run app
if __name__ == "__main__":
    app.run(debug=True)