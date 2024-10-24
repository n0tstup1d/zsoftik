import asyncio
import data.db_helper as db_helper
import requests
from multiprocessing import Lock
import uniq.uniq_confetti as uniq_confetti
import sys
import time
import json
import random
import re
import os
import imaplib
import email
import string
import traceback
lock = Lock()
error_message = traceback.format_exc()
from openpyxl import Workbook, load_workbook
from datetime import datetime

def append_to_excel(file_path, unique_id):
  try:
    # Попробуем загрузить существующую книгу
    workbook = load_workbook(file_path)
    sheet = workbook.active
  except FileNotFoundError:
    # Если файл не существует, создаем новую книгу
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Лист1"

  # Находим первую пустую строку
  next_row = sheet.max_row + 1

  # Формируем значение для столбца A (с символом @)
  account_value = f"@{unique_id}"

  # Текущая дата и время для столбца B
  current_time = datetime.now().strftime("%m/%d/%Y %H:%M")

  # Записываем в столбец A и B
  sheet[f"A{next_row}"] = account_value
  sheet[f"B{next_row}"] = current_time

  # Сохраняем изменения
  workbook.save(file_path)
  print(f"Запись {account_value} успешно добавлена в файл.")


def get_random_avatar(directory):
    # Получаем список всех файлов в папке
    try:
      files = os.listdir(directory)
    except Exception as e:
      print('opa')
      print(e)

    # Фильтруем список, оставляя только файлы с изображениями (например, .jpg, .png)
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Если в папке нет изображений, возвращаем None
    if not image_files:
        return None

    # Выбираем случайный файл из списка
    random_file = random.choice(image_files)

    return random_file

def upload_image_to_fileio(file_path):
    url = "https://file.io"

    # Открываем файл изображения
    with open(file_path, 'rb') as image_file:
        files = {
            'file': image_file,
        }
        # Отправляем POST-запрос для загрузки изображения
        response = requests.post(url, files=files)

        if response.status_code == 200:
            json_response = response.json()
            if json_response['success']:
                download_url = json_response['link']  # Извлекаем ссылку на файл
                return download_url
            else:
                print("Ошибка на стороне сервера File.io")
                return None
        else:
            print(f"Ошибка при загрузке: {response.status_code}")
            return None

def generate_random_string():
    length = random.randint(10, 20)  # Выбираем случайную длину строки
    letters = string.ascii_lowercase  # Строчные буквы
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_string_with_symbols():
    length = random.randint(8, 11)  # Выбираем случайную длину строки
    characters = string.ascii_lowercase + string.digits   # Строчные буквы, цифры и символы
    return ''.join(random.choice(characters) for _ in range(length))



# Функция для случайного выбора почтового домена
async def get_random_email_domain():
    email_domains = [
        "@gmail.com",
        "@yahoo.com",
        "@outlook.com",
        "@hotmail.com",
        "@icloud.com",
        "@protonmail.com",
        "@zoho.com",
        "@aol.com",
        "@gmx.com",
        "@fastmail.com"
    ]
    return random.choice(email_domains)

def my_function(log_queue, i):
    version = asyncio.run(db_helper.get_app_version())
    info = asyncio.run(db_helper.fetch_data())
    locale = asyncio.run(db_helper.get_current_locale())
    api_key = asyncio.run(db_helper.get_token())
    # api_key = '33e6ed01c2dc4bf1901854d8a6696bae'
    region = asyncio.run(db_helper.get_geo_zaliv())
    SOURCE = 'xiaomi_devices'
    while True:
        try:
            proxy_m_o_o = asyncio.run(db_helper.get_proxy_value())
            if proxy_m_o_o == 'TRUE':
                with lock:
                    try:
                        proxy_id, proxy_value = asyncio.run(db_helper.get_proxy_mobile())
                        if proxy_id and proxy_value:
                            print(f"Found Proxy ID: {proxy_id}, Proxy: {proxy_value}")
                            # Удаляем строку по id
                            asyncio.run(db_helper.delete_proxy_mobile_by_id(proxy_id))
                            print(f"Deleted Proxy with ID: {proxy_id}")
                        else:
                            print("No proxy found.")
                    except:
                        log_queue.put(f"[{i}] что то не так с прокси(")
                        continue
            else:
                with lock:
                    try:
                        # Получаем прокси и его id
                        proxy_id, proxy_value = asyncio.run(db_helper.get_proxy())
                        if proxy_id and proxy_value:
                            print(f"Found Proxy ID: {proxy_id}, Proxy: {proxy_value}")
                            # Удаляем строку по id
                            asyncio.run(db_helper.delete_proxy_by_id(proxy_id))
                            print(f"Deleted Proxy with ID: {proxy_id}")
                        else:
                            print("No proxy found.")
                    except:
                        log_queue.put(f"[{i}] что то не так с прокси(")
                        continue
            if proxy_m_o_o == 'TRUE':
                print(123)
                try:
                    update_url = proxy_value.split('|')[1]
                    print(update_url)
                    proxy_inf = proxy_value.split('|')[0]
                    print(proxy_inf)
                    proxy = f"http://{proxy_inf.split(':')[2]}:{proxy_inf.split(':')[3]}@{proxy_inf.split(':')[0]}:{proxy_inf.split(':')[1]}"
                    requests.get(update_url)
                except Exception as e:
                    print(e)
            else:
                proxy = f"http://{proxy_value.split(':')[2]}:{proxy_value.split(':')[3]}@{proxy_value.split(':')[0]}:{proxy_value.split(':')[1]}"
        except Exception as e:
            print(e)
        birthday = f"{random.randint(1980, 2001)}-{random.randint(10, 12)}-{random.randint(10, 28)}"
        print(birthday)
        random_email_domain = asyncio.run(get_random_email_domain())
        random_string = generate_random_string()
        fake_mail = f'{random_string}{random_email_domain}'
        fake_passt = generate_random_string_with_symbols()
        fake_pass = fake_passt + "@A"
        print(fake_pass)
        print(fake_mail)
        try:
            url = "http://lumiservices.net/v1/passport/email/signup"
            payload ={
                      "email": f"{str(fake_mail)}",
                      "password": f"{str(fake_pass)}",
                      "birthday": f"{str(birthday)}"
                    }
            print(proxy)

            headers = {
                'x-proxy': proxy,
                'x-region': region,
                'x-api-key': api_key,
                'x-project-name': 'tokapi'
            }
            print(SOURCE)
            print(version)
            print(payload)
            print(headers)
            signup_result = requests.post(url, json=payload,params={'app_version': version, 'source': SOURCE}, headers=headers)
            try:
                print(signup_result.status_code)
            except Exception as e:
                print(e)
            data = json.loads(signup_result.text)
            x_device = data.get('device', {})
            x_cookie = data.get('cookie', {})
            x_device = json.dumps(x_device)
            verifyTicket = data.get('verify_ticket', {})

            if signup_result.status_code == 200:
                print(f'[{i}]Успешно зарегистрировали аккаунт')
                print('Успешно зарегистрировались')
            try:
                print('получаю данные аккаунта')
                # api.tokapi.online
                #url = f"http://lumiservices.net/v1/user/self?app_version={version}&locale={str(locale)}"
                url = f"http://lumiservices.net/v1/user/self?app_version={version}&locale={str(locale)}"

                get_headers = {
                  "accept": "application/json",
                  "x-api-key": f"{api_key}",
                  "x-proxy": f"{proxy}",
                  "x-device": f"{x_device}",
                  "x-cookie": f"{x_cookie}",
                  "x-project-name": "tokapi"
                }
                response = requests.get(url, headers=get_headers, timeout=300)
                print("RESPONSE")
                print(response.status_code)
                # x_device_header = get_headers["x-device"]
                if x_device == '{}':

                  print('НАЧАЛО ИНФОРМАЦИИ ОБ ОШИБКЕ x_db_lanuks')

                  print("RESPONSE")
                  print(response.text)
                  print()
                  print(f"x-api-key: {api_key}\n"
                        f"x-proxy: {proxy}\n"
                        f"x-device: {x_device}\n"
                        f"x-cookie: {x_cookie}")
                  print("response.status_code == 401:")
                  print("status_login_auth = 1")
                  print("КОНЕЦ ИНФОРМАЦИИ ОБ ОШИБКЕ x_db_lanuks")
                  print(555222)
                  time.sleep(1)
                  continue
                else:
                  print(f"x-api-key: {api_key}\n"
                        f"x-proxy: {proxy}\n"
                        f"x-device: {x_device}\n"
                        f"x-cookie: {x_cookie}")

                if response.status_code == 200:
                  try:
                    # Printing the response from the server
                    data = json.loads(response.text)

                    user_id_acc = data['user']['uid']
                    nickname = data['user']['nickname']
                    unique_id = data['user']['unique_id']
                    print(
                      f'Данные аккаунта получены успешно\n\nUser_id: {user_id_acc}\nNickname: {nickname}\nUnique_id: {unique_id}\n\n')
                    time.sleep(1)
                  except Exception as e:
                    print(e)
                else:
                  time.sleep(1)
                  print(f'Произошла ошибка при получении данных аккаунта: {response}')
                  continue
            except Exception as e:
                print(f'Не удалось отправить запрос на получение необходимых данных: {e}')
                print(e)
                print(f"Ошибка: {error_message}")
                # Либо отправляем в очередь логов
                log_queue.put(f"[{i}]Ошибка: {error_message}")
                time.sleep(1)
                continue
            uploaded_video_count = 1
            uploaded_video_count_total = 0
            counter_tags = 3
            counter_tags2 = 0
            video_names = asyncio.run(db_helper.get_single_video_to_update())
            try:
              print(video_names)
              asyncio.run(db_helper.update_single_video_status(video_names))
            except:
              print(video_names[0])
              asyncio.run(db_helper.update_single_video_status(video_names[0]))

            if info[12] == 1:
              video_path = f'temp//unique_{video_names[0]}'
              video_name = f'unique_{video_names[0]}'
              print(video_names[0])
              video_s = video_names[0]
              try:
                asyncio.run(uniq_confetti.process_video(video_s, i))
              except:
                log_queue.put(f'[{i}]Не удалось уникализировать видео')
                print(f'[{i}]Не удалось уникализировать видео')
            else:
              video_path = f'videos\\{video_names[0]}'
              video_name = f'{video_names[0]}'
              print(video_path)
              print(video_name)
            while True:
                if info[10] == 1:
                  hashtags_text = asyncio.run(db_helper.get_random_hashtags(info[11]))
                  print(hashtags_text)
                else:
                  hashtags_text = ' '
                if info[7] == 1:
                  mark_text = asyncio.run(db_helper.get_single_mark())
                  # print(hashtags_text)
                else:
                  mark_text = ' '
                if info[4] == 1:
                  description_text = asyncio.run(db_helper.get_single_description())
                  print(description_text)
                else:
                  description_text = ''
                is_auto_caption_enabled = random.choice([True, False])
                is_audience_control_enabled = random.choice([True, False])
                is_duet_enabled = random.choice([True, False])
                is_stitch_enabled = random.choice([True, False])
                is_ai_generated_content_enabled = random.choice([True, False])
                # api.tokapi.online
                #url = f"http://lumiservices.net/v1/post/create?region={str(region)}&locale={str(locale)}&app_version={version}"
                url = f"http://lumiservices.net/v1/post/create?region={str(region)}&locale={str(locale)}&app_version={version}"
                '''if info[7] != 'Нет':
                    if phone_info[36] == '1':
                        description = ''
                        mentions = ''
                        hashtags = ''
                    else:
                        description = f'{new_desc}\n {phone_info[17]} {text_hashtags}'
                        mentions = f'{phone_info[17]}

                    try:
                        payload = {
                            'cover_time': '0.0',

                            'description': f'{description}',
                            'mentions': {f'{mentions}': {'uid': f'{uid}', 'sec_uid': f'{sec_uid}'}},
                            'hashtags': hashtags,

                            'is_auto_caption_enabled': is_auto_caption_enabled,
                            'is_audience_control_enabled': False,
                            'is_duet_enabled': is_duet_enabled,
                            'is_stitch_enabled': is_stitch_enabled,
                            'is_ai_generated_content_enabled': is_ai_generated_content_enabled,
                            'is_gallery_video_upload': False
                        }
                    except:
                        payload = {
                            'cover_time': '0.0',
                            'description': f'{description}',
                            'hashtags': hashtags,
                            'is_auto_caption_enabled': is_auto_caption_enabled,
                            'is_audience_control_enabled': False,
                            'is_duet_enabled': is_duet_enabled,
                            'is_stitch_enabled': is_stitch_enabled,
                            'is_ai_generated_content_enabled': is_ai_generated_content_enabled,
                            'is_gallery_video_upload': False
                        }



                    else:'''
                '''if info[1] != '1':
                        description = ''
                        mentions = ''
                        hashtags = ''
                    else:
                        description = f'{description_text}\n {hashtags_text} {mark_text}'''

                payload = {
                        'cover_time': '0.0',
                        'description': f'{description_text}\n {hashtags_text}',
                        'hashtags': hashtags_text,
                        'is_auto_caption_enabled': is_auto_caption_enabled,
                        'is_audience_control_enabled': False,
                        'is_duet_enabled': is_duet_enabled,
                        'is_stitch_enabled': is_stitch_enabled,
                        'is_ai_generated_content_enabled': is_ai_generated_content_enabled,
                        'is_gallery_video_upload': False

                }
                with open(video_path, 'rb') as video_file:
                  files = {
                    'data': (None, json.dumps(payload), 'application/json'),
                    'video': (f'{video_name}', video_file, 'video/mp4')
                  }

                  headers = {
                    "accept": "application/json",
                    "x-api-key": f"{api_key}",
                    "x-proxy": f"{proxy}",
                    "x-device": f"{x_device}",
                    "x-cookie": f"{x_cookie}",
                    "x-project-name": "tokapi"

                  }

                  response = requests.post(url, files=files, headers=headers)
                  if uploaded_video_count >= 7:
                    break
                  elif uploaded_video_count_total > 9:
                    break
                  if response.status_code == 200:
                    log_queue.put(f'[{i}]Видео {uploaded_video_count} загружено')
                    uploaded_video_count += 1
                    counter_tags += 3
                    counter_tags2 += 3
                  else:
                    print(response.text)
                    uploaded_video_count_total += 1
                    log_queue.put(f'[{i}]Не получилось залить {uploaded_video_count} видео. Пробуем залить следующее.')
                    time.sleep(1)
                    log_queue.put(f'[{i}]Ошибка при загрузке видео {uploaded_video_count}, пробую ещё раз')
                  # ЗАЛИВ АВАТАРКИ
            if info[8] == 1:
                avatars_directory = 'avatars'
                try:
                    # Укажите путь к папке с изображениями
                  random_avatar = get_random_avatar(avatars_directory)
                  print(random_avatar)
                  path_ava = f'avatars/{random_avatar}'
                  if random_avatar:
                    image_url = upload_image_to_fileio(path_ava)
                    # api.tokapi.online
                    #url = f"http://lumiservices.net/v1/user/{user_id_acc}/profile?app_version={version}&locale={str(locale)}"
                    url = f"http://lumiservices.net/v1/user/{user_id_acc}/profile?app_version={version}&locale={str(locale)}"
                    print(url)
                    try:
                      payload = {
                        "profile": {
                          "avatar_uri": f"{str(image_url)}"
                        }
                      }
                      get_headers = {
                        "accept": "application/json",
                        "x-api-key": f"{api_key}",
                        "x-proxy": f"{proxy}",
                        "x-device": f"{x_device}",
                        "x-cookie": f"{x_cookie}",
                        "x-project-name": "tokapi"

                      }

                      response = requests.post(url, json=payload, headers=get_headers)

                      if response.status_code == 200:
                        print(2)
                        print('Аккаунт АВАТАРКА успешно обновлен')
                        time.sleep(1)
                        print(response.text)
                      else:
                        print(3)
                        print(response.text)
                        print(f'Произошла ошибка при обновлении аккаунта {response.text}')
                        time.sleep(1)
                        # print(response.text)
                        print(122)
                    except Exception as e:
                      log_queue.put(f"[{i}]Ошибка в заливе авы. {str(e)}")
                  else:
                    log_queue.put(f"[{i}]Нет фотографии для аватарок в папке.")
                except:
                  log_queue.put(f'[{i}]Не получилось залить аву')
            if info[9] == 1:
                tt = 0
                try:
                  while tt < 50:
                    if tt < 50:
                      name = asyncio.run(db_helper.get_random_biz_name())
                      cat_id = asyncio.run(db_helper.get_biz_cat_by_name(name))
                      print(cat_id)
                      print(name)
                      if cat_id == None:
                        log_queue.put(f'[{i}]У вас нет данных для вставки биз ссылки')
                      try:
                        # api.tokapi.online
                        #url = f"http://lumiservices.net/v1/user/business_account/enable"
                        url = f"http://lumiservices.net/v1/user/business_account/enable"

                        payload = {
                          "settings": {
                            'category_id': f"{cat_id}",
                            'category_name': f"{name}"
                          }
                        }

                        get_headers = {
                          "accept": "application/json",
                          "x-api-key": f"{api_key}",
                          "x-proxy": f"{proxy}",
                          "x-device": f"{x_device}",
                          "x-cookie": f"{x_cookie}",
                          "x-project-name": "tokapi"

                        }

                        response = requests.post(url, json=payload, headers=get_headers)
                        data = json.loads(response.text)
                        print(data)
                        print(123)
                        # account_type = data['user']['account_type']
                        # api.tokapi.online
                        #url = f"http://lumiservices.net/v1/user/self?app_version={version}&locale={str(locale)}"
                        url = f"http://lumiservices.net/v1/user/self?app_version={version}&locale={str(locale)}"
                        get_headers = {
                          "accept": "application/json",
                          "x-api-key": f"{api_key}",
                          "x-proxy": f"{proxy}",
                          "x-device": f"{x_device}",
                          "x-cookie": f"{x_cookie}",
                          "x-project-name": "tokapi"

                        }
                        response = requests.get(url, headers=get_headers)
                        if response.status_code == 200:
                          data = json.loads(response.text)
                          print(data)
                          print(123)
                          account_type = data['user']['account_type']
                          print(account_type)
                          if int(account_type) == 3:
                            tt += 100
                            print('Подключили биз, ураааааа')
                            print('К аккаунту успешно подключён к биз. ссылке')
                            # mail_biz = phone_info[43]
                            try:
                              mail_biz = asyncio.run(db_helper.get_random_biz_url())
                            except Exception as e:
                              log_queue.put(f'[{i}]Нету ссылки(')
                            time.sleep(1)
                            count = 0
                            while count < 100:
                              try:
                                url = f"http://lumiservices.net/v1/user/{user_id_acc}/profile"

                                payload = {
                                  "profile": {
                                    "bio_url": f"{mail_biz}"
                                  }
                                }

                                get_headers = {
                                  "accept": "application/json",
                                  "x-api-key": f"{api_key}",
                                  "x-device": f"{x_device}",
                                  "x-cookie": f"{x_cookie}",
                                  "x-proxy": f"{proxy}",
                                  "x-project-name": "tokapi"

                                }

                                response = requests.post(url, json=payload, headers=get_headers)
                              except Exception as e:
                                print(e)

                                print(f"Ошибка: {error_message}")
                                # Либо отправляем в очередь логов
                                log_queue.put(f"[{i}]Ошибка: {error_message}")
                                # requests.get(
                                #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось залить biz \n {response.status_code} \n {response.text} \n\n {e} ')
                              if response.status_code == 200:
                                # requests.get(
                                #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={user_id}&text=[{thread_number}]: Подключили биз ссылку')
                                print('К аккаунту успешно подключён к биз. ссылке')
                                time.sleep(1)
                                count = 100
                              else:
                                if count > 100:
                                  # requests.get(
                                  #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={user_id}&text=[{thread_number}]: Не удалось подключить биз')
                                  print(f'Произошла ошибка при обновлении биз аккаунта {response}')
                                  print(response.text)
                                  print(response.status_code)
                                  time.sleep(1)
                                  print(count)
                                  count += 1
                                print(response)
                                print(response.text)
                                print(response.status_code)
                                print(count)
                                count += 1

                              ''' #else:
                              #print(response.text)
                              #print(response.status_code)
                              #requests.get(
                              #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={user_id}&text=[{thread_number}]: Не удалось подключить биз')
                              #print(f'Произошла ошибка при обновлении аккаунта {response}')
                              #time.sleep(1)
                              # print(response.text)'''
                          else:
                            log_queue.put(f'[{i}]Не получилось залить биз ссылку, так как у вас отсутсвуют данные')
                            tt += 100
                            count += 100
                        else:
                          tt += 1
                          print(f'Пиздец с {tt} попытки не подключили')
                          if tt > 50:
                            # requests.get(
                            #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={user_id}&text=[{thread_number}]: Не удалось отправить запрос на включения биз аккаунта. Скрипт остановлен')
                            time.sleep(1)

                      except Exception as e:
                        if tt > 50:
                          print(e)
                          print(f"Ошибка: {error_message}")
                          # Либо отправляем в очередь логов
                          log_queue.put(f"[{i}]Ошибка: {error_message}")
                          # requests.get(
                          #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось залить biz \n {response.status_code} \n {response.text} \n\n {e} ')
                          # requests.get(
                          #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={user_id}&text=[{thread_number}]: Не удалось отправить запрос на включения биз аккаунта. Скрипт остановлен')
                          time.sleep(1)
                          print(nickname)
                        tt += 1

                    else:
                      print('Пиздец с сотой попытки не подключили')
                except:
                  pass
            try:
                bioinnick = 0
                # api.tokapi.online
                #url = f"http://lumiservices.net/v1/user/{user_id_acc}/profile?app_version={version}&locale={str(locale)}"
                url = f"http://lumiservices.net/v1/user/{user_id_acc}/profile?app_version={version}&locale={str(locale)}"
                if info[6] == 1:
                  nickname = asyncio.run(db_helper.get_nick_zaliv())
                  print(nickname)
                  bio = asyncio.run(db_helper.get_bio_zaliv())
                  print(bio)
                  if info[5] == 1:
                    bioinnick += 1
                    bio = asyncio.run(db_helper.get_bio_zaliv())
                    payload = {
                      "profile": {
                        "signature": f"{bio}",
                        "nickname": f"{nickname}"
                      }

                    }

                  else:
                    payload = {
                      "profile": {
                        "nickname": f"{nickname}"
                      }

                    }

                  get_headers = {
                    "accept": "application/json",
                    "x-api-key": f"{api_key}",
                    "x-proxy": f"{proxy}",
                    "x-device": f"{x_device}",
                    "x-cookie": f"{x_cookie}",
                    "x-project-name": "tokapi"
                  }
                  response = requests.post(url, json=payload, headers=get_headers)
                  if response.status_code == 200:
                    if bioinnick == 0:
                      print('никнейм успешно обновлен')
                    else:
                      print('Био и никнейм успешно обновлен')
                    time.sleep(1)
                  else:
                    # requests.get(
                    #    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={user_id}&text=[{thread_number}]: Не удалось заполнить био')
                    print(f'Произошла ошибка при обновлении аккаунта {response}')
                    time.sleep(1)
                    # print(response.text)
                if info[5] == 1:
                  if bioinnick == 0:
                    bio = asyncio.run(db_helper.get_bio_zaliv())
                    payload = {
                      "profile": {
                        "signature": f"{bio}",
                        "nickname": f"{nickname}"
                      }

                    }

                  else:
                    payload = {
                      "profile": {
                        "nickname": f"{nickname}"
                      }

                    }

                  get_headers = {
                    "accept": "application/json",
                    "x-api-key": f"{api_key}",
                    "x-proxy": f"{proxy}",
                    "x-device": f"{x_device}",
                    "x-cookie": f"{x_cookie}",
                    "x-project-name": "tokapi"

                  }
                  response = requests.post(url, json=payload, headers=get_headers)
                  if response.status_code == 200:
                    print('Био успешно обновлен')
                    time.sleep(1)
                  else:
                    print(f'Произошла ошибка при обновлении аккаунта {response}')
                    time.sleep(1)
            except Exception as e:
                print(e)
                print(f"Ошибка: {error_message}")
                # Либо отправляем в очередь логов
                log_queue.put(f"[{i}]Ошибка: {error_message}")
            if info[1] == 1:
              try:
                with lock:
                  unique_id = asyncio.run(db_helper.get_username_zaliv())
                  print(unique_id)
                  asyncio.run(db_helper.delete_username(unique_id))
                if unique_id == None:
                  log_queue.put(f"[{i}]У вас закончились юзернеймы")
                else:
                  # api.tokapi.online
                  #url = f'http://lumiservices.net/v1/post/user/{user_id_acc}/posts'
                  url = f'http://lumiservices.net/v1/post/user/{user_id_acc}/posts'
                  payload = {
                      "username": f"{unique_id}"
                  }
                  get_headers = {
                      "accept": "application/json",
                      "x-api-key": f"{api_key}",
                      "x-project-name": 'tokapi'
                  }

                  response = requests.get(url, json=payload, headers=get_headers)
                  print(response.text)
                  print(response.status_code)
                  data = json.loads(response.text)

                  aweme_ids = [item.get('aweme_id') for item in data.get('aweme_list', [])]


                  print(response)
                  if response.status_code == 200:
                    log_queue.put(f'[{i}]Успешно залили username на аккаунт')
                  else:
                    log_queue.put(f'[{i}]Не удалось залить username на аккаунт')
              except Exception as e:
                print(e)
            try:
                print('получаю данные аккаунта')
                # api.tokapi.online
                #url = f"http://lumiservices.net/v1/user/self?app_version={version}&locale={str(locale)}"
                url = f"http://lumiservices.net/v1/user/self?app_version={version}&locale={str(locale)}"

                get_headers = {
                  "accept": "application/json",
                  "x-api-key": f"{api_key}",
                  "x-proxy": f"{proxy}",
                  "x-device": f"{x_device}",
                  "x-cookie": f"{x_cookie}",
                  "x-project-name": "tokapi"

                }
                response = requests.get(url, headers=get_headers, timeout=300)
                print("RESPONSE")
                print(response.status_code)
                # x_device_header = get_headers["x-device"]
                if x_device == '{}':

                  print('НАЧАЛО ИНФОРМАЦИИ ОБ ОШИБКЕ x_db_lanuks')

                  print("RESPONSE")
                  print(response.text)
                  print()
                  print(f"x-api-key: {api_key}\n"
                        f"x-proxy: {proxy}\n"
                        f"x-device: {x_device}\n"
                        f"x-cookie: {x_cookie}")
                  print("response.status_code == 401:")
                  print("status_login_auth = 1")
                  print("КОНЕЦ ИНФОРМАЦИИ ОБ ОШИБКЕ x_db_lanuks")
                  print(555222)
                  time.sleep(1)
                  continue
                else:
                  print(f"x-api-key: {api_key}\n"
                        f"x-proxy: {proxy}\n"
                        f"x-device: {x_device}\n"
                        f"x-cookie: {x_cookie}")

                if response.status_code == 200:
                  try:
                    # Printing the response from the server
                    data = json.loads(response.text)

                    user_id_acc = data['user']['uid']
                    nickname = data['user']['nickname']
                    unique_id = data['user']['unique_id']
                    print(
                      f'Данные аккаунта получены успешно\n\nUser_id: {user_id_acc}\nNickname: {nickname}\nUnique_id: {unique_id}\n\n')
                    time.sleep(1)
                  except Exception as e:
                    print(e)
                else:
                  time.sleep(1)
                  print(f'Произошла ошибка при получении данных аккаунта: {response}')
                  continue
            except Exception as e:
                print(f'Не удалось отправить запрос на получение необходимых данных: {e}')
                print(e)
                print(f"Ошибка: {error_message}")
                # Либо отправляем в очередь логов
                log_queue.put(f"[{i}]Ошибка: {error_message}")
                time.sleep(1)
                continue


            if info[12] == 0:
                asyncio.run(db_helper.update_single_video_status_back(video_names[0]))
                # удаление уникализированного видео
            else:
                video_path = f'temp\\unique_{video_names[0]}'
                os.remove(video_path)
                asyncio.run(db_helper.update_single_video_status_back(video_names[0]))

            log_queue.put(f'[{i}]✅Аккаунт @{unique_id} успешно пролит, записали в Excel таблицу "usernames"!!')
            print(f'[{i}]✅Аккаунт @{unique_id} успешно пролит!!')
            excel_file = "usernames.xlsx"

            # Переменная unique_id, которую нужно записать
            #
            # Замени это значение своим

            # Записываем в файл
            append_to_excel(excel_file, unique_id)
            continue



        except ValueError as e:
            log_queue.put(f"[{i}]Ошибка в my_function: {str(e)}")