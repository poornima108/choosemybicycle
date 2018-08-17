import csv
import os
import psycopg2
from flask import Flask,request,jsonify
app = Flask(__name__)

conn_string="dbname='db2' user='postgres' password='root' host='localhost'"
conn=psycopg2.connect(conn_string)
cursor=conn.cursor()
@app.route("/products/-import", methods=['POST'])
def products_import():
    file = request.files["file"]
    file.save(os.path.join(file.filename))
    re = csv.reader(open(os.path.join(file.filename),'r'))
    for row in re:
        statement ="INSERT INTO product(sku,description,price," \
                "is_active) VALUES('"+str(row[1])+"','"\
                + str(row[2])+ "',"+ str(row[3])+","+str(row[4])+") returning id"
        try:
            cursor.execute(statement)
        except:
            return "error"
    conn.commit()
    return "successfull"
@app.route("/products", methods=['GET'])
def products_display():
    cursor.execute("select * from product_template");
    rows=cursor.fetchall()
    li=[]
    for row in rows:
        li.append({"id":row[0],"sku":row[1],"description":row[2],"price":row[3],"is_active":row[4]})
        print(row)
    conn.commit()
    return jsonify(li)
if __name__ == "__main__":
    command='''create table if not exists category(skuid varchar(50) primary key,des varchar(20))'''
    cursor.execute(command);
    conn.commit()
    command='''insert into category(skuid,des)values('a1','hello');insert into category(skuid,des)values('a2','hello');insert into category(skuid,des)values('a3','hello');insert into category(skuid,des)values('a4','hello');insert into category(skuid,des)values('a5','hello');insert into category(skuid,des)values('a6','hello');insert into category(skuid,des)values('a7','hello');insert into category(skuid,des)values('a8','hello');insert into category(skuid,des)values('a9','hello');insert into category(skuid,des)values('a10','hello');'''
    cursor.execute(command);
    conn.commit()
    command='''
        CREATE TABLE if not exists product(
            id SERIAL PRIMARY KEY,
            sku VARCHAR(50) references category(skuid),
            description varchar(50),
            price int,
            is_active boolean )
            '''
    cursor.execute(command);
    conn.commit()
    
    app.run()
    
