import threading
import time
from cProfile import label
from http.client import responses
import json
from tkinter.ttk import Progressbar
from typing import reveal_type
import requests
from pprint import  pprint
from tkinter import *
from tkinter import  messagebox
import datetime
from requests import request


# ID App 52723729


# 1. Класс для работы с API VK


class VKAPIClient:

    API_BASE_URL = 'https://api.vk.com/method/'

    # Токен приложения для рабочего компьютера

    # access_token = (
    #                 'vk1.a.3Pq7X_XicKLFSiqgmO2qYvPVR6dlplc_9SKflZMqe6WNO5L0wCq4N'
    #                 'mfyNdNoKsCUwP9kEGf-2_RZ8QxULKLHmzK3PStlCDGAarKNEeTES-G6I6sc'
    #                 'VTlsr9Bv7M4lxiTxO-S2t4uwKF0svDvZtm7Hj1tpyYXZVL6OGpLtLNHXan8'
    #                 'sTdj37AC62s9z-LwLjmZOJMCRSLEm8boVmnKQnZZrjw'
    # )


    # Токен приложения для домашнего компьютера

    access_token = 'vk1.a.96eGhn0Y-Sa7MYUuZilPWc82HcUclozGyFEG6-mpbkxrffdOkFziz5KiuRoZBScm_xX8CUGBJecyE6LjZPYcNSK6lhpXJHOJjlJ05Dtz_Q_hbZ71cj7hS1VGg3vSvvyODcGf-gWZAGTO82pE9Em_oUx4qGO-Wz218ussMU1lp2H4YFVNCTo2AWK63ZvU3cAPOmX22QUHT2dSd4nr7u2KEA'

    @staticmethod
    def write_result_to_json(photo_set):
        with open(r'files\result.json', 'w', encoding = 'utf-8') as f:
            json.dump(photo_set, f, indent=2)

    @staticmethod
    def read_result_from_json():
        with open(r'files\result.json', encoding = 'utf-8') as f:
            data = json.load(f)
            return data

    def __init__(self, user_id):
        self.token = self.access_token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.199'
        }

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def get_profile_photos_set(self):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile',
                       'extended': 1, 'photo_sizes': 1})
        response = requests.get(self._build_url('photos.get'), params=params)
        response_json = response.json()
        photo_set = {}
        for photo in response_json['response']['items']:
            photo_set[photo['id']] = {}
            for element in photo:
                photo_set[photo['id']]['likes'] = photo['likes']['count']
                photo_set[photo['id']]['date'] = photo['date']
                photo_set[photo['id']]['height'] = photo['sizes'][-1][
                    'height']
                photo_set[photo['id']]['width'] = photo['sizes'][-1][
                    'width']
                photo_set[photo['id']]['size_type'] = photo['sizes'][
                    -1]['type']
                photo_set[photo['id']]['url'] = photo['sizes'][-1]['url']
        photo_set = sorted(photo_set.items(),key=lambda item:
                                  item[1].get('height', 0) *
                                  item[1].get('width', 0),
                                  reverse = True)
        pprint(photo_set)
        return photo_set

    def get_app_permissions(self):
        params = params = self.get_common_params()
        response = requests.get(self._build_url('account.getAppPermissions'),
                                params=params)
        return response.json()

    def users_info(self):
        params = params = self.get_common_params()
        response = requests.get(self._build_url('users.get'), params=params)
        return response.json()


# 2. Класс для работы с API ЯндексДиска


class APIYaDiClient:

    base_api_yadi_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, yadi_token):
        self.yadi_token = yadi_token
        self.upload_counter = 0
        self.same_id_list = []

    def get_base_params(self):
        pass
        return {}

    def get_base_headers(self):
        return {
            'Content-Type': 'application/json'
        }

    def create_directory(self, dir_name):
        headers = self.get_base_headers()
        headers.update({'Authorization': f'OAuth {self.yadi_token}'})
        params = self.get_base_params()
        params['path'] = dir_name
        response = requests.put(self.base_api_yadi_url, params=params,
                                headers=headers)
        status = response.status_code
        request_info = response.json()
        if status == 201:
            messagebox.showinfo(f'Статус запроса: {status}',
                                message = 'Папка успешно создана')
            return status
        elif status == 409:
            messagebox.showinfo(f'Статус запроса: {status}',
                                message = 'Папка уже существует')
            return status
        else:
            messagebox.showerror(f'Код ошибки: {status}',
                             message = request_info['message'])
            return status

    @staticmethod
    def get_date(publication_date):
        return datetime.datetime.fromtimestamp(publication_date).strftime(
            '%Y-%m-%d')

    def get_equal_likes_id(self, data_list, number):
        if data_list and number != 0:
            for i in range(number - 1):
                j = i
                while j != number - 1:
                    if data_list[i][1]['likes'] == data_list[j + 1][1][
                        'likes']:
                        if data_list[i][0] not in self.same_id_list:
                            self.same_id_list.append(data_list[i][0])
                        if data_list[j + 1][0] not in self.same_id_list:
                            self.same_id_list.append(data_list[j + 1][0])
                    j += 1

    @staticmethod
    def get_filename(photo_id_list, photo_data: tuple):
        if photo_data[0] in photo_id_list:
            filename = (f'{photo_data[1]['likes']}_'
                        f'{APIYaDiClient.get_date(photo_data[1]['date'])}')
            return filename
        else:
            filename = f'{photo_data[1]['likes']}'
            return filename

    @staticmethod
    def get_file_extension(url_string):
        return url_string.rpartition('?')[0].rpartition('.')[2]

    def upload_photo(self, photo_data_list, item_number, resourse_name):
        request_app.create_progressbar(item_number)
        status = self.create_directory(resourse_name)
        if status == 201 or status == 409:
            headers = self.get_base_headers()
            headers.update({'Authorization': f'OAuth {self.yadi_token}'})
            params = self.get_base_params()
            self.get_equal_likes_id(photo_data_list, item_number)
            request_url  = f'{self.base_api_yadi_url}/upload'
            result_report = []
            for item in photo_data_list[:item_number]:
                filename = self.get_filename(self.same_id_list, item)
                file_extension = self.get_file_extension(item[1]['url'])
                params['path'] = (f'{resourse_name}/{str(filename)}'
                                  f'.{file_extension}')
                params['url'] = item[1]['url']
                response = requests.post(request_url, params=params,
                                         headers=headers)
                self.upload_counter += 1
                status = response.status_code
                result_report.append({'file_name': f'{filename}.{file_extension}',
                                      'size': item[1]['size_type']})
                request_info = response.json()
                if status != 202 and status != 409:
                    return messagebox.showerror(f'Код ошибки: {status}',
                                            message=request_info['message'])
                request_app.start_progressbar(self.upload_counter, item_number)
            VKAPIClient.write_result_to_json(result_report)
            request_app.stop_progressbar()
            return result_report


# 3. Класс для работы с графическим интерфейсом


class GUIRequestApplication:
    def __init__(self, root):
        self.root = root
        self.root.title('Резервная копия фотографий профиля VK')
        self.root.iconbitmap(r'resourses/icon-sm-gru.ico')
        self.root.geometry('450x500')
        self.root.resizable(width=False, height=False)
        self.root['bg'] = 'blue'
        self.user_id_entry = ''
        self.token_entry = ''
        self.photo_number_entry = ''
        self.resourse_name_entry = ''
        self.photo_data_list = []
        self.photo_counter = 0
        self.create_widgets()
        self.progressbar = None
        self.message_text = ''

    def send_request(self):
        user_id = self.user_id_entry.get()
        if user_id.isdigit() and len(user_id) == 9:
            user_id = int(user_id)
        else:
            messagebox.showerror(message= 'Ошибка ввода ID пользователя!')
        token = self.token_entry.get()
        if token:
            vk_client = VKAPIClient(user_id)
            photo_set = vk_client.get_profile_photos_set()
            if photo_set:
                self.get_responce_result(photo_set)
                self.photo_data_list = photo_set
        else:
            messagebox.showerror(message='Ошибка загрузки!')

    def create_widgets(self):
        user_id_label = Label(self.root, text='ID пользователя в VK',
                              font='Arial 11 bold', bg='blue', fg='white',
                              padx=10, pady=10)
        user_id_label.pack()

        self.user_id_entry = Entry(self.root, font='Arial 12', bg='lightblue',
                                   fg='black', width=12)
        self.user_id_entry.pack()

        token_label = Label(self.root, text ='Токен доступа к Яндекс.Диск',
                            font='Arial 11 bold',bg='blue', fg='white',
                            padx=10, pady=10)
        token_label.pack()

        self.token_entry = Entry(self.root, font='Arial 12', bg='lightblue',
                                 fg='black', width=45)
        self.token_entry.pack()

        send_btn = Button(self.root, text ='Отправить запрос',
                          font='Arial 10 bold', command=self.send_request,
                          foreground='blue')
        send_btn.pack(padx=10, pady=20)

    def get_responce_result(self, responce_result):
        if responce_result:
            self.photo_counter = len(responce_result)
            responce_text = (f'В вашем альбоме профиля {self.photo_counter} '
                             f'фотографий.\nСколько '
                             f'фотографий загрузить на Яндекс.Диск?')

            responce_label = Label(self.root, text=responce_text,
                                   font='Arial 10 bold', bg='blue', fg='white',
                                   padx=10, pady=10)
            responce_label.pack()

            self.photo_number_entry = Entry(self.root, font='Arial 12',
                                            bg='lightblue',fg='black', width=5)
            self.photo_number_entry.pack()

            resourse_name_label = Label(self.root, text='Введите имя папки',
                                   font='Arial 10 bold', bg='blue', fg='white',
                                   padx=10, pady=10)
            resourse_name_label.pack()

            self.resourse_name_entry = Entry(self.root, font='Arial 12',
                                            bg='lightblue', fg='black',
                                            width=30)
            self.resourse_name_entry.pack()

            upload_btn = Button(self.root, text='Загрузить',
                                font='Arial 10 bold', foreground='blue',
                                command=self.start_upload_photo)
            upload_btn.pack(padx=10, pady=10)
        else:
            return 'Отправка запроса не удалась!'

    def start_upload_photo(self):
        item_number = self.photo_number_entry.get()
        if item_number.isdigit():
            item_number = int(item_number)
        else:
            messagebox.showerror(message='Ошибка ввода числа фотографий!')
        resourse_name = self.resourse_name_entry.get()
        yadi_token = self.token_entry.get()
        if item_number <= self.photo_counter:
            yadi_client = APIYaDiClient(yadi_token)
            yadi_client.upload_photo(self.photo_data_list, item_number,
                                     resourse_name)
        else:
            messagebox.showerror(message='Ошибка ввода числа фотографий!')

    def create_progressbar(self, value):
        self.message_text = StringVar()

        num_label = Label(self.root, font='Arial 10 bold',
                          textvariable=self.message_text,
                          bg='blue', fg='white', padx=10, pady=10)
        num_label.pack()

        self.progressbar = Progressbar(self.root, orient=HORIZONTAL,length=300,
                                       mode='determinate', maximum=value)
        self.progressbar.pack(pady=10)

        return self.progressbar

    def start_progressbar(self, progress, counter):
        self.progressbar['value'] = progress
        self.message_text.set(f'Загружено {self.progressbar['value']} из'
                          f' {counter} фотографий')
        self.root.update_idletasks()

    def stop_progressbar(self):
        self.progressbar.destroy()
        self.message_text.set('Загрузка завершена!')
        result_json_btn = Button(self.root, text='Просмотреть\nрезультат',
                            font='Arial 10 bold', foreground='blue',
                            command=self.get_upload_result)
        result_json_btn.pack(padx=10, pady=10)

    def get_upload_result(self):
        window = Tk()
        window.title('Результат загрузки')
        window.geometry('450x500')
        close_button = Button(window, text='Закрыть окно',
                              command=lambda: window.destroy())
        close_button.pack(side='bottom')
        text_area = Text(window, width=100, height=50, font='Arial 12')
        text_area.pack()
        try:
            with open(r'files/result.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(data)
                text_area.delete('1.0', END)
                text_area.insert(INSERT, str(data))
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Невозможно декодировать JSON")



root = Tk()
request_app = GUIRequestApplication(root)
root.mainloop()
# token = 'OAuth y0_AgAEA7qkZeZYAADLWwAAAAEY18JCAABjJwF-aJBDhog39WFo7_nk1o4IAA'
# test = APIYaDiClient(token)
# test.create_directory('test_2')



