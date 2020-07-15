from flask import Flask, render_template, request, json, url_for
from werkzeug.exceptions import abort
#import pymysql
import pymysql.cursors


app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345949',
                             db='mydb',
                             charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)
print("-----------------------connect successful!!")


try:
    cursor = connection.cursor()
    # SQL
    sql = "SELECT * FROM cartrige"
    # Выполнить команду запроса (Execute Query).
    cursor.execute(sql)
    # 1 строка данных
    oneRow = cursor.fetchone()
    cursor.close()


finally:
    print("finally: ")
    # Закрыть соединение (Close connection).
    # connection.close()


def get_post(part_number):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM cartrige WHERE part_number='%s'" % (part_number,))# cartrige_id="+str(cartrige_id)
        #cursor.execute("SELECT printer.*, cartrige.* FROM printer, cartrige WHERE part_number='%s'" % (part_number,))
        #cursor.execute("SELECT select_1 UNION [ALL] select_2 UNION [ALL] FROM cartrige WHERE part_number='%s'" % (part_number,))
        #cursor.execute("SELECT part_number,title FROM printer WHERE part_number='%s' UNION SELECT part_number,title FROM cartrige" % (part_number,))
        #cursor.execute("CREATE VIEW view_name AS SELECT part_number,title FROM printer UNION SELECT part_number,title FROM cartrige")
        #"JOIN printer_cartrige on printer_cartrige.printer_printer_id = printer.printer_id "
        #"JOIN cartrige on cartrige.cartrige_id = printer_cartrige.cartrige_cartrige_id group by printer.printer_id")
        cursor.execute("SELECT * FROM view_name WHERE part_number='%s'" % (part_number,))
        post = cursor.fetchone()
        # print(post)
        cursor.close()

    if post is None:
        abort(404)
    return post


def get_post2(part_number):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM view_name WHERE part_number='%s'" % (part_number,))
        post = cursor.fetchone()
        # print(post)
        cursor.close()

    if post is None:
        abort(404)
    return post


# @app.route('/search', methods=['GET', 'POST'])
# def search():


@app.route('/', methods=['GET', 'POST'])
def main():


    #cursor = connection.cursor()
    #sql = "SELECT * FROM cartrige"
    #cursor.execute(sql)
    # cursor.execute("SELECT * FROM cartrige")
    # cursor.execute(sql)
    #data = json.dumps({'message':'User created successfully !'})
    # oneRow = cursor.fetchone()
    # print("Row Result: ", oneRow)
    # print("data Result: ", data)
    # print("data Result: ", data)
    # cartrigeinfo = cursor.execute.query("SELECT * FROM cartrige")
    # print("cartrigeinfo Result: ", cartrigeinfo)
    # cursor.execute(sql)
    with connection.cursor() as cursor:
        cursor.execute("SELECT printer.*, cartrige.name FROM printer "
                       "JOIN printer_cartrige on printer_cartrige.printer_printer_id = printer.printer_id "
                       "JOIN cartrige on cartrige.cartrige_id = printer_cartrige.cartrige_cartrige_id")
        data = cursor.fetchall()
        cursor.execute(sql)

        cursor.execute("SELECT printer.*, group_concat(cartrige.name) FROM printer "
                       "JOIN printer_cartrige on printer_cartrige.printer_printer_id = printer.printer_id "
                       "JOIN cartrige on cartrige.cartrige_id = printer_cartrige.cartrige_cartrige_id group by printer.printer_id")
        data2 = cursor.fetchall()

        #cursor.execute("SELECT printer.part_number FROM printer JOIN cartrige")
        #cursor.execute("CREATE VIEW view_name AS SELECT part_number,title FROM printer") #" UNION SELECT part_number,title FROM cartrige")
        #cursor.execute("DROP VIEW view_name")
        cursor.execute("SELECT * FROM view_name")
        data3 = cursor.fetchall()
        print(data3)
        cursor.close()
    return render_template('index.html', result=data, result2=data2, result3=data3)


@app.route('/hp', methods=['GET', 'POST'])
def hp():

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cartrige WHERE brand_id=2")
        data_cartridge = cursor.fetchall()
        cursor.execute("SELECT * FROM printer WHERE printer_brand_id=1")
        data_printer = cursor.fetchall()
        cursor.close()
    return render_template('hp.html', data_cartridges=data_cartridge, data_printers=data_printer)


@app.route('/canon', methods=['GET', 'POST'])
def canon():
    q = request.args.get('q')

    with connection.cursor() as cursor:
        if q:
            cursor.execute("SELECT * FROM cartrige WHERE brand_id="+str(q))
            data = cursor.fetchall()
            print('q=', q)
        else:
            cursor.execute("SELECT * FROM cartrige WHERE brand_id=3")
            data = cursor.fetchall()
            print('q=else', q)
        cursor.close()
    return render_template('canon.html', resultcanon=data)


@app.route('/samsung', methods=['GET', 'POST'])
def samsung():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cartrige WHERE brand_id=1")
        data = cursor.fetchall()
        cursor.close()
    return render_template('samsung.html', result_samsung=data)


@app.route('/solutions', methods=['POST', 'GET'])
def solutions():
    return render_template('solutions.html')




# """Генерация страницы (карточки) картриджа"""
@app.route('/<part_number>')
def post(part_number):
    post = get_post(part_number)
    post2 = get_post2(part_number)
    return render_template('post.html', post=post, post2=post2)



# # '''Генерация страницы (карточки) принтера'''
# @app.route('/<printer_name>')
# def printer_page(printer_name):
#     post = printer_page(printer_name)
#     return render_template('printer_page.html', post=post)


# """Страница не найдена 404"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()



