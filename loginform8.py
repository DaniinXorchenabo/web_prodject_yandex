#https://basicweb.ru/html/tag_section.php - справочник
#http://qaru.site/questions/140124/multiple-forms-in-a-single-page-using-flask-and-wtforms - формы
#https://it-developer.in.ua/kak-izmenit-temu-v-notepad.html - стили в нодпад++
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from time import sleep
from flask import Flask, redirect, render_template, session, json,request
from PIL import Image
from random import randint
import threading
import socket, pickle



class InputIP(threading.Thread):
    def __init__(self,interval, sock, parent_class, host=True, name="без имени"):
        threading.Thread.__init__(self)
        self.parent_class = parent_class
        self.sock = sock
        self.host = host
        self.name = name
        
    def run(self):
        if self.host:  # режим сервера
            self.sock.listen(1)
            request1 = self.sock.recv(4096)
            data_arr = pickle.loads(otvet)
            print('принял:',data_arr, "    --напечатано в потоке", self.name)
            self.parent_class.input_answer = data_arr[0] 
        else:  # режим клиента
            
            data = self.sock.recv(9100)
            data_arr = pickle.loads(data)  # Формат - Ссылка, IP
            print('принял:', data_arr, "    --напечатано в потоке", self.name) 
            self.sock.close()
            self.parent_class.res = data_arr[::]
          
        
class AddToDictHerfsAndIP(threading.Thread):
    def __init__(self,interval, sock, dict_IP, name="без имени"):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
        self.interval = interval
        self.dict_IP = dict_IP
        self.name = name
        
    def run(self):
        
        while self.running:
            #print('сервер 9060 работает', "    --напечатано в потоке", self.name)
            self.sock.listen(1)
            #print('установил лимит подключений', "    --напечатано в потоке", self.name)
            conn, addr = self.sock.accept()
            print('Sock name: {}'.format(self.sock.getsockname()), "    --напечатано в потоке", self.name)
            #print('жду данные', "    --напечатано в потоке", self.name)
            data = conn.recv(9100)
            print("данные пришли", "    --напечатано в потоке", self.name)
            data_arr = pickle.loads(data)  # Формат - Ссылка, IP
            #print('принял', "    --напечатано в потоке", self.name)
            print('принял',data_arr, "    --напечатано в потоке", self.name)  
            try:
                self.dict_IP[data_arr[0]] = (data_arr[1], int(data_arr[2]))
                print('занёс в словарь', "    --напечатано в потоке", self.name) 
                data1 = pickle.dumps(["ok"])
                print('отправляю ["ok"]', "    --напечатано в потоке", self.name)
            except Exception as e:
                print("ошибка при добавлении в словарь IP", e, "    --напечатано в потоке", self.name)
                data1 = pickle.dumps(["No"])
            conn.sendall(data1)
            conn.close()
            #-------------------------------------------------------------------
            #       занесение в словарь, обработка ответа
            #-------------------------------------------------------------------
            
            sleep(self.interval)
        
        
class ProSoket():
    def __init__(self, port, dict_IP=None, host=None, name="без имени"):
        self.adres, self.port = host ,port
        self.name = name
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("gmail.com",80))
            self.my_ip = s.getsockname()[0]
            print('мои ip', self.my_ip, "    --напечатано в сокете", self.name)
        except Exception as e:
            self.my_ip = None
            print('я не подключен к сети, не могу знать свой ip', e, "    --напечатано в сокете", self.name)
        s.close()
        self.sock = socket.socket()
        if host: # клиент
            self.data = None
            self.res = None
        else: # сервер
            self.dict_IP = dict_IP
            self.sock_first = socket.socket()
            print('запущен как сервер', self.port, "    --напечатано в сокете", self.name)
            self.sock_first.bind(('', self.port))        
            self.data_arr = []
            self.first_input =  AddToDictHerfsAndIP(1, self.sock_first, dict_IP, name="приёма IP теплиц")
            self.input_answer = None
        
    def add_to_dict_herfs_and_ip(self):
        self.first_input.start()
        print('процесс добавления теплиц запущен....', "    --напечатано в сокете", self.name)
        
    def input_requests(self, connect_sock=False):
        if self.adres:  # клиент
            if connect_sock:
                self.sock.connect((self.adres, int(self.port)))
            locak_obj = InputIP(1, self.sock, self, host=False, name="приёма данных в режиме клиента")
            locak_obj.start()
        else:
            
            locak_obj = InputIP(1, self.sock, self, name="приёма данных в режиме сервера")
            locak_obj.start()
        
    def output_data(self, data, connect_sock=False):
        self.data = data  # массив [Login, IP]
        if self.adres:  # ЕСЛИ КЛИЕНТ
            if connect_sock:
                self.sock.connect((self.adres, self.port))
            data1 = pickle.dumps(data)
            self.sock.sendall(data1)  
            print("отправил:", data, "    --напечатано в сокете", self.name)
                       
        
dict_herfs_and_ip = dict()  
my_main_soket = ProSoket(9060, dict_IP=dict_herfs_and_ip, name="занесения IP теплиц в словарь")
my_main_soket.add_to_dict_herfs_and_ip()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///u6.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SERVER_NAME'] = '195.78.126.85'
db = SQLAlchemy(app)
who_go_id = -1
users_dict = dict()   
my_ip = my_main_soket.my_ip or '0.0.0.0'
dict_herfs_and_ip['http://' + my_ip +':5000/1'] = (my_ip, 8081,)
dict_herfs_and_ip['http://' + my_ip +':5000/2'] = (my_ip, 8082,)
dict_herfs_and_ip['http://' + my_ip +':5000/3'] = (my_ip, 8083,)
dict_herfs_and_ip['http://' + my_ip +':5000/4'] = (my_ip, 8084,)
dict_herfs_and_ip['http://' + my_ip +':5000/5'] = (my_ip, 8085,)
dict_herfs_and_ip['http://' + my_ip +':8090/1'] = (my_ip, 8086,)
dict_herfs_and_ip['http://' + my_ip +':8090/2'] = (my_ip, 8087,)
#db_raspb = SQLAlchemy(raspb)

 
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


class UsersClassBD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passwod = db.Column(db.String(150), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    green_houses = db.Column(db.String(3000), unique=False, nullable=True)
    #code = db.Column(db.String(1000), unique=False, nullable=True)
 
    def __repr__(self):
        return '<UsersClassBD {} {} {} {} {} {} {} >'.format(
            self.id, self.username, self.passwod,
                self.name, self.surname, self.email, str(self.green_houses) + ' *')



    
    
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
     
     
class AddGreenHouseForm(FlaskForm):
    herf = StringField('URL теплицы', validators=[DataRequired()])
    #password = PasswordField('Пароль (указан на блоке управления)', validators=[DataRequired()])
    submit = SubmitField('Добавить')
    imgpole = StringField('<img src=' + '"' + "static/for_chief_page4.jpg" +'"' + "alt='тут должна быть картинка, но её нет'>")  # 
    
    
class GetAnswerFromGreenHouse(FlaskForm):
    answer = StringField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    
    
nomber_class_delite = 1
def users_dict_controle(what, name, t=1):
    global nomber_class_delite
    if True:
        class Rooq(FlaskForm):
            delite = SubmitField('Добавить', id='delite'+str(nomber_class_delite))
    else:
        class Rooq(FlaskForm):
            delite = SubmitField('Добавить')            
    users_dict[name].append(Rooq)
    nomber_class_delite +=1
db.create_all()

'''
user1 = UsersClassBD(username='test_user1',
                     passwod=str(111),
                     name='Иван',
                     surname="Иванов",
                     email="testuser1@none.com")

user2 = UsersClassBD(username='test_user2',
                     passwod=str(111),
                     name='Петя',
                     surname="Иванов",
                     email="testuser2@none.com")

user3 = UsersClassBD(username='test_user3',
                     passwod=str(111),
                     name='Лёня1',
                     surname="Иванов1",
                     email="testuser41@none.com",
                     green_houses='http://192.168.0.102/2 http://192.168.0.102/1')

user4 = UsersClassBD(username='test_user4',
                     passwod=str(111),
                     name='Лёня',
                     surname="Иванов",
                     email="testuser4@none.com",
                     green_houses='http://192.168.0.102/2 http://192.168.0.102/1')

db.session.add(user1)
db.session.add(user2)

db.session.add(user3)
db.session.add(user4)
'''

db.session.commit()


print(UsersClassBD.query.all())
a = [UsersClassBD.query.filter_by(name='Иван')]

print(a)
print(UsersClassBD.query.filter_by(name='Петр'))

user_model = UsersClassBD.query.filter_by(username='test_user2').first()
user_model.green_houses = 'http://' + my_ip +':8090/1 ' + 'http://' + my_ip +':8090/2'
user_model = UsersClassBD.query.filter_by(username='test_user1').first()
user_model.green_houses = 'http://' + my_ip +':8090/2 '
user_model = UsersClassBD.query.filter_by(username='test_user4').first()
user_model.green_houses = 'http://' + my_ip +':8090/2 '
db.session.commit()
     

def write_session_for_green_house(login, ip, herfs):
    print("-----функция отправки авторизации")
    
    herfs = herfs.split()
    for herf in herfs:
        try:
            ip, port = dict_herfs_and_ip[herf]
            authorization_green_house = ProSoket(int(port), host=ip, name="отправки авторизации на " + ip + ':' + str(port))
            authorization_green_house.output_data([str(user_model.username), str(request.environ['REMOTE_ADDR'])], connect_sock=True)
            authorization_green_house.input_requests()
            print(" теплица с ip", ip + ':' + str(port),"прошла функция авторизации успешно")
        except Exception as e:
            print("ошибка в функции отправки авторизации у ip", ip + ':' + str(port) + ":", e)
    print("//-----завершена функция отправки авторизации")
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    add_green_house_form = AddGreenHouseForm()
    print('-------------login')
    print("IP подключившегося", request.environ['REMOTE_ADDR'])
    print(*[(i,dict_herfs_and_ip[i]) for i in dict_herfs_and_ip], sep="\n")
    try:
        print(session)
        
        session['username']
        #return redirect('/success')
        user_model = UsersClassBD.query.filter_by(username=session.username).first()
        for i in range(len(user_model.green_houses.split())-len(users_dict[user_model.username])):
            users_dict_controle('_', user_model.username ,t=i)
        print('пользовотель находится в сессии в /login')
        return redirect('/success')
    except Exception as e:
        print("ошибка в ~290 строчке", e)
    
    if form.validate_on_submit():
        user_name = str(form.username.data)
        password = str(form.password.data)
        print("регистрационная форма отправленна на сервер со следующими данными", user_name, password)
        user_model = UsersClassBD.query.filter_by(username=user_name).first()
        if user_model:
            
            print("user_model:", user_model)
            
            if user_model.passwod == password:
                session['username'] = user_name
                session['user_id'] = user_model.username
                users_dict[user_name] = []
                #who_go_id = session['user_id']
                print("session", session['user_id'], session)
                #delete_form = DeleteGreenHouseClass(
                for i in range(len(user_model.green_houses.split())-len(users_dict[user_model.username])):
                    users_dict_controle('_', user_model.username)
                return redirect('/success')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
        
    return render_template('sacsess1.html', title='Авторизация', form=form, addform=add_green_house_form, )

    
@app.route('/success', methods=['GET', 'POST'])
def sucsess():
    print('-----------success')
    try:
        session['username']
        print('залогинен')
    except Exception as e:
        print('вернуть, ибо не залогинен', e)
        return redirect('/login')        
    user_model = UsersClassBD.query.filter_by(username=session['username']).first()
    write_session_for_green_house(str(user_model.username), str(request.environ['REMOTE_ADDR']), str(user_model.green_houses))
    form = LoginForm()   
    add_green_house_form = AddGreenHouseForm()
    get_answer = GetAnswerFromGreenHouse()
    if form.validate_on_submit():
        return redirect('/login')
    try:
        session['username']
    except Exception as e:
        print('не находится в сессии', e)
    if add_green_house_form.validate_on_submit():
        
        herf = str(add_green_house_form.herf.data)
        print("---форма добавления теплицы со ссылкой", herf)
        otvet = None
        #-----------------------------------------------------------------------
        print(herf, *dict_herfs_and_ip, herf[-1], herf[:-1:], (herf[-1] == '/', herf[:-1:] in dict_herfs_and_ip,), sep="\n")
        if (herf[-1] == '/' and herf[:-1:] in dict_herfs_and_ip):
            herf = herf[:-1:]
        if (herf in dict_herfs_and_ip) or (herf + '/' in dict_herfs_and_ip) or (herf[-1] == '/' and herf[:-1:] in dict_herfs_and_ip):
            try:
                host_gr, port_gr = dict_herfs_and_ip[herf]
                print("говорим теплице, что её добавили.  IP:", host_gr, "порт:", port_gr)
                write_login = ProSoket(int(port_gr), host=host_gr, name="отправки имени пользователя на " + host_gr + ':' + str(port_gr))
                write_login.output_data([str(user_model.username), str(request.environ['REMOTE_ADDR'])], connect_sock=True)
                write_login.input_requests()
                for i in range(14):
                    if write_login.res == ["ok"]:
                        otvet = True
                        break
                    elif write_login.res != None:
                        otvet = False
                        break
                    sleep(0.5)
                print("write_login.res",write_login.res, "otvet", otvet)
            except Exception as e:
                otvet = None
                print("в строчка ~370 ошибка при попытке авторизации", e)
        #  отправка и приём ответа
        #-----------------------------------------------------------------------
        
        if otvet:
            if herf not in user_model.green_houses.split():
                user_model.green_houses += ' ' + herf
                users_dict_controle('_', user_model.username)
                db.session.commit() 
        elif otvet == False:
            print("неправельный пароль")
        else:
            print("отказ в доступе")
    herfs = user_model.green_houses.split()
    herfs = [[herfs[i], str(i + 1), None] for i in range(len(herfs))]
    #print('_+_+_',len(user_model.green_houses.split()), len(users_dict[user_model.username]),users_dict[user_model.username])
    n = None
    for i in range(len(user_model.green_houses.split()) -len(users_dict[user_model.username])): # -len(users_dict[user_model.username])
        print('удалятор добавлен')
        users_dict_controle('_', user_model.username)
    for i in range(len(user_model.green_houses.split())):
        obj = users_dict[user_model.username][i](prefix="form" + str(i))
        #print('-=-=-=-=',users_dict[user_model.username][i], obj, obj.delite, obj.delite(),'\n', obj.delite.id)
        herfs[i][2] = obj
        if obj.validate_on_submit():
            print('нашёл на', i)
            n = user_model.green_houses.split()
            n[i] = ' _ '
            user_model.green_houses = ' '.join(n[::])
    if n:
        user_model.green_houses = user_model.green_houses.replace('_', '')
        #print(user_model.green_houses)
        db.session.commit()
        print('закомитил')
        herfs = user_model.green_houses.split()
        herfs = [[herfs[i], str(i + 1), None] for i in range(len(herfs))]  
        for i in range(len(user_model.green_houses.split())):
            obj = users_dict[user_model.username][i](prefix="form" + str(i))
            herfs[i][2] = obj        

    print("ссылки:", herfs)
    return render_template('sacsess1.html', adres=my_ip+':5000', form=form, green_houses_herfs=herfs, addform=add_green_house_form)  
                                                                                                  

@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')

@app.route('/check_passwod')
def check_passwod():
    return render_template('main_input_iframe1_junga.html')

@app.route('/add_green_house')
def add_green_house_function():
    return redirect('/success')

@app.route('/delated_green_house')
def delated_green_house():
    print('-----------delated_green_house')
    return redirect('/success')

@app.route('/1')
def esucsess():
    return render_template('одностраничник.html')

@app.route('/2')
def ee():
    return render_template('одностраничник1.html')

@app.route('/3')
def e1e():
    return render_template('одностраничник1.html')


@app.route('/4')
def e2e():
    
    return render_template('print_iframe.html')
@app.route('/5')
def e3e():
    return render_template('add_file_client.html')

'''
class AddFlagForm(FlaskForm):
    login = StringField('логин', validators=[DataRequired()], id="lo")
    password = StringField('пароль', validators=[DataRequired()], id="Pa")
    submit = SubmitField('Добавить', id="Clickable")
   
    

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
'''            
        
if __name__ == '__main__':
    #server = Server()
    #server.start()
    app.run(host=my_ip)
    #raspb.run(, host=my_ip)
#a71bfaa56d12b1550a784e3c2890771c16a3f800
#a71bfaa56d12b1550a784e3c2890771c16a3f800