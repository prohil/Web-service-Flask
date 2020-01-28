# -*- coding: utf-8 -*-
from flask import render_template, request, session
from app import app
from app.forms import RecognizeForm, SearchDbForm
import requests
import json
from app import db
from app.methods import get_categories, get_sites
from app.models import Site, Classes
# import time

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    with app.app_context():
        db.create_all()
    btn_names = Classes.query.all()
    print(type(btn_names))
    category_pressed = ''

    btn_names[0] = 'Авто, Мото'
    btn_names[4] = 'Анонимные прокси'
    btn_names[16] = 'Вредоносное ПО'
    btn_names[17] = 'Государство'
    btn_names[29] = 'Культура'
    btn_names[30] = 'Литература'
    btn_names[33] = 'Мультимедиа'
    btn_names[35] = 'Насилие'
    btn_names[38] = 'Некомерч. организации'
    btn_names[50] = 'Порнография'
    btn_names[52] = 'Производство'
    btn_names[55] = 'Развлечения'
    btn_names[56] = 'Аморальные'
    btn_names[59] = 'Популярные люди'
    btn_names[60] = 'Сельское хозяйство'
    btn_names[61] = 'Социальные сети'
    btn_names[69] = 'Форумы, Блоги'
    btn_names[71] = 'Взлом программ'

    search_result = []
    print(search_result)
    sites=[]
    #search_result=[]
    category = ''
    site = ''
    accuracy = 0
    #session.pop('Recognize_pressed')
    recognizeForm = RecognizeForm()
    searchForm = SearchDbForm()
    session['Recognize_pressed'] = False
    if 'View_recognition' not in session: # ---первая загрузка
        session['View_recognition'] = True
        session['View_db'] = False
        session['Categories_scroll'] = False
        session['Recognize_pressed'] = False
    print(session)

    if (request.method == 'POST'):
        for (key, value) in request.form.items():
            print('key=', key)
            if ((key == 'btn_recognize') | (key == 'btn_view_recognition') | (key == 'btn_view_db') | (key.isdigit()) | (key == 'btn_search')):
                # ---------------------------------------обработка нажатия и валидации кнопки
                if (key == 'btn_recognize'):
                    session['Recognize_pressed'] = True
                    if (recognizeForm.address_field.validate(recognizeForm)):  #
                        session['View_recognition'] = True
                        session['View_db'] = False
                        session['Validate_recogn'] = True
                    else:
                        session['Validate_recogn'] = False
                # ---------------------------------------обработка переключения двух вкладок
                if (key == 'btn_view_recognition'):
                    session['View_recognition'] = True
                    session['View_db'] = False
                else:
                    if (key == 'btn_view_db'):
                        session['View_db'] = True
                        session['View_recognition'] = False
                # ---------------------------------------обработка нажатия на скролл бар
                if (key.isdigit()):  # Нажата категория
                    session['Categories_scroll'] = True
                    session['Categories_meaning'] = str(int(key) + 1)
                    session['Search_pressed'] = False
                    session['Validate_search'] = False
                    session['Search_meaning'] = ''
                #------------------------- #Нажата кнопка поиска по базе
                if (key == 'btn_search'):
                    session['Search_pressed'] = True
                    if (searchForm.site_search_field.validate(searchForm)):  #
                        session['Categories_scroll'] = False
                        session['Categories_meaning'] = ''
                        session['Search_meaning'] = searchForm.site_search_field.data
                        session['Validate_search'] = True
                    else:
                        session['Validate_search'] = False

        if 'Categories_meaning' in session:
            if session['Categories_scroll'] == True:
                print(Classes.query.get(session['Categories_meaning']))
                category_pressed = str(Classes.query.get(session['Categories_meaning']))
                print('Category:', category_pressed)
                #req = requests.post(url='http://127.0.0.1:5002/getsites', json=json.dumps({'category': str(Classes.query.get(session['Categories_meaning']))}))
                sites = get_sites(category_pressed)

        print(session)
        if 'Search_pressed' in session:
            if ((session['Search_pressed'] == True) & (session['Validate_search'] == True)):
                print(type(session['Search_meaning']))
                search_result = get_categories(session['Search_meaning'])
                print('Поиск')
                print(search_result)
        print(session)
    if recognizeForm.address_field.validate(recognizeForm):
        print('Валидация прошла успешна')
        site = recognizeForm.address_field.data

        # Format the address - https://apple.com - www.apple.com ?
        check_db = get_categories(site)
        if check_db:
            category = check_db[0][0]
            print(category)
        else:
            print('а')
        # Check the address in the database
        if True:
            print('Выполнен запрос к серверу')
        # Post request returns a category and an accuracy
        else:
            req = requests.post(url='http://127.0.0.1:5002/', json=json.dumps({'site': site}))
            if req.status_code == requests.codes.ok:
                response = req.json()
                print('Response from server: ', response)
                # возвращается категория, точность и сайт
                category_id = response['category']
                site = response['site']
                category = str(Classes.query.get(category_id))
                add_site(site, category)

        # append result to the db
    return render_template('index.html', title='Category Recognition',
                           recognizeForm=recognizeForm, searchForm=searchForm, btn_names=btn_names,
                           site=site, category=category, category_pressed=category_pressed,
                           session=session,
                           sites=sites, search_result=search_result)
