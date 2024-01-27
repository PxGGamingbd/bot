import zipfile
from zipfile import ZipFile
from os import system 
from TheAmino import TheAmino
import sys
import threading
from threading import Thread
import os
os.system("pip install TheAmino")
from os import urandom
import re
import urllib
import string
import hmac
import hashlib
from hashlib import sha1
import time
from time import sleep
import base64
from uuid import uuid4
from io import BytesIO
import requests
import json
from gtts import gTTS, lang
from contextlib import suppress
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from unicodedata import normalize
from string import punctuation
from random import uniform, choice, randint
from yt_dlp import YoutubeDL
from json import dumps, load
import random

path_utilities = "utilities"
path_download = "audio"
path_lock = f"{path_utilities}/locked"


client = TheAmino()
client.wait = 3
client.spam_message = "𝐂𝐨𝐨𝐥𝐝𝐨𝐰𝐧, 𝐩𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐛𝐞𝐟𝐨𝐫𝐞 𝐝𝐨𝐢𝐧𝐠 𝐚 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐚𝐠𝐚𝐢𝐧 ⌛"
client.bio = f"𝐈'𝐦 𝐚 𝐛𝐨𝐭 𝐦𝐚𝐝𝐞 𝐛𝐲 𝐭𝐡𝐞 𝐂𝐨𝐝𝐞 𝐓𝐞𝐚𝐦"
client.activity = True

def print_exception(exc):
    print(repr(exc))


def nope(data):
    return False

def is_it_me(data):
    return data.authorId in ('f451ceba-5a3e-4ba1-8894-e2d75b6d1e7d,8a5f07a4-d785-4664-9767-64ab4e8bae73,10c47e28-4d9d-4358-babb-dc4bde63a3a0,816d376a-29f3-4964-aa52-998517905c2b,501cc6f5-1e38-4a22-9df5-cd0625b0205e,d0d5e7f5-5010-413f-a9fc-d4ee6addb6dd')

def is_staff(data):
    return data.authorId in ('f451ceba-5a3e-4ba1-8894-e2d75b6d1e7d,8a5f07a4-d785-4664-9767-64ab4e8bae73,10c47e28-4d9d-4358-babb-dc4bde63a3a0,816d376a-29f3-4964-aa52-998517905c2b,501cc6f5-1e38-4a22-9df5-cd0625b0205e,d0d5e7f5-5010-413f-a9fc-d4ee6addb6dd') or data.subClient.is_in_staff(data.authorId)


def join_community(comId: str = None, inv: str = None):
    if inv:
        try:
            client.request_join_community(comId=comId, message='Cookie for everyone!!')
            return True
        except Exception as e:
            print_exception(e)
    else:
        try:
            client.join_community(comId=comId, invitationId=inv)
            return True
        except Exception as e:
            print_exception(e)



@client.command(condition=is_it_me)
def spy(data):
    data.subClient.send_message(data.chatId)
    
@client.command(condition=is_it_me)
def joincm(args):
    invit = None
    if client.len_community >= 1000:
        args.subClient.send_message(args.chatId, "The bot has joined too many communities!")
        return

    staff = args.subClient.get_staff(args.message)

    if not staff:
        args.subClient.send_message(args.chatId, "Wrong amino ID!")
        return

    try:
        test = args.message.strip().split()
        amino_c = test[0]
        invit = test[1]
        invit = invit.replace("http://aminoapps.com/invite/", "")
    except Exception:
        amino_c = args.message
        invit = None

    try:
        val = client.get_from_code(f"http://aminoapps.com/c/{amino_c}")
        comId = val.json["extensions"]["community"]["ndcId"]
    except Exception:
        return

    isJoined = val.json["extensions"]["isCurrentUserJoined"]
    if not isJoined:
        size = val.json['extensions']['community']['membersCount']
        if size < 100:
            args.subClient.send_message(args.chatId, "Community must have at least 100 members")
            return

        join_community(comId, invit)
        val = client.client.get_from_code(f"http://aminoapps.com/c/{amino_c}")
        isJoined = val.json["extensions"]["isCurrentUserJoined"]

        args.subClient.send_message(args.chatId, "Waiting for join!")
        return
    else:
        args.subClient.send_message(args.chatId, "Allready joined!")
        return

    args.subClient.send_message(args.chatId, "Something went wrong!")

@client.command(condition=is_staff)
def frame(data):
	z=data.subClient.get_user_info(data.authorId).avatarFrameId
	data.subClient.apply_avatar_frame(avatarId=z,applyToAll=False)
	data.subClient.send_message(message="Frame Applied",chatId=data.chatId,replyTo=data.messageId)


@client.command()
def ai(data):
    link = f"http://api.brainshop.ai/get?bid=178390&key=W0eKhJQMLt8BHOrP&uid=1&msg={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = json_data["cnt"]
    data.subClient.send_message(chatId=data.chatId, message=f"{chatbot}", replyTo=data.messageId)


@client.command(condition=is_staff)
def bubble(data):
	z=data.subClient.get_user_info(data.authorId).json['extensions']['defaultBubbleId']
	data.subClient.apply_bubble(bubbleId=z,chatId=data.chatId,applyToAll=True)
	data.subClient.send_message(message="Chatbubble Applied",chatId=data.chatId,replyTo=data.messageId)

@client.command()
def startvc(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "[cb]Started Vc!")

@client.command(condition=is_staff)
def endvc(data):
      data.subClient.delete_message(data.chatId, data.messageId) 
      client.end_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=2) 
      data.subClient.send_message(data.chatId, "[cb]Ended Vc!")

@client.command(condition=is_staff)
def startvid(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_video_chat(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "[CB]Started Video chat!")

@client.command()
def startsc(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_screen_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "[CB]Started Screening!")

@client.command(condition=is_staff)
def endsc(data):
      data.subClient.delete_message(data.chatId, data.messageId) 
      client.end_voice_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=2) 
      data.subClient.send_message(data.chatId, "[CB]Ended Screening!")

@client.command(condition=is_staff)
def endvid(data):
      data.subClient.delete_message(data.chatId, data.messageId) 
      client.end_voice_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=2) 
      data.subClient.send_message(data.chatId, "[CB]Ended Video chat!")

@client.command()
def notifyall(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    users = data.subClient.get_online_users(start=0, size=1000)
    for user in users.profile.userId:
        data.subClient.live_notify(chatId=data.chatId,userId=[user])
        data.subClient.send_message(chatId=data.chatId,message=f"[cb]Notified to all gc members")
        return True

@client.command(condition=is_staff)
def inviteall(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    h = data.subClient.get_online_users(start=0, size=1000)
    for u in h.profile.userId:
        data.subClient.invite_to_chat(chatId=data.chatId,userId=u)
        return True

@client.command(condition=is_staff)
def vc(data):
    id=data.subClient.get_user_info(userId=data.authorId).userId
    data.subClient.invite_to_vc(userId=id,chatId=data.chatId)

@client.command()
def pvp(data):
    import time
    msg = data.message + " null null "
    msg = msg.split(" ")
    try:
        rounds = int(msg[0])
    except (TypeError, ValueError):
        rounds = 5
        msg[2] = msg[1]
        msg[1] = msg[0]
        msg[0] = 5

    if msg[1] == '' or msg[1] == ' ' or msg[1] == 'null':
        msg[1] = data.author
    if msg[2] == '' or msg[1] == ' ' or msg[2] == 'null':
        msg[2] = data.author
    if msg[1] == msg[2]:
        msg[2] = f'Reverse_{msg[1]}'

    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message=f"[icu]{data.author} started a PvP."
                                                                    f"\n[ci]{msg[1]} ⚔ {msg[2]}"
                                                                    f'\n[ci]May the best win!')
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)
    win1 = 0
    win2 = 0
    round = 0
    for tpvp in range(0, rounds):
        round = round + 1
        punch = randint(0, 1)
        if punch == 0:
            win1 = win1 + 1
            agress = msg[1]
            defens = msg[2]
        else:
            win2 = win2 + 1
            agress = msg[2]
            defens = msg[1]
        time.sleep(4)
        while True:
            try:
                data.subClient.send_message(chatId=data.chatId, message=f"[cu]Round {round}"
                                                                        f"\n[ci]{msg[1]} ⚔ {msg[2]}"
                                                                        f"\n[ic] {agress} destroyed {defens}!")
                break
            except:
                print(f"Error... Retrying in 5 seconds")
                time.sleep(5)
    while True:
        try:
            if win1 > win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[bcu]{msg[1]} has won!"
                                                                        f"\n[ciu][{win1} x {win2}]")
            elif win1 < win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[bcu]{msg[2]} has won!"
                                                                        f"\n[cic][{win1}x{win2}]")
            elif win1 == win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[iC]Tie.")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command(condition=is_it_me)
def leavecm(args):
    args.subClient.send_message(args.chatId, "Leaving the Community!")
    args.subClient.stop_instance()
    args.subClient.leave_amino()

def extra(uid : str):
    event=uuid4()
    data = {
        "reward":{"ad_unit_id":"255884441431980_807351306285288","credentials_type":"publisher","custom_json":{"hashed_user_id":f"{uid}"},"demand_type":"sdk_bidding","event_id":f"{event}","network":"facebook","placement_tag":"default","reward_name":"Amino Coin","reward_valid":"true","reward_value":2,"shared_id":"dc042f0c-0c80-4dfd-9fde-87a5979d0d2f","version_id":"1569147951493","waterfall_id":"dc042f0c-0c80-4dfd-9fde-87a5979d0d2f"},
        "app":{"bundle_id":"com.narvii.amino.master","current_orientation":"portrait","release_version":"3.4.33567","user_agent":"Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"},"date_created":1620295485,"session_id":"49374c2c-1aa3-4094-b603-1cf2720dca67","device_user":{"country":"US","device":{"architecture":"aarch64","carrier":{"country_code":602,"name":"Vodafone","network_code":0},"is_phone":"true","model":"GT-S5360","model_type":"Samsung","operating_system":"android","operating_system_version":"29","screen_size":{"height":2260,"resolution":2.55,"width":1080}},"do_not_track":"false","idfa":"7495ec00-0490-4d53-8b9a-b5cc31ba885b","ip_address":"","locale":"en","timezone":{"location":"Asia\/Seoul","offset":"GMT+09:00"},"volume_enabled":"true"}
        }

    headers={
        "cookies":"__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096",
        "authorization":"Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA=="
    }
    requests.post("https://ads.tapdaq.com/v4/analytics/reward",json=data, headers=headers)


@client.command("title")
def title(args):
    if client.check(args, 'staff', id_=client.botId):
        try:
            title, color = args.message.split("color=")
            color = color if color.startswith("#") else f'#{color}'
        except Exception:
            title = args.message
            color = None

        if args.subClient.add_title(args.authorId, title, color):
            args.subClient.send_message(args.chatId, f"The titles of {args.author} has changed")

@client.command(condition=is_staff)
def bgicon(data):
	info = data.subClient.get_message_info(chatId = data.chatId, messageId = data.messageId)
	reply_message = info.json['extensions']
	if reply_message:
		image = info.json['extensions']['replyMessage']['mediaValue']
		filename = image.split("/")[-1]
		filetype = image.split(".")[-1]
		urllib.request.urlretrieve(image, filename)
		with open(filename, 'rb') as fp:
			im=[fp]
			for i in range(1,3):
				try:
					data.subClient.edit_profile(imageList=im)
				except Exception:
					data.subClient.send_message(data.chatId, message="Profile bg pic changed")
					os.remove(filename)

@client.command(condition=is_staff)
def bgcolor(data):
	data.subClient.edit_profile(backgroundColor=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"Profile bg color changed")

@client.command(condition=is_staff)
def pfp(data):
	info = data.subClient.get_message_info(chatId = data.chatId, messageId = data.messageId)
	reply_message = info.json['extensions']
	if reply_message:
		image = info.json['extensions']['replyMessage']['mediaValue']
		filename = image.split("/")[-1]
		filetype = image.split(".")[-1]
		urllib.request.urlretrieve(image, filename)
		with open(filename, 'rb') as fp:
			for i in range(1,3):
				try:
					data.subClient.edit_profile(icon=fp)
				except Exception:
					data.subClient.send_message(data.chatId, message="Profile pic changed")
					os.remove(filename)


@client.command("ship")
def ship(data):
			percentage = uniform(0, 100)
			img=open("ship.png","rb")
			quote = ' '
			if percentage <= 10:
				quote = "It's low, but don't give up."
			elif 10 <= percentage <= 25:
			    quote = 'Eh, find someone else.'
			elif 25 <= percentage <= 50:
			    quote = "It's below average, you have to find someone else."
			elif 50 <= percentage <= 80:
			    quote = 'A relationship is possible.'
			elif 80 <= percentage <= 100:
			 	quote = 'Chances high, this is best option.'	
			 	
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("ship.png") 
				img1 = Image.open(".haas.png").resize((196,196))
				img2= Image.open(".aie.png").resize((196,196))
				img.paste(img1, (101,101))
				img.paste(img2, (402,102))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					data.subClient.send_message(chatId=data.chatId,file=imgg,fileType="image",embedTitle= f"Love Match {percentage:.2f}% ",embedContent=quote)
					
				except:
					pass
				
@client.command("ship")
def ship(data):
			percentage = uniform(0, 100)
			img=open("ship.png","rb")
			quote = ' '
			if percentage <= 10:
				quote = "It's low, but don't give up."
			elif 10 <= percentage <= 25:
			    quote = 'Eh, find someone else.'
			elif 25 <= percentage <= 50:
			    quote = "It's below average, you have to find someone else."
			elif 50 <= percentage <= 80:
			    quote = 'A relationship is possible.'
			elif 80 <= percentage <= 100:
			 	quote = 'Chances high, this is best option.'	
			 	
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("ship.png") 
				img1 = Image.open(".haas.png").resize((196,196))
				img2= Image.open(".aie.png").resize((196,196))
				img.paste(img1, (101,101))
				img.paste(img2, (402,102))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]᯾ 𝐋𝐎𝐕𝐄 𝐌𝐀𝐓𝐂𝐇 {percentage:.2f}% ᯾")
					
				except:
					pass
   
@client.command("fship")
def fship(data):
			percentage = uniform(0, 100)
			img=open("friend.png","rb")
			 	
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("friend.png") 
				img1 = Image.open(".haas.png").resize((247,247))
				img2= Image.open(".aie.png").resize((247,247))
				img.paste(img1, (31,84))
				img.paste(img2, (447,85))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]᯾ 𝐅𝐑𝐈𝐄𝐍𝐃𝐒𝐇𝐈𝐏  {percentage:.2f}% ᯾")
					
				except:
					pass

@client.command("hate")
def hate(data):
			percentage = uniform(0, 100)
			img=open("hate.png","rb")
			 	
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("hate.png") 
				img1 = Image.open(".haas.png").resize((260,260))
				img2= Image.open(".aie.png").resize((260,260))
				img.paste(img1, (36,54))
				img.paste(img2, (453,53))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]᯾ 𝐇𝐀𝐓𝐄 💔 {percentage:.2f}% ᯾")
					
				except:
					pass

@client.command("marry")
def marry(data):
			percentage = uniform(0, 100)
			img=open("marry.png","rb")
			 	
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("marry.png") 
				img1 = Image.open(".haas.png").resize((1,1))
				img2= Image.open(".aie.png").resize((1,1))
				img.paste(img1, (36,54))
				img.paste(img2, (453,53))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]🩷 Oh yay! {data.author}\n[CB]wants to marry {n}\n[CB]just like Mitsuru and Kokoro!\n[CB]What do you say {n}? \n[CB]If you don't respond...  \n[CB]I'll take it as a no.")
					
				except:
					pass

@client.command(condition=is_staff)
def prefix(args):
    if args.message:
        args.subClient.set_prefix(args.message)
        args.subClient.send_message(args.chatId, f"prefix set as {args.message}")



@client.command(condition=is_it_me)
def stopamino(args):
    args.subClient.stop_instance()
    del client[args.subClient.community_id]

def deviceaoss(identifier):
    mac = hmac.new(bytes.fromhex('02b258c63559d8804321c5d5065af320358d366f'), b"\x42" + identifier, hashlib.sha1)
    return (f"42{identifier.hex()}{mac.hexdigest()}").upper()

@client.command(condition=is_staff)
def deviceid(data):
     genids = deviceaoss(identifier=urandom(20))
     data.subClient.send_message(data.chatId, message=genids)

@client.command(condition=is_staff)
def ban(data):
          mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
          for user in mention:
            data.subClient.ban(userId=str(user), reason=f"{data.author}:{data.message}")
            data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
            try:
              data.subClient.send_message(data.chatId, message="Banned")
            except Exception:
              data.subClient.send_message(data.chatId, "Specify reason for ban")

@client.command(condition=is_staff)
def bio(data):
	data.subClient.edit_profile(content=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"Bio changed!!")


@client.command(condition=is_staff)
def name(data):
	data.subClient.edit_profile(nickname=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"name changed to {data.message}")

@client.command(condition=is_staff)
def getco(data):
	id=data.subClient.get_user_info(userId=data.authorId).userId
	with suppress(Exception):
		data.subClient.edit_chat(chatId=data.chatId,coHosts=[id])

@client.command(condition=is_staff)
def vm(data):
    id = data.subClient.get_chat_threads(start=0, size=40).chatId
    for chat in id:
        with suppress(Exception):
            data.subClient.edit_chat(chatId=chat, viewOnly=True)

@client.command(condition=is_staff)
def unvm(data):
    id = data.subClient.get_chat_threads(start=0, size=40).chatId
    for chat in id:
        with suppress(Exception):
            data.subClient.edit_chat(chatId=chat, viewOnly=False)





@client.command(condition=is_staff)
def join(args):
    val = args.subClient.join_chatroom(args.message, args.chatId)
    if val or val == "":
        args.subClient.send_message(args.chatId, f"Chat {val} joined".strip())
    else:
        args.subClient.send_message(args.chatId, "No chat joined")
        
def telecharger(url):
    music = None
    if ("=" in url and "/" in url and " " not in url) or ("/" in url and " " not in url):
        if "=" in url and "/" in url:
            music = url.rsplit("=", 1)[-1]
        elif "/" in url:
            music = url.rsplit("/")[-1]

        if music in os.listdir(path_download):
            return music

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            'extract-audio': True,
            'outtmpl': f"{path_download}/{music}.webm",
            }

        with YoutubeDL(ydl_opts) as ydl:
            video_length = ydl.extract_info(url, download=True).get('duration')
            ydl.cache.remove()

        music = music+".mp3"

        return music, video_length
    return url, False


def search_internet_music(music_name):
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    return telecharger(clip2)


def decoupe(musical, temps):
    size = 180
    with open(musical, "rb") as fichier:
        nombre_ligne = len(fichier.readlines())

    if temps < 181 or temps > 540:
        return False

    decoupage = int(size*nombre_ligne / temps)

    t = 0
    file_list = []
    for a in range(0, nombre_ligne, decoupage):
        b = a + decoupage
        if b >= nombre_ligne:
            b = nombre_ligne

        with open(musical, "rb") as fichier:
            lignes = fichier.readlines()[a:b]

        with open(musical.replace(".mp3", "PART"+str(t)+".mp3"),  "wb") as mus:
            for ligne in lignes:
                mus.write(ligne)

        file_list.append(musical.replace(".mp3", "PART"+str(t)+".mp3"))
        t += 1
    return file_list        
        
        
        
        
@client.command(condition=is_staff)
def leave(args):
    if args.message:
        chat_ide = args.subClient.get_chat_id(args.message)
        if chat_ide:
            args.chatId = chat_ide
    args.subClient.leave_chat(args.chatId)

@client.command("block", False)
def block(args):
    val = args.subClient.get_user_id(args.message)
    if val:
        args.subClient.client.block(val[1])
        args.subClient.send_message(args.chatId, f"User {val[0]} blocked!")

@client.command("unblock", False)
def unblock(args):
    val = args.subClient.client.get_blocked_users()
    for aminoId, userId in zip(val.aminoId, val.userId):
        if args.message in aminoId:
            args.subClient.client.unblock(userId)
            args.subClient.send_message(args.chatId, f"User {aminoId} unblocked!")


@client.command(condition=is_staff)
def gethost(data):
	id=data.subClient.get_user_info(userId=data.authorId).userId
	data.subClient.transfer_host(data.chatId,userIds=[id])
	data.subClient.send_message(data.chatId,message="Host request sended")

@client.command(condition=is_staff)
def givehost(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
		id=data.subClient.get_user_info(userId=str(user)).userId
		data.subClient.transfer_host(data.chatId,userIds=[id])
		data.subClient.send_message(data.chatId,message="Host request sended")

@client.command()
def accept(args):
    if args.subClient.accept_role(args.chatId):
        args.subClient.send_message(args.chatId, "Accepted!")
        return
    val = args.subClient.get_notices(start=0, size=25)
    for elem in val:
        print(elem["title"])

    res = None

    for elem in val:
        if 'become' in elem['title'] or "host" in elem['title']:
            res = elem['noticeId']

        if res and args.subClient.accept_role(res):
            args.subClient.send_message(args.chatId, "Accepted!")
            return
    else:
        args.subClient.send_message(args.chatId, "Error!")

@client.command(condition=is_staff)
def announce(args):
    #if client.check(args,'staff'):
    	try:
    		val = args.subClient.get_chat_threads(start=0,size=100).chatId
    		print(val)
    		for g in val:
            			args.subClient.send_message(chatId=g,message=f"""

{args.message}""")

    	except Exception:
    		  	args.subClient.send_message(args.chatId,message=f"""
Finished Announcement
""")

@client.command(condition=is_it_me)
def ask(args):
    lvl = ""
    boolean = 1
    if "lvl=" in args.message:
        lvl = args.message.rsplit("lvl=", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl="+lvl, "").strip()
    elif "lvl<" in args.message:
        lvl = args.message.rsplit("lvl<", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl<"+lvl, "").strip()
        boolean = 2
    elif "lvl>" in args.message:
        lvl = args.message.rsplit("lvl>", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl>"+lvl, "").strip()
        boolean = 3
    try:
        lvl = int(lvl)
    except ValueError:
        lvl = 20

    args.subClient.ask_all_members(args.message+f"\n[CUI]This message was sent by {args.author}\n[CUI]I am a bot and have a nice day^^", lvl, boolean)
    args.subClient.send_message(args.chatId, "Asking...")

@client.command(condition=is_it_me)
def askstaff(args):
    args.subClient.send_message(args.chatId, "Asking...")
    amino_list = client.client.sub_clients()
    for commu in amino_list.comId:
        client.get_community(commu).ask_amino_staff(message=args.message)
    args.subClient.send_message(args.chatId, "Asked")

@client.command("lock", is_staff)
def lock_command(args):
    if not args.message or args.message in args.subClient.locked_command or args.message not in client.commands_list() or args.message in ("lock", "unlock"):
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.add_locked_command(args.message)
    args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("unlock", is_staff)
def unlock_command(args):
    if args.message:
        try:
            args.message = args.message.lower().strip().split()
        except Exception:
            args.message = [args.message.lower().strip()]
        args.subClient.remove_locked_command(args.message)
        args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("llock")
def locked_command_list(args):
    val = ""
    if args.subClient.locked_command:
        for elem in args.subClient.locked_command:
            val += elem+"\n"
    else:
        val = "No locked command"
    args.subClient.send_message(args.chatId, val)


@client.command("mention")
def mention(args):
    try:
        size = int(args.message.strip().split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        size = 1

    val = args.subClient.get_user_id(args.message)
    if not val:
        args.subClient.send_message(chatId=args.chatId, message="Username not found")
        return

    if size > 5:
        size = 5

    if val:
        for _ in range(size):
            with suppress(Exception):
                args.subClient.send_message(chatId=args.chatId, message=f"‎‏‎‏@{val[0]}‬‭", mentionUserIds=[val[1]])
                
@client.command("msg")
def msg(args):
    value = 0
    size = 1
    ment = None
    with suppress(Exception):
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True, reason="Clear")

    if "chat=" in args.message:
        chat_name = args.message.rsplit("chat=", 1).pop()
        chat_ide = args.subClient.get_chat_id(chat_name)
        if chat_ide:
            args.chatId = chat_ide
        args.message = " ".join(args.message.strip().split()[:-1])

    try:
        size = int(args.message.split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        size = 0

    try:
        value = int(args.message.split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        value = size
        size = 1

    if not args.message and value == 1:
        args.message = f"‎‏‎‏@{args.author}‬‭"
        ment = args.authorId

    if size > 10:
        size = 10

    for _ in range(size):
        with suppress(Exception):
            args.subClient.send_message(chatId=args.chatId, message=f"{args.message}", messageType=value, mentionUserIds=ment)

@client.command()
def check(args):
	args.subClient.send_message(args.chatId, f"""
[b]➢ 𝗖𝗼𝗺𝗺𝘂𝗻𝗶𝘁𝘆 𝗮𝗰𝘁𝗶𝘃𝗲 ✓

[b]➢ 𝗖𝗵𝗮𝘁 𝗮𝗰𝘁𝗶𝘃𝗲 ✓

[b]➢ 𝗕𝗼𝘁 𝗮𝗰𝘁𝗶𝘃𝗲 ✓

[b]➢ 𝗔𝗻𝘁𝗶-𝗿𝗮𝗶𝗱 ✓""")



@client.command()
def gspam(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    qte = args.message.rsplit(" ", 1)
    msg, quantity= qte[0], qte[1]
    quantity = 1 if not quantity.isdigit() else int(quantity)
    quantity = 100 if quantity > 100 else quantity

    for _ in range(quantity):
        args.subClient.send_message(args.chatId, msg, messageType=114)

@client.command("mentionco")
def mentionco(data):
    hostlist = data.subClient.get_chat_thread(data.chatId).coHosts
    msg = 'Co-Hosts:\n'
    for item in hostlist:
        n = data.subClient.get_user_info(str(item)).nickname
        msg += f'<$@{n}$>\n'
    data.subClient.send_message(chatId=data.chatId, message=msg, mentionUserIds=hostlist)

                                       

@client.command("Dare")
def height_ball(data):
    ball= choice(["Bother anything in this gc for 10 mins",
"Send your crush something wholesome",
"Lucky! You didn't get any dare to do",
"Confess to your amino crush",
"Repost a post from my page",
"Sing and send a voice note",
"Send a picture of anything that is near you",
"Send the fifth person in your message history 20 seconds of keyboard spam",
"Show everyone here your screen time",
"Give dare to the person who gave you this dare",
"Do an impression of someone until another player can guess who you are",
"Send screenshot of your phone's lockscreen",
"Go to an random gc and confess to someone",
"Close your eyes and send a blind message",
"Show everyone the last YouTube video you watched",
"Make a poem using names of fruits",
"Be really annoying for the next minute",
"Lie for 10 mins straight",
"Show everyone here your last 10 google searches",
"Show everyone your Instagram for you page",
"Show everyone to the last song you listened to",
"Post an embarrassing photo on your Instagram story",
"Show everyone here the last 5 messages with the last person you messaged/messaged you",
"Dedicate a quote for me",
"Show the list of people in your DMs",
"Draw something in a paper and send it",
"Share the most funniest picture you have in your phone",
"Send the latest photo you downloaded from the internet",
"Voice act a cartoon character of the group's choice",
"Text the first six people in your message history 'a' and don't reply if they bring it up"]
)
    data.subClient.send_message(data.chatId, ball,replyTo=data.messageId)

@client.command("Dice")
def height_ball(data):
    ball= choice(["[CB]⚀", "[CB]⚁", "[CB]⚂","[CB]⚃","[CB]⚄","[CB]⚅"])
    data.subClient.send_message(data.chatId, ball)

@client.command("Truth")
def height_ball(data):
    ball= choice(["Who is your least favorite person in this server?",
"What's the most spontaneous thing you've ever done?",
"When was the last time you cried, and what made you cry?",
"If you could have any superpower, what would you choose?",
"Where is your favorite place to go on vacation?",
"Do you have a reddit account?",
"Which one of your parents are you closer to?",
"Of all the problems in the world, which one would you like to see solved first?",
"If you had to delete one app from your phone, which one would it be?",
"Have you ever had a dream about one of your relatives?",
"Is there a part of your culture that you don't like?",
"What is your least favorite music genre?",
"What is the most annoying thing that one of your siblings has done?",
"What is your weirdest habit?",
"What is the lowest grade you have ever scored in school?",
"What's the most embarrassing thing your parents have caught you doing?",
"If you had an extra hour a day that had to be allocated to one specific purpose, how would you use it?",
"Have you ever thought about changing your name? If yes, to what?",
"What animal most resembles your personality?",
"What's your favorite school subject?",
"If you found a large amount of money would you keep it or try to find the owner?",
"How close are you to your parents?",
"Have you showered today?",
"At what age did you learn to ride a bike?",
"What is something that you absolutely will not put up with?",
"What is the one talent you wish you possessed?",
"Have you ever blamed something you did on another person?",
"What's simply too difficult? Why haven't you done it yet?",
"What's simply too difficult? Why haven't you done it yet?",
"Are you a planner or more of a go with whatever happens when it comes to travel?",
"If there was no such thing as money, what your life be like?",
"Have you ever stolen anything?",
"Have you ever been punished for something you didn't do?"])
    data.subClient.send_message(data.chatId, ball,replyTo=data.messageId)

@client.command("say")
def say_something(data):
    audio_file = f"{path_download}/ttp.mp3"
    gTTS(text=data.message, lang='hi', slow=False).save(audio_file)
    with open(audio_file, 'rb') as fp:
        data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
        data.subClient.send_message(data.chatId, file=fp, fileType="audio")
        os.remove(audio_file)


@client.command()
def bg(data):
    image = data.subClient.get_chat_thread(chatId=data.chatId).backgroundImage
    if image:
        filename = os.path.basename(image)
        urllib.request.urlretrieve(image, filename)
        with open(filename, 'rb') as fp:
            data.subClient.send_message(data.chatId, file=fp, fileType="image")
        os.remove(filename)

@client.command()
def bgi(data):
    image = data.subClient.get_chat_thread(chatId=data.chatId).icon
    if image:
        filename = os.path.basename(image)
        urllib.request.urlretrieve(image, filename)
        with open(filename, 'rb') as fp:
            data.subClient.send_message(data.chatId, file=fp, fileType="image")
        os.remove(filename)

@client.command()
def joinvc(data):
	client.join_voice_chat(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)

@client.command()
def joinsc(data):
	client.join_screen_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
  
@client.command()
def spam(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    qte = args.message.rsplit(" ", 1)
    msg, quantity= qte[0], qte[1]
    quantity = 1 if not quantity.isdigit() else int(quantity)
    quantity = 100 if quantity > 100 else quantity

    for _ in range(quantity):
        args.subClient.send_message(args.chatId, msg)
        
@client.command(condition=is_staff)
def clear(args):
    #if client.check(args, 'staff', client.botId):
        try:
            size = int(args.message)
        except Exception:
            size = 1
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True, reason="Clear")

        if size > 99:
            size = 99

        messages = args.subClient.get_chat_messages(chatId=args.chatId, size=size).messageId

        for message in messages:
            args.subClient.delete_message(args.chatId, messageId=message, asStaff=True, reason="Clear")

@client.command("all")
def everyone(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    mention = [userId for userId in args.subClient.get_chat_users(chatId=args.chatId).userId]
    # test = "".join(["‎‏‎‏‬‭" for user in args.subClient.get_chat_users(chatId=args.chatId).userId])
    args.subClient.send_message(chatId=args.chatId, message=f"[iu]@everyone‎‏‎‏‬‭‎‏‎‏‬‭ {args.message}", mentionUserIds=mention)
    

@client.command()
def gif(args):
  search = (args.message)
  with suppress(Exception):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
  response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=7G8jLZHM52O5YLJ0fPcBOawMvew5a1e1')
  # print(response.text)
  data = json.loads(response.text)
  gif_choice = randint(0, 9)
  image = data['data'][gif_choice]['images']['original']['url']
  print("URL",image)
  if image is not None:
    print(image)
    filename = image.split("/")[-1]
    urllib.request.urlretrieve(image, filename)
    with open(filename, 'rb') as fp:
        args.subClient.send_message(args.chatId, file=fp, fileType="gif")
        print(os.remove(filename))

@client.command()
def img(args):
  search = (args.message)
  with suppress(Exception):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
  response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=7G8jLZHM52O5YLJ0fPcBOawMvew5a1e1')
  # print(response.text)
  data = json.loads(response.text)
  gif_choice = randint(0, 9)
  image = data['data'][gif_choice]['images']['original']['url']
  print("URL",image)
  if image is not None:
    print(image)
    filename = image.split("/")[-1]
    urllib.request.urlretrieve(image, filename)
    with open(filename, 'rb') as fp:
        args.subClient.send_message(args.chatId, file=fp, fileType="image")
        print(os.remove(filename))

@client.command("chatlist", condition=is_staff)
def get_chats(args):
    val = args.subClient.get_chats()
    for title, _ in zip(val.title, val.chatId):
        args.subClient.send_message(args.chatId, title)

@client.command("cmlist", condition=is_staff)
def amino_list(args):
    val = args.subClient.amino_list()
    for title, _ in zip(val.title, val.chatId):
        args.subClient.send_message(args.chatId, title)

@client.command("chatid")
def chat_id(args):
    val = args.subClient.get_chats()
    for title, chat_id in zip(val.title, val.chatId):
        if args.message.lower() in title.lower():
            args.subClient.send_message(args.chatId, f"{title} | {chat_id}")

@client.command(condition=is_staff)
def joinall(args):
        args.subClient.join_all_chat()
        args.subClient.send_message(args.chatId, "All chat joined")

@client.command(condition=is_staff)
def leaveall(args):
    args.subClient.send_message(args.chatId, "Leaving all chat...")
    args.subClient.leave_all_chats()

@client.command(condition=is_staff)
def sw(args):
    message = args.message.strip()
    val = message.replace("[C]", "[c]").replace("[c]", "\n[c]")
    val = val.replace("[I]", "[i]").replace("[i]", "\n[i]")
    val = val.replace("[U]", "[u]").replace("[u]", "\n[u]")
    val = val.replace("[S]", "[s]").replace("[s]", "\n[s]")
    val = val.replace("[B]", "[b]").replace("[b]", "\n[b]")
    val = val.replace("[CU]", "[cu]").replace("[cu]", "\n[cu]")
    val = val.replace("[BC]", "[bc]").replace("[bc]", "\n[bc]")

    args.subClient.set_welcome_message(val)
    args.subClient.send_message(args.chatId, "Welcome wall message changed")
     
@client.command("help")
def help(data):
    thecode=open("thecode.png","rb")
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId,embedImage=thecode,embedTitle="Made By The Code",embedLink="http://aminoapps.com/p/k1xmmn", message="""

[BC]      𝙔𝙚𝙨 𝙗𝙤𝙨𝙨
[c]       ʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ
[c]     ╔═════*.·:·.☽✧ ✦ ✧☾.·:·.*═════╗

           ☞︎︎︎ 𝐁𝐎𝐓𝐏𝐑𝐎𝐅𝐈𝐋𝐄    ☞︎︎︎ 𝐌𝐎𝐃
           ☞︎︎︎ 𝐈𝐌𝐆𝐅𝐔𝐍             ☞︎︎︎ 𝐂𝐇𝐀𝐓
           ☞︎︎︎ 𝐀𝐃𝐌𝐈𝐍                ☞︎︎︎ 𝐂𝐇𝐄𝐂𝐊
           ☞︎︎︎ 𝐂𝐎𝐍𝐓𝐀𝐂𝐓           ☞︎︎︎ 𝐅𝐔𝐍
                  
[c]     ╚═════*.·:·.☽✧ ✦ ✧☾.·:·.*═════╝
""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("fun")
def fun(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]𝙁𝙐𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎
            
[c]╔════*.·:·.☽✧ ✦ ✧☾.·:·.*════╗
             
            ☞︎︎︎ 𝐀𝐈            ☞︎︎︎ 𝐅𝐈𝐍𝐃𝐁𝐅
            ☞︎︎︎ 𝐈𝐌𝐆        ☞︎︎︎ 𝐆𝐈𝐅
            ☞︎︎︎ 𝐌𝐒𝐆       ☞︎︎︎ 𝐃𝐈𝐂𝐄
            ☞︎︎︎ 𝐐𝐔𝐎𝐓𝐄  ☞︎︎︎ 𝐏𝐋𝐀𝐘
            ☞︎︎︎ 𝐒𝐇𝐈𝐏       ☞︎︎︎ 𝐅𝐒𝐇𝐈𝐏
            ☞︎︎︎ 𝐓𝐑𝐔𝐓𝐇   ☞︎︎︎ 𝐃𝐀𝐑𝐄
            ☞︎︎︎ 𝐏𝐕𝐏         ☞︎︎︎ 𝐇𝐀𝐓𝐄
            ☞︎︎︎ 𝐒𝐀𝐘         ☞︎︎︎ 𝐅𝐈𝐍𝐃𝐆𝐅
        
[c]╚════*.·:·.☽✧ ✦ ✧☾.·:·.*════╝


""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("imgfun")
def imgfun(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]𝙄𝙈𝘼𝙂𝙀 𝙁𝙐𝙉
            
[c]╔═════*.·:·.☽✧ ✦ ✧☾.·:·.*═════╗
             
           ☞︎︎︎ 𝐒𝐋𝐀𝐏          ☞︎︎︎ 𝐇𝐔𝐆
           ☞︎︎︎ 𝐊𝐈𝐒𝐒           ☞︎︎︎ 𝐊𝐈𝐋𝐋
           ☞︎︎︎ 𝐊𝐈𝐂𝐊          ☞︎︎︎ 𝐏𝐔𝐍𝐂𝐇
           ☞︎︎︎ 𝐇𝐅𝐈𝐕𝐄        ☞︎︎︎ 𝐋𝐎𝐕𝐄
           ☞︎︎︎ 𝐓𝐑𝐀𝐒𝐇       ☞︎︎︎ 𝐒𝐓𝐔𝐏𝐈𝐃
                   
[c]╚═════*.·:·.☽✧ ✦ ✧☾.·:·.*═════╝

""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("admin")
def admin(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]𝘼𝘿𝙈𝙄𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎
            
[c]╔══════*.·:·.☽✧ ✦ ✧☾.·:·.*══════╗

       ☞︎︎︎ 𝐀𝐃𝐌𝐈𝐍𝐋𝐈𝐒𝐓   ☞︎︎︎ 𝐓𝐄𝐀𝐌
       ☞︎︎︎ 𝐑𝐄𝐒𝐓𝐀𝐑𝐓        ☞︎︎︎ 𝐆𝐋𝐎𝐁𝐀𝐋
       ☞︎︎︎ 𝐀𝐂𝐂𝐄𝐏𝐓          ☞︎︎︎ 𝐃𝐄𝐕𝐈𝐂𝐄𝐈𝐃
       ☞︎︎︎ 𝐁𝐋𝐎𝐂𝐊            ☞︎︎︎ 𝐔𝐍𝐁𝐋𝐎𝐂𝐊
       ☞︎︎︎ 𝐁𝐀𝐍                  ☞︎︎︎ 𝐂𝐋𝐄𝐀𝐑
       ☞︎︎︎ 𝐉𝐎𝐈𝐍                 ☞︎︎︎ 𝐉𝐎𝐈𝐍𝐀𝐋𝐋
       ☞︎︎︎ 𝐋𝐄𝐀𝐕𝐄.            ☞︎︎︎ 𝐋𝐄𝐀𝐕𝐄𝐀𝐋𝐋
                                      
[c]╚══════*.·:·.☽✧ ✦ ✧☾.·:·.*══════╝
      
""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("mod")
def mod(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]𝙈𝙊𝘿 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎

[c]╔═════*.·:·.☽✧ ✦ ✧☾.·:·.*═════╗

   ☞︎︎︎ 𝐀𝐒𝐊                 ☞︎︎︎ 𝐀𝐍𝐍𝐎𝐔𝐍𝐂𝐄
   ☞︎︎︎ 𝐀𝐁𝐖                ☞︎︎︎ 𝐑𝐁𝐖
   ☞︎︎︎ 𝐒𝐏𝐀𝐌              ☞︎︎︎ 𝐕𝐌
   ☞︎︎︎ 𝐔𝐍𝐕𝐌             ☞︎︎︎ 𝐆𝐄𝐓𝐂𝐎
   ☞︎︎︎ 𝐆𝐄𝐓𝐇𝐎𝐒𝐓      ☞︎︎︎ 𝐂𝐇𝐀𝐓𝐈𝐃
   ☞︎︎︎ 𝐆𝐈𝐕𝐄𝐇𝐎𝐒𝐓    ☞︎︎︎ 𝐂𝐇𝐀𝐓𝐋𝐈𝐒𝐓
   ☞︎︎︎ 𝐋𝐋𝐎𝐂𝐊           ☞︎︎︎ 𝐋𝐎𝐂𝐊
   ☞︎︎︎ 𝐔𝐍𝐋𝐎𝐂𝐊        ☞︎︎︎ 𝐉𝐎𝐈𝐍𝐂𝐌
   ☞︎︎︎ 𝐋𝐄𝐀𝐕𝐄𝐂𝐌      ☞︎︎︎ 𝐁𝐖𝐋
   ☞︎︎︎ 𝐒𝐓𝐎𝐏               ☞︎︎︎ 𝐒𝐓𝐎𝐏𝐂𝐌     
 
[c]╚═════*.·:·.☽✧ ✦ ✧☾.·:·.*═════╝

""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("chat")
def chat(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]𝘾𝙃𝘼𝙏 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎

[c]╔══════*.·:·.☽✧ ✦ ✧☾.·:·.*══════╗

    ☞︎︎︎ 𝐒𝐓𝐀𝐑𝐓𝐕𝐂          ☞︎︎︎ 𝐄𝐍𝐃𝐕𝐂
    ☞︎︎︎ 𝐉𝐎𝐈𝐍𝐕𝐂             ☞︎︎︎ 𝐒𝐓𝐀𝐑𝐓𝐒𝐂
    ☞︎︎︎ 𝐄𝐍𝐃𝐒𝐂               ☞︎︎︎ 𝐒𝐓𝐀𝐑𝐓𝐕𝐈𝐃
    ☞︎︎︎ 𝐄𝐍𝐃𝐕𝐈𝐃             ☞︎︎︎ 𝐉𝐎𝐈𝐍𝐒𝐂
    ☞︎︎︎ 𝐈𝐍𝐕𝐈𝐓𝐄𝐀𝐋𝐋       ☞︎︎︎ 𝐍𝐎𝐓𝐈𝐅𝐘𝐀𝐋𝐋
    ☞︎︎︎ 𝐀𝐋𝐋                     ☞︎︎︎ 𝐁𝐆𝐈
    ☞︎︎︎ 𝐁𝐆                       ☞︎︎︎ 𝐏𝐑𝐎𝐅𝐈𝐋𝐄
    ☞︎︎︎ 𝐌𝐄𝐍𝐓𝐈𝐎𝐍         ☞︎︎︎𝐌𝐄𝐍𝐓𝐈𝐎𝐍𝐂𝐎
                                                                                             
[c]╚══════*.·:·.☽✧ ✦ ✧☾.·:·.*══════╝

  """)
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("team")
def team(data):
    codex=open("codex.png","rb")
    rav=open("rav.png","rb")
    ak=open("ak.png","rb")
    ar=open("ar.png","rb")
    anya=open("anya.png","rb")
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId,embedLink="https://instagram.com/min.i9563",embedTitle="ㅤㅤㅤ   ㅤArjun",embedImage=rav, message="""
[CB]                    ☯︎ 𝐓𝐄𝐀𝐌 ☯︎
		  
[CB]ㅤPFP	        ||        NAME

""")


            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(1)             
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId,embedLink="https://instagram.com/cyber__codex",embedTitle="ㅤㅤㅤㅤCodex",embedImage=codex,message="""		  
[CB]ㅤPFP	        ||        NAME

""")

            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(1)   
              
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId,embedLink="https://instagram.com/seleno_luna_",embedTitle="ㅤㅤㅤㅤAradhya",embedImage=ar,message="""		  
[CB]ㅤPFP	        ||        NAME

""")

            break
        except:
            
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)    
             
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId,embedLink="https://instagram.com/veruleikinn_er_ekkert",embedTitle="ㅤㅤㅤㅤAnya",embedImage=anya,message="""		  
[CB]ㅤPFP	        ||        NAME

""")

            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)                 
                                                        
               
@client.command("contact")
def contact(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""

[BC]𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙐𝙎

[c]╔══════*.·:·.☽✧ ✦ ✧☾.·:·.*══════╗

𝗗𝗜𝗦𝗖𝗢𝗥𝗗 - https://discord.com/invite/3jSySTTxdt

𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟 𝗖𝗠 - http://aminoapps.com/p/k1xmmn

𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 - https://t.me/thecoder3534
https://t.me/the_code_24

𝙔𝙊𝙐 𝙏𝙐𝘽𝙀 -
https://youtube.com/@the_code692?si=j-nUKMGCQ1ZAQxqE

[c]╚══════*.·:·.☽✧ ✦ ✧☾.·:·.*══════╝

                        """)
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)                                

@client.command("botprofile")
def botprofile(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]𝘽𝙊𝙏 𝙋𝙍𝙊𝙁𝙄𝙇𝙀

[c]              ╔══*.·:·.☽✧ ✦ ✧☾.·:·.*══╗               

                   ☞︎︎︎ 𝐍𝐀𝐌𝐄
                   ☞︎︎︎ 𝐏𝐅𝐏
                   ☞︎︎︎ 𝐁𝐆𝐈𝐂𝐎𝐍
                   ☞︎︎︎ 𝐁𝐆𝐂𝐎𝐋𝐎𝐑
                   ☞︎︎︎ 𝐁𝐔𝐁𝐁𝐋𝐄
                   ☞︎︎︎ 𝐅𝐑𝐀𝐌𝐄
                   ☞︎︎︎ 𝐁𝐈𝐎

[c]╚══*.·:·.☽✧ ✦ ✧☾.·:·.*══╝

                        """)
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)            
                                                                                                            
@client.command("adminlist")
def adminlist(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""
[CB]-----̳A̳d̳m̳i̳n̳l̳i̳s̳t̳----
----------------------------------------------------
[CB]404
-----------------------------------------------------
                        """)
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)                                           
                                    
@client.command()
def dictionary(data):
    link = f"https://some-random-api.ml/dictionary?word={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['definition']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")

@client.command()
def quote(data):
    var = "quote"
    link = f"https://some-random-api.ml/animu/{var}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['sentence']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")
            
            
@client.command("global",condition=is_staff)
def globall(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
	   AID=client.get_user_info(userId=str(user)).aminoId
	   data.subClient.send_message(data.chatId,message="https://aminoapps.com/u/"+str(AID))
	   	 	   

					
@client.command("hug")
def hug(data):
			img=open("hug.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("hug.png") 
				img1 = Image.open(".haas.png").resize((150,150)) 
				img2= Image.open(".aie.png").resize((130,130))
				img.paste(img1, (167,187))
				img.paste(img2, (155,34))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} hugs {n}!!")
					
				except:
					pass


@client.command("kiss")
def kiss(data):
			img=open("kiss.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("kiss.png") 
				img1 = Image.open(".haas.png").resize((300,300)) 
				img2= Image.open(".aie.png").resize((300,300))
				img.paste(img1, (8,230))
				img.paste(img2, (394,132))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")															
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} kisses {n}'s lips~")
					
				except:
					pass

@client.command("slap")
def slap(data):
			img=open("slap1.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("slap1.png") 
				img1 = Image.open(".haas.png").resize((190,190)) 
				img2= Image.open(".aie.png").resize((190,190))
				img.paste(img1, (39,433))
				img.paste(img2, (314,84))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
																
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} slaps {n}!! oof.")
					
				except:
					pass

@client.command("kill")
def kill(data):
			img=open("kill.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("kill.png") 
				img1 = Image.open(".haas.png").resize((90,90)) 
				img2= Image.open(".aie.png").resize((90,90))
				img.paste(img1, (41,60))
				img.paste(img2, (377,17))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")

																
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} killed {n}!! oh my...")         
					
				except:
					pass

@client.command("kick")
def kick(data):
			img=open("kick.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("kick.png") 
				img1 = Image.open(".haas.png").resize((90,90)) 
				img2= Image.open(".aie.png").resize((90,90))
				img.paste(img1, (163,24))
				img.paste(img2, (483,167))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
																		
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} kicked {n}!! oh sad")
					
					
				except:
					pass

@client.command("punch")
def punch(data):
			img=open("punch.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("punch.png") 
				img1 = Image.open(".haas.png").resize((140,140)) 
				img2= Image.open(".aie.png").resize((140,140))
				img.paste(img1, (266,5))
				img.paste(img2, (25,152))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
			
																
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} gives {n} a punch! Ouch!")
					
				except:
					pass

@client.command("hfive")
def hfive(data):
			img=open("highfive.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("highfive.png") 
				img1 = Image.open(".haas.png").resize((140,140)) 
				img2= Image.open(".aie.png").resize((140,140))
				img.paste(img1, (86,127))
				img.paste(img2, (548,88))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
																	
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} gives {n} a highfive!")
					
				except:
					pass

@client.command("love")
def love(data):
			img=open("love.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("love.png") 
				img1 = Image.open(".haas.png").resize((140,140)) 
				img2= Image.open(".aie.png").resize((140,140))
				img.paste(img1, (84,75))
				img.paste(img2, (284,49))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
																	
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = f"[CB]{data.author} loves {n} 💘")
					
				except:
					pass


@client.command("trash")
def trash(data):
			img=open("trash.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				response=requests.get(f"{h}")
				file=open(".aiyijhale.png","wb")
				file.write(response.content)
				file.close()
				img = Image.open("trash.png")
				img1 = Image.open(".aiyijhale.png").resize((120,120))
				img.paste(img1, (406,219))
				img=img.save(".yihh3.png")
				imgg=open(".yihh3.png","rb")
				try:
					data.subClient.send_message(chatId=data.chatId,file=imgg,fileType="image")
				except:
					pass

@client.command("stupid")
def stupid(data):
			img=open("stupid.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				response=requests.get(f"{h}")
				file=open(".aiyijhale.png","wb")
				file.write(response.content)
				file.close()
				img = Image.open("stupid.png")
				img1 = Image.open(".aiyijhale.png").resize((50,50))
				img2 = Image.open(".aiyijhale.png").resize((70,70))
				img.paste(img1, (358,302))
				img.paste(img2, (138,534))
				img=img.save(".yihh3.png")
				imgg=open(".yihh3.png","rb")
				try:
					data.subClient.send_message(chatId=data.chatId,file=imgg,fileType="image")
				except:
					pass

@client.command("findgf")
def findgf(data):
			msg=choice(["""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : vampy 
[CB]Age : 21

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Dara 
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : tia
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Venus 
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : piper
[CB]Age : 21

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : tyler
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : iris 
[CB]Age : 21

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : tulip
[CB]Age : 17

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : lilac
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : ivy
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : chloe
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : gia
[CB]Age : 23

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : lucie
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : isla
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : ella
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : cana 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : clara
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : lana
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Romy 
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Maia 
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Mimi 
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Rya
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : lou
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : lace
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Adley 
[CB]Age : 17

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : sweety 
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Rasha
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : kit 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : iggy
[CB]Age : 21

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Hallie
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Girlfriend Found ♥️

[BC]Name : Ava
[CB]Age : 21

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎"""])
			img=choice([open("gf1.png","rb"),open("gf2.png","rb"),open("gf3.png","rb"),open("gf4.png","rb"),open("gf5.png","rb"),open("gf6.png","rb"),open("gf7.png","rb"),open("gf8.png","rb"),open("gf9.png","rb"),open("gf10.png","rb"),open("gf11.png","rb"),open("gf12.png","rb"),open("gf13.png","rb"),open("gf14.png","rb"),open("gf15.png","rb"),open("gf16.png","rb"),open("gf17.png","rb"),open("gf18.png","rb"),open("gf19.png","rb"),open("gf20.png","rb"),open("gf21.png","rb"),open("gf22.png","rb"),open("gf23.png","rb"),open("gf24.png","rb"),open("gf25.png","rb"),open("gf26.png","rb"),open("gf27.png","rb"),open("gf28.png","rb"),open("gf29.png","rb")])
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				response=requests.get(f"{h}")
				file=open(".aiyijhale.png","wb")
				file.write(response.content)
				file.close()
				img = choice([Image.open("gf1.png"),Image.open("gf2.png"),Image.open("gf3.png"),Image.open("gf4.png"),Image.open("gf5.png"),Image.open("gf6.png"),Image.open("gf7.png"),Image.open("gf8.png"),Image.open("gf9.png"),Image.open("gf10.png"),Image.open("gf11.png"),Image.open("gf12.png"),Image.open("gf13.png"),Image.open("gf14.png"),Image.open("gf15.png"),Image.open("gf16.png"),Image.open("gf17.png"),Image.open("gf18.png"),Image.open("gf19.png"),Image.open("gf20.png"),Image.open("gf21.png"),Image.open("gf22.png"),Image.open("gf23.png"),Image.open("gf24.png"),Image.open("gf25.png"),Image.open("gf26.png"),Image.open("gf27.png"),Image.open("gf28.png"),Image.open("gf29.png")])
				img1 = Image.open(".aiyijhale.png").resize((275,275))
				img.paste(img1, (396,72))
				img=img.save(".yihh3.png")
				imgg=open(".yihh3.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = msg )
				except:
					pass

@client.command("findbf")
def findbf(data):
			msg=choice(["""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : henry
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : jack
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : oliver
[CB]Age : 23

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : noah
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : harry
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : Willian 
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : leo
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : Adam 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : Alfie 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ Boyfriend Found ♥️

[BC]Name : Oscar 
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : liam
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Thomas 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : eithan 
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : joseph
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Finley 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Arlo 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Roman 
[CB]Age : 23

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Rory 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : daniel
[CB]Age : 17

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Toby 
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Ezra 
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Toby 
[CB]Age : 20 

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : liam 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Jago 
[CB]Age : 18

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Alfred 
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Jake 
[CB]Age : 19

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Owen 
[CB]Age : 22

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : drew 
[CB]Age : 24

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎""",
"""[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎
     
[bc]♥️ boyfriend Found ♥️

[BC]Name : Alwyn 
[CB]Age : 20

[C]☯︎━━━━━━━━━⊱⋆⊰━━━━━━━━━☯︎"""])
			
			img=choice([open("bf1.png","rb"),open("bf2.png","rb"),open("bf3.png","rb"),open("bf4.png","rb"),open("bf5.png","rb"),open("bf6.png","rb"),open("bf7.png","rb"),open("bf8.png","rb"),open("bf9.png","rb"),open("bf10.png","rb"),open("bf11.png","rb"),open("bf12.png","rb"),open("bf13.png","rb"),open("bf14.png","rb"),open("bf15.png","rb"),open("bf16.png","rb"),open("bf17.png","rb")])
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				response=requests.get(f"{h}")
				file=open(".aiyijhale.png","wb")
				file.write(response.content)
				file.close()
				img = choice([Image.open("bf1.png"),Image.open("bf2.png"),Image.open("bf3.png"),Image.open("bf4.png"),Image.open("bf5.png"),Image.open("bf6.png"),Image.open("bf7.png"),Image.open("bf8.png"),Image.open("bf9.png"),Image.open("bf10.png"),Image.open("bf11.png"),Image.open("bf12.png"),Image.open("bf13.png"),Image.open("bf14.png"),Image.open("bf15.png"),Image.open("bf16.png"),Image.open("bf17.png")])
				img1 = Image.open(".aiyijhale.png").resize((275,275))
				img.paste(img1, (396,72))
				img=img.save(".yihh3.png")
				imgg=open(".yihh3.png","rb")
				try:
					return data.subClient.full_embed(image = imgg,chatId = data.chatId,link="",message = msg )
				except:
					pass

@client.command(condition=is_staff)
def abw(args):
    if not args.message or args.message in args.subClient.banned_words:
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.add_banned_words(args.message)
    args.subClient.send_message(args.chatId, "Banned word list updated")

@client.command(condition=is_staff)
def rbw(args):
    if not args.message:
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.remove_banned_words(args.message)
    args.subClient.send_message(args.chatId, "Banned word list updated")
        
@client.command("bwl",condition=is_staff)
def banned_word_list(args):
    val = ""
    if args.subClient.banned_words:
        for elem in args.subClient.banned_words:
            val += elem + "\n"
    else:
        val = "No words in the list"
    args.subClient.send_message(args.chatId, val)

@client.command("welcome", condition=is_staff)
def welcome_channel(args):
    args.subClient.set_welcome_chat(args.chatId)
    args.subClient.send_message(args.chatId, "Welcome channel set!")

@client.command("unwelcome", condition=is_staff)
def unwelcome_channel(args):
    args.subClient.unset_welcome_chat()
    args.subClient.send_message(args.chatId, "Welcome channel unset!")


@client.command(condition=is_it_me)
def restart(args):
    args.subClient.send_message(args.chatId, "[CB]Restarting Bot 🔁")
    os.execv(sys.executable, ["None", "None"])

@client.command(condition=is_it_me)
def stop(args):
    args.subClient.send_message(args.chatId, "[CB]Stopping Bot 🔴")
    os.execv(sys.executable, ["None", "None"])

@client.command(condition=is_it_me)
def stopcm(args):
    args.subClient.stop_instance()
    del client[args.subClient.community_id]

link_list = ["https://amino.com/c/"]

@client.on_message()
def on_message(data):
    [data.subClient.delete_message(data.chatId, data.messageId, reason=f"{data.message}", asStaff=True) for elem in link_list if elem in data.message]


@client.command("profile")
def profileinfo(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
	   	repa = data.subClient.get_user_info(userId=str(user)).reputation
	   	lvl = data.subClient.get_user_info(userId=str(user)).level
	   	crttime = data.subClient.get_user_info(userId=str(user)).createdTime
	   	followers = data.subClient.get_user_achievements(userId=str(user)).numberOfFollowersCount
	   	profilchange = data.subClient.get_user_info(userId=str(user)).modifiedTime
	   	commentz = data.subClient.get_user_info(userId=str(user)).commentsCount
	   	posts = data.subClient.get_user_achievements(userId=str(user)).numberOfPostsCreated
	   	followed = data.subClient.get_user_info(userId=str(user)).followingCount
	   	sysrole = data.subClient.get_user_info(userId=str(user)).role
	   	h=data.subClient.get_user_info(userId=str(user)).nickname
	   	id=data.subClient.get_user_info(userId=str(user)).userId
	   	data.subClient.send_message(data.chatId, message=f"""

[CB]───── ❝ 𝐏𝐫𝐨𝐟𝐢𝐥𝐞 𝐈𝐧𝐟𝐨 ❞ ─────

: ̗̀➛ Nickname: {h} Test

: ̗̀➛ UserId: {id}

: ̗̀➛ Account created time: {crttime}

: ̗̀➛ Last time the profile was changed: {profilchange}

: ̗̀➛ Reputation points: {repa}

: ̗̀➛ Account level: {lvl}

: ̗̀➛ Number of posts: {posts}

: ̗̀➛ Number of comments on wall: {commentz}

: ̗̀➛ Number of following: {followed}

: ̗̀➛ Number of followers: {followers}

	""")

@client.on_message()
def text_message(data):
  content=data.message
  if "aminoapps.com/c" in content or "aminoapps.com/p" in content:
    info = client.get_from_code(content)
    comid = info.path[1:info.path.index("/")]
    if comid != f'{data.comId}':
      try:
      	 data.subClient.delete_message(chatId=data.chatId,messageId=data.messageId,asStaff=True, reason='link share')
      	 data.subClient.warn(userId=data.authorId,reason="Sending links of other community")
      except:
      	pass

@client.on_member_join_chat()
def welcome(data):
    info=data.subClient.get_chat_thread(chatId=data.chatId)
    data.subClient.send_message(data.chatId, f'''[BC][C]━━━━━━━━━━━━━━━━━━━━
[C] {data.author} 𝑊𝑒𝑙𝑐𝑜𝑚𝑒 𝑡𝑜 𝑡𝒉𝑖𝑠 𝑔𝑟𝑜𝑢𝑝 𝑐𝒉𝑎𝑡.

[c]𝑀𝑎𝑘𝑒 𝑛𝑒𝑤 𝑓𝑟𝑖𝑒𝑛𝑑𝑠 𝑎𝑛𝑑 𝒉𝑎𝑣𝑒 𝑓𝑢𝑛.

𝐷𝑜 𝑛𝑜𝑡 𝑎𝑏𝑢𝑠𝑒, 𝑑𝑜 𝑛𝑜𝑡 𝑖𝑛𝑠𝑢𝑙𝑡 𝑎𝑛𝑦𝑜𝑛𝑒 𝑖𝑓 𝑦𝑜𝑢 𝑑𝑜 𝑡𝒉𝑖𝑠 𝑡𝒉𝑒𝑛 𝑦𝑜𝑢 𝑤𝑖𝑙𝑙 𝑏𝑒 𝑘𝑖𝑐𝑘𝑒𝑑 𝑜𝑢𝑡 𝑜𝑓 𝑡𝒉𝑒 𝑔𝑟𝑜𝑢𝑝 𝑏𝑦 𝒉𝑜𝑠𝑡 𝑜𝑟 𝐶𝑜-𝐻𝑜𝑠𝑡.𝑃𝑙𝑒𝑎𝑠𝑒 𝑑𝑜  𝑓𝑜𝑙𝑙𝑜𝑤 𝑎𝑙𝑙 𝑟𝑢𝑙𝑒𝑠 𝑎𝑛𝑑 𝑔𝑢𝑖𝑑𝑒𝑙𝑖𝑛𝑒𝑠.𝐻𝑜𝑝𝑒 𝑦𝑜𝑢 𝒉𝑎𝑣𝑒 𝑓𝑢𝑛 𝒉𝑒𝑟𝑒.😌

[C]━━━━━━━━━━━━━━━━━━━━
''')
def upload(url):
    link = requests.get(url)
    result = BytesIO(link.content)
    return result


@client.command("searchboy")
def searchboy(data):
	ship=(random.randint(18,25))
	y=requests.get("https://randomuser.me/api/1.4/?gender=male")
	h=(y.text)
	u=json.loads(h)
	o=(u["results"])
	for j in o:
		url=j["picture"]["large"]
		filename ="newbb.png"
		urllib.request.urlretrieve(url, filename)
		Image.open("newbb.png").resize((600,600)).save("girlnn.png")
		ff=open("girlnn.png","rb")
		title=(j["name"]["title"])
		first=j["name"]["first"]
		last=j["name"]["last"]
		dob=j["dob"]["age"]
		loc=j["location"]["street"]["number"]
		adr=j["location"]["street"]["name"]
		City=j["location"]["city"]
		state=j["location"]["state"]
		coun=j["location"]["country"]
		msg=f"""[C]New Boy Found ✔️
[C]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁

◈ Name : {title} {first} {last}
◈ Age : {ship}
◈ Address : {loc} {adr}
◈ City : {City}
◈ State : {state}
◈ Country : {coun}

[C]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁"""
		data.subClient.full_embed("https://t.me/the_code_24",ff,msg,data.chatId)
		os.remove("newbb.png")
		os.remove("girlnn.png")
		
	#data.subClient.full_embed("https://youtube.com/c/techvision7",ff,msg,data.chatId)



@client.command("pro")
def pro(data):
    if data.message:
    	user=(client.get_from_code(data.message.split(' ')[0]).objectId)
    else:
    	user=data.authorId
    	
    x=data.subClient.get_user_info(userId=client.userId).json["role"]
    
    ic=data.subClient.get_user_info(str(user)).icon
    response=requests.get(f"{ic}")
    file=open(".yays.png","wb")
    file.write(response.content)
    file.close()
    imgg=(".yays.png")
    Image.open(imgg).resize((800,800)).save("ar.png")
    ff=open("ar.png","rb")
    repa= data.subClient.get_user_info(userId=str(user)).reputation
    h=data.subClient.get_user_info(userId=str(user)).nickname
    lvl = data.subClient.get_user_info(userId=str(user)).level
    crttime = data.subClient.get_user_info(userId=str(user)).createdTime
    followers = data.subClient.get_user_achievements(userId=str(user)).numberOfFollowersCount
    profilchange = data.subClient.get_user_info(userId=str(user)).modifiedTime
    commentz = data.subClient.get_user_info(userId=str(user)).commentsCount
    posts = data.subClient.get_user_achievements(userId=str(user)).numberOfPostsCreated


    if vip==1:
    	vips="Active"
    else:
    	vips="Not Active"
    if bg ==None:
    	bgs="No Image"
    else:
    	bgs=bg[0][1]
    msg=f"""[cu]{h}'s ᴘʀᴏғɪʟᴇ



"""
    embdfull(data,user)
    ftf=open("neeee.png","rb")
    data.subClient.full_embed(f"ndc://x{data.comId}/user-profile/{user}",ftf,msg,data.chatId)
    os.remove("fame/frame.png")
    os.remove("fame/frame.webp")


@client.command("hack",is_it_me)
def hack(data):
	it=randint(500,2000)
	ist=randint(50,630)
	iss=randint(10,40)
	o=randint(1,9)
	v=randint(23,98)
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
		repa= data.subClient.get_user_info(userId=str(user)).reputation
		h=data.subClient.get_user_info(userId=str(user)).nickname
		lvl = data.subClient.get_user_info(userId=str(user)).level
		crttime = data.subClient.get_user_info(userId=str(user)).createdTime
		followers = data.subClient.get_user_achievements(userId=str(user)).numberOfFollowersCount
		profilchange = data.subClient.get_user_info(userId=str(user)).modifiedTime
		commentz = data.subClient.get_user_info(userId=str(user)).commentsCount
		posts = data.subClient.get_user_achievements(userId=str(user)).numberOfPostsCreated
		followed = data.subClient.get_user_info(userId=str(user)).followingCount
		glob=client.get_user_info(userId=str(user)).aminoId

		#data.subClient.send_message(data.chatId,message="Are you sure(Y/N)")
		#time.sleep(5)
		data.subClient.send_message(data.chatId,message=f"Started Loading {h}'s profile....")
		time.sleep(7)
		data.subClient.send_message(data.chatId,message="Collecting device IP........")
		time.sleep(7)
		data.subClient.send_message(data.chatId,message=f"{h}'s device IP address 192.158.{o}.{v}")
		time.sleep(7)
		data.subClient.send_message(data.chatId,message=f"""
{h}'s profile loaded

• ɴᴀᴍᴇ - {h}
• ʟᴇᴠᴇʟ - {lvl}
• ʀᴇᴘs - {repa}
• ғᴏʟʟᴏᴡᴇʀs - {followers}
• ғᴏʟʟᴏᴡᴇᴅ - {followed}
• ᴡᴀʟʟ ᴄᴏᴍᴍᴇɴᴛs - {commentz}
• ᴘᴏsᴛs - {posts}
• ɢʟᴏʙᴀʟɪᴅ - {glob}
• ɪᴅ ᴄʀᴇᴀᴛᴇᴅ - {crttime}
• ᴍᴏᴅɪғɪᴇᴅ - {profilchange}
• ᴜsᴇʀɪᴅ - {str(user)}""")
		data.subClient.send_message(data.chatId,message="System files loading.....")
		time.sleep(7)
		data.subClient.send_message(data.chatId,message=f"{it} chats found from {h}'s account")
		time.sleep(7)
		data.subClient.send_message(data.chatId,message=f"""
{h}'s System Information...

{it} files loaded
{ist} Image files loaded
{iss} Video files loaded""")


		time.sleep(7)
		data.subClient.send_message(data.chatId,message=f"""🕸️ Network Information
type: wifi
rtt: 50
saveData: false
effectiveType: 4g
downlink: 7.85
downlinkMax: Infinity
cookieEnabled: true
doNotTrack: null
maxTouchPoints: 5
""")
		time.sleep(7)		
		data.subClient.send_message(data.chatId,message="Verifying all files.....")
		time.sleep(7)
		data.subClient.send_message(data.chatId,message=f"Successfully hacked {h}'s device")
		time.sleep(5)
		data.subClient.send_message(data.chatId,message=f"<$@{h}$> your device is hacked",mentionUserIds=[str(user)])    	 
		
@client.command("searchgirl")
def searchgirl(data):
	ship=(random.randint(18,25))
	y=requests.get("https://randomuser.me/api/1.4/?gender=female")
	h=(y.text)
	u=json.loads(h)
	o=(u["results"])
	for j in o:
		url=j["picture"]["large"]
		filename ="newg.png"
		urllib.request.urlretrieve(url, filename)
		Image.open("newg.png").resize((600,600)).save("girln.png")
		ff=open("girln.png","rb")
		title=(j["name"]["title"])
		first=j["name"]["first"]
		last=j["name"]["last"]
		dob=j["dob"]["age"]
		loc=j["location"]["street"]["number"]
		adr=j["location"]["street"]["name"]
		City=j["location"]["city"]
		state=j["location"]["state"]
		coun=j["location"]["country"]
		msg=f"""[C]New Girl Found ✔️
[C]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁

◈ Name : {title} {first} {last}
◈ Age : {ship}
◈ Address : {loc} {adr}
◈ City : {City}
◈ State : {state}
◈ Country : {coun}

[C]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁"""
		data.subClient.full_embed("https://t.me/the_code_24",ff,msg,data.chatId)
		os.remove("newg.png")
		os.remove("girln.png")

@client.command("remoji")
def remoji(args):
	lis = ['😰😨😱😓🤯', '??????🤕??', '🌝🥸👻🎃', '😺👹😈😇💩', '😛😉😊😘🥳', '🤣😀😆🥰🙂', '☺️😑🙃😶🤗', '🤩😋😔😌☺️', '🤫🤐🥺🙄🤔', '🧐😤😠😳🤯', '😓😥😩😖😵', '🌞🤮🤧🤒🎃', '😍😚🤭🥲😄', '😃😂🤣😭😰', '🤬😡😮😯😲', '🤓🤠😷', '🥵🥶👺☠️👽', '😸😹😺😻😼', '😽🙀😿😾💀', '❤️🧡💛💚💙', '💜🤎🖤🤍♥️', '💘💝💖💗💓', '💞💕💌💟❣️', '💔💋👅👄👀', '🦾🦠🦷🏵️💐', '🧝🧙🧛🧟🥷', '😪😴🥱🤤🙄', '👿😈🔥⭐🌟', '🎊🎉🕳️💤💦', '🌜👻🤖💢⚡', '✨💫👁️🍂☀️', '🧠🫀🫁🩸🌡️', '👉👌🍺🍷👄', '🦁🐻🐼🐨🐹', '🐭🐷🐸🙉🐶', '🌌🌠🌉🌆🌃', '🕊️🦅🐦🦥🦏', '🐲🦖🐢🦮🐈', '🐐🦬🐖🐑🐆', '🦍🦧🐿️🦦🦈', '🐝🐠🐋🦋🐜', '🍔🍖🍗🌭🥪', '🥞🍳🫓🌮🍕', '🍉🍓🍒🫐🍎', '🧆🥙🥘🍜🦪', '🍧🍱🥟🍚🍢', '🍰🍙🍡🍣🍟', '🧇🥯🌯🥟🥡', '🍭🍩🍪🥮🍨', '🥗🍲🫕🍥🍿', '🥃🍾🍹🍸🍻', '🅿️🅾️🆘ℹ️🖕🏿', '🤏✋👊🙌👇', '👾🕹️🎮🎲🃏', '💵💴💶💷💰', '🇺🇸🇹🇨🇸🇻🇺🇦🇼🇸', '🏤🏣🏨🏥🏩']
	args.subClient.send_message(args.chatId, message=str(random.choice(lis)))
	
	
@client.command("follow")
def follow(args):
    args.subClient.follow_user(args.authorId)
    args.subClient.send_message(args.chatId, f"Bot followed <$@{args.author}$>",mentionUserIds=[args.authorId])


@client.command("unfollow")
def unfollow(args):
    args.subClient.unfollow_user(args.authorId)
    args.subClient.send_message(args.chatId, f"Bot unfollowed <$@{args.author}$>",mentionUserIds=[args.authorId])	
	
	
@client.command("rank")
def rank(data):
	try:
		ranktoday(data)
		rankweek(data)
	except:
		pass
	
def rankweek(data):
	nicka=[]
	acti=[]
	val=""
	cal=""
	dal=""
	q=data.subClient.get_leaderboard_info(type="day",size=5).json
	for x in q:
		nick=x["nickname"]
#		actii=x["activeTime"]
	#	act=actii/3600
		nicka.append(nick)
	#	acti.append(int(act))
		
	for i, vl in enumerate(nicka,1):
		val +=str(i)+" - "+vl+"\n"
#	for vli in merged_list:
	#	cal =vli +" Hr"+"\n"
	#dal=dal + +"\n"
	data.subClient.send_message(chatId=data.chatId,message=f"""
[c]Top Active users - Weekly
[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁

{val}
[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁""")

def ranktoday(data):
	nicka=[]
	acti=[]
	val=""
	cal=""
	dal=""
	q=data.subClient.get_leaderboard_info(type="hour",size=5).json
	for x in q:
		nick=x["nickname"]
	#	actii=x["activeTime"]
	#	act=actii/3600
		nicka.append(nick)
		#acti.append(int(act))
		
	
	for i, vl in enumerate(nicka,1):
		val +=str(i)+" - "+vl +"\n"
	#for vli in acti:
		#cal =cal+ str(vli) +" Hr"+"\n"
	#dal=dal + val+ " - " + cal +"\n"
	data.subClient.send_message(chatId=data.chatId,message=f"""
[c]Top Active users - Daily
[c]𐄁𐄙??𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁

{val} 
[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁""")

@client.on_member_leave_chat()
def goodbye(data):
    data.subClient.send_message(data.chatId, '''•❅──────✧❅✦❅✧──────❅•

[CB]「 𝐎𝐇 𝐍𝐎𝐎 !! 」
[CB]† 𝐒𝐨𝐦𝐞𝐨𝐧𝐞 𝐡𝐚𝐬 𝐥𝐞𝐟𝐭 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 †
[CB]🪦 𝐏𝐥𝐞𝐚𝐬𝐞 𝐑𝐢𝐩 🪦

•❅──────✧❅✦❅✧──────❅•''')

client.launch(True)
print("Bot is Working")

def Root():
    j = 0
    while True:
        if j >= 60:
            client.close()
            print("socket close")
            client.run_amino_socket()
            print("socket start")
            j = 0
        j += 1
        time.sleep(1)
Root()

socketloop = threading.Thread(target=reconsocketloop, daemon=True)
socketloop.start()

		