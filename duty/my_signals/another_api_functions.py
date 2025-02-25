import os
import requests

from duty.objects import MySignalEvent, dp
from duty.utils import find_mention_by_event


@dp.longpoll_event_register('группы')
@dp.my_signal_event_register('группы')
def groups(event: MySignalEvent) -> str:
    uid = find_mention_by_event(event) or event.db.owner_id
    message = requests.get(f'http://api.lisi4ka.ru/groups/{uid}').json()['message']  # от ты жопа, пришёл код спиздить?)
    event.edit(message, keep_forward_messages=1)


@dp.longpoll_event_register('приложения')
@dp.my_signal_event_register('приложения')
def apps(event: MySignalEvent) -> str:
    uid = find_mention_by_event(event) or event.db.owner_id
    message = requests.get(f'http://api.lisi4ka.ru/apps/{uid}').json()['message']
    event.edit(message, keep_forward_messages=1)


@dp.my_signal_event_register('отвязать') # не апи функция, но какая разница где оно лежит?
def unbind_chat(event: MySignalEvent) -> str: # нахуя оно ток надо?
    e = event.db.chats.pop(event.obj['chat'], None)
    message = 'Чат успешно отвязан!' if e else 'Такого чата уже нет.'
    event.edit(message)


@dp.my_signal_event_register('связать')
def iosif_prosti(event: MySignalEvent) -> str:
    name = os.path.join(os.getcwd(), 'ICAD', 'duty', 'sorry.ogg')
    topovoe_audio_msg = open(name, "rb")
    nu_ne_zlis = event.api('docs.getUploadServer',
                           type='audio_message')['upload_url']
    budet_poshalka = requests.post(nu_ne_zlis,
                             files={'file': topovoe_audio_msg}).json()['file']
    a = event.api('docs.save', file=budet_poshalka)['audio_message']
    event.send(attachment=f'audio_message{a["owner_id"]}_{a["id"]}')


@dp.longpoll_event_register('курс')
@dp.my_signal_event_register('курс')
def exchange_rate(event: MySignalEvent) -> str:
    code = event.msg['text'].split()[-1]
    valutes = requests.get('https://api.lisi4ka.ru/valute').json()
    if code != 'курс':
        valute = valutes.get(code.upper())
        if valute is None:
            message = 'Центробанк не в курсе о такой валюте...'
        else:
            message = f'Курс валюты \"{valute["name"]}\": {valute["value"]}'
    else:
        message = f'$ Курс доллара: {valutes["USD"]["value"]}\n€ Курс евро: {valutes["EUR"]["value"]}'
    event.edit(message)
