#https://basicweb.ru/html/tag_section.php - справочник
#http://qaru.site/questions/140124/multiple-forms-in-a-single-page-using-flask-and-wtforms - формы
#https://it-developer.in.ua/kak-izmenit-temu-v-notepad.html - стили в нодпад++
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template, session, json,request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from random import randint


DOM_HERF = "/"
sicret_password = '5555'
avtor_str = 'autorisation'
delited = "delited"
raspb = Flask(__name__)
raspb.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
my_ip = '192.168.0.104'
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
    
@raspb.route('/', methods=['GET', 'POST'])
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




if __name__ == '__main__':
    raspb.run(port=8000, host=my_ip)