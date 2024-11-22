from http.client import responses
import json
import requests
from pprint import  pprint
from tkinter import *
from tkinter import  messagebox

# ID App 52723729


# 1. Класс для работы с API VK

class VKAPIClient:


    API_BASE_URL = 'https://api.vk.com/method/'

    access_token = (
                    'vk1.a.3Pq7X_XicKLFSiqgmO2qYvPVR6dlplc_9SKflZMqe6WNO5L0wCq4N'
                    'mfyNdNoKsCUwP9kEGf-2_RZ8QxULKLHmzK3PStlCDGAarKNEeTES-G6I6sc'
                    'VTlsr9Bv7M4lxiTxO-S2t4uwKF0svDvZtm7Hj1tpyYXZVL6OGpLtLNHXan8'
                    'sTdj37AC62s9z-LwLjmZOJMCRSLEm8boVmnKQnZZrjw'
    )

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
        return photo_set

    @staticmethod
    def write_result_to_json(photo_set):
        with open(r'files\result.json', 'w', encoding = 'utf-8') as f:
            json.dump(photo_set, f)

    @staticmethod
    def read_result_from_json():
        with open(r'files\result.json', encoding = 'utf-8') as f:
            data = json.load(f)
            return data

    def get_app_permissions(self):
        params = params = self.get_common_params()
        response = requests.get(self._build_url('account.getAppPermissions'),
                                params=params)
        return response.json()

    def users_info(self):
        params = params = self.get_common_params()
        response = requests.get(self._build_url('users.get'), params=params)
        return response.json()

# vk_client = VKAPIClient(844252190)
# photos_info = vk_client.get_profile_photos_set()
# print(photos_info)


# 2. Класс для работы с API ЯндексДиска

class APIYaDiClient:

    base_api_yadi_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, yadi_token):
        self.yadi_token = yadi_token

    def get_base_params(self):
        pass
        return {}

    def get_base_headers(self):
        return {
            'Content-Type': 'application/json'
        }

    def create_directory(self,dir_name):
        headers = self.get_base_headers()
        headers.update({'Authorization': f'OAuth {token}'})
        params = self.get_base_params()
        params['path'] = dir_name
        response = requests.put(self.base_api_yadi_url, params=params,
                                headers=headers)
        status = response.status_code
        request_info = response.json()
        if status == 201:
            return messagebox.showinfo(f'Статус запроса: {status}',
                                message = 'Папка успешно создана')
        elif status == 409:
            return messagebox.showinfo(f'Статус запроса: {status}',
                                message = 'Папка уже существует')
        else:
            return messagebox.showerror(f'Код ошибки: {status}',
                             message = request_info['message'])

    def get_equal_likes_id(data_list, number):
        if data_list and number != 0:
            id_list = []
            for i in range(number - 1):
                j = i
                while j != number - 1:
                    if data_list[i][1]['likes'] == data_list[j + 1][1][
                        'likes']:
                        if data_list[i][0] not in id_list:
                            id_list.append(data_list[i][0])
                        if data_list[j + 1][0] not in id_list:
                            id_list.append(data_list[j + 1][0])
                    j += 1
        return id_list

    def get_filename(data_list):
        same_likes_id = self.get_equal_likes_id(data_list, number):



    def upload_photo(self, data_list, number, dir_name):

        headers = self.get_base_headers()
        headers.update({'Authorization': f'OAuth {token}'})
        params = self.get_base_params()
        for item in data_list:
            while number !=0:

                params['path'] = f'{dir_name}/test_{number}.jpg'
                response = requests.put(self.base_api_yadi_url, params=params,
                                        headers=headers, data=item)
                number -= 1
                status = response.status_code
                request_info = response.json()
                if status == 202:
                    return messagebox.showinfo(f'Статус запроса: {status}',
                                        message = f'Фотография успешно загружена! Номер файла: {number}')
                else:
                    return messagebox.showerror(f'Код ошибки: {status}',
                                            message=request_info['message'])
                break
        response = requests.put(self.base_api_yadi_url, params=params,
                                headers=headers)
        status = response.status_code
        request_info = response.json()
        if status == 202:
            return messagebox.showinfo(f'Статус запроса: {status}',
                                    message = 'Фотография успешно загружена!')
        else:
            return messagebox.showerror(f'Код ошибки: {status}',
                                        message=request_info['message'])

url_img = 'https://sun9-8.userapi.com/s/v1/ig2/DbA4aS63eykzzE7wnpkjGVFI6Fva39zo4m3GvlkOOqBvOP3GvfaLHIQ7PVCQIvls5SLu8elSshhvvuNdER44xi8l.jpg?quality=95&as=32x18,48x27,72x40,108x61,160x90,240x135,360x202,480x270,540x303,640x360,712x400&from=bu&cs=510x340'

headers = {
    'Authorization': 'OAuth y0_AgAEA7qkZeZYAADLWwAAAAEY18JCAABjJwF-aJBDhog39WFo7_nk1o4IAA',
    'Content-Type': 'application/json',
}
yadi_url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
params = {
    'url': url_img,
    'path': 'test_2/test'
}
response = requests.get(yadi_url_upload, params=params, headers=headers)
# upload_url = response.json()['href']

# upload_url = response.json().get('href')
#
# with (open(filename, 'rb') as f):
#     response = requests.put(upload_url, files={'file': f})


# 3. Класс для работы с графическим интерфейсом

class GUIRequestApplication:
    def __init__(self, root):
        self.root = root
        self.root.title('Резервная копия фотографий профиля VK')
        self.root.geometry('450x250')
        self.root.resizable(width=False, height=False)
        self.root['bg'] = 'blue'
        self.user_id_entry = ''
        self.token_entry = ''
        # self.progressbar = root.Progressbar(self.root, orient=HORIZONTAL,
        #                                    length=200, mode='determinate')
        # self.progressbar.pack(pady=10)
        self.create_widgets()

    def send_request(self):
        user_id = self.user_id_entry.get()
        if user_id.isdigit() and len(user_id) == 9:
            user_id = int(user_id)
        else:
            messagebox.showerror(message= 'Ошибка ввода ID пользователя!')
        token = self.token_entry.get()
        if token:
            vk_client = VKAPIClient(user_id)
            return vk_client.get_profile_photos_set()
        else:
            messagebox.showerror(message='Ошибка ввода токена!')


    def create_widgets(self):
        user_id_label = Label(self.root,text ='ID пользователя в VK',
                              font='Arial 11 bold',
                               bg='blue', fg='white', padx=20, pady=10)
        user_id_label.pack()

        self.user_id_entry = Entry(self.root, font='Arial 12',
                                    bg='lightblue',
                               fg='black')
        self.user_id_entry.pack()

        token_label = Label(self.root, text ='Токен доступа к '
                                                  'Яндекс.Диск',
                            font='Arial 11 bold',bg='blue', fg='white',
                            padx=20, pady=10)
        token_label.pack()

        self.token_entry = Entry(self.root, font='Arial 12', bg='lightblue',
                             fg='black')
        self.token_entry.pack()

        send_btn = Button(self.root, text ='Отправить запрос',
                          command=self.send_request,
                          foreground='blue')
        send_btn.pack(padx=40, pady=20)



    # def start_progressbar(self):
    #     # Создание потока для обновления прогресс бара
    #     self.thread = threading.Thread(target=self.update_progressbar)
    #     self.thread.start()
    #
    # def update_progressbar(self):
    #     # Обновление прогресс бара
    #     for i in range(101):
    #         self.progressbar['value'] = i
    #         self.root.update_idletasks()
    #         time.sleep(0.05)
    #     self.label.config(text="Завершено!")


# def click():
#     window = Tk()
#     window.title("Новое окно")
#     window.geometry("250x200")
#     close_button = ttk.Button(window, text="Закрыть окно",
#                               command=lambda: window.destroy())
#     close_button.pack(anchor="center", expand=1)
#
#
# open_button = ttk.Button(text="Создать окно", command=click)
# open_button.pack(anchor="center", expand=1)



root = Tk()
request_app = GUIRequestApplication(root)
root.mainloop()
# token = 'OAuth y0_AgAEA7qkZeZYAADLWwAAAAEY18JCAABjJwF-aJBDhog39WFo7_nk1o4IAA'
# test = APIYaDiClient(token)
# test.create_directory('test_2')



