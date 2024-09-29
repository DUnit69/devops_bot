import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error
import logging
import re
import paramiko
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

load_dotenv()


emailListBig = []
phoneListBig = []

chat_id = "5702008976"
TOKEN = os.getenv('TOKEN')

DATABASE = range(1)
DATABASE2 = range(1)

host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Подключаем логирование
#logging.basicConfig(
#//    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
#//)

#logger = logging.getLogger(__name__)

phoneNumberRegex = re.compile(r'\d{1}-\d{3}-\d{3}-\d{2}-\d{2}')



def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def helpCommand(update: Update, context):
    update.message.reply_text('Help!')

def getPhones(update: Update, context):

    connection = None
    print("Wait..")

    try:
        #db_engine = get_db_engine().connect()
        connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                        password=os.getenv('DB_PASSWORD'),
                                        host=os.getenv('DB_HOST'),
                                        port=os.getenv('DB_PORT'), 
                                        database=os.getenv('DB_DATABASE'))
        cursor = connection.cursor()
        print("YES")
        cursor.execute("SELECT * FROM phones;")
        #select_query = f"SELECT * FROM phones;"
        #data = db_engine.execute(select_query)
        
        data = cursor.fetchall()
        for row in data:
            print(row)  
            row = str(row).replace('\\n', '\n').replace('\\t', '\t')
            update.message.reply_text(row)
        #logging.info("Команда успешно выполнена")
    #except (Exception, Error) as error:
        #logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            #db_engine.close()
            cursor.close()
            connection.close()

def getEmails(update: Update, context):
    print("Wait..")
    connection = None
    print("Wait2..")
    try:
        #db_engine = get_db_engine().connect()
        connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                        password=os.getenv('DB_PASSWORD'),
                                        host=os.getenv('DB_HOST'),
                                        port=os.getenv('DB_PORT'), 
                                        database=os.getenv('DB_DATABASE'))
        cursor = connection.cursor()
        print("YES")
        #select_query = f"SELECT * FROM emails;"
        #data = db_engine.execute(text(select_query))
        
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        for row in data:
            print(row)  
            row = str(row).replace('\\n', '\n').replace('\\t', '\t')
            update.message.reply_text(row)
        #logging.info("Команда успешно выполнена")
    #except (Exception, Error) as error:
        #logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("supa")
            #db_engine.close()

def getRepl(update: Update, context):

    connection = None
    print("Wait2..")
    try:
        #db_engine = get_db_engine().connect()
        connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                        password=os.getenv('DB_PASSWORD'),
                                        host=os.getenv('DB_HOST'),
                                        port=os.getenv('DB_PORT'), 
                                        database=os.getenv('DB_DATABASE'))
        cursor = connection.cursor()
        print("YES")
        #select_query = f"SELECT * FROM emails;"
        #data = db_engine.execute(text(select_query))
        
        cursor.execute("SELECT pg_read_file(pg_current_logfile());")
        data = cursor.fetchall()
        for row in data:
            print(row)
            row = str(row).replace('\\n', '\n').replace('\\t', '\t')
            if len(row) > 4096:
                for x in range(0, len(row), 4096):
                    update.message.reply_text(row[x:x+4096])
            else:
                update.message.reply_text(row)
        #logging.info("Команда успешно выполнена")
    #except (Exception, Error) as error:
        #logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("supa")
            #db_engine.close()

def getRelease(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /etc/*-release')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getUname(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getUptime(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getDf(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getFree(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getMpstat(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getW(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getAuths(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -q SYSLOG_FACILITY=4 -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getCritical(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -p 2 -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getPs(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(' ps ')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getSs(update: Update, context):
    
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(' ss -u -t')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getServices(update: Update, context):

    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('service --status-all')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def getAptListCommand(update: Update, context):
    update.message.reply_text('Введите название пакета: ')

    return 'getAptListAll'
        

def getAptListAll(update: Update, context):
    user_input = update.message.text
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('apt list | grep ^' + user_input)
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    print(data)
    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            update.message.reply_text(data[x:x+4096])
    else:
        update.message.reply_text(data)
    return ConversationHandler.END

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'


def findPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'\+?[8|7]-? ?\(?\d{3}\)? ?-?\d{3}-? ?\d{2}-? ?\d{2}') # формат 8 (000) 000-00-00

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return # Завершаем выполнение функции
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
    global phoneListBig
    phoneListBig = phoneNumberList
        
    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю
    update.message.reply_text('Хотите записать найденные телефоны в базу данных? [да]/[*]') # Отправляем сообщение пользователю
    return DATABASE2

def databasePhones(update: Update, context):
    global phoneListBig
    user_input = update.message.text
    if str(user_input) == "да":
        print(2)
        connection = None

        try:
            #db_engine = get_db_engine().connect()
            connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                        password=os.getenv('DB_PASSWORD'),
                                        host=os.getenv('DB_HOST'),
                                        port=os.getenv('DB_PORT'), 
                                        database=os.getenv('DB_DATABASE'))
            
            cursor = connection.cursor()
            for i in phoneListBig:
                #insert_query = f"INSERT INTO phones (phone) VALUES ('{i}');"
                #db_engine.execute(text(insert_query).execution_options(autocommit=True))
                cursor.execute("INSERT INTO phones (phone) VALUES ('"+i+"');")
            print(3)
            connection.commit()
            update.message.reply_text("Команда успешно выполнена")
            return ConversationHandler.END
        except (Exception, Error) as error:
            update.message.reply_text("Ошибка при работе с PostgreSQL: %s", error)
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                #db_engine.close()
    else:
        update.message.reply_text('Ладно...')
        return ConversationHandler.END # Завершаем работу обработчика диалога    


def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска электронных почт: ')

    return 'findEmail'


def databaseEmail(update: Update, context):
    global emailListBig
    user_input = update.message.text
    if str(user_input) == "да":
        print(2)
        connection = None

        try:
            #db_engine = get_db_engine().connect()
            connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                        password=os.getenv('DB_PASSWORD'),
                                        host=os.getenv('DB_HOST'),
                                        port=os.getenv('DB_PORT'), 
                                        database=os.getenv('DB_DATABASE'))
            
            cursor = connection.cursor()
            for i in emailListBig:
                print(i)
                i = str(i)
                #insert_query = f"INSERT INTO public.emails (email) VALUES ('"+i+"');"
                #db_engine.execute(text(insert_query))
                cursor.execute("INSERT INTO emails (email) VALUES ('"+i+"');")
            print(3)
            connection.commit()
            update.message.reply_text("Команда успешно выполнена")
            #db_engine.close()
            return ConversationHandler.END
        except (Exception, Error) as error:
            update.message.reply_text("Ошибка при работе с PostgreSQL: %s", error)
        finally:
            if connection is not None:
                #db_engine.close()
                cursor.close()
                connection.close()

    else:
        update.message.reply_text('Ладно...')
        return ConversationHandler.END # Завершаем работу обработчика диалога    

def findEmail (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) почт

    emailRegex = re.compile(r'\w+@\w+[\.\w]+') # формат sample@sample.sample[].sample]

    emailList = emailRegex.findall(user_input) # Ищем почты

    if not emailList: # Обрабатываем случай, когда номеров почт нет
        update.message.reply_text('электронные почты не найдены')
        return ConversationHandler.END# Завершаем выполнение функции
    
    emails = '' # Создаем строку, в которую будем записывать почты
    for i in range(len(emailList)):
        emails += f'{i+1}. {emailList[i]}\n' # Записываем очередную почту
    global emailListBig
    emailListBig = emailList

    update.message.reply_text(emails)
    update.message.reply_text('Хотите записать найденные почты в базу данных? [да]/[*]') # Отправляем сообщение пользователю
    return DATABASE
    
    


def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль: ')

    return 'verifyPassword'

def verifyPassword (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий пароль

    passRegex = re.compile(r'.*') # формат

    passw = passRegex.findall(user_input)


    flagiex = False
    numbersinpass = "0123456789"
    if any(c in numbersinpass for c in passw[0]):
        flagiex = True
    
    flagi = False
    special_characters = "!@#$%^&*()"
    if any(c in special_characters for c in passw[0]):
        flagi = True

    flagi1 = False
    for test in passw[0]:
        if test.isupper():
            #update.message.reply_text("Upper")
            flagi1 = True
            break
    
    flagi2 = False
    for test in passw[0]:
        if test.islower():
            #update.message.reply_text("Lower")
            flagi2 = True
            break
    
    if len(passw[0]) >= 8:
        #update.message.reply_text("digit8")
        flagi4 = True
    else:
        flagi4 = False
    #update.message.reply_text('мда')


    if flagi1 and flagi2 and flagi and flagiex and flagi4 == True:
        update.message.reply_text('Сложный пароль') # Отправляем сообщение пользователю
    else: 
        update.message.reply_text('Простой пароль')

    return ConversationHandler.END # Завершаем работу обработчика диалога    

def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

   

    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
            DATABASE : [MessageHandler(Filters.text & ~Filters.command, databaseEmail)],
        },
        fallbacks=[]
    )

     # Обработчик диалога


    convHandlergetAptListCommand = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'getAptListAll': [MessageHandler(Filters.text & ~Filters.command, getAptListAll)],
        },
        fallbacks=[]
    )
	
        # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            DATABASE2 : [MessageHandler(Filters.text & ~Filters.command, databasePhones)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )

	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_services", getServices))
    dp.add_handler(CommandHandler("get_ss", getSs))
    dp.add_handler(CommandHandler("get_ps", getPs))
    dp.add_handler(CommandHandler("get_critical", getCritical))
    dp.add_handler(CommandHandler("get_auths", getAuths))
    dp.add_handler(CommandHandler("get_w", getW))
    dp.add_handler(CommandHandler("get_mpstat", getMpstat))
    dp.add_handler(CommandHandler("get_free", getFree))
    dp.add_handler(CommandHandler("get_df", getDf))
    dp.add_handler(CommandHandler("get_uptime", getUptime))
    dp.add_handler(CommandHandler("get_uname", getUname))
    dp.add_handler(CommandHandler("get_release", getRelease))
    dp.add_handler(CommandHandler("get_repl_logs", getRepl))
    dp.add_handler(CommandHandler("get_emails", getEmails))
    dp.add_handler(CommandHandler("get_phone_numbers", getPhones))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlergetAptListCommand)
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)

    dp.add_handler(convHandlerVerifyPassword)
		
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
