#https://basicweb.ru/html/tag_section.php - справочник
#http://qaru.site/questions/140124/multiple-forms-in-a-single-page-using-flask-and-wtforms - формы
#https://it-developer.in.ua/kak-izmenit-temu-v-notepad.html - стили в нодпад++
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template, json,request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from random import randint
import threading
import socket, pickle
from time import sleep
from flask import session


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("gmail.com",80))
    main_host = s.getsockname()[0]
except Exception as e:
    main_host = 'localhost'
s.close()
DOM_HERF = "/"
sicret_password = '5555'
avtor_str = 'autorisation'
delited = "delited"
raspb = Flask(__name__)
raspb.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
my_ip = main_host
my_site_port = 8080
my_port_dialog = 8050
my_first_port_for_output_IP = 9060
raspb.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_BD2.db'
raspb.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_raspb = SQLAlchemy(raspb)
herf_me = "http://" + my_ip + ':' + str(my_site_port)
key_session = "username_"+my_ip + ":" + str(my_site_port)
#http://192.168.0.100:5000/login

class GreenHouseUsers(db_raspb.Model):
    id = db_raspb.Column(db_raspb.Integer, primary_key=True)
    username = db_raspb.Column(db_raspb.String(80), unique=True, nullable=False)
    name = db_raspb.Column(db_raspb.String(80), unique=False, nullable=True)
    surname = db_raspb.Column(db_raspb.String(80), unique=False, nullable=True)
    email = db_raspb.Column(db_raspb.String(120), unique=True, nullable=True)
    sess = db_raspb.Column(db_raspb.String(30), unique=False, nullable=True)
    IP = db_raspb.Column(db_raspb.String(120), unique=False, nullable=True)
    def __repr__(self):
        return '<GreenHouseUsers {}>'.format(
            self.id)
    
db_raspb.create_all()

'''
user2 = GreenHouseUsers(username='test_user2',
                     name='Петя',
                     surname="Иванов",
                     email="testuser2@none.com")


user3 = GreenHouseUsers(username='test_user4',
                     name='Лёня',
                     surname="Иванов",
                     email="testuser4@none.com")
db_raspb.session.add(user2)
db_raspb.session.add(user3)
db_raspb.session.commit()

user_model = GreenHouseUsers.query.filter_by(username='test_user2').first()
user_model.sess = 'Yes'
user_model = GreenHouseUsers.query.filter_by(username='test_user1').first()
user_model.sess = 'No'
'''

db_raspb.session.commit() 

class InputSocket(threading.Thread):
    def __init__(self, interval, sock, parent_class, name="без имени"):
        threading.Thread.__init__(self)
        self.sock = sock
        self.parent_class = parent_class
        self.name = name
        
    def run(self):
        data = self.sock.recv(9100)
        data_arr = pickle.loads(data)  # 
        print('принял', data_arr, "напечатано в потоке", self.name )
        self.sock.close()
        self.parent_class.res = data_arr[::]
        
class LayerBetweenSocket(threading.Thread):
    def __init__(self, parent_class, name="без имени"):
        threading.Thread.__init__(self)
        self.parent_class = parent_class
        self.running = True
        self.res = [None]
        self.name = name
        
    def run(self):
        while self.running:
            write_server = InputSocket(1, self.parent_class.sock, self, name="приёма данных от сокета-клиента")
            write_server.start()
            sleep(10)
            if self.res:
                self.running = False
                print("IP принят сервером", "напечатано в потоке", self.name)
                break
            else:
                sleep(randint(1,100)*60)
                self.parent_class.soket_otpravka(self.parent_class.data) 
            #write_server.kill()
            #del write_server
        
class ProSoket():
    def __init__(self,port, host=None, name="без имени"):
        self.adres, self.port = host,port
        self.name = name
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        try:
            s.connect(("gmail.com",80))
            self.my_ip = s.getsockname()[0]
        except Exception as e:
            self.my_ip = None
            print('я не подключен к сети, не могу знать свой ip', e, 'напечатано в сокете', self.name)
        s.close()
        self.sock = socket.socket()
        if self.adres:  # если сокет является клиентом
            pass
        else: # если сервером
            self.sock.bind(('', port))
            self.login_input = None
            self.IP_input = None
        
        
    def soket_otpravka(self, data):  # data имеет вид: [Herf, IP]
        self.data = data
        print("адрес и айпи", (self.adres, self.port), 'напечатано в сокете', self.name)
        self.sock.connect((self.adres, self.port))
        data1 = pickle.dumps(data)
        self.sock.sendall(data1)
        print("отправил", 'напечатано в сокете', self.name)
        
        
    def socket_priem(self):
        if self.adres:  # если сокет является клиентом
            layer_write = LayerBetweenSocket(self, name="прослойки сокета-клиента")
            layer_write.start()
            print("запустил поток приёма сокета клиента в сокете", self.name)
        else:           #  если сокет является сервером
            input_login = SocketServer(1, self.sock, self, name="приёма авторизации пользователя")
            input_login.start()
            print("запустил поток приёма сокета сервера в сокете", self.name)

class SocketServer(threading.Thread):
    def __init__(self,interval, sock, parent_calss, name="сокета-сервера"):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
        self.interval = interval
        self.parent_calss = parent_calss
        self.name = name
        
    def run(self):
        while self.running:
            self.sock.listen(1)
            print("установил лимит подключений", "     --напечатано в потоке", self.name)
            conn, addr = self.sock.accept()
            #print("получил принимающий сокет", "     --напечатано в потоке", self.name)
            data = conn.recv(9100)
            #print("принял данные", "     --напечатано в потоке", self.name)
            data_arr = pickle.loads(data)  # Формат - [login]
            print('принял:', data_arr, "     --напечатано в потоке", self.name)
            self.parent_calss.login_input = str(data_arr[0])
            self.parent_calss.IP_input = str(data_arr[1])
            user_model = GreenHouseUsers.query.filter_by(username=str(data_arr[0])).first()
            if user_model:
                user_model.IP = str(data_arr[1])
                user_model.sess = "No"
                db_raspb.session.commit()
                print("в БД IP старого пользователя обновлен", "напечатано в потоке", self.name) 
                #GreenHouseUsers(username=str(data_arr[0]), sess="No", IP=str(data_arr[1]))
                
                #db_raspb.session.add(user2)
                #db_raspb.session.commit()  
                #print("в БД занесен новый пользователь", "напечатано в потоке", self.name)
                #session.pop('username',0)
            else:
                adding_user = GreenHouseUsers(username=str(data_arr[0]),
                                              sess="No",
                                              IP=str(data_arr[1]))
                db_raspb.session.add(adding_user)
                #session.rollback()
                #user_model = GreenHouseUsers.query.filter_by(username=str(data_arr[0])).first()
                #user_model.IP = str(data_arr[1])
                db_raspb.session.commit() 
                print("в БД занесен новый пользователь", "напечатано в потоке", self.name)
                #session.pop('username',0)
                #except Exception as e1:
                    #print("ошибка БД", e1, "напечатано в потоке", self.name)                
            
            print('Received',data_arr, repr(data), "напечатано в потоке", self.name)  
            data1 = pickle.dumps(["ok"])
            print('отправляю ["ok"]', "напечатано в потоке", self.name)
            conn.sendall(data1)
            conn.close()
            sleep(self.interval)

        


 
forms_list = []
add_flag = [False]
form_nomber = 0
form_list = []
duttons_data_list = [[['woter_on.jpg', "woter_off.jpg", "on", "off"]], 
                     [['fire_on.jpg', "fire_off.jpg", "on", "off"]],
                     [['windy_on.jpg', "windy_off.jpg", "on", "off"],
                      ['cold_on.jpg', "cold_off.jpg", "on", "off"]],
                     [['parring_on.jpg', "parring_off.jpg", "on", "off"],
                      ['windy_root_on.jpg', "windy_root_off.jpg", "on", "off"]]]
obj_list = []
loc_list = [1,1,2,2] 
#user_model = GreenHouseUsers.query.filter_by(username="not-user").first()
#if user_model:
#    print('&&&&')
#else: 
#   print('/////&&&&')
#user_model = GreenHouseUsers.query.filter_by(username="test_user4").first()
#if user_model:
#   print('222&&&&')
#else: 
#   print('222/////&&&&')
#print("сессия самом в начале", session)    
first_socket = ProSoket(my_first_port_for_output_IP, host=main_host, name="отправки IP")

first_socket.soket_otpravka([herf_me, my_ip, my_port_dialog])
first_socket.socket_priem()
my_main_soket = ProSoket(my_port_dialog, name="приёма логина")
my_main_soket.socket_priem()
my_ip = my_main_soket.my_ip or '0.0.0.0'


class AddFlagForm(FlaskForm):
    #login = StringField('логин', validators=[DataRequired()], id="lo")
    password = StringField('пароль', validators=[DataRequired()], id="Pa")
    submit = SubmitField('Добавить', id="Clickable")
   
    
def button_form_create(form_list=None, stile_data=None, oncl=None):
    global form_nomber
    form_nomber +=1
    
    
    class Rooq(FlaskForm):
        button_on = SubmitField('yyyyy', id='button_on'+str(form_nomber))
        button_off = SubmitField('ddddd', id='button_off'+str(form_nomber))
        imgpole = StringField(str(form_nomber))
        
        
    if form_list:
        form_list.append(Rooq)
    return (Rooq, form_nomber)


def generate_list():  
    form_list = [[[*button_form_create()] for j1 in range(loc_list[i])] for i in range(4)]
    print(form_list)
    return form_list

def edit_list_buttons( name):
    global duttons_data_list, form_list
    status, nomber = name.split('/')
    nomber = int(nomber)
    for i in range(len(form_list)):
        for j in range(len(form_list[i])):   
            print(j)
            if form_list[i][j][1] != nomber:
                continue
            loc_p = duttons_data_list[i][j][::-1]
            
            duttons_data_list[i][j] = (loc_p[2::] + loc_p[:2:])[::]
            print('--------',duttons_data_list[i][j])
    
@raspb.route('/', methods=['GET', 'POST'])
def main_operator():
    global form_list, obj_list
    add_flag_form = AddFlagForm()
    print("сессия в начале", session)
    try:
        session[key_session]
        session['username']
        user_model = GreenHouseUsers.query.filter_by(username=str(session.username)).first()
        if user_model.sess != "yes":
            session.pop(key_session,0) 
        print('--')
    except Exception as e:
        print("в строке ~295 ошибка     в сесии", e)
        #return render_template('local_green_house_proba7.html', add_list_form=add_flag_form, show=add_flag[0], domen_herf=DOM_HERF) 
    print("сессия в начале", session)
    if add_flag_form.validate_on_submit():
        log_in = my_main_soket.login_input
        #-----------------------------------------------------------------------
        #        приём логина
        #-----------------------------------------------------------------------
        print("add form пришла", add_flag_form.password.data, log_in)
        user_model = GreenHouseUsers.query.filter_by(username=str(log_in)).first()
        if user_model:
            for i in range(14):
                try:
                    if str(request.environ['REMOTE_ADDR']) == user_model.IP:
                        pass
                    if user_model.IP != "None":
                        break
                except Exception as e:
                    print("IP не найден " + str(i) + "'ный раз", end=" -- ")
                    if i == 13:
                        user_model.IP = "None"
                        db_raspb.session.commit()
                sleep(0.5)
            print()
        if user_model and str(add_flag_form.password.data) == sicret_password and str(request.environ['REMOTE_ADDR']) == user_model.IP:
            print("пароль верен")
            add_flag[0] = True
            user_model = GreenHouseUsers.query.filter_by(username=str(log_in)).first()
            if user_model:
                user_model.sess = "Yes"
                user_model.IP = str(request.environ['REMOTE_ADDR'])
                db_raspb.session.commit() 
                print("в БД сессия старого пользователя обновлена")
                session[key_session] = str(log_in)
            else:
                user2 = GreenHouseUsers(username=str(log_in), sess="Yes", IP=str(request.environ['REMOTE_ADDR']))
                db_raspb.session.add(user2)
                db_raspb.session.commit()  
                print("в БД занесен новый пользователь")
                session[key_session] = str(log_in)
                #return render_template('add_file_client.html', otvet="No", herf=DOM_HERF)       
        else:
            print("не правильный пароль")
            #return render_template('add_file_client.html', otvet="No", herf=DOM_HERF)
    try:
        session[key_session]
    except Exception as e:
        print("в строке ~330 ошибка в сесии", e)
        return render_template('local_green_house_proba7.html', add_list_form=add_flag_form, show=add_flag[0], domen_herf=DOM_HERF, key_session=key_session)    
    if form_list == []:
        '''заполнение списка кнопок'''
        print('заполнение списка кнопок')
        form_list = generate_list()
        #print(form_list)           
    obj_list = [[[form_list[i][j][0],
                  form_list[i][j][1],
                  *duttons_data_list[i][j]] for j in range(len(form_list[i]))] for i in range(len(form_list))]
    print(obj_list)
    for i in range(len(obj_list)):
        #print('---', obj_list[i])
        for j in range(len(obj_list[i])):
            #print('------', obj_list[i][j])
            try:
                
                obj = obj_list[i][j][0](prefix="form" + str(form_list[i][j][1]))
                obj_list[i][j][0] = obj
                #print('---------', obj_list[i][j][0])
                #int("bfbcn")
                
                #if obj.validate_on_submit():
                    #print('нашёл на', str(i)+ str(j))
                    #obj_list[i][j][0] = obj
                    #return redirect(DOM_HERF)
                #obj_list[i][j][0] = obj
            except Exception as e:
                print('ошибка при создании объекта кнопки:', e)
    #print('form_list', form_list)
    #print('obj_list', *obj_list, sep='\n')
    return render_template('local_green_house_proba7.html', form_list=obj_list, show=add_flag[0], domen_herf=DOM_HERF, key_session=key_session)
#session1
    


@raspb.route(DOM_HERF+'get_len', methods=['GET', 'POST'])
def get_len():
    print("---------------get_len", request.form, end=" ")
    try:
        for i in range(1, sum(loc_list)+1):
            local_name = request.form['name' + str(i)]
            if local_name != '':
                name = local_name
        #print(name)
        edit_list_buttons(name)
    except Exception as e:
        print("ошибка в приёме данных", e)
        name = 'None'
    #print()
    image = "static/web_cam.jpg"
    if name == "off/5":
        image = "static/web_cam1.jpg"
    elif name =="off/4":     
        image = "static/web_cam2.jpg"
    return json.dumps({'len': len("dfhxdfhdf"), "image": image, 'temp': randint(19,26), 'humory': randint(40,98)})

@raspb.route(DOM_HERF + 'logout')
def logout():
    session.pop(key_session,0)
    return redirect('/')



if __name__ == '__main__':
    #input_IP_obj = InputIP(5)
    #input_IP_obj.start()
    raspb.run(host=my_ip, port=my_site_port)
# ---------------get_len ImmutableMultiDict([('form1-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNb2KQ.zqxuoSZpMiP1bDgI09JL06O-lN8'), ('name1', ''), ('form2-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNb2KQ.zqxuoSZpMiP1bDgI09JL06O-lN8'), ('name2', ''), ('form3-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNb2KQ.zqxuoSZpMiP1bDgI09JL06O-lN8'), ('name3', ''), ('form4-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNb2KQ.zqxuoSZpMiP1bDgI09JL06O-lN8'), ('name4', ''), ('form5-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNb2KQ.zqxuoSZpMiP1bDgI09JL06O-lN8'), ('name5', ''), ('form6-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNb2KQ.zqxuoSZpMiP1bDgI09JL06O-lN8'), ('name6', '')]) ошибка в приёме данных local variable 'name' referenced before assignment

#---------------get_len ImmutableMultiDict([('form1-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNcRhQ.wIIolV3yggyLdmrCEl2jEuwx92s'), ('form1-button_on', 'yyyyy'), ('name1', 'off/1')]) ошибка в приёме данных 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.

#---------------get_len ImmutableMultiDict([('form6-csrf_token', 'ImUyNjAzYjc2ODEwNmQ4ZjFkYzcyYTM4YTJkMGRiNjM2ODAwNDBmOTci.XNcRhQ.wIIolV3yggyLdmrCEl2jEuwx92s'), ('form6-button_on', 'yyyyy'), ('name6', 'off/6')]) ошибка в приёме данных 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.