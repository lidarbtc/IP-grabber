from flask import Flask, render_template, request
import datetime
import flask
import pymysql

app = Flask(__name__)
app.config["SECRET_KEY"] = b'{Q>GOR(76X^ys!H.V#x:<@HQJRpg{P7)QMKCe]SUTJDe%/aPUN'
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=60)

HTML_PATH_MAIN = './main.html'

def db_connector(sql_command):
    MYSQL_DB = {
        'user'     : 'dbuser',
        'password' : 'abcd1234',
        'host'     : 'localhost',
        'port'     : '3306',
        'database' : 'grabber'
    }
    db = pymysql.connect(
        host=MYSQL_DB['host'],
        port=int(MYSQL_DB['port']),
        user=MYSQL_DB['user'],
        passwd=MYSQL_DB['password'],
        db=MYSQL_DB['database'],
        charset='utf8'
    )
    cursor = db.cursor()
    cursor.execute(sql_command)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return str(result).replace("(", "").replace(")", "").replace("'", "").replace(',', '').rstrip()

@app.route('/', methods=['GET', 'POST']) 
def index():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    useragent = request.headers.get('User-Agent')
    db_connector(f"INSERT IGNORE INTO info(userip, useragent) VALUES('{ip_address}', '{useragent}');")
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host="localhost", port="3000",debug=False, threaded=True)
