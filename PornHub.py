import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download
from config import OWNER, BOT_NAME, ARQ_API_KEY, UPDATES_CHANNEL, TOKEN

session = ClientSession()


arq = ARQ("http://thearq.tech/", ARQ_API_KEY, session)
pornhub = arq.pornhub

bot1 = Client(f"{BOT_NAME}", bot_token=f"{TOKEN}", api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")



db = {}

# Let's Go----------------------------------------------------------------------
@bot1.on_message(
    filters.command(["search"]) & ~filters.edited & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo")
    )
async def sarch(_,message):
    m = await message.reply_text("finding your title provided Video Details...")
    search = message.text.split(' ', 1)[1]
    try:
        resp = await pornhub(search,thumbsize="large_hd")
        res = resp.result
    except:
        await m.delete()
        pass
    if not resp.ok:
        await m.edit("error search or link detected.")
        return
    resolt = f"""
**✨ Title:** {res[0].title}
**⏰ Duration:** {res[0].duration}
**👁‍🗨 Viewers:** {res[0].views}
**🌟 Rating:** {res[0].rating}
"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Next ⏭️",
                                         callback_data="next"),
                    InlineKeyboardButton("Watch On PornHub 📽️",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("Screenshot 🚫",
                                         callback_data="ss"),
                    InlineKeyboardButton("Download ✅",
                                         callback_data="downbad"),
               
                ]               
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@bot1.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("Back 🔙",
                                         callback_data="previous"),
                    InlineKeyboardButton("Screenshot 🚫",
                                         callback_data="ss")
                    
                ],
                [
                    InlineKeyboardButton("Watch On PornHub 📽️",
                                         callback_data="delete"),
                    InlineKeyboardButton("Download ✅",
                                         callback_data="downbad")
              
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("Back 🔙",
                                         callback_data="previous"),
                    InlineKeyboardButton("Next ⏭️",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("Watch On PornHub 📽️",
                                         callback_data="delete"),
                    InlineKeyboardButton("Screenshot 🚫",
                                         callback_data="ss"),
                    InlineKeyboardButton("Download ✅",
                                         callback_data="downbad"),
              
                    
                ]
              ]
    resolt = f"""
**🏷 Title:** {res[cur_page].title}
**⏰ Duration:** {res[cur_page].duration}
**👁‍🗨 Viewed:** {res[cur_page].views}
**🌟 Rating:** {res[cur_page].rating}
"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@bot1.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("Back 🔙",
                                         callback_data="previous"),
                    InlineKeyboardButton("Next ⏭️",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("Watch On PornHub 📽️",
                                         callback_data="delete"),
                    InlineKeyboardButton("Screenshot 🚫",
                                         callback_data="ss"),
                    InlineKeyboardButton("Download ✅",
                                         callback_data="downbad")
              
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("Next ⏭️",
                                         callback_data="next"),
                    InlineKeyboardButton("Watch On PornHub 📽️",
                                         callback_data="Delete"),
                ],
                [ 
                    InlineKeyboardButton("Screenshot 🚫",
                                         callback_data="ss"),
                    InlineKeyboardButton("Download ✅",
                                         callback_data="downbad"),
              
                ]
                
            ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}
"""
    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )


# Delete Button-------------------------------------------------------------------------- 
#@bot1.on_callback_query(filters.regex("delete"))
@bot1.on_callback_query(filters.regex("delete"))
def callback_query_delete(bot, query):
    #await query.message.delete()
     data = db[query.message.chat.id]
     res = data['result']
     curr_page = int(data['curr_page'])
     cur_page = curr_page-1
     db[query.message.chat.id]['curr_page'] = cur_page
     umrl = res[curr_page].url
     bot.send_message(text=umrl,chat_id=query.message.chat.id,disable_web_page_preview=True)



# SCREENSHOT BUTTON ---------------------------------------

@bot1.on_callback_query(filters.regex("ss"))
async def callback_query_delete(bot, query):
    data = db[query.message.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    ss = res[curr_page].thumbnails
    for src in ss:
      await bot.send_photo(photo=src.src,chat_id=query.message.chat.id)



# DOWNLOAD BUTTON ------------------------------------------

import requests, os, validators
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton











def downloada(url, quality):
  
    if quality == "2":
        ydl_opts_start = {
            'format': 'best', #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    
@bot1.on_callback_query(filters.regex("downbad"))
def webpage(c, m): # c Mean Client | m Mean Message
    print(m.message.chat.id)
    data = db[m.message.chat.id]
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1

    vidtitle = data['result'][curr_page].title
    vidurl = data['result'][curr_page].url
    
    url1 = res = data['result'][curr_page].url
    if validators.url(url1):
        sample_url = "https://da.gd/s?url={}".format(url1)
        url = requests.get(sample_url).text
    

  
    global check_current
    check_current = 0
    def progress(current, total): #Thanks to my dear friend Hassan Hoot for Progress Bar :)
        global check_current
        if ((current//1024//1024) % 50 )== 0 :
            if check_current != (current//1024//1024):
                check_current = (current//1024//1024)
                upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
        elif (current//1024//1024) == (total//1024//1024):
            upmsg.delete()

   
    url1=f"{url} and 2"
    chat_id = m.message.chat.id
    data = url1
    url, quaitly = data.split(" and ")
    dlmsg = c.send_message(chat_id, '`downloading video..`')
    path = downloada(url, quaitly)
    upmsg = c.send_message(chat_id, '`uploading video..`')
    dlmsg.delete()
    thumb = path.replace('.mp4',".jpg",-1)
    if  os.path.isfile(thumb):
        thumb = open(thumb,"rb")
        path = open(path, 'rb')
        #c.send_photo(chat_id,thumb,caption=' ') #Edit it and add your Bot ID :)
        c.send_video(chat_id, path, thumb=thumb, caption=f'[{vidtitle}]({vidurl})',
                    file_name=" ", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
        upmsg.delete()
    else:
        path = open(path, 'rb')
        c.send_video(chat_id, path, caption=f'[{vidtitle}]({vidurl})',
                    file_name=" ", supports_streaming=True, progress=progress)
        upmsg.delete()





bot1.run()
