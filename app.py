from flask import Flask
app = Flask (__name__)

@app.route("/")
def homepage():
    return """
<!DOCTYPE html>
<head>
   <title>Karchek</title>
   <link rel="stylesheet" href="http://stash.compjour.org/assets/css/foundation.css">
</head>
<body style="width: 880px; margin: auto;">
    <h1>Karchek</h1>
    <p>Sending booca new Mitos, Ficos and C4's daily</p>
    </a>
</body>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)