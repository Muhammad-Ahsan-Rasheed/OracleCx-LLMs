from flask import Flask, render_template, request, abort, redirect, url_for
import cx_Oracle
from AI import get_query, turn_into_sentence, turn_into_table
from contextlib import contextmanager

app = Flask(__name__)

# App configuration here for database

db_conn = None


@contextmanager
def get_cursor():
    global db_conn
    if db_conn is None:
        try:
            db_conn = cx_Oracle.connect(
                app.config['ORACLE_USER'],
                app.config['ORACLE_PASSWORD'],
                app.config['ORACLE_DSN']
            )
            print("Database Connection Established")
        except cx_Oracle.DatabaseError as e:
            print("Database Connection Failed")
            print(e)
            db_conn = None

    if db_conn is None:
        abort(500, 'Database Connection Failed')

    cursor = db_conn.cursor()
    try:
        yield cursor
    except cx_Oracle.DatabaseError as e:
        db_conn.rollback()
        raise e
    finally:
        cursor.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def completion_response():
    Question = request.args.get('msg')
    try:
        with get_cursor() as cursor:
            query = get_query(Question, 512)
            print('Query: ', query)

            data = cursor.execute(query).fetchall()
            print(data)
            # get column names
            col_names = [row[0] for row in cursor.description]

        print('Column: ', col_names)
        table_html = "<table><tbody>"

        # add header row
        table_html += "<tr>"
        for col in col_names:
            table_html += f"<th>{col}</th>"
        table_html += "</tr>"

        for row in data:
            table_html += "<tr>"
            for col in row:
                # if col is int or float, foramt it
                if isinstance(col, int) or isinstance(col, float):
                    table_html += f"<td>{col:,.2f}</td>"
                else:
                    table_html += f"<td>{col}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"

        response = turn_into_table(data, Question, query, 2048)

        print('Response: ', response)
        return str(response) + table_html

    except Exception as e:
        print('Sorry, I am not able to answer your question, Tell me in more details.')
        print(e)
        return redirect(url_for('error', error_message="Sorry, I am not able to answer your question, Tell me in more details."))


@app.route('/error')
def error():
    # Get the error message from the query parameter
    error_message = request.args.get('error_message')
    redirect(url_for('index'))
    return f"An error occurred: {error_message}"
