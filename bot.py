import telebot  # импорт библиотеки для работы с telegram-api
to_add_point = -1  # этапы для режима "добавления предложения"

# импорт списка из файла
items = list()
item = list()
with open('list.txt', 'r') as file:
    for line in file:
        if line == '\n':
            items.append(item)
            item = list()
        else:
            line = line.strip()
            item.append(line)

bot = telebot.TeleBot(<token>)  # инициализируем бота, используя полученный api


@bot.message_handler(commands=['start'])  # обработка команды '/start'
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Я помогу найти тебе энергетики по самым привлекательным ценам!')


@bot.message_handler(commands=['list'])  # обработка команды '/list'
def show_list(message):
    info = ''
    counter = 0
    for i in items:
        info += 'Наименование: {0}\nЦена: {1}\nГород: {2}\nМагазин: {3}\n\n'.format(i[0], i[1], i[2], i[3])
        counter += 1
        if counter == 4:
            bot.send_message(message.chat.id, info)
            info = ''
            counter = 0
    if counter != 0:
        bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['add'])  # обработка команды '/add'
def add_switch(message):
    global to_add_point
    to_add_point = 0
    bot.send_message(message.chat.id, '+ Добавление предложения в список\nВведите наименование:')


@bot.message_handler(content_types=['text'])  # обработка информации о предложении
def add_to_list(message):
    global to_add_point
    global item
    if to_add_point == 0:
        item = list()
        item.append(str(message.text))
        to_add_point = 1
        return bot.send_message(message.chat.id, '+ Добавление предложения в список\nВведите цену:')
    if to_add_point == 1:
        try:
            item.append(str(float(message.text)))
            to_add_point = 2
            return bot.send_message(message.chat.id, '+ Добавление предложения в список\nВведите город:')
        except:
            return bot.send_message(message.chat.id, '+ Добавление предложения в список\nВведите цену:')
    if to_add_point == 2:
        item.append(str(message.text))
        to_add_point = 3
        return bot.send_message(message.chat.id, '+ Добавление предложения в список\nВведите магазин:')
    if to_add_point == 3:
        to_add_point = -1
        item.append(str(message.text))
        items.append(item)
        item = list()
        with open('list.txt', 'w') as file:  # сохранение предложения в файле
            for i in items:
                for j in i:
                    file.write(j + '\n')
                file.write('\n')
        return bot.send_message(message.chat.id, '+ Добавление предложения в список\nПредложение добавлено!')


if __name__ == '__main__':  # мониторинг сообщений
    bot.polling()
