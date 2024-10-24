import asyncio
import flet as ft
import data.db_helper as db_helper  # Импортируем наш db_helper с асинхронными функциями
import os
import time
import shutil
import pandas as pd
import openpyxl
import multiprocessing
import logging
import os

import subprocess
import app.appm as appm
import app.appmc as appmc
import app.appp as appp
import app.apppc as apppc
import app.apprzm as apprzm
import app.apprzfm as apprzfm
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app_log.log')
processes = []




def worker_process(log_queue):
    """Запуск функции из appm.py в процессе и передача логов через очередь."""
    try:
        log_queue.put("Процесс запущен.")
        appm.my_function(log_queue)  # Передаем очередь в my_function
        log_queue.put("Процесс завершен успешно.")
    except Exception as e:
        log_queue.put(f"Ошибка в процессе: {str(e)}")

def start_fill_process(log_output, stream_count_value,  fill_type_value, description_value, bio_value, usernames_value, nicknames_value,hashtags_value, marks_value, ava_value, bizz_value,uniq_value,hashtag_count_value):
    log_queue = multiprocessing.Queue()
    log_queue.put("Процесс запущен.")
    print(fill_type_value)
    try:
        if int(fill_type_value) == 1:
            log_queue.put("Вы выбрали залив видео, аккаунты обычные.")
            # Запускаем процессы
            for i in range(stream_count_value):
                p = multiprocessing.Process(
                    target=appm.my_function,
                    args=(log_queue, i),  # Передаем очередь в процессы
                    name=f"Process-{i}"
                )
                processes.append(p)
                p.start()
                log_output.value += f"Запущен {p.name}\n"
                log_output.update()
        elif int(fill_type_value) == 2:
            log_queue.put("Вы выбрали залив видео, аккаунты куки.")
            # Запускаем процессы
            for i in range(stream_count_value):
                p = multiprocessing.Process(
                    target=appm.my_function,
                    args=(log_queue, i),  # Передаем очередь в процессы
                    name=f"Process-{i}"
                )
                processes.append(p)
                p.start()
                log_output.value += f"Запущен {p.name}\n"
                log_output.update()
        elif int(fill_type_value) == 3:
            log_queue.put("Вы выбрали залив каруселей, аккаунты обычные.")
            # Запускаем процессы
            for i in range(stream_count_value):
                p = multiprocessing.Process(
                    target=appm.my_function,
                    args=(log_queue, i),  # Передаем очередь в процессы
                    name=f"Process-{i}"
                )
                processes.append(p)
                p.start()
                log_output.value += f"Запущен {p.name}\n"
                log_output.update()
        elif int(fill_type_value) == 4:
            log_queue.put("Вы выбрали залив каруселей, аккаунты куки.")
            # Запускаем процессы
            for i in range(stream_count_value):
                p = multiprocessing.Process(
                    target=appm.my_function,
                    args=(log_queue, i),  # Передаем очередь в процессы
                    name=f"Process-{i}"
                )
                processes.append(p)
                p.start()
                log_output.value += f"Запущен {p.name}\n"
                log_output.update()
        elif int(fill_type_value) == 5:
            log_queue.put("Вы выбрали залив через регистрацию вашей почты, аккаунты куки.")
            # Запускаем процессы
            for i in range(stream_count_value):
                p = multiprocessing.Process(
                    target=apprzm.my_function,
                    args=(log_queue, i),  # Передаем очередь в процессы
                    name=f"Process-{i}"
                )
                processes.append(p)
                p.start()
                log_output.value += f"Запущен {p.name}\n"
                log_output.update()
        elif int(fill_type_value) == 6:
            log_queue.put("Вы выбрали залив через регистрацию фейковых аккаунтов, аккаунты куки.")
            # Запускаем процессы
            for i in range(stream_count_value):
                p = multiprocessing.Process(
                    target=apprzfm.my_function,
                    args=(log_queue, i),  # Передаем очередь в процессы
                    name=f"Process-{i}"
                )
                processes.append(p)
                p.start()
                log_output.value += f"Запущен {p.name}\n"
                log_output.update()
                time.sleep(5)
        else:
            log_queue.put("Ошибка")
        # Асинхронно считываем логи из очереди
        while any(p.is_alive() for p in processes):
            while not log_queue.empty():
                log_message = log_queue.get()
                log_output.value += f"{log_message}\n"
                log_output.update()
            time.sleep(0.1)

        # Ожидаем завершения всех процессов
        for p in processes:
            p.join()

        print(1234554321)



    except Exception as e:
            log_output.value += f"Ошибка: {str(e)}\n"
            log_output.update()

def show_log_window(page, stream_count_value,  fill_type_value, description_value, bio_value, usernames_value, nicknames_value,hashtags_value, marks_value, ava_value, bizz_value,uniq_value,hashtag_count_value):
    """Функция для отображения окна логов"""

    log_output = ft.Text(value="", width=900, height=900, color=ft.colors.WHITE)

    # Создаем контейнер с логами и включаем скроллинг
    scrollable_container = ft.Container(
        content=ft.Column(
            [log_output],
            scroll=ft.ScrollMode.AUTO  # Включаем автоматическую прокрутку
        ),
        width=900,
        height=900
    )

    # Создаем модальное окно
    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Логи процессов. Чтобы остановить работу нажмите кнопку закрыть"),
        content=scrollable_container,
        actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal, page))],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    page.overlay.append(modal)
    modal.open = True
    page.update()

    # Запускаем процесс и выводим логи в модальное окно
    start_fill_process(log_output, stream_count_value,  fill_type_value, description_value, bio_value, usernames_value, nicknames_value,hashtags_value, marks_value, ava_value, bizz_value,uniq_value,hashtag_count_value)

def kill_all_processes():
    """Функция для завершения всех процессов."""
    global processes
    for p in processes:
        if p.is_alive():
            p.terminate()  # Завершаем процесс
            p.join()  # Ожидаем завершения
    processes.clear()  # Очищаем список процессов после завершения

def close_modal(modal, page):
    """Закрытие модального окна и завершение всех процессов"""
    asyncio.run(db_helper.update_single_video_status_back_all())
    kill_all_processes()  # Завершаем все процессы перед закрытием окна
    modal.open = False
    page.update()

def main(page: ft.Page):
    # Инициализация базы данных
    asyncio.run(db_helper.create_db())
    # Устанавливаем тему и свойства окна
    page.title = "SoftikUBT"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK

    # Функция для показа модального окна с сообщением
    def show_modal_dialog(title, content):
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER  # Центрирование кнопки Закрыть
        )
        page.overlay.append(modal)
        modal.open = True
        page.update()

    def close_modal(modal):
        modal.open = False
        page.update()

    #Начало бизссылки
    def show_usernames_upload_modal():
        file_path = None  # Переменная для хранения пути к файлу

        # Функция для обработки загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path  # Сохраняем путь к файлу
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения юзернеймов в базу данных
        def on_save_click(e):
            if file_path:
                # Чтение файла и запись юзернеймов в базу данных
                with open(file_path, "r") as file:
                    usernames = file.read().splitlines()
                    asyncio.run(db_helper.insert_usernames(usernames))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(usernames)} юзернеймов.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех юзернеймов
        def on_view_usernames_click(e):
            usernames = asyncio.run(db_helper.get_usernames())
            if usernames:
                usernames_list = "\n".join(usernames)
                show_modal_dialog("Список юзернеймов", usernames_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет юзернеймов.")

        # Функция для удаления всех юзернеймов
        def on_delete_usernames_click(e):
            asyncio.run(db_helper.delete_all_usernames())
            show_modal_dialog("Удаление завершено", "Все юзернеймы удалены из базы данных.")

        # Получаем количество юзернеймов
        usernames_count = len(asyncio.run(db_helper.get_usernames()))  # Получаем количество юзернеймов из БД

        # Создание элемента выбора файла
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Статус загрузки
        upload_status = ft.Text("Файл не выбран")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть все юзернеймы", on_click=on_view_usernames_click),
                ft.ElevatedButton("Удалить все юзернеймы", on_click=on_delete_usernames_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Выровнять по вертикали
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Выровнять по горизонтали
            spacing=10
        )

        # Оборачиваем содержимое в контейнер с фиксированным размером и показываем количество юзернеймов
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Управление юзернеймами (Всего: {usernames_count})"),  # Отображаем количество юзернеймов
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER  # Центрирование кнопок действий
        )

        # Открыть модальное окно
        page.overlay.append(modal)
        modal.open = True
        page.update()
    #Конец добавления бизсылки

    #NICKNAMES
    def show_nickname_upload_modal():
        file_path = None  # Переменная для хранения пути к файлу
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path  # Сохраняем путь к файлу
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения юзернеймов в базу данных
        def on_save_click(e):
            if file_path:
                # Чтение файла и запись юзернеймов в базу данных
                with open(file_path, "r") as file:
                    nicknames = file.read().splitlines()
                    asyncio.run(db_helper.insert_nick(nicknames))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(nicknames)} никнеймов.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех юзернеймов
        def on_view_nicknames_click(e):
            nicknames = asyncio.run(db_helper.get_nick())
            if nicknames:
                nick_list = "\n".join([str(nickname[1]) for nickname in nicknames])
                show_modal_dialog("Список никнеймов", nick_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет никнеймы.")

        # Функция для удаления всех юзернеймов
        def on_delete_nicknames_click(e):
            asyncio.run(db_helper.delete_all_nick())
            show_modal_dialog("Удаление завершено", "Все никнеймы удалены из базы данных.")

        # Получаем количество юзернеймов
        nicknames_count = len(asyncio.run(db_helper.get_nick()))  # Получаем количество юзернеймов из БД

        # Создание элемента выбора файла
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Статус загрузки
        upload_status = ft.Text("Файл не выбран")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть все никнеймы", on_click=on_view_nicknames_click),
                ft.ElevatedButton("Удалить все никнеймы", on_click=on_delete_nicknames_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Выровнять по вертикали
            scroll=ft.ScrollMode.ALWAYS,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Выровнять по горизонтали
            spacing=10
        )

        # Оборачиваем содержимое в контейнер с фиксированным размером и показываем количество юзернеймов
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Управление никнеймы (Всего: {nicknames_count})"),  # Отображаем количество юзернеймов
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            # Центрирование кнопок действий
        )

        # Открыть модальное окно
        page.overlay.append(modal)
        modal.open = True
        page.update()
    #NICKNAMES

    # Отметки

    def count_avatars():
        avatar_folder = "avatars"
        if os.path.exists(avatar_folder):
            return len(os.listdir(avatar_folder))
        return 0

    # Функция для показа модального окна для загрузки аватара
    def show_avatar_upload_modal():
        avatar_folder = "avatars"
        file_paths = []  # Переменная для хранения путей к файлам

        # Функция для обработки загрузки файлов
        def on_file_upload(e):
            nonlocal file_paths
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_paths = [file.path for file in file_picker.result.files]  # Сохраняем пути к файлам
                upload_status.value = f"Выбрано файлов: {len(file_paths)}"
            else:
                upload_status.value = "Файлы не выбраны"
            page.update()

        # Функция для сохранения загруженных фотографий
        def on_save_click(e):
            if file_paths:
                os.makedirs(avatar_folder, exist_ok=True)
                for file_path in file_paths:
                    save_location = os.path.join(avatar_folder, os.path.basename(file_path))
                    shutil.copy(file_path, save_location)  # Копируем файл

                show_modal_dialog("Загрузка завершена", f"Сохранено {len(file_paths)} фотографий.")
            else:
                show_modal_dialog("Ошибка", "Файлы не выбраны.")

        # Функция для удаления аватаров
        def on_delete_click(e):
            avatars = os.listdir(avatar_folder) if os.path.exists(avatar_folder) else []
            if avatars:
                for avatar in avatars:
                    avatar_path = os.path.join(avatar_folder, avatar)
                    os.remove(avatar_path)  # Удаляем все файлы в папке
                show_modal_dialog("Удаление завершено", f"Удалено {len(avatars)} аватарок.")
            else:
                show_modal_dialog("Ошибка", "Нет загруженных аватарок для удаления.")
            page.update()

        # Получаем количество аватаров в папке
        avatar_count = count_avatars()

        # Создание элемента выбора файлов
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        upload_status = ft.Text("Файлы не выбраны")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                ft.Text(f"В папке {avatar_count} загруженных фото."),
                ft.Text("Можно загрузить несколько фотографий сразу."),
                upload_status,
                ft.ElevatedButton("Выбрать изображения", on_click=lambda e: file_picker.pick_files(allow_multiple=True, allowed_extensions=['jpg', 'png'])),
                ft.ElevatedButton("Сохранить изображения", on_click=on_save_click),
                ft.ElevatedButton("Удалить все аватары", on_click=on_delete_click)  # Кнопка удаления аватаров
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Загрузка аватаров (Всего: {avatar_count})"),  # Подсчет аватаров в заголовке
            content=ft.Container(content=modal_content, width=400, height=250),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()
    def show_mark_upload_modal():
            file_path = None  # Переменная для хранения пути к файлу

            def on_file_upload(e):
                nonlocal file_path
                file_picker = e.control
                if file_picker.result and file_picker.result.files:
                    file_path = file_picker.result.files[0].path  # Сохраняем путь к файлу
                    upload_status.value = f"Файл выбран: {file_path}"
                else:
                    upload_status.value = "Файл не выбран"
                page.update()


            def on_save_click(e):
                if file_path:

                    with open(file_path, "r") as file:
                        mark = file.read().splitlines()
                        asyncio.run(db_helper.insert_mark(mark))
                        show_modal_dialog("Загрузка завершена", f"Загружено {len(mark)} никнеймов.")
                else:
                    show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

            # Функция для просмотра всех юзернеймов
            def on_view_marks_click(e):
                marks = asyncio.run(db_helper.get_mark())
                if marks:
                    marks_list = "\n".join([str(nickname[1]) for nickname in marks])
                    show_modal_dialog("Список никнеймов", marks_list)
                else:
                    show_modal_dialog("Список пуст", "В базе данных нет никнеймы.")

            # Функция для удаления всех юзернеймов
            def on_delete_marks_click(e):
                asyncio.run(db_helper.delete_all_mark())
                show_modal_dialog("Удаление завершено", "Все никнеймы удалены из базы данных.")

            # Получаем количество юзернеймов
            nicknames_count = len(asyncio.run(db_helper.get_mark()))  # Получаем количество юзернеймов из БД

            # Создание элемента выбора файла
            file_picker = ft.FilePicker(on_result=on_file_upload)
            page.overlay.append(file_picker)

            # Статус загрузки
            upload_status = ft.Text("Файл не выбран")

            # Элементы модального окна
            modal_content = ft.Column(
                [
                    upload_status,
                    ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                    ft.ElevatedButton("Сохранить", on_click=on_save_click),
                    ft.ElevatedButton("Посмотреть все отметки", on_click=on_view_marks_click),
                    ft.ElevatedButton("Удалить все отметки", on_click=on_delete_marks_click),

                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Выровнять по вертикали
                scroll=ft.ScrollMode.ALWAYS,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Выровнять по горизонтали
                spacing=10
            )

            # Оборачиваем содержимое в контейнер с фиксированным размером и показываем количество юзернеймов
            modal = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Управление отметок (Всего: {nicknames_count})"),  # Отображаем количество юзернеймов
                content=ft.Container(content=modal_content, width=400, height=400),
                actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                # Центрирование кнопок действий
            )

            # Открыть модальное окно
            page.overlay.append(modal)
            modal.open = True
            page.update()


        # Отметки

    # Функция для показа модального окна загрузки файла и управления юзернеймами
    def show_usernames_upload_modal():
        file_path = None  # Переменная для хранения пути к файлу

        # Функция для обработки загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path  # Сохраняем путь к файлу
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения юзернеймов в базу данных
        def on_save_click(e):
            if file_path:
                # Чтение файла и запись юзернеймов в базу данных
                with open(file_path, "r") as file:
                    usernames = file.read().splitlines()
                    asyncio.run(db_helper.insert_usernames(usernames))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(usernames)} юзернеймов.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех юзернеймов
        def on_view_usernames_click(e):
            usernames = asyncio.run(db_helper.get_usernames())
            if usernames:
                usernames_list = "\n".join(usernames)
                show_modal_dialog("Список юзернеймов", usernames_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет юзернеймов.")

        # Функция для удаления всех юзернеймов
        def on_delete_usernames_click(e):
            asyncio.run(db_helper.delete_all_usernames())
            show_modal_dialog("Удаление завершено", "Все юзернеймы удалены из базы данных.")

        # Получаем количество юзернеймов
        usernames_count = len(asyncio.run(db_helper.get_usernames()))  # Получаем количество юзернеймов из БД

        # Создание элемента выбора файла
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Статус загрузки
        upload_status = ft.Text("Файл не выбран")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть все юзернеймы", on_click=on_view_usernames_click),
                ft.ElevatedButton("Удалить все юзернеймы", on_click=on_delete_usernames_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Выровнять по вертикали
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Выровнять по горизонтали
            spacing=10
        )

        # Оборачиваем содержимое в контейнер с фиксированным размером и показываем количество юзернеймов
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Управление юзернеймами (Всего: {usernames_count})"),  # Отображаем количество юзернеймов
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER  # Центрирование кнопок действий
        )

        # Открыть модальное окно
        page.overlay.append(modal)
        modal.open = True
        page.update()


    def show_hashtags_upload_modal():
        file_path = None  # Переменная для хранения пути к файлу

        # Функция для обработки загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path  # Сохраняем путь к файлу
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения юзернеймов в базу данных
        def on_save_click(e):
            if file_path:
                # Чтение файла и запись юзернеймов в базу данных
                with open(file_path, "r") as file:
                    hashtags = file.read().splitlines()
                    asyncio.run(db_helper.insert_hashtags(hashtags))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(hashtags)} hashtags.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех юзернеймов
        def on_view_hashtags_click(e):
            hashtags = asyncio.run(db_helper.get_hashtags())
            if hashtags:
                hashtags_list = "\n".join(hashtags)
                show_modal_dialog("Список юзернеймов", hashtags_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет hashtags.")

        # Функция для удаления всех юзернеймов
        def on_delete_hashtags_click(e):
            asyncio.run(db_helper.delete_all_hashtags())
            show_modal_dialog("Удаление завершено", "Все hashtags удалены из базы данных.")

        # Получаем количество юзернеймов
        hashtags_count = len(asyncio.run(db_helper.get_hashtags()))  # Получаем количество юзернеймов из БД

        # Создание элемента выбора файла
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Статус загрузки
        upload_status = ft.Text("Файл не выбран")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть все hashtags", on_click=on_view_hashtags_click),
                ft.ElevatedButton("Удалить все hashtags", on_click=on_delete_hashtags_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Выровнять по вертикали
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Выровнять по горизонтали
            spacing=10
        )

        # Оборачиваем содержимое в контейнер с фиксированным размером и показываем количество юзернеймов
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Управление hashtags (Всего: {hashtags_count})"),  # Отображаем количество юзернеймов
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER  # Центрирование кнопок действий
        )

        # Открыть модальное окно
        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_bio_upload_modal():
        file_path = None

        # Функция для загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения bio в базу данных
        def on_save_click(e):
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    bio_data = file.read().splitlines()
                    bio_entries = [line.replace(',', ';') for line in bio_data]  # Преобразование разделителей
                    asyncio.run(db_helper.insert_bio(bio_entries))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(bio_entries)} bio-записей.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех bio записей
        def on_view_bio_click(e):
            bio_records = asyncio.run(db_helper.get_bio())
            if bio_records:
                bio_list = "\n".join([f"{r[1]}" for r in bio_records])
                show_modal_dialog("Список bio", bio_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет bio-записей.")

        # Функция для удаления всех bio записей
        def on_delete_bio_click(e):
            asyncio.run(db_helper.delete_all_bio())
            show_modal_dialog("Удаление завершено", "Все bio-записи удалены из базы данных.")
        # Получаем количество bio записей

        bio_count = asyncio.run(db_helper.get_bio_count())

        # Элементы интерфейса
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        upload_status = ft.Text("Файл не выбран")

        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть все bio", on_click=on_view_bio_click),
                ft.ElevatedButton("Удалить все bio", on_click=on_delete_bio_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Управление bio (Всего: {bio_count})"),  # Отображаем количество bio
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()
    def show_opi_upload_modal():
        file_path = None

        # Функция для загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения bio в базу данных
        def on_save_click(e):
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    opi_data = file.read().splitlines()
                    opi_entries = [line.replace(',', ';') for line in opi_data]  # Преобразование разделителей
                    asyncio.run(db_helper.insert_opi(opi_entries))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(opi_entries)} описания.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех bio записей
        def on_view_bio_click(e):
            opi_records = asyncio.run(db_helper.get_opi())
            if opi_records:
                opi_list = "\n".join([f"{r[1]}" for r in opi_records])
                show_modal_dialog("Список Описания", opi_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет описания.")

        # Функция для удаления всех bio записей
        def on_delete_bio_click(e):
            asyncio.run(db_helper.delete_all_opi())
            show_modal_dialog("Удаление завершено", "Все описания удалены из базы данных.")
        # Получаем количество bio записей

        opi_count = asyncio.run(db_helper.get_opi_count())

        # Элементы интерфейса
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        upload_status = ft.Text("Файл не выбран")

        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть описание", on_click=on_view_bio_click),
                ft.ElevatedButton("Удалить описание", on_click=on_delete_bio_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Управление Описанием (Всего: {opi_count})"),  # Отображаем количество bio
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    # Функция для отображения главной страницы
    def show_main_page():
        page.views.clear()

        def on_profile_click(e):
            show_profile_modal()

        def on_settings_click(e):
            show_config_fill_page()

        def on_fill_click(e):
            show_fill_page()



        # Кнопка для загрузки юзернеймов из файла

        profile_button = ft.ElevatedButton(
            "Профиль",
            on_click=on_profile_click,
            color=ft.colors.WHITE
        )

        settings_button = ft.ElevatedButton(
            "Настройка конфига",
            on_click=on_settings_click,
            color=ft.colors.WHITE
        )
        fill_button = ft.ElevatedButton(
            "Залив",
            on_click=on_fill_click,
            color=ft.colors.WHITE
        )


        image = ft.Image(src="resources/logo.jpg", width=150, height=150, fit=ft.ImageFit.CONTAIN)

        page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text('Главное меню', size=42),
                                image,
                                ft.Container(profile_button, width=200, height=50),
                                ft.Container(settings_button, width=200, height=50),
                                ft.Container(fill_button, width=200, height=50),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                        animate=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT)
                    )
                ]
            )
        )
        page.update()

    def show_proxy_modal(page):
        file_path = None

        # Получаем текущее значение прокси из таблицы settings
        current_proxy_value = asyncio.run(db_helper.get_current_proxy_type())

        # Устанавливаем начальное значение для прокси (False - обычные, True - мобильные)
        initial_value = "TRUE" if current_proxy_value == "TRUE" else "FALSE"

        # Создаем переменную для сохранения текущего значения прокси
        proxy_type_value = ft.Text(value=initial_value)

        # Текст для отображения текущего выбора прокси
        current_proxy_text = ft.Text(f"Текущий тип прокси: {'Мобильные' if initial_value == 'TRUE' else 'Обычные'}")

        # Функция для обработки изменений в RadioGroup
        def radiogroup_changed(e):
            proxy_type_value.value = e.control.value
            current_proxy_text.value = f"Текущий тип прокси: {'Мобильные' if e.control.value == 'TRUE' else 'Обычные'}"
            page.update()

        # Создаем RadioGroup для выбора прокси
        cg = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="FALSE", label="Обычные прокси"),
                ft.Radio(value="TRUE", label="Мобильные прокси")
            ]),
            value=initial_value,  # Устанавливаем начальное значение
            on_change=radiogroup_changed  # Обработка изменения значения
        )

        # Функция для сохранения выбранного типа прокси
        def on_proxy_type_change(e):
            new_value = proxy_type_value.value
            asyncio.run(db_helper.update_proxy_type(new_value))
            proxy_type_text = "Мобильные прокси" if new_value == "TRUE" else "Обычные прокси"

            # Создаем и открываем модальное окно для подтверждения успешного обновления
            success_dialog = ft.AlertDialog(
                title=ft.Text("Тип прокси обновлен"),
                content=ft.Text(f"Вы выбрали: {proxy_type_text}"),
                actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
                actions_alignment=ft.MainAxisAlignment.CENTER
            )
            page.overlay.append(success_dialog)
            success_dialog.open = True
            page.update()

        # Функция для обработки загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения прокси
        def on_save_click(e):
            if file_path:
                with open(file_path, "r") as file:
                    proxies = file.read().splitlines()
                    is_mobile = proxy_type_value.value == "TRUE"  # Проверяем текущее значение радиокнопок
                    asyncio.run(db_helper.insert_proxies(proxies, is_mobile))
                    save_dialog = ft.AlertDialog(
                        title=ft.Text("Загрузка завершена"),
                        content=ft.Text(f"Загружено {len(proxies)} прокси."),
                        actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
                        actions_alignment=ft.MainAxisAlignment.CENTER
                    )
                    page.overlay.append(save_dialog)
                    save_dialog.open = True
            else:
                error_dialog = ft.AlertDialog(
                    title=ft.Text("Ошибка"),
                    content=ft.Text("Файл не выбран."),
                    actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
                    actions_alignment=ft.MainAxisAlignment.CENTER
                )
                page.overlay.append(error_dialog)
                error_dialog.open = True
            page.update()

        # Функция для удаления всех прокси
        def on_delete_click(e):
            is_mobile = proxy_type_value.value == "TRUE"  # Проверяем текущее значение радиокнопок
            asyncio.run(db_helper.delete_all_proxies(is_mobile))
            delete_dialog = ft.AlertDialog(
                title=ft.Text("Удаление завершено"),
                content=ft.Text("Все прокси удалены."),
                actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
                actions_alignment=ft.MainAxisAlignment.CENTER
            )
            page.overlay.append(delete_dialog)
            delete_dialog.open = True
            page.update()

        # Получаем количество прокси
        regular_proxy_count = asyncio.run(db_helper.get_proxy_count(False))
        mobile_proxy_count = asyncio.run(db_helper.get_proxy_count(True))

        upload_status = ft.Text("Файл не выбран")
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Modal content
        modal_content = ft.Column(
            [
                current_proxy_text,  # Текущий тип прокси
                ft.Text(f"Обычные прокси: {regular_proxy_count}"),
                ft.Text(f"Мобильные прокси: {mobile_proxy_count}"),
                cg,  # Радиогруппа для выбора прокси
                ft.ElevatedButton("Сохранить изменения", on_click=on_proxy_type_change),  # Кнопка сохранения
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить прокси", on_click=on_save_click),
                ft.ElevatedButton("Удалить все прокси", on_click=on_delete_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Управление прокси"),
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_email_modal(page):
        file_path = None  # Переменная для хранения пути к файлу

        # Функция для обработки загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path  # Сохраняем путь к файлу
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Функция для сохранения почт в базу данных
        def on_save_click(e):
            if file_path:
                # Чтение файла и запись почт в базу данных
                with open(file_path, "r") as file:
                    emails = file.read().splitlines()  # Предполагаем, что каждая строка файла — это одна почта
                    asyncio.run(db_helper.insert_emails(emails))
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(emails)} почт.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран. Пожалуйста, выберите файл.")

        # Функция для просмотра всех почт
        def on_view_emails_click(e):
            emails = asyncio.run(db_helper.get_emails())
            if emails:
                emails_list = "\n".join(emails)
                show_modal_dialog("Список почт", emails_list)
            else:
                show_modal_dialog("Список пуст", "В базе данных нет почт.")

        # Функция для удаления всех почт
        def on_delete_emails_click(e):
            asyncio.run(db_helper.delete_all_emails())
            show_modal_dialog("Удаление завершено", "Все почты удалены из базы данных.")

        # Создание элемента выбора файла
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Статус загрузки
        upload_status = ft.Text("Файл не выбран")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                upload_status,
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть все почты", on_click=on_view_emails_click),
                ft.ElevatedButton("Удалить все почты", on_click=on_delete_emails_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        # Создание модального окна
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Управление почтами"),
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER  # Центрирование кнопок действий
        )

        # Открыть модальное окно
        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_accounts_modal(page):
        file_path = None

        # Получаем текущее значение типа аккаунта из базы данных при загрузке страницы
        current_account_typ = asyncio.run(db_helper.get_current_account_type())
        current_account_type = current_account_typ[0][0]

        # Устанавливаем начальное значение на основе типа аккаунта
        if current_account_type == "TRUE":
            initial_value = "cookie"  # Если куки-аккаунты
        else:
            initial_value = "ordinary"  # Если обычные аккаунты

        account_type_value = ft.Text(value=initial_value)

        # Считаем количество обычных и куки-аккаунтов
        ordinary_count = len(asyncio.run(db_helper.get_ordinary_accounts()))  # Количество обычных аккаунтов
        cookie_count = len(asyncio.run(db_helper.get_cookie_accounts()))  # Количество куки-аккаунтов

        # Отображаем счетчики аккаунтов
        account_type_text = ft.Text(f"Обычные аккаунты: {ordinary_count}\nКуки-аккаунты: {cookie_count}")

        # Обработка изменения типа аккаунта
        def on_account_type_change(e):
            account_type_value.value = e.control.value  # Устанавливаем выбранный тип аккаунта
            page.update()

        # Радиокнопки для выбора типа аккаунта
        rg = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="ordinary", label="Обычные аккаунты"),
                ft.Radio(value="cookie", label="Куки-аккаунты")
            ]),
            value=initial_value,  # Устанавливаем начальное значение при загрузке страницы
            on_change=on_account_type_change
        )

        # Сохранение выбранного типа аккаунта в базу данных
        def save_account_type_to_db():
            acc_type = "TRUE" if account_type_value.value == "cookie" else "FALSE"
            asyncio.run(db_helper.update_accs_type(acc_type))  # Сохраняем тип аккаунта в базу данных

        # Обработчик загрузки файла
        def on_file_upload(e):
            nonlocal file_path
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_path = file_picker.result.files[0].path
                upload_status.value = f"Файл выбран: {file_path}"
            else:
                upload_status.value = "Файл не выбран"
            page.update()

        # Сохранение аккаунтов в базу данных
        def on_save_click(e):
            save_account_type_to_db()  # Сначала сохраняем тип аккаунта
            if file_path:
                # Если выбран файл txt, это обычные аккаунты
                if file_path.endswith(".txt"):
                    with open(file_path, "r") as file:
                        accounts = file.read().splitlines()

                    # Проверяем, какой тип аккаунта выбран
                    if account_type_value.value == "ordinary":
                        asyncio.run(db_helper.insert_ordinary_accounts(accounts))  # Вставляем обычные аккаунты
                    else:
                        show_modal_dialog("Ошибка", "Вы выбрали куки-аккаунты, но файл содержит обычные аккаунты.")

                # Если выбран файл Excel, это куки-аккаунты
                elif file_path.endswith(".xlsx"):
                    excel_data = pd.read_excel(file_path)
                    cookie_accounts = [(row[0].strip(), row[1].strip()) for _, row in excel_data.iterrows()]
                    asyncio.run(db_helper.insert_cookie_accounts(cookie_accounts))  # Вставляем куки-аккаунты
                if file_path.endswith(".txt"):
                    show_modal_dialog("Загрузка завершена", f"Загружено {len(accounts)} аккаунтов.")
                else:
                    show_modal_dialog("Загрузка завершена", f"Загружены аккаунты.")
            else:
                show_modal_dialog("Ошибка", "Файл не выбран.")

        # Подтверждение выбора типа аккаунта
        def on_confirm_click(e):
            save_account_type_to_db()
            selected_type = "Куки-аккаунты" if account_type_value.value == "cookie" else "Обычные аккаунты"
            show_modal_dialog("Выбор подтвержден", f"Вы выбрали: {selected_type}")
            page.update()

        # Просмотр аккаунтов
        def on_view_accounts_click(e):
            if account_type_value.value == "ordinary":
                accounts = asyncio.run(db_helper.get_ordinary_accounts())
            else:
                accounts = asyncio.run(db_helper.get_cookie_accounts())
            if accounts:
                show_modal_dialog("Список аккаунтов", "\n".join(accounts))
            else:
                show_modal_dialog("Список пуст", "Аккаунтов нет.")

        # Удаление всех аккаунтов
        def on_delete_accounts_click(e):
            if account_type_value.value == "ordinary":
                asyncio.run(db_helper.delete_all_ordinary_accounts())
            else:
                asyncio.run(db_helper.delete_all_cookie_accounts())
            show_modal_dialog("Удаление завершено", "Все аккаунты удалены.")

        # Состояние загрузки файла
        upload_status = ft.Text("Файл не выбран")
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        # Содержимое модального окна
        modal_content = ft.Column(
            [
                account_type_text,  # Счетчики аккаунтов
                ft.Text("Выберите тип аккаунта:"),
                rg,
                ft.ElevatedButton("Подтвердить выбор", on_click=on_confirm_click),
                upload_status,
                ft.ElevatedButton("Как добавлять аккаунты?",
                                  on_click=lambda e: show_modal_dialog("Как добавлять аккаунты?",
                                                                       "Обычные аккаунты: .txt файл\nКуки-аккаунты: .xlsx файл (x_device, x_cookie)")),
                ft.ElevatedButton("Выбрать файл", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Сохранить аккаунты", on_click=on_save_click),
                ft.ElevatedButton("Посмотреть аккаунты", on_click=on_view_accounts_click),
                ft.ElevatedButton("Удалить все аккаунты", on_click=on_delete_accounts_click),

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Управление аккаунтами"),
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_add_video_modal():
        video_folder = "videos"
        file_paths = []

        def count_videos_in_folder():
            """Подсчитывает количество видеофайлов в папке videos"""
            video_folder = "videos"
            if os.path.exists(video_folder):
                return len([name for name in os.listdir(video_folder) if name.endswith('.mp4')])
            return 0

        def delete_all_videos_and_files():
            """Удаляет все видеофайлы и их записи из базы данных"""
            video_folder = "videos"

            # Удаление всех файлов из папки
            if os.path.exists(video_folder):
                for video_file in os.listdir(video_folder):
                    file_path = os.path.join(video_folder, video_file)
                    os.remove(file_path)

            # Удаление записей из базы данных
            asyncio.run(db_helper.delete_all_videos())

            show_modal_dialog("Удаление завершено", "Все видео и их записи удалены.")

        def on_file_upload(e):
            nonlocal file_paths
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_paths = [file.path for file in file_picker.result.files]  # Сохраняем пути к файлам
                upload_status.value = f"Выбрано файлов: {len(file_paths)}"
            else:
                upload_status.value = "Файлы не выбраны"
            page.update()

        def on_save_click(e):
            if file_paths:
                os.makedirs(video_folder, exist_ok=True)
                for i, file_path in enumerate(file_paths):
                    unique_name = f"video_{i + 1}_{int(time.time())}.mp4"
                    save_location = os.path.join(video_folder, unique_name)
                    shutil.copy(file_path, save_location)  # Копирование файла

                    # Запись в базу данных
                    asyncio.run(db_helper.insert_video(unique_name, save_location))

                show_modal_dialog("Загрузка завершена", f"Сохранено {len(unique_name)} видео.")
            else:
                show_modal_dialog("Ошибка", "Файлы не выбраны.")

        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        upload_status = ft.Text("Файлы не выбраны")
        video_count = count_videos_in_folder()

        modal_content = ft.Column(
            [
                ft.Text(f"Всего видео: {video_count}"),
                upload_status,
                ft.ElevatedButton("Выбрать видео", on_click=lambda e: file_picker.pick_files(allow_multiple=True,
                                                                                             allowed_extensions=[
                                                                                                 'mp4'])),
                ft.ElevatedButton("Сохранить видео", on_click=on_save_click),
                ft.ElevatedButton("Удалить все видео", on_click=lambda e: delete_all_videos_and_files())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавление видео"),
            content=ft.Container(content=modal_content, width=400, height=300),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_unique_settings_modal():
        # Функция для обновления значения ползунка из текстового поля
        def update_slider_value(slider, text_field):
            slider.value = float(text_field.value)
            page.update()

        # Функция для обновления значения текстового поля при изменении ползунка
        def update_text_field_value(slider, text_field):
            text_field.value = str(slider.value)
            page.update()


        # Ползунки с текстовыми полями для значений
        speed_slider = ft.Slider(min=0.1, max=1.9, value=1.0,
                                 on_change=lambda e: update_text_field_value(speed_slider, speed_text))
        speed_text = ft.TextField(value=str(speed_slider.value),
                                  on_change=lambda e: update_slider_value(speed_slider, speed_text), width=100)

        opacity_slider = ft.Slider(min=0.1, max=1.9, value=1.0,
                                   on_change=lambda e: update_text_field_value(opacity_slider, opacity_text))
        opacity_text = ft.TextField(value=str(opacity_slider.value),
                                    on_change=lambda e: update_slider_value(opacity_slider, opacity_text), width=100)

        scale_slider = ft.Slider(min=0.1, max=1.9, value=1.0,
                                 on_change=lambda e: update_text_field_value(scale_slider, scale_text))
        scale_text = ft.TextField(value=str(scale_slider.value),
                                  on_change=lambda e: update_slider_value(scale_slider, scale_text), width=100)

        duration_slider = ft.Slider(min=0.1, max=1.9, value=1.0,
                                    on_change=lambda e: update_text_field_value(duration_slider, duration_text))
        duration_text = ft.TextField(value=str(duration_slider.value),
                                     on_change=lambda e: update_slider_value(duration_slider, duration_text), width=100)

        # Настройки конфетти
        confetti_amount_slider = ft.Slider(min=10, max=100, value=50,
                                           on_change=lambda e: update_text_field_value(confetti_amount_slider,
                                                                                       confetti_amount_text))
        confetti_amount_text = ft.TextField(value=round(float(confetti_amount_slider.value)),
                                            on_change=lambda e: update_slider_value(confetti_amount_slider,
                                                                                    confetti_amount_text), width=100)

        confetti_speed_slider = ft.Slider(min=0.1, max=0.9, value=0.5,
                                          on_change=lambda e: update_text_field_value(confetti_speed_slider,
                                                                                      confetti_speed_text))
        confetti_speed_text = ft.TextField(value=str(confetti_speed_slider.value),
                                           on_change=lambda e: update_slider_value(confetti_speed_slider,
                                                                                   confetti_speed_text), width=100)

        # Чекбоксы для эффектов
        fade_checkbox = ft.Checkbox(label="Эффект Fade")
        light_checkbox = ft.Checkbox(label="Засветление")
        dark_checkbox = ft.Checkbox(label="Затемнение")
        confetti_checkbox = ft.Checkbox(label="Конфетти")

        # Функция для загрузки настроек из БД при открытии окна
        def load_settings():
            settings = asyncio.run(db_helper.get_uniq_confetti())  # Получаем настройки из базы данных
            if settings:
                # Обновляем ползунки и текстовые поля значениями из базы данных
                speed_slider.value = settings["speed"]
                opacity_slider.value = settings["opacity"]
                scale_slider.value = settings["scale"]
                duration_slider.value = settings["duration"]
                confetti_amount_slider.value = settings["confetti_amount"]
                confetti_speed_slider.value = settings["confetti_speed"]

                # Обновляем чекбоксы
                fade_checkbox.value = settings["fade"]
                light_checkbox.value = settings["light"]
                dark_checkbox.value = settings["dark"]
                confetti_checkbox.value = settings["confetti"]

                # Обновляем текстовые поля значений
                update_text_field_value(speed_slider, speed_text)
                update_text_field_value(opacity_slider, opacity_text)
                update_text_field_value(scale_slider, scale_text)
                update_text_field_value(duration_slider, duration_text)
                update_text_field_value(confetti_amount_slider, confetti_amount_text)
                update_text_field_value(confetti_speed_slider, confetti_speed_text)

                page.update()

        # Функция для сохранения настроек
        def save_settings(e):
            speed = float(speed_text.value)
            opacity = float(opacity_text.value)
            scale = float(scale_text.value)
            duration = float(duration_text.value)
            fade = fade_checkbox.value
            light = light_checkbox.value
            dark = dark_checkbox.value
            confetti = confetti_checkbox.value
            confetti_amount = round(float(confetti_amount_text.value))
            confetti_speed = float(confetti_speed_text.value)

            # Сохранение в базу данных
            asyncio.run(db_helper.insert_uniq_confetti(speed, opacity, scale, duration, fade, light, dark, confetti,
                                                       confetti_amount, confetti_speed))
            show_modal_dialog("Успех", "Настройки уникальности успешно сохранены!")

        # Загружаем настройки из БД при открытии окна
        load_settings()

        # Создание модального окна с ползунками, текстовыми полями, чекбоксами и кнопкой
        modal_content = ft.Column(
            [
                ft.Row([ft.Text("Скорость движения"), speed_slider, speed_text]),
                ft.Row([ft.Text("Прозрачность"), opacity_slider, opacity_text]),
                ft.Row([ft.Text("Масштабирование"), scale_slider, scale_text]),
                ft.Row([ft.Text("Длительность затемнения"), duration_slider, duration_text]),
                fade_checkbox,
                light_checkbox,
                dark_checkbox,
                confetti_checkbox,
                ft.Text("Настройка конфетти"),
                ft.Row([ft.Text("Количество конфетти"), confetti_amount_slider, confetti_amount_text]),
                ft.Row([ft.Text("Скорость конфетти"), confetti_speed_slider, confetti_speed_text]),
                ft.ElevatedButton("Сохранить настройки", on_click=save_settings),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        )

        # Открываем модальное окно
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Настройка уникальности"),
            content=ft.Container(content=modal_content, width=500, height=600),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_carousel_settings_modal():
        # Функция для обновления значения ползунка из текстового поля
        def update_slider_value(slider, text_field):
            slider.value = float(text_field.value)
            page.update()

        # Функция для обновления значения текстового поля при изменении ползунка
        def update_text_field_value(slider, text_field):
            text_field.value = str(slider.value)
            page.update()

        # Ползунки с текстовыми полями для значений
        stickers_slider = ft.Slider(min=1, max=99, value=50,
                                    on_change=lambda e: update_text_field_value(stickers_slider, stickers_text))
        stickers_text = ft.TextField(value=str(stickers_slider.value),
                                     on_change=lambda e: update_slider_value(stickers_slider, stickers_text), width=100)

        size_slider = ft.Slider(min=1, max=10, value=5,
                                on_change=lambda e: update_text_field_value(size_slider, size_text))
        size_text = ft.TextField(value=str(size_slider.value),
                                 on_change=lambda e: update_slider_value(size_slider, size_text), width=100)

        stripes_slider = ft.Slider(min=1, max=20, value=10,
                                   on_change=lambda e: update_text_field_value(stripes_slider, stripes_text))
        stripes_text = ft.TextField(value=str(stripes_slider.value),
                                    on_change=lambda e: update_slider_value(stripes_slider, stripes_text), width=100)

        angle_slider = ft.Slider(min=0, max=45, value=20,
                                 on_change=lambda e: update_text_field_value(angle_slider, angle_text))
        angle_text = ft.TextField(value=str(angle_slider.value),
                                  on_change=lambda e: update_slider_value(angle_slider, angle_text), width=100)

        transparency_slider = ft.Slider(min=0.0, max=1.0, value=0.5,
                                        on_change=lambda e: update_text_field_value(transparency_slider,
                                                                                    transparency_text))
        transparency_text = ft.TextField(value=str(transparency_slider.value),
                                         on_change=lambda e: update_slider_value(transparency_slider,
                                                                                 transparency_text), width=100)

        resize_slider = ft.Slider(min=0.1, max=1.0, value=0.5,
                                  on_change=lambda e: update_text_field_value(resize_slider, resize_text))
        resize_text = ft.TextField(value=str(resize_slider.value),
                                   on_change=lambda e: update_slider_value(resize_slider, resize_text), width=100)

        blur_slider = ft.Slider(min=1, max=10, value=5,
                                on_change=lambda e: update_text_field_value(blur_slider, blur_text))
        blur_text = ft.TextField(value=str(blur_slider.value),
                                 on_change=lambda e: update_slider_value(blur_slider, blur_text), width=100)

        # Функция для загрузки настроек из базы данных
        def load_settings():
            settings = asyncio.run(db_helper.get_carousel_settings())  # Получаем настройки из базы данных
            if settings:
                stickers_slider.value = settings["stickers"]
                size_slider.value = settings["size"]
                stripes_slider.value = settings["stripes"]
                angle_slider.value = settings["angle"]
                transparency_slider.value = settings["transparency"]
                resize_slider.value = settings["resize"]
                blur_slider.value = settings["blur"]

                update_text_field_value(stickers_slider, stickers_text)
                update_text_field_value(size_slider, size_text)
                update_text_field_value(stripes_slider, stripes_text)
                update_text_field_value(angle_slider, angle_text)
                update_text_field_value(transparency_slider, transparency_text)
                update_text_field_value(resize_slider, resize_text)
                update_text_field_value(blur_slider, blur_text)

                page.update()

        # Функция для сохранения настроек в базу данных
        def save_settings(e):
            stickers = round(float(stickers_text.value))
            size = round(float(size_text.value))
            stripes = round(float(stripes_text.value))
            angle = round(float(angle_text.value))
            transparency = float(transparency_text.value)
            resize = float(resize_text.value)
            blur = round(float(blur_text.value))

            asyncio.run(db_helper.insert_carousel_settings(stickers, size, stripes, angle, transparency, resize, blur))
            show_modal_dialog("Успех", "Настройки карусели успешно сохранены!")

        # Загружаем настройки из БД при открытии окна
        load_settings()

        # Создание модального окна
        modal_content = ft.Column(
            [
                ft.Row([ft.Text("Количество стикеров"), stickers_slider, stickers_text]),
                ft.Row([ft.Text("Размер стикера"), size_slider, size_text]),
                ft.Row([ft.Text("Количество полосок"), stripes_slider, stripes_text]),
                ft.Row([ft.Text("Угол поворота"), angle_slider, angle_text]),
                ft.Row([ft.Text("Прозрачность"), transparency_slider, transparency_text]),
                ft.Row([ft.Text("Изменение размера"), resize_slider, resize_text]),
                ft.Row([ft.Text("Блюр фона"), blur_slider, blur_text]),
                ft.ElevatedButton("Сохранить настройки", on_click=save_settings),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        )

        # Открываем модальное окно
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Настройка карусели"),
            content=ft.Container(content=modal_content, width=500, height=600),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_add_photo_modal():
        base_photo_folder = "photos"
        file_paths = []
        selected_folder = None  # Переменная для хранения выбранной папки

        # Создаём 6 папок при необходимости
        def ensure_folders_exist():
            for i in range(1, 7):
                folder_path = os.path.join(base_photo_folder, str(i))
                os.makedirs(folder_path, exist_ok=True)

        # Подсчёт количества фото в выбранной папке для каруселей
        def count_photos_in_folder(folder):
            folder_path = os.path.join(base_photo_folder, folder)
            if os.path.exists(folder_path):
                return len(os.listdir(folder_path))
            return 0

        # Функция для обработки загрузки файлов
        def on_file_upload(e):
            nonlocal file_paths
            file_picker = e.control
            if file_picker.result and file_picker.result.files:
                file_paths = [file.path for file in file_picker.result.files]  # Сохраняем пути к файлам
                upload_status.value = f"Выбрано файлов: {len(file_paths)}"
            else:
                upload_status.value = "Файлы не выбраны"
            page.update()

        # Функция для сохранения загруженных фотографий
        def on_save_click(e):
            if file_paths and selected_folder:
                folder_path = os.path.join(base_photo_folder, selected_folder)
                os.makedirs(folder_path, exist_ok=True)
                for file_path in file_paths:
                    save_location = os.path.join(folder_path, os.path.basename(file_path))
                    shutil.copy(file_path, save_location)  # Копируем файл

                show_modal_dialog("Загрузка завершена",
                                  f"Сохранено {len(file_paths)} фотографий в папку {selected_folder}.")
            else:
                show_modal_dialog("Ошибка", "Файлы не выбраны или папка не выбрана.")

        # Функция для удаления всех фотографий в выбранной папке
        def on_delete_click(e):
            if selected_folder:
                folder_path = os.path.join(base_photo_folder, selected_folder)
                if os.path.exists(folder_path):
                    for file_name in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file_name)
                        os.remove(file_path)  # Удаление всех файлов в папке
                    show_modal_dialog("Удаление завершено", f"Все фотографии для {selected_folder} слайда удалены.")
                else:
                    show_modal_dialog("Ошибка", f"Папка для {selected_folder} слайда не существует.")
            else:
                show_modal_dialog("Ошибка", "Папка для слайда не выбрана.")

        # Функция для выбора папки
        def on_folder_select(folder):
            nonlocal selected_folder
            selected_folder = folder
            photo_count = count_photos_in_folder(folder)
            folder_status.value = f"Выбрана папка для {folder} слайда, в ней {photo_count} фото."
            page.update()

        # Создаём папки (1-6), если их ещё нет
        ensure_folders_exist()

        # Создание элемента выбора файлов
        file_picker = ft.FilePicker(on_result=on_file_upload)
        page.overlay.append(file_picker)

        upload_status = ft.Text("Файлы не выбраны")
        folder_status = ft.Text("Папка для слайда не выбрана")

        # Элементы модального окна
        modal_content = ft.Column(
            [
                ft.Text('В карусели доступно 6 фотографий на одну карусель, \nниже выберите слайд куда на который желаете добавить\n'
                        'P.s. можно выбрать несколько фоток за раз'),
                folder_status,
                ft.Row(
                    [
                        ft.ElevatedButton(f"Слайд {i}", on_click=lambda e, i=i: on_folder_select(str(i)))
                        for i in range(1, 4)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(f"Слайд {i}", on_click=lambda e, i=i: on_folder_select(str(i)))
                        for i in range(4, 7)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                upload_status,
                ft.ElevatedButton("Выбрать изображения", on_click=lambda e: file_picker.pick_files(allow_multiple=True,
                                                                                                   allowed_extensions=[
                                                                                                       'jpg', 'png'])),
                ft.ElevatedButton("Сохранить изображения", on_click=on_save_click),
                ft.ElevatedButton("Удалить все изображения", on_click=on_delete_click)  # Кнопка удаления
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавление фото"),
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_creo_management_page():
        # Функции для каждой кнопки
        def on_add_video_click(e):
            show_add_video_modal()

        def on_add_photo_click(e):
            show_add_photo_modal()

        def on_unique_settings_click(e):
            # Функционал для настройки уникальности
            pass

        def on_unique_carousel_settings_click(e):
            # Функционал для настройки уникальности каруселей
            pass

        # Кнопки управления
        page.views.clear()
        page.views.append(
            ft.View(
                "/creo_management",
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.ElevatedButton("Добавление видео", on_click=lambda e: on_add_video_click(e), color=ft.colors.WHITE, width=200, height=50),
                                ft.ElevatedButton("Добавление фото", on_click=lambda e: on_add_photo_click(e), color=ft.colors.WHITE, width=200, height=50),
                                ft.ElevatedButton("Настройка уника", on_click=lambda e: show_unique_settings_modal(), color=ft.colors.WHITE, width=200, height=50),
                                ft.ElevatedButton("Настройка уника каруселей", on_click=lambda e: show_carousel_settings_modal(), color=ft.colors.WHITE, width=200, height=50),
                                ft.ElevatedButton("Назад", on_click=lambda e: show_main_page(), width=200)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10

                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),


                ],
                padding=ft.padding.all(20),
            )
        )

        page.update()











    def insert_geo(geo_code):
        asyncio.run(db_helper.insert_or_update_geo(geo_code))
        show_modal_dialog("Успех", f"Код страны {geo_code} успешно обновлен в базе данных.")

    # Функция для показа модального окна с выбором GEO
    def show_fill_page():
        # Переменные для потоков и выбранного типа заливов
        stream_count = ft.TextField(label="Введите количество потоков", width=300, height=40)
        fill_type = ft.Dropdown(
            options=[
                ft.dropdown.Option(key="1", text="Видео"),
                ft.dropdown.Option(key="2", text="Видео Куки"),
                ft.dropdown.Option(key="5", text="Залив видео через регу "),
                ft.dropdown.Option(key="6", text="Залив видео через фейк регу "),
            ],

            label="Выберите тип заливов",
            width=300, height=40
        )
        '''ft.dropdown.Option(key="3", text="Фото"),
        ft.dropdown.Option(key="4", text="Фото Куки"),'''

        # Переменная для хранения состояния хэштегов
        hashtag_count_field = ft.TextField(label="Введите количество хэштегов (до 9)", visible=False, width=300, height=40)

        # Функция для показа/скрытия поля для хэштегов
        def on_hashtag_checked(e):
            hashtag_count_field.visible = e.control.value  # Показать поле, если чекбокс выбран
            page.update()

        # Список чекбоксов с полем для хэштегов под соответствующим чекбоксом
        checkboxes = [
            ft.Checkbox(label="Описание"),
            ft.Checkbox(label="Био"),
            ft.Checkbox(label="Юзернеймы"),
            ft.Checkbox(label="Никнеймы"),
            ft.Column(
                [
                    ft.Checkbox(label="Хэштеги", on_change=on_hashtag_checked),
                    hashtag_count_field  # Поле для ввода количества хэштегов
                ]
            ),
            ft.Checkbox(label="Отметки"),
            ft.Checkbox(label="Аватарка"),
            ft.Checkbox(label="Подключение биз. ссылки"),
            ft.Checkbox(label="Уникализатор видео")
        ]

        # Функция обновления данных с базы
        def on_fill_click(e):
            profile = asyncio.run(db_helper.get_profile_data())

            if profile:
                # Пример обновления полей и чекбоксов на основе данных
                stream_count.value = profile[2]  # Количество потоков
                fill_type.value = profile[3]  # Тип заливов
                io = 0
                for i in range(12):
                    print(profile[io])
                    io += 1
                # Обновляем чекбоксы
                checkboxes[0].value = profile[4] == 1  # Для description
                checkboxes[1].value = profile[5] == 1  # Для bio
                checkboxes[2].value = profile[1] == 1  # Для usernames
                checkboxes[3].value = profile[6] == 1  # Для nicknames
                checkboxes[4].controls[0].value = profile[10] == 1  # Для hashtags
                hashtag_count_field.value = profile[11]  # Количество хэштегов
                checkboxes[5].value = profile[7] == 1  # Для marks
                checkboxes[6].value = profile[8] == 1  # Для ava
                checkboxes[7].value = profile[9] == 1  # Для bizz
                checkboxes[8].value = profile[10] == 1  # Для bizz
                page.update()  # Обновляем страницу

        # Функция для сохранения настроек
        def save_settings():
            # Получение значений из полей ввода
            stream_count_value = int(stream_count.value)
            fill_type_value = fill_type.value

            # Для чекбоксов сохраняйте 0 или 1 в зависимости от их состояния
            description_value = 1 if checkboxes[0].value else 0
            bio_value = 1 if checkboxes[1].value else 0
            usernames_value = 1 if checkboxes[2].value else 0
            nicknames_value = 1 if checkboxes[3].value else 0
            hashtags_value = 1 if checkboxes[4].controls[0].value else 0
            marks_value = 1 if checkboxes[5].value else 0
            ava_value = 1 if checkboxes[6].value else 0
            bizz_value = 1 if checkboxes[7].value else 0
            uniq_value = 1 if checkboxes[8].value else 0
            # Получаем количество хэштегов, если чекбокс для хэштегов активен
            hashtag_count_value = int(hashtag_count_field.value) if hashtags_value == 1 else 0

            # Вызов функции для сохранения данных в БД
            asyncio.run(db_helper.save_or_update_profile(
                stream_count_value, fill_type_value, description_value, bio_value,
                usernames_value, nicknames_value, marks_value, ava_value, bizz_value, hashtags_value,
                hashtag_count_value, uniq_value
            ))
            show_modal_dialog("Успешно!", "Настройки сохранены.")

        def start_potok():
            # Получение значений из полей ввода
            stream_count_value = int(stream_count.value)
            fill_type_value = fill_type.value

            # Для чекбоксов сохраняйте 0 или 1 в зависимости от их состояния
            description_value = 1 if checkboxes[0].value else 0
            bio_value = 1 if checkboxes[1].value else 0
            usernames_value = 1 if checkboxes[2].value else 0
            nicknames_value = 1 if checkboxes[3].value else 0
            hashtags_value = 1 if checkboxes[4].controls[0].value else 0
            marks_value = 1 if checkboxes[5].value else 0
            ava_value = 1 if checkboxes[6].value else 0
            bizz_value = 1 if checkboxes[7].value else 0
            uniq_value = 1 if checkboxes[8].value else 0
            # Получаем количество хэштегов, если чекбокс для хэштегов активен
            hashtag_count_value = int(hashtag_count_field.value) if hashtags_value == 1 else 0

            show_log_window(page, stream_count_value,  fill_type_value, description_value, bio_value, usernames_value, nicknames_value,hashtags_value, marks_value, ava_value,
                            bizz_value,uniq_value,hashtag_count_value)

        log_output = ft.Text(value="", width=500, height=300, color=ft.colors.WHITE)
        # Кнопки "Запустить" и "Назад"
        fill_button = ft.ElevatedButton("Выгрузить настройки ⤴", on_click=on_fill_click, color=ft.colors.WHITE,
                                          width=250, height=30)
        save_button = ft.ElevatedButton("Сохранить настройки ⤵", on_click=lambda e: save_settings(), color=ft.colors.WHITE,
                                          width=250, height=30)
        start_button = ft.ElevatedButton("Запустить", on_click=lambda e: start_potok(), color=ft.colors.WHITE,
                                          width=250, height=30)
        back_button = ft.ElevatedButton("Назад", on_click=lambda e: show_main_page(), color=ft.colors.WHITE,
                                          width=250, height=30)

        # Добавляем кнопки и чекбоксы на страницу
        page.views.clear()
        page.views.append(
            ft.View(
                "/fill_page",
                [
                    ft.Row(
                        [
                            ft.Column(
                                [stream_count, fill_type] + checkboxes,
                                scroll=ft.ScrollMode.ALWAYS,
                                width=400,
                                height=500
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row([fill_button, save_button, start_button,  back_button],
                           alignment=ft.MainAxisAlignment.CENTER,
                           vertical_alignment=ft.CrossAxisAlignment.END
                           )
                ],
                padding=ft.padding.all(50),
            )
        )
        page.update()

    '''def start_fill_process():
        # Логика запуска процесса заливов
        show_modal_dialog("Запуск", "Процесс заливов запущен.")'''

    def show_categories_modal(page, selected_biz_name):
        async def fetch_categories():
            categories = await db_helper.get_biz_categories()
            return categories

        categories = asyncio.run(fetch_categories())

        # Функция для обработки нажатия на категорию
        '''def on_category_select(e, category_name):
            # Обновляем бизнес-ссылку с выбранной категорией
            print(selected_biz_name)
            asyncio.run(db_helper.update_biz_name(selected_biz_name))
            close_modal(modal)
            page.update()'''

        # Создаем список кнопок для категорий
        category_buttons = []

        # Функция для обработки выбора категории
        def on_category_select(e, category):
            # Здесь обрабатывается выбранная категория
            print(f"Выбрана категория: {category}")
            asyncio.run(db_helper.update_biz_name(category))
            show_modal_dialog("Успешно!", "Категория обновлена")
            '''close_modal(modal)
            page.update()'''


        # Создаем кнопки для каждой категории
        for category in categories:
            button = ft.ElevatedButton(
                text=category[0],  # Отображаемое имя категории
                on_click=lambda e, cat=category[0]: on_category_select(e, cat),  # Привязка текущей категории
                color=ft.colors.WHITE,
                width=200,
                height=50
            )
            category_buttons.append(button)
        '''category_buttons = [
            ft.ElevatedButton(category[0], on_click=lambda e, cat=category[0]: on_category_select(e, cat),
                              color=ft.colors.WHITE, width=200, height=50)
            for category in categories
        ]'''

        # Создаем модальное окно с кнопками категорий
        modal_content = ft.Column(category_buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=10,
            scroll = ft.ScrollMode.ALWAYS)

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Выберите категорию"),
            content=ft.Container(content=modal_content, width=400, height=400),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_biz_links_page(page):
        page.views.clear()

        async def fetch_biz_links():
            links = await db_helper.get_biz_links()
            return links
        async def fetch_biz_lins():
            lins = await db_helper.get_biz_lins()
            return lins

        biz_links = asyncio.run(fetch_biz_links())
        biz_lins = asyncio.run(fetch_biz_lins())
        try:
            url = biz_lins[0][1]
        except:
            url = 'null'
        try:
            name = biz_lins[0][0]
        except:
            name = 'null'
        # Отображение бизнес-ссылок
        links_list = ft.Column([
            ft.Row([ft.Text(f'Ваша биз ссылка: {url}'), ft.Text(f'Ваша категория: {name}')], alignment=ft.MainAxisAlignment.CENTER)
        ],
            scroll = ft.ScrollMode.ALWAYS, alignment=ft.MainAxisAlignment.CENTER)

        # Определение функций для кнопок
        def on_add_click(e):
            # Добавление бизнес-ссылки
            pass

        def on_delete_click_biz(e):
            asyncio.run(db_helper.delete_biz_url())
            show_modal_dialog('Успешно удалено', ' ')


        def on_categories_click(e, biz_name):
            # Вызов модального окна категорий
            show_categories_modal(page, biz_name)

        def on_back_click(e):
            # Возврат на предыдущую страницу
            page.go("/config_options")  # Укажите путь, на который нужно вернуться

        # Создание кнопок
        add_button = ft.ElevatedButton("Добавить бизнес-ссылку", on_click=lambda e: show_biz_link_modal(), color=ft.colors.WHITE,
                                       width=200, height=50)
        '''delete_button = ft.ElevatedButton("Удалить бизнес-ссылку", on_click=lambda e: on_delete_click_biz(e), color=ft.colors.WHITE,
                                          width=200, height=50)'''

        # Пример кнопки для выбора категории с передачей biz_name
        categories_button = ft.ElevatedButton("Категории", on_click=lambda e: on_categories_click(e, biz_links[0][0]),
                                              color=ft.colors.WHITE, width=200, height=50)

        back_button = ft.ElevatedButton(
            "Назад",
            on_click=lambda e: show_config_fill_page(),
            width=200
        )

        # Макет страницы с бизнес-ссылками
        page.views.append(
            ft.View(
                "/biz_links",
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                links_list,  # Список бизнес-ссылок
                                ft.Row([categories_button, add_button],
                                       alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                back_button  # Кнопка назад
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            scroll = ft.ScrollMode.ALWAYS
                        ),
                        alignment=ft.alignment.center,
                        expand=True  # Размещение по центру
                    )
                ]
            )
        )
        page.update()

    def show_biz_link_modal():
        # Field for entering the URL
        biz_url_input = ft.TextField(label="Введите бизнес-ссылку", width=300)

        # Function to save the link
        def on_save_click(e):
            biz_url = biz_url_input.value
            if biz_url:
                print(biz_url)
                asyncio.run(db_helper.update_biz_link(biz_url))
                show_modal_dialog("Успех", "Ссылка успешно сохранена!")
                close_modal(modal)  # Close the modal after saving
            else:
                show_modal_dialog("Ошибка", "Введите действительную ссылку.")

        # Modal structure
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Добавление ссылки"),
            content=ft.Container(
                content=ft.Column(
                    [
                        biz_url_input,
                        ft.ElevatedButton("Сохранить", on_click=on_save_click)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                width=400,
                height=200
            ),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        # Show modal
        page.overlay.append(modal)
        modal.open = True
        page.update()

    def show_geo_modal():
        countries = [
            ("Австралия", "AU"),
            ("Австрия", "AT"),
            ("Азербайджан", "AZ"),
            ("Албания", "AL"),
            ("Алжир", "DZ"),
            ("Ангола", "AO"),
            ("Андорра", "AD"),
            ("Антигуа и Барбуда", "AG"),
            ("Аргентина", "AR"),
            ("Армения", "AM"),
            ("Афганистан", "AF"),
            ("Багамы", "BS"),
            ("Бангладеш", "BD"),
            ("Барбадос", "BB"),
            ("Бахрейн", "BH"),
            ("Беларусь", "BY"),
            ("Белиз", "BZ"),
            ("Бельгия", "BE"),
            ("Бенин", "BJ"),
            ("Болгария", "BG"),
            ("Боливия", "BO"),
            ("Босния и Герцеговина", "BA"),
            ("Ботсвана", "BW"),
            ("Бразилия", "BR"),
            ("Бруней", "BN"),
            ("Буркина-Фасо", "BF"),
            ("Бурунди", "BI"),
            ("Бутан", "BT"),
            ("Вануату", "VU"),
            ("Ватикан", "VA"),
            ("Великобритания", "GB"),
            ("Венгрия", "HU"),
            ("Венесуэла", "VE"),
            ("Восточный Тимор", "TL"),
            ("Вьетнам", "VN"),
            ("Габон", "GA"),
            ("Гаити", "HT"),
            ("Гайана", "GY"),
            ("Гамбия", "GM"),
            ("Гана", "GH"),
            ("Гватемала", "GT"),
            ("Гвинея", "GN"),
            ("Гвинея-Бисау", "GW"),
            ("Германия", "DE"),
            ("Гондурас", "HN"),
            ("Гренада", "GD"),
            ("Греция", "GR"),
            ("Грузия", "GE"),
            ("Дания", "DK"),
            ("Джибути", "DJ"),
            ("Доминика", "DM"),
            ("Доминиканская Республика", "DO"),
            ("Египет", "EG"),
            ("Замбия", "ZM"),
            ("Зимбабве", "ZW"),
            ("Израиль", "IL"),
            ("Индия", "IN"),
            ("Индонезия", "ID"),
            ("Иордания", "JO"),
            ("Ирак", "IQ"),
            ("Иран", "IR"),
            ("Ирландия", "IE"),
            ("Исландия", "IS"),
            ("Испания", "ES"),
            ("Италия", "IT"),
            ("Йемен", "YE"),
            ("Кабо-Верде", "CV"),
            ("Казахстан", "KZ"),
            ("Камбоджа", "KH"),
            ("Камерун", "CM"),
            ("Канада", "CA"),
            ("Катар", "QA"),
            ("Кения", "KE"),
            ("Кипр", "CY"),
            ("Киргизия", "KG"),
            ("Кирибати", "KI"),
            ("Китай", "CN"),
            ("Колумбия", "CO"),
            ("Коморы", "KM"),
            ("Конго", "CG"),
            ("Конго (ДРК)", "CD"),
            ("Коста-Рика", "CR"),
            ("Кот-д’Ивуар", "CI"),
            ("Куба", "CU"),
            ("Кувейт", "KW"),
            ("Лаос", "LA"),
            ("Латвия", "LV"),
            ("Лесото", "LS"),
            ("Либерия", "LR"),
            ("Ливан", "LB"),
            ("Ливия", "LY"),
            ("Литва", "LT"),
            ("Лихтенштейн", "LI"),
            ("Люксембург", "LU"),
            ("Маврикий", "MU"),
            ("Мавритания", "MR"),
            ("Мадагаскар", "MG"),
            ("Македония", "MK"),
            ("Малави", "MW"),
            ("Малайзия", "MY"),
            ("Мали", "ML"),
            ("Мальдивы", "MV"),
            ("Мальта", "MT"),
            ("Марокко", "MA"),
            ("Маршалловы Острова", "MH"),
            ("Мексика", "MX"),
            ("Микронезия", "FM"),
            ("Мозамбик", "MZ"),
            ("Молдова", "MD"),
            ("Монако", "MC"),
            ("Монголия", "MN"),
            ("Мьянма", "MM"),
            ("Намибия", "NA"),
            ("Непал", "NP"),
            ("Нигер", "NE"),
            ("Нигерия", "NG"),
            ("Нидерланды", "NL"),
            ("Никарагуа", "NI"),
            ("Новая Зеландия", "NZ"),
            ("Норвегия", "NO"),
            ("Объединенные Арабские Эмираты", "AE"),
            ("Оман", "OM"),
            ("Пакистан", "PK"),
            ("Палау", "PW"),
            ("Панама", "PA"),
            ("Папуа — Новая Гвинея", "PG"),
            ("Парагвай", "PY"),
            ("Перу", "PE"),
            ("Польша", "PL"),
            ("Португалия", "PT"),
            ("Россия", "RU"),
            ("Руанда", "RW"),
            ("Румыния", "RO"),
            ("Сальвадор", "SV"),
            ("Самоа", "WS"),
            ("Сан-Марино", "SM"),
            ("Сан-Томе и Принсипи", "ST"),
            ("Саудовская Аравия", "SA"),
            ("Северная Корея", "KP"),
            ("Сейшельские Острова", "SC"),
            ("Сенегал", "SN"),
            ("Сент-Винсент и Гренадины", "VC"),
            ("Сент-Китс и Невис", "KN"),
            ("Сент-Люсия", "LC"),
            ("Сербия", "RS"),
            ("Сингапур", "SG"),
            ("Сирия", "SY"),
            ("Словакия", "SK"),
            ("Словения", "SI"),
            ("Соломоновы Острова", "SB"),
            ("Сомали", "SO"),
            ("Судан", "SD"),
            ("Суринам", "SR"),
            ("США", "US"),
            ("Сьерра-Леоне", "SL"),
            ("Таджикистан", "TJ"),
            ("Таиланд", "TH"),
            ("Танзания", "TZ"),
            ("Того", "TG"),
            ("Тонга", "TO"),
            ("Тринидад и Тобаго", "TT"),
            ("Тувалу", "TV"),
            ("Тунис", "TN"),
            ("Туркмения", "TM"),
            ("Турция", "TR"),
            ("Уганда", "UG"),
            ("Узбекистан", "UZ"),
            ("Украина", "UA"),
            ("Уругвай", "UY"),
            ("Фиджи", "FJ"),
            ("Филиппины", "PH"),
            ("Финляндия", "FI"),
            ("Франция", "FR"),
            ("Хорватия", "HR"),
            ("Центральноафриканская Республика", "CF"),
            ("Чад", "TD"),
            ("Черногория", "ME"),
            ("Чехия", "CZ"),
            ("Чили", "CL"),
            ("Швейцария", "CH"),
            ("Швеция", "SE"),
            ("Шри-Ланка", "LK"),
            ("Эквадор", "EC"),
            ("Экваториальная Гвинея", "GQ"),
            ("Эритрея", "ER"),
            ("Эсватини", "SZ"),
            ("Эстония", "EE"),
            ("Эфиопия", "ET"),
            ("Южная Корея", "KR"),
            ("Южно-Африканская Республика", "ZA"),
            ("Южный Судан", "SS"),
            ("Ямайка", "JM"),
            ("Япония", "JP")
        ]


        def insert_geo(geo_code):
            asyncio.run(db_helper.insert_or_update_geo(geo_code))
            show_modal_dialog("Успех", f"Код страны {geo_code} успешно обновлен в базе данных.")

        search_field = ft.TextField(label="Поиск страны", on_change=lambda e: filter_buttons(e.control.value))

        # Создаем начальный список кнопок для каждой страны
        geo_buttons = []


        def filter_buttons(search_query):
            filtered_countries = [
                (country, code) for country, code in countries if search_query.lower() in country.lower()
            ]
            update_buttons(filtered_countries)

        def update_buttons(filtered_countries):
            # Удаляем старые кнопки
            geo_buttons.clear()  # Очищаем список кнопок

            # Создаем новые кнопки на основе отфильтрованных стран
            for country, code in filtered_countries:
                button = ft.ElevatedButton(f"{country} — {code}", on_click=lambda e, c=code: insert_geo(c))
                geo_buttons.append(button)

            # Обновляем содержимое модального окна
            modal_content.controls = [search_field] + geo_buttons
            modal_content.update()  # Обновляем содержимое модального окна

        geo_cod = asyncio.run(db_helper.get_geo())
        try:
            region = geo_cod[0][0]
        except IndexError:
            region = "Пуст"

        # Создание содержимого модального окна
        modal_content = ft.Column(
            [search_field] + geo_buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Выберите страну (Выбранный ГЕО: {region})"),
            content=ft.Container(content=modal_content, width=400, height=300),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: modal.close())],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()
    # Функция для настройки конфига залива
    def show_profile_modal():
        """Display the profile modal with the current token and option to update it."""

        # Asynchronously retrieve the current token from the database
        current_token = asyncio.run(db_helper.get_token())

        token_field = ft.TextField(value=current_token, width=300, label="Текущий токен")
        save_button = ft.ElevatedButton("Сохранить изменения", on_click=lambda e: save_token(token_field.value))
        back_button = ft.ElevatedButton("Назад", on_click=lambda e: close_modal(modal))

        modal_content = ft.Column(
            [
                ft.Text("Профиль"),
                token_field,
                save_button,
                back_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Профиль"),
            content=modal_content,
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def save_token(new_token):
        """Save the new token to the database."""
        asyncio.run(db_helper.update_token(new_token))
        show_modal_dialog("Успешно", "Токен обновлен.")
    def show_config_fill_page():
        page.views.clear()

        back_button = ft.ElevatedButton(
            "Назад",
            on_click=lambda e: show_main_page(),
            width=200
        )

        config_fill_button = ft.ElevatedButton(
            "Конфиг залива",
            on_click=lambda e: show_config_options_page(),
            color=ft.colors.WHITE, width=200, height=50
        )
        tik_tok_setting = ft.ElevatedButton(
            "Настройка Тик Тока",
            on_click=lambda e: show_setting_tt_page(),
            color=ft.colors.WHITE, width=200, height=50
        )
        GEO_button = ft.ElevatedButton(
            "ГЕО",
            on_click=lambda e: show_geo_modal(),
            color=ft.colors.WHITE, width=200, height=50
        )
        PROXY_button = ft.ElevatedButton(
            "Прокси",
            on_click=lambda e: show_proxy_modal(page),
            color=ft.colors.WHITE, width=200, height=50
        )
        ACC_button = ft.ElevatedButton(
            "Аккаунты",
            on_click=lambda e: show_accounts_modal(page),
            color=ft.colors.WHITE, width=200, height=50
        )
        MAIL_button = ft.ElevatedButton(
            "Почты",
            on_click=lambda e: show_email_modal(page),
            color=ft.colors.WHITE, width=200, height=50
        )
        CREO_button = ft.ElevatedButton(
            "Управление крео",
            on_click=lambda e: show_creo_management_page(),
            color=ft.colors.WHITE, width=200, height=50
        )
        locale_button = ft.ElevatedButton(
            "Locale",
            on_click=lambda e: show_locale_modal(),
            color=ft.colors.WHITE, width=200, height=50
        )

        page.views.append(
            ft.View(
                "/config_fill",
                [
                    ft.Container(
                        content=ft.Column(

                            [ft.Text(value='Настройка конфига', size=32, height=70),

                                GEO_button,
                                CREO_button,PROXY_button,
                                ft.Row(
                                    controls=[
                                        ACC_button,
                                        MAIL_button
                                    ],alignment=ft.MainAxisAlignment.CENTER,  # Выровняем кнопки по центру строки
                                    spacing=10
                                    ),
                                config_fill_button, tik_tok_setting,locale_button,
                                ft.Container(back_button, width=200, height=50)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ]
            )
        )
        page.update()

    # Страница с конфигурационными настройками
    def show_config_options_page():
        page.views.clear()

        back_button = ft.ElevatedButton(
            "Назад",
            on_click=lambda e: show_config_fill_page(),
            width=200
        )

        config_buttons = [
            ft.Container(
                ft.ElevatedButton("Аватарка", color=ft.colors.WHITE, on_click=lambda e: show_avatar_upload_modal()),width=200, height=50),
            ft.Container(ft.ElevatedButton("Юзернеймы", color=ft.colors.WHITE, on_click=lambda e: show_usernames_upload_modal()), width=200, height=50),
            ft.Container(ft.ElevatedButton("Хэштеги", color=ft.colors.WHITE, on_click=lambda e: show_hashtags_upload_modal()), width=200, height=50),
            ft.Container(ft.ElevatedButton("Био", color=ft.colors.WHITE, on_click=lambda e: show_bio_upload_modal()), width=200, height=50),
            ft.Container(ft.ElevatedButton("Описание", color=ft.colors.WHITE, on_click=lambda e: show_opi_upload_modal()), width=200, height=50),
            ft.Container(ft.ElevatedButton("Никнеймы", color=ft.colors.WHITE, on_click=lambda e: show_nickname_upload_modal()),width=200, height=50),
            ft.Container(ft.ElevatedButton("Отметки", color=ft.colors.WHITE, on_click=lambda e: show_mark_upload_modal()), width=200, height=50),
            ft.Container(ft.ElevatedButton("Биз. ссылка", color=ft.colors.WHITE, on_click=lambda e: show_biz_links_page(page)),width=200, height=50),
        ]

        page.views.append(
            ft.View(
                "/config_options",
                [
                    ft.Container(
                        content=ft.Column(
                            config_buttons,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Container(
                        back_button,
                        alignment=ft.alignment.bottom_center,
                        padding=ft.padding.only(bottom=20)
                    )
                ]
            )
        )
        page.update()

    def show_version_modal():
        # Получаем текущую версию
        current_version = asyncio.run(db_helper.get_current_version())

        # Функция обработки выбора версии
        def on_version_select(version):
            # Обновляем версию в базе данных
            asyncio.run(db_helper.update_version(version))
            # Показать подтверждение
            show_modal_dialog("Обновление версии", f"Версия TikTok обновлена на {version}")

        # Список версий из изображения
        versions = ["28.9.3", "29.8.4", "29.7.3", "30.8.4", "30.9.2", "30.9.1", "31.1.3", "31.5.3", "32.8.3"]
        versions2 = ["34.4.4", "34.5.2", "34.5.3", "34.9.3", "34.9.5", "35.0.4", "35.1.3", "35.7.3", "36.4.2"]

        # Создание кнопок для каждой версии
        version_buttons = [ft.ElevatedButton(text=v, on_click=lambda e, v=v: on_version_select(v)) for v in versions]
        version_buttons2 = [ft.ElevatedButton(text=v, on_click=lambda e, v=v: on_version_select(v)) for v in versions2]

        # Содержимое модального окна: показываем текущую версию и кнопки для выбора версии
        modal_content = ft.Column(
            [
                ft.Text(f"Текущая версия TikTok: {current_version}"),
                *version_buttons,
                *version_buttons2# Разворачиваем список кнопок
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        )

        # Создаем и отображаем модальное окно
        version_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Выберите версию TikTok"),
            content=modal_content,
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_modal(version_modal))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.overlay.append(version_modal)
        version_modal.open = True
        page.update()

    def show_locale_modal():
        try:
            current_locale = asyncio.run(db_helper.get_current_locale())
            if "-" in current_locale:
                first_part, second_part = current_locale.split("-", 1)
            else:
                first_part, second_part = "", ""

            # Creating the two TextFields
            locale_part1 = ft.TextField(value=first_part, width=100, label="Language")
            hyphen = ft.Text("-")
            locale_part2 = ft.TextField(value=second_part, width=100, label="Country")

            # Function to save the new locale
            def save_locale(e):
                new_locale = f"{locale_part1.value}-{locale_part2.value}"
                asyncio.run(db_helper.update_locale(new_locale))
                show_modal_dialog("Успешно", f"Locale обновлен на {new_locale}")

            # Button to save changes
            save_button = ft.ElevatedButton("Сохранить изменения", on_click=save_locale)

            # Modal structure
            modal_content = ft.Row(
                [locale_part1, hyphen, locale_part2],
                alignment=ft.MainAxisAlignment.CENTER
            )
            modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Изменить Locale"),
                content=ft.Column([modal_content, save_button]),
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )

            page.overlay.append(modal)
            modal.open = True
            page.update()
        except Exception as e:
            print(e)
    def show_setting_tt_page():
        page.views.clear()

        back_button = ft.ElevatedButton(
            "Назад",
            on_click=lambda e: show_config_fill_page(),
            width=200
        )

        config_buttons = [
            ft.Container(
                ft.ElevatedButton("Версии Тик Тока ", color=ft.colors.WHITE, on_click=lambda e: show_version_modal()),width=200, height=50),

        ]

        page.views.append(
            ft.View(
                "/config_options",
                [
                    ft.Container(
                        content=ft.Column(
                            config_buttons,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),

                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Container(

                        back_button,
                        alignment=ft.alignment.bottom_center,
                        padding=ft.padding.only(bottom=20)
                    )
                ]
            )
        )
        page.update()
    # Обработчик изменения маршрута
    def route_change(route):
        if page.route == "/fill":
            show_fill_page()
        elif page.route == "/config_fill":
            show_config_fill_page()
        elif page.route == "/config_options":
            show_config_options_page()
        else:
            show_main_page()

        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    # Защищаем основной код от повторного запуска в каждом процессе
    multiprocessing.freeze_support()  # Для Windows, чтобы предотвратить повторный запуск
    ft.app(target=main)
