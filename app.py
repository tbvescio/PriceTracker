from bs4 import BeautifulSoup
import requests, smtplib, config, pymysql, config, time 
from flask import Flask, render_template, request, abort


app = Flask(__name__)


### FLASK ### 
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        mail = request.form['mail']
        

        try: #comprueba que la url sea valida
            price = check_price(url)
        except:
            abort(404)


        save_sql(url,price,mail) #guarda los datos
        
        
        return render_template("index.html")

    return render_template("index.html")
   


def save_sql(url, price,mail):
    try:
        db = pymysql.connect(config.host, config.user, config.password, config.table)
        cursor = db.cursor()
        sql = "INSERT INTO price(ID,URL,PRICE,MAIL) VALUES (ID, '{}', {}, '{}')".format(url,price,mail)
        cursor.execute(sql)
        db.commit()
        cursor.close

        return "SAVED"
    except:
        return "NOT! SAVED"


def get_row(id):
    db = pymysql.connect(config.host, config.user, config.password, config.table)
    cursor = db.cursor()
    sql = "select * from price where ID = {}".format(id)
    cursor.execute(sql)
    row = cursor.fetchone() #devuelve una lista
    db.commit()
    cursor.close
    row = row[1:] #selecciona todo menos el id
    return row


def get_ids():
    db = pymysql.connect(config.host, config.user, config.password, config.table)
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM price" #devuelve cuantas rows hay
    cursor.execute(sql)
    ids = cursor.fetchone()[0]
    db.commit()
    cursor.close
    return ids



def check_price(url):
    url = url
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,features="html.parser")
    #elemento html que parsea
    price= soup.find('span', {'class':'price-tag-fraction'}).get_text()
    return price

def send_email(mail, url):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(config.username, config.password_mail)
    msg_url = "THE PRICE IS LOWER!\n {}".format(url) #envia el msg + la url
    server.sendmail("pythonscript640@gmail.com", 
                    mail, #dirrecion a la que manda
                    msg_url)
    server.quit()
    return



def main():
    while True:
        ids = get_ids()
        for i in (1,ids+1): #recorre todo las entradas
            row = get_row(i)
            price = check_price(row[0])
            
            if int(price) < row[1]: #compara el precio nuevo con viejo 
                send_email(row[2], row[0]) #dir. email , url
        
        return
        time.sleep(600) #espera 10 min




    




if __name__ == "__main__":
    app.run(debug=True)
    main()
