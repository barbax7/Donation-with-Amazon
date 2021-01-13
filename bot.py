import os
import random
import time

import psycopg2
import requests
import telebot
from amazon.exception import AmazonException
from amazon.paapi import AmazonAPI
from flask import Flask, render_template, request
from telebot import types

'''Sito: http://www.donationwithamazon.it'''

token=os.environ['BOT_TOKEN'] #token bot telegram
bot = telebot.AsyncTeleBot(token)
app = Flask(__name__)

#TODO: Funzione per salvare tutti i messaggi in database
#TODO: Pulire tutte le funzioni db

def conn_amzn(tag):
    key =os.environ['AMAZON_KEY']
    secret =os.environ['AMAZON_SECRET']
    amazon = AmazonAPI(key, secret, tag, 'IT')
    return amazon

#Connessione al database PostgreSQL
def conn_db():
    conn = psycopg2.connect(os.environ['DATABASE_URL'],sslmode='require')
    return conn

def onlus(userid):
    m=types.InlineKeyboardMarkup()
    conn=conn_db()
    cur=conn.cursor()
    cur.execute(f"SELECT tag FROM utenti WHERE userid={userid}")
    a=cur.fetchall()
    el=a[0][0].split(',')
    for i in tag.keys():
        if i in el:
            b=types.InlineKeyboardButton(f'✅ {i}',callback_data=i)
            m.add(b)
        else:
            b=types.InlineKeyboardButton(f'{i}',callback_data=i)
            m.add(b)
    b=types.InlineKeyboardButton('Finito', callback_data='finito')
    m.add(b)
    return m

def check(userid):
    conn=conn_db()
    cur=conn.cursor()
    cur.execute("SELECT userid from utenti WHERE userid='{}'".format(userid))
    a=cur.fetchall()
    try:
        if a[0][0]==userid:
            return True
    except IndexError:
        return False

def check_tag(userid):
    conn=conn_db()
    cur=conn.cursor()
    cur.execute("SELECT tag from utenti WHERE userid='{}'".format(userid))
    a=cur.fetchall()
    t=False
    el=a[0][0].split(',')
    for i in tag.keys():
        if i in el:
            t=True
    return t

def home(message):
    bot.send_message(message.chat.id,f'Bentornato {message.from_user.first_name}. 😉\n\nManda un link amazon per ottenere il link referenziato. Per cambiare le tue Onlus preferite premi il comando /onlus.\nPer altre informazioni manda /help.').wait()

def select_tag(userid):
    bot.send_message(userid,'Quale fondazione vuoi sostenere?\nPuoi selezionarne più di una.\n\nQuando hai finito manda /finito',reply_markup=onlus(userid)).wait()


def store_db_web_access(tag,link):
    conn=conn_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO weblog VALUES ('{}','{}','{}')".format(time.strftime("%a, %d %b %Y %H:%M:%S +1h", time.localtime()),tag,link))
    conn.commit()
    cur.close()
    conn.close()

def clean_db_weblog():
    conn=conn_db()
    cur=conn.cursor()
    cur.execute("SELECT evento FROM weblog")
    a=cur.fetchall()
    for i in a:
        if time.mktime(time.strptime(i[0],"%a, %d %b %Y %H:%M:%S +1h"))<time.mktime(time.localtime())-604800:
            cur.execute("DELETE FROM weblog WHERE evento='{}'".format(i[0]))
            conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def homepage():
    return render_template('index.html',form=True)

@app.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/unicef', methods=['POST'])
def unicef():
    inputl=''
    if request.method =='POST' and 'input' in request.form:
        inputl=request.form.get('input')
        amazon=conn_amzn(tag['Unicef'])
        try:
            session = requests.Session()
            link = session.head(inputl, allow_redirects=True).url
            product=amazon.get_product(link)
            url=product.url
            return render_template('index.html',link=url,onlus='Unicef')
        except AmazonException as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Unicef\n\n{}\n\nTesto inserito nel box: {}\n\nAmazonException'.format(e,inputl))
            return render_template('errore.html',tag='Unicef', amazonexception=True,link=link_dict['Unicef'])
        except Exception as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Unicef\n\n{}\n\nTesto inserito nel box: {}'.format(e,inputl))
            return render_template('errore.html',amazonexception=False)
        finally:
            store_db_web_access('Unicef',inputl)
    

@app.route('/savethechildren', methods=['POST'])
def savethechildren():
    inputl=''
    if request.method =='POST' and 'input' in request.form:
        inputl=request.form.get('input')
        amazon=conn_amzn(tag['Save the Children'])
        try:
            session = requests.Session()
            link = session.head(inputl, allow_redirects=True).url
            product=amazon.get_product(link)
            url=product.url
            return render_template('index.html',link=url,onlus='Save the Children')
        except AmazonException as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Save the Children\n\n{}\n\nTesto inserito nel box: {}\n\nAmazonException'.format(e,inputl))
            return render_template('errore.html',tag='Save the Children', amazonexception=True,link=link_dict['Save the Children'])
        except Exception as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Save the Children\n\n{}\n\nTesto inserito nel box: {}'.format(e,inputl))
            return render_template('errore.html',amazonexception=False)
        finally:
            store_db_web_access('Save the Children',inputl)
    

@app.route('/caritas', methods=['POST'])
def caritas():
    inputl=''
    if request.method =='POST' and 'input' in request.form:
        inputl=request.form.get('input')
        amazon=conn_amzn(tag['Caritas'])
        try:
            session = requests.Session()
            link = session.head(inputl, allow_redirects=True).url
            product=amazon.get_product(link)
            url=product.url
            return render_template('index.html',link=url,onlus='Caritas')
        except AmazonException as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Caritas\n\n{}\n\nTesto inserito nel box: {}\n\nAmazonException'.format(e,inputl))
            return render_template('errore.html',tag='Caritas', amazonexception=True,link=link_dict['Caritas'])
        except Exception as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Caritas\n\n{}\n\nTesto inserito nel box: {}'.format(e,inputl))
            return render_template('errore.html',amazonexception=False)
        finally:
            store_db_web_access('Caritas',inputl)
    

@app.route('/bancoalimentare', methods=['POST'])
def bancoalimentare():
    inputl=''
    if request.method =='POST' and 'input' in request.form:
        inputl=request.form.get('input')
        amazon=conn_amzn(tag['Banco alimentare'])
        try:
            session = requests.Session()
            link = session.head(inputl, allow_redirects=True).url
            product=amazon.get_product(link)
            url=product.url
            return render_template('index.html',link=url,onlus='Banco alimentare')
        except AmazonException as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Banco alimentare\n\n{}\n\nTesto inserito nel box: {}\n\nAmazonException'.format(e,inputl))
            return render_template('errore.html',tag='Banco alimentare', amazonexception=True,link=link_dict['Banco alimentare'])
        except Exception as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Banco alimentare\n\n{}\n\nTesto inserito nel box: {}'.format(e,inputl))
            return render_template('errore.html',amazonexception=False)
        finally:
            store_db_web_access('Banco alimentare',inputl)
    

@app.route('/telethon', methods=['POST'])
def telethon():
    inputl=''
    if request.method =='POST' and 'input' in request.form:
        inputl=request.form.get('input')
        amazon=conn_amzn(tag['Telethon'])
        try:
            session = requests.Session()
            link = session.head(inputl, allow_redirects=True).url
            product=amazon.get_product(link)
            url=product.url
            return render_template('index.html',link=url,onlus='Telethon')
        except AmazonException as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Telethon\n\n{}\n\nTesto inserito nel box: {}\n\nAmazonException'.format(e,inputl))
            return render_template('errore.html',tag='Telethon', amazonexception=True,link=link_dict['Telethon'])
        except Exception as e:
            bot.send_message(me,'Si è presentato il seguente errore dal sito:\n\nTag: Telethon\n\n{}\n\nTesto inserito nel box: {}'.format(e,inputl))
            return render_template('errore.html',amazonexception=False)
        finally:
            store_db_web_access('Telethon',inputl)


@bot.callback_query_handler(func=lambda call: call.data=='finito')
def next(call):
    bot.edit_message_text('Abbiamo salvato le tue Onlus preferite. Ora ti basta mandare il link di un prodotto Amazon per ricevere un link referenziato, le cui commissioni saranno devolute a una Onlus scelta casualmente tra le tue preferite.\nPotrai modificare le Onlus preferite con il comando /onlus',call.message.chat.id,call.message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def salva_onlus(call):
    conn=conn_db()
    cur=conn.cursor()
    cur.execute(f"SELECT tag FROM utenti WHERE userid='{call.message.chat.id}'")
    a=cur.fetchall()
    tag=a[0][0].split(',')
    if None in tag:
        tag.remove(None)
    if call.data in tag:
        tag.remove(call.data)
    else:
        tag.append(call.data)
    el=''
    for i in tag:
        if not i=='':
            el=el+i+','
    cur.execute(f"UPDATE utenti SET tag='{el}' WHERE userid='{call.message.chat.id}'")
    conn.commit()
    cur.close()
    conn.close()
    bot.edit_message_text('Quale fondazione vuoi sostenere?\nPuoi selezionarne più di una.\n\nQuando hai finito manda /finito',call.message.chat.id,call.message.message_id,reply_markup=onlus(call.message.chat.id))

@bot.message_handler(commands=['onlus'])
def change_onlus(message):
    bot.send_message(message.chat.id,'Quale fondazione vuoi sostenere?\nPuoi selezionarne più di una.\n\nQuando hai finito manda /finito',reply_markup=onlus(message.chat.id))

@bot.message_handler(commands=['finito'])
def next_command(message):
    bot.send_message(message.chat.id,'Abbiamo salvato le tue Onlus preferite. Ora ti basta mandare il link di un prodotto Amazon per ricevere un link referenziato, le cui commissioni saranno devolute a una Onlus scelta casualmente tra le tue preferite.\nPotrai modificare le Onlus preferite con il comando /onlus').wait()

@bot.message_handler(commands=['help'])
def send_help(message):
    text='❗️AIUTO❓\n\nDopo aver selezionato le tue Onlus preferite, ossia le Onlus a cui vorresti destinare le donazioni, è sufficiente mandare un link di un prodotto Amazon. Io mi occuperò del resto, creerò un link referenziato, e se acquisterai il prodotto dal mio link riceverò una commissione con un codice speciale. Saprò quindi che quella commissione sarà destinata a una specifica Onlus.\n\nOgni primo del mese verrà mandato un report relativo al mese precedente e verranno effettuate le donazioni.\n\nAbbiamo anche un sito in cui potranno essere svolte le stesse funzioni del bot, utile per chi non ha Telegram o per lavorare da PC: www.donationwithamazon.it.\n\nSei uno sviluppatore? Supportaci migliorando il codice: https://github.com/barbax7/Donation-with-Amazon\n\nElenco dei comandi disponibili:\n/start - Avvia il bot e porta alla pagina principale\n/help - Manda questo messaggio\n/onlus - Cambia le Onlus preferite'
    bot.send_message(message.chat.id, text).wait()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn=conn_db()
    cur = conn.cursor()
    cur.execute('SELECT userid FROM utenti;')
    a=cur.fetchall()
    found=False
    for i in a:
        if message.chat.id==i[0]:
            found=True
    if found==False:
        cur.execute(f"INSERT INTO utenti (userid,tag) VALUES ({message.chat.id},1)")
        conn.commit()
        bot.send_message(message.chat.id,f'Benvenuto {message.from_user.first_name}!\n\nSono contento che hai deciso di utilizzare me per i tuoi acquisti. 😍\nOgni ricavato dalle commissioni pubblicitare verrà devoluto in donazione alla fondazione ONLUS che tu sceglierai.\nProcediamo quindi con la registrazione. 👇🏻').wait()
        select_tag(message.chat.id)
        cur.close()
        conn.close()
    else:
        home(message)

@bot.message_handler(regexp="www.amazon")
def ref_link(message):
    if check(message.chat.id) and check_tag(message.chat.id):
        for i in message.entities:
            if i.type.lower()=='url':
                link=message.text[i.offset:i.offset+i.length]
                break
        try:
            conn=conn_db()
            cur=conn.cursor()
            cur.execute("SELECT tag FROM utenti WHERE userid='{}'".format(message.chat.id))
            a=cur.fetchall()
            cur.close()
            conn.close()
            lista=a[0][0].split(',')
            lista.remove('1')
            lista.remove('')
            indice=random.randint(0,len(lista)-1)
            amazon=conn_amzn(tag[lista[indice]])
            product=amazon.get_product(link)
            text=f'***{product.title}***\n\n{product.url}\n\n€ {product.prices.price.value}\n\nEffettuando l\'acquisto da questo link sosterrai: {lista[indice]}'
            bot.send_photo(message.chat.id,product.images.large,text, parse_mode='Markdown').wait()
        except AmazonException as e:
            bot.send_message(message.chat.id, f'C\'è stato un problema con i server di Amazon. Usa questo link per accedere ad Amazon e sostenere {lista[indice]}\n{link_dict[indice]}').wait()
            bot.send_message(me, f'Errore dopo l\'invio di un link.\n\n{e}n\nLink normale: {message.text}\n\nUtente: {message.chat.id}\n\nAmazonException').wait()
        except Exception as e:
            bot.send_message(message.chat.id, 'C\'è stato un problema con il link. Riprova fra 5 minuti').wait()
            bot.send_message(me, f'Errore dopo l\'invio di un link.\n\n{e}n\nLink normale: {message.text}\n\nUtente: {message.chat.id}').wait()
    elif check(message.chat.id) and not check_tag(message.chat.id):
        bot.send_message(message.chat.id,'Non hai salvato nessuna Onlus preferita, premi /onlus').wait()
    else:
        bot.send_message(message.chat.id,'Non sei registrato, manda /start per avviare la registrazione.').wait()

@bot.message_handler(regexp='amzn.to')
def ref_short_link(message):
    if check(message.chat.id) and check_tag(message.chat.id):
        for i in message.entities:
            if i.type.lower()=='url':
                link= message.text[i.offset:i.offset+i.length]
                break
        session = requests.Session()
        short_url=link
        url = session.head(short_url, allow_redirects=True).url
        try:
            conn=conn_db()
            cur=conn.cursor()
            cur.execute("SELECT tag FROM utenti WHERE userid='{}'".format(message.chat.id))
            a=cur.fetchall()
            cur.close()
            conn.close()
            lista=a[0][0].split(',')
            lista.remove('1')
            lista.remove('')
            indice=random.randint(0,len(lista)-1)
            amazon=conn_amzn(tag[lista[indice]])
            product=amazon.get_product(url)
            bot.send_chat_action(message.chat.id,'Sto inviando un link...')
            text=f'***{product.title}***\n\n{product.url}\n\n€ {product.prices.price.value}\n\nEffettuando l\'acquisto da questo link sosterrai: {lista[indice]}'
            bot.send_photo(message.chat.id,product.images.large,text, parse_mode='Markdown').wait()
        except AmazonException:
            bot.send_message(message.chat.id, f'C\'è stato un problema con i server di Amazon. Usa questo link per accedere ad Amazon e sostenere {lista[indice]}\n{link_dict[indice]}').wait()
            bot.send_message(me, f'Errore dopo l\'invio di un link.\n\n{e}n\nLink breve: {message.text}\n\nUtente: {message.chat.id}\n\nAmazonException').wait()
        except Exception as e:
            bot.send_message(message.chat.id, 'C\'è stato un problema con il link. Riprova fra 5 minuti').wait()
            bot.send_message(me, f'Errore dopo l\'invio di un link.\n\n{e}\n\nLink breve: {message.text}\n\nUtente: {message.chat.id}').wait()
    elif check(message.chat.id) and not check_tag(message.chat.id):
        bot.send_message(message.chat.id,'Non hai salvato nessuna Onlus preferita, premi /onlus').wait()
    else:
        bot.send_message(message.chat.id,'Non sei registrato, manda /start per avviare la registrazione.').wait()

if __name__ == "__main__":
    import variabili  # Dizionari con i partner tag e i link brevi
    tag=variabili.tag #Partner tag creati con Amazon Associates
    link_dict=variabili.link_dict #Link refereniati alla homepage di Amazon creati con SiteStripe
    me=variabili.me #Userid del contatto Telegram
    clean_db_weblog()
    bot.remove_webhook()
    time.sleep(1)
    heroku=os.environ['HEROKU_LINK'] #Link su cui si trova la webapp
    bot.set_webhook(url=heroku + token)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    
