import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from wikipedia import wikipedia

vk_session = vk_api.VkApi(token="0ac7157fbe6a96742bf0acb3c58575ff1752a3ab15250d936c83a5cbc11dd8f987b3a435eeaa1df26b718")

vk_long = VkLongPoll(vk_session)
vk = vk_session.get_api()

wikipedia.set_lang('ru')


def sendmessage(user_id, text):
    vk.messages.send(
        random_id=get_random_id(),
        user_id=user_id,
        message=text)


for event in vk_long.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        peer_id = event.peer_id
        cmd = str(event.text).split(" ")
        if cmd[0] == '/search':
            try:
                to_find = str(event.text).replace(cmd[0] + " ", "")
                page = wikipedia.page(to_find)
                to_len = len(page.content) + 180 - len(page.content)
                message = page.title + "\n\n" + page.content[:to_len] + "\n\n" + "Подробнее: " + page.url
                sendmessage(peer_id, message)
            except NameError:
                sendmessage(peer_id, "Использование /search <Запрос>")
            except IndexError:
                sendmessage(peer_id, "Использование /search <Запрос>")
            except wikipedia.DisambiguationError:
                sendmessage(peer_id, "Таких статей несколько, в дальнейшем будет исправлено")
            except wikipedia.PageError:
                sendmessage(peer_id, "Такого запроса не существует в Википедии")
