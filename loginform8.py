#https://basicweb.ru/html/tag_section.php - справочник
#http://qaru.site/questions/140124/multiple-forms-in-a-single-page-using-flask-and-wtforms - формы
#https://it-developer.in.ua/kak-izmenit-temu-v-notepad.html - стили в нодпад++
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template, session, json,request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from random import randint
import threading

#<Config {'ENV': 'production', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': 'yandexlyceum_secret_key', 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093}>

# button_form_create
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
my_ip = '192.168.0.104'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///u6.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
who_go_id = -1
users_dict = dict()   

DOM_HERF = "/success/10/"
sicret_password = '5555'
avtor_str = 'autorisation'
delited = "delited"
raspb = Flask(__name__)
raspb.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
my_ip = '192.168.0.104'
print(raspb.config)
raspb.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_BD1.db'
raspb.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_raspb = SQLAlchemy(raspb)

 
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
    password = PasswordField('Пароль (указан на блоке управления)', validators=[DataRequired()])
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
#user_model = UsersClassBD.query.filter_by(username='test_user3').first()
#user_model.green_houses = 'http://' + my_ip +':8090/2 '
user_model = UsersClassBD.query.filter_by(username='test_user4').first()
user_model.green_houses = 'http://' + my_ip +':8090/2 '
db.session.commit()
     

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    add_green_house_form = AddGreenHouseForm()
    print('-------------login')
    try:
        session['username']
        user_model = UsersClassBD.query.filter_by(username=session.username).first()
        for i in range(len(user_model.green_houses.split())-len(users_dict[user_model.username])):
                    users_dict_controle('_', user_model.username ,t=i)
        print('-------------')
        return redirect('/success')
    except Exception as e:
        print(e)
    
    if form.validate_on_submit():
        user_name = str(form.username.data)
        password = str(form.password.data)
        print(user_name, password)
        user_model = UsersClassBD.query.filter_by(username=user_name).first()
        if user_model:
            
            print(user_model)
            
            if user_model.passwod == password:
                session['username'] = user_name
                session['user_id'] = user_model.username
                users_dict[user_name] = []
                #who_go_id = session['user_id']
                print(session['user_id'], session)
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
    form = LoginForm()   
    add_green_house_form = AddGreenHouseForm()
    get_answer = GetAnswerFromGreenHouse()
    if form.validate_on_submit():
        return redirect('/login')
    try:
        session['username']
    except Exception as e:
        print('ошибка в форме form', e)
    if add_green_house_form.validate_on_submit():
        herf = str(add_green_house_form.herf.data)
        user_model.green_houses += ' ' + herf
        users_dict_controle('_', user_model.username)
        db.session.commit() 
        
    if add_green_house_form.validate_on_submit() or get_answer.validate_on_submit():
        print('add_green_house_form сработало')
        password = str(add_green_house_form.password.data)
        herf = str(add_green_house_form.herf.data)
        if get_answer.validate_on_submit():
            herf = str(add_green_house_form.herf.data)
            print('сработало get_answer')
            print('пришло', str(get_answer.answer.data))
            if str(get_answer.answer.data) == 'Yes':
                print('условие get_answer сработало', herf)
                
                print('теплица добавлена', user_model.green_houses)
                return redirect('/success')
            else:
                print('не сработало get_answer')
                herfs_list = user_model.green_houses.split()[:-1:]
                user_model.green_houses = ' '.join(herfs_list)
                del users_dict[user_model.username][-1]
                db.session.commit()   
                return redirect('/success')
            
        print('показать сайт отправки/приёма')        
        return render_template('main_input_iframe1_junga.html', herf=herf, password=password, form=get_answer, user_name=str(user_model.username))
        #main_input_iframe1_junga.html'''
        #return redirect('/check_passwod')
    else:
        print('add_green_house_form не сработало')
    print('2 формы успешно')
    herfs = user_model.green_houses.split()
    herfs = [[herfs[i], str(i + 1), None] for i in range(len(herfs))]
    print('_+_+_',len(user_model.green_houses.split()), len(users_dict[user_model.username]),users_dict[user_model.username])
    n = None
    for i in range(len(user_model.green_houses.split()) -len(users_dict[user_model.username])): # -len(users_dict[user_model.username])
        print('удалятор добавлен')
        users_dict_controle('_', user_model.username)
    for i in range(len(user_model.green_houses.split())):
        obj = users_dict[user_model.username][i](prefix="form" + str(i))
        print('-=-=-=-=',users_dict[user_model.username][i], obj, obj.delite, obj.delite(),'\n', obj.delite.id)
        herfs[i][2] = obj
        if obj.validate_on_submit():
            print('нашёл на', i)
            n = user_model.green_houses.split()
            n[i] = ' _ '
            user_model.green_houses = ' '.join(n[::])
    if n:
        user_model.green_houses = user_model.green_houses.replace('_', '')
        print(user_model.green_houses)
        db.session.commit()
        print('закомитил')
        herfs = user_model.green_houses.split()
        herfs = [[herfs[i], str(i + 1), None] for i in range(len(herfs))]  
        for i in range(len(user_model.green_houses.split())):
            obj = users_dict[user_model.username][i](prefix="form" + str(i))
            herfs[i][2] = obj        

    print(herfs)
    return render_template('sacsess1.html', adres=my_ip+':8000', form=form, green_houses_herfs=herfs, addform=add_green_house_form)  
                                                                                                  

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



class GreenHouseUsers(db_raspb.Model):
    id = db_raspb.Column(db_raspb.Integer, primary_key=True)
    username = db_raspb.Column(db_raspb.String(80), unique=True, nullable=False)
    name = db_raspb.Column(db_raspb.String(80), unique=False, nullable=True)
    surname = db_raspb.Column(db_raspb.String(80), unique=False, nullable=True)
    email = db_raspb.Column(db_raspb.String(120), unique=True, nullable=True)
    sess = db_raspb.Column(db_raspb.String(30), unique=False, nullable=True)
 
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


class AddFlagForm(FlaskForm):
    login = StringField('логин', validators=[DataRequired()], id="lo")
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
    
@raspb.route(DOM_HERF, methods=['GET', 'POST'])
def main_operator():
    global form_list, obj_list
    add_flag_form = AddFlagForm()
    if add_flag_form.validate_on_submit():
        print("add form пришла", add_flag_form.password.data, add_flag_form.login.data)
        if str(add_flag_form.password.data) == sicret_password:
            print("пароль верен")
            add_flag[0] = True
            try:
                user2 = GreenHouseUsers(username=str(add_flag_form.login.data), sess="Yes")
                db_raspb.session.add(user2)
                db_raspb.session.commit()  
                print("в БД занесен новый пользователь")
            except Exception as e:
                try:
                    user_model = GreenHouseUsers.query.filter_by(username=str(add_flag_form.login.data)).first()
                    user_model.sess = "Yes"
                    db_raspb.session.commit() 
                    print("в БД сессия старого пользователя обновлена")
                except Exception as e1:
                    print("ошибка БД", e1)
                    add_flag[0] = False
                    return render_template('add_file_client.html', otvet="No", herf=DOM_HERF)
            if add_flag[0]:
                print("вернуть 'Да'")
                return render_template('add_file_client.html', otvet="Yes", herf=DOM_HERF)
            
        elif str(add_flag_form.password.data) == avtor_str:
            print("если это авторизация теплицы")
            try:
                user_model = GreenHouseUsers.query.filter_by(username=str(add_flag_form.login.data)).first()
                if user_model.sess == "Yes":
                    session['username'] = user_model.username
                    user_model.sess = "Yes"
                    add_flag[0] = True
                    print("сессия одобрена")
                else:
                    print("сессия не одобрена")
            except Exception as e1:
                print("ошибка", e1)
                add_flag[0] = False
        elif str(add_flag_form.password.data) == delited:
            print("если это удаление теплицы")
            try:
                
                del session['username']
                user_model = GreenHouseUsers.query.filter_by(username=str(add_flag_form.login.data)).first()
                user_model.sess = "No"
                add_flag[0] = False
                print("удалить")
            except Exception as e1:
                print("ошибка при удалении", e1)
                add_flag[0] = False            
        else:
            print("не правильный пароль")
            return render_template('add_file_client.html', otvet="No", herf=DOM_HERF)
    if add_flag[0]:
        if form_list == []:
            '''заполнение списка кнопок'''
            print('заполнение списка кнопок')
            form_list = generate_list()
            print(form_list)           
        obj_list = [[[form_list[i][j][0],
                      form_list[i][j][1],
                      *duttons_data_list[i][j]] for j in range(len(form_list[i]))] for i in range(len(form_list))]
        for i in range(len(obj_list)):
            print('---', obj_list[i])
            for j in range(len(obj_list[i])):
                print('------', obj_list[i][j])
                try:
                    
                    obj = obj_list[i][j][0](prefix="form" + str(form_list[i][j][1]))
                    obj_list[i][j][0] = obj
                    print('---------', obj_list[i][j][0])
                    int("bfbcn")
                    if obj.validate_on_submit():
                        print('нашёл на', str(i)+ str(j))
                        obj_list[i][j][0] = obj
                        return redirect(DOM_HERF)
                    obj_list[i][j][0] = obj
                except Exception as e:
                    print('ошибка при создании объекта кнопки:', e)
        print('form_list', form_list)
        print('obj_list', *obj_list, sep='\n')
        return render_template('local_green_house_proba7.html', form_list=obj_list, show=add_flag[0], domen_herf=DOM_HERF)
    else:
        return render_template('local_green_house_proba7.html', add_list_form=add_flag_form, show=add_flag[0], domen_herf=DOM_HERF)
    


@raspb.route(DOM_HERF+'get_len', methods=['GET', 'POST'])
def get_len():
    print("---------------get_len", request.form, end=" ")
    try:
        for i in range(1, sum(loc_list)+1):
            local_name = request.form['name' + str(i)]
            if local_name != '':
                name = local_name
        print(name)
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


#def ff():
    #app.run(port=8080, host=my_ip)
    
    
class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)  
    def run(self):
        ff()
        
if __name__ == '__main__':
    #server = Server()
    #server.start()
    app.run(port=8080, host=my_ip)
    raspb.run(port=8080, host=my_ip)
