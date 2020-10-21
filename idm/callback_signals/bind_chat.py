from idm.objects import dp, Event, Chat


@dp.event_register('bindChat')
def bind_chat(event: Event) -> str:
    cmid_key = 'conversation_message_id'
    search_res = event.api("messages.search",
                           q=event.msg['text'], count=10, extended=1)
    for msg in search_res['items']:
        if msg[cmid_key] == event.msg[cmid_key]:
            if msg['from_id'] == event.msg['from_id']:
                message = msg
                break
    for conv in search_res['conversations']:
        if conv['peer']['id'] == message['peer_id']:  # type: ignore
            chat_name = conv['chat_settings']['title']
            break
    chat_raw = {
        "peer_id": message['peer_id'],  # type: ignore
        "name": chat_name,  # type: ignore
        "installed": False
    }
    event.db.chats.update({event.obj['chat']: chat_raw})
    event.db.save()
    event.chat = Chat(chat_raw, event.obj['chat'])
    event.api.msg_op(1, event.chat.peer_id,
                     event.responses['chat_bind'].format(имя=event.chat.name))
    return "ok"
