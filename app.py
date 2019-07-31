from bs4 import BeautifulSoup
import requests, smtplib, config, pymysql, config
from flask import Flask, render_template, request

app = Flask(__name__)

db = pymysql.connect(config.host, config.user, config.password, config.table)

### FLASK ### 
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        
        
        txt_write(url) #guarda la url en el txt
        return render_template("index.html")

    return render_template("index.html")
   



def check_price(url):
    url = url
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,features="html.parser")
    price= soup.find('span', {'class':'price-tag-fraction'}).get_text()
    return price

def txt_write(url):
    url_file = open("url.txt", "a")
    
    url_file.write(url)
    url_file.write("\n")
    url_file.close()
    return "###URL SAVED###"

def txt_read():
    url_file = open("url.txt", "r")
    url_list = []
    for x in url_file:
        url_list.append(x)

    return url_list #return lista


def main():
    url_list = txt_read()
    for x in range(1,len(url_list)):
        input(url_list[x])
        #check precio de url en poscion x
        print(check_price(url_list[x])) 

main()
    
    




if __name__ == "__main__":
    app.run(debug=True)
