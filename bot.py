from os import getenv, urandom

import sqlalchemy
import telegram
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from app import db
from table import User, Chat, Group

session = db.session


def reply(update, text, *args, **kwargs):
    update.message.reply_text(text, args, **kwargs)


def add_commit(*args, **kwargs):
    session.add(*args, **kwargs)
    session.commit()


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update: Update, context):
    try:
        user_id = update['message']['from_user']['id']
        if update['message']['chat']['type'] == 'private':
            if session.query(User).filter(User.id == user_id).count():
                reply(update, '''Вы уже состоите в классе и можете использовать возможности бота.
Полная справка /help''')
            else:
                reply(update, '''Вы не состоите в классе. Если вы есть в группе, где бот используется, '''
                              '''напишите туда /start
Если хотите создать свой класс, введите /create
Полная справка /help''')
        else:
            chat_id = update['message']['chat']['id']
            user = session.query(User).filter(User.id == user_id).first()
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if user and user.access > 0:
                if chat:
                    if chat.group == user.group:
                        reply(update, 'Эта группа уже привязана к вашему классу')
                    else:
                        reply(update, 'Вы владеете классом, а эта группа уже привязана к другому классу')
                else:
                    chat = Chat(id=chat_id, group=user.group)
                    add_commit(chat)
                    reply(update, 'Эта группа привязана к вашему классу')
                    context.bot.send_message(chat_id, 'Чтобы писать боту в ЛС сначала напишите сюда /start')
            elif not user:
                if chat:
                    user = User(id=user_id, name=update['message']['from_user']['first_name'] + ' ' +
                                                 update['message']['from_user']['last_name'])
                    user.group = chat.group
                    context.bot.send_message(user_id, 'Вы успешно добавлены в класс')
                    if chat.group.creator_id == user.id:
                        user.access = 2
                        context.bot.send_message(user_id, 'Вы были создателем этого класса, права возвращены')
                    add_commit(user)
                else:
                    reply(update, 'Сначала нужно создать класс. Напишите боту в лс.')
            elif user.group != chat.group:
                reply(update, 'Вы должны являться администратором класса, чтобы привязать его к группе')
    except Exception as e:
        print(e)


def create(update, context):
    try:
        if update['message']['chat']['type'] != 'private':
            reply(update, 'Создать класс можно только в лс')
        else:
            user = session.query(User).filter(User.id == update['message']['from_user']['id']).first()
            if user:
                reply(update, 'Вы не можете создать класс, пока привязаны к другому. Выйти - /leave')
            else:
                group = Group(creator_id=update['message']['from_user']['id'])
                user = User(id=group.creator_id, group=group, access=2,
                            name=update['message']['from_user']['first_name'] + ' ' +
                            update['message']['from_user']['last_name'])
                session.add(user)
                add_commit(group)
                reply(update, 'Вы создали класс')
    except Exception as e:
        print(e)


def leave(update, context):
    try:
        if update['message']['chat']['type'] != 'private':
            reply(update, 'Ливать можно только в лс')
        else:
            user = session.query(User).filter(User.id == update['message']['from_user']['id']).first()
            if user:
                if len(user.group.users) == 1:
                    for i in user.group.chats:
                        context.bot.send_message(i.id, '''Последний пользователь привязанного класса вышел
Класс удалён''')
                    for i in [user.group.chats, user.group.lessons, user.group.subgroups, user.group.teachers]:
                        for j in i:
                            session.delete(j)
                    reply(update, 'ты чево наделал...')
                else:
                    reply(update, 'Вы вышли из класса')
                session.delete(user.group)
                session.delete(user)
                session.commit()
            else:
                reply(update, 'Вы не привязаны ни к какому классу')
    except Exception as e:
        print(e)


def get_code(update, context):
    if update['message']['chat']['type'] == 'private':
        user = session.query(User).filter(User.id == update['message']['from_user']['id']).first()
        if user:
            code = urandom(8).hex()
            user.set_password(code)
            session.commit()
            update.message.reply_markdown(f'Ваш код: `{code}`\nДействителен 1 день')


def bot():
    if getenv("PROXY_URL"):
        updater = Updater(getenv('TOKEN'), use_context=True,
                          request_kwargs={'proxy_url': getenv("PROXY_URL")})
    else:
        updater = Updater(getenv('TOKEN'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('create', create))
    dp.add_handler(CommandHandler('leave', leave))
    dp.add_handler(CommandHandler('get_code', get_code))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    try:
        updater.idle()
    except ValueError as e:
        print(e)
        pass


if __name__ == '__main__':
    bot()
