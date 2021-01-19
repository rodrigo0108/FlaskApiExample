import flask
from flask import request, jsonify
from flaskext.mysql import MySQL, pymysql

app = flask.Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'Project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config["DEBUG"] = True

mysql.init_app(app)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Authors</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM author')
    results = cursor.fetchall()
    conn.close()

    return jsonify(results)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    # results = filter(lambda book: book['id'] == id, books)

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM author WHERE id = %s', id)

    results = cursor.fetchone()

    # app.logger.info('result is: %s', results)

    conn.close()

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()