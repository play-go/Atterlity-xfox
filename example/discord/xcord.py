import disnake,json
import disnake.ext.commands as dext
import disnake.ext.tasks as deks
import xfox
cache_embed=xfox.CacheData()
MISSING = disnake.utils.MISSING

async def parse(code: str, autostr: bool | None = True, clear_output:bool=True,**kwargs):
    global cache_embed
    a=await xfox.parse(code, autostr,clear_output,**kwargs)
    cache_embed=xfox.CacheData()
    return a

@xfox.addfunc(xfox.funcs)
async def botname(*args, **kwargs):
    return kwargs["bot"].user.name

@xfox.addfunc(xfox.funcs)
async def defer(*args, **kwargs):
    await kwargs["ctx"].response.defer()
    return ''

@xfox.addfunc(xfox.funcs)
async def authorid(*args, **kwargs):
    return kwargs["ctx"].author.id

@xfox.addfunc(xfox.funcs, 'title')
async def xfembed_t(col:int,text:str, *args, **kwargs):
    setattr(kwargs["embed"], f"{col}_title", text)
    return ''

@xfox.addfunc(xfox.funcs, 'description')
async def xfembed_d(col:int,text:str, *args, **kwargs):
    setattr(kwargs["embed"], f"{col}_description", text)
    return ''

@xfox.addfunc(xfox.funcs, 'color')
async def xfembed_c(col:int,color:str,*args, **kwargs):
    try: 
        setattr(kwargs["embed"], f"{col}_color", int(color))
        return ''
    except: pass
    setattr(kwargs["embed"], f"{col}_color", getattr(disnake.Color, color.lower()))
    return ''

@xfox.addfunc(xfox.funcs, 'footer')
async def xfembed_f(col:int,text:str,url:str=None,*args, **kwargs):
    setattr(kwargs["embed"], f"{col}_footer", [text,url])
    return ''

@xfox.addfunc(xfox.funcs, "thumbnail")
async def xfembed_t(col:int,url:str,*args, **kwargs):
    setattr(kwargs["embed"], f"{col}_thumbnail", url)
    return ''

@xfox.addfunc(xfox.funcs, 'author')
async def xfembed_ath(col:int,text:str,url:str=None,*args, **kwargs):
    setattr(kwargs["embed"], f"{col}_author", [text,url])
    return ''

@xfox.addfunc(xfox.funcs, "image")
async def xfembed_img(col:int,url:str,*args, **kwargs):
    setattr(kwargs["embed"], f"{col}_image", url)
    return ''

@xfox.addfunc(xfox.funcs, "addfield")
async def xfembed_field(col:int,name:str, value:str, inline:bool=True,*args, **kwargs):
    setattr(kwargs["embed"], f"{col}_field_{name}", [value,inline])
    return ''

@xfox.addfunc(xfox.funcs, "embed")
async def xfembed(col:int,*args, **kwargs):
    cache_embed=kwargs["embed"]
    emb={}
    if hasattr(cache_embed,f"{col}_title"):
        emb["title"]=getattr(cache_embed,f"{col}_title")
    if hasattr(cache_embed,f"{col}_description"):
        emb["description"]=getattr(cache_embed,f"{col}_description")
    if hasattr(cache_embed,f"{col}_color"):
        try: emb["color"]=int(getattr(cache_embed,f"{col}_color"))
        except: emb["color"]=disnake.Color.to_rgb(getattr(cache_embed,f"{col}_color")())
    if hasattr(cache_embed,f"{col}_footer"):
        footer=getattr(cache_embed,f"{col}_footer")
        emb[f"footer"]=(footer[0],footer[1])
    if hasattr(cache_embed,f"{col}_thumbnail"):
        emb[f"thumbnail"]=getattr(cache_embed,f"{col}_thumbnail")
    if hasattr(cache_embed,f"{col}_author"):
        author=getattr(cache_embed,f"{col}_author")
        emb[f"author"]=(author[0],author[1])
    if hasattr(cache_embed,f"{col}_image"):
        emb[f"image"]=getattr(cache_embed,f"{col}_image")
    field_attrs = [attr for attr in dir(cache_embed) if attr.startswith(f"{col}_field_")]
    emb[f"add_field"]=[]
    for i in field_attrs:
        atr=getattr(cache_embed,i)
        emb[f"add_field"].append((i.replace(f"{col}_field_",""),atr[0],atr[1]))
    setattr(kwargs["embed"],f"{col}_embed",json.dumps(emb))
    return ''
#embed


@xfox.addfunc(xfox.funcs)
async def send_response(message:str,col:int=-1,*args, **kwargs):
    if col == -1:
        embe=MISSING
    else:
        jso=dict(json.loads(getattr(kwargs[f'embed'],f'{col}_embed'))) 
        embe=disnake.Embed()
        if "title" in jso:
            embe.title=jso["title"]
        if "description" in jso:
            embe.description=jso["description"]
        if "color" in jso:
            try:
                embe.colour=int(float(jso["color"]))
            except: 
                embe.color=disnake.Color.from_rgb(*jso["color"])
        if "footer" in jso:
            footer=jso["footer"]
            embe.set_footer(text=footer[0],icon_url=footer[1])
        if "thumbnail" in jso:
            embe.set_thumbnail(jso["thumbnail"])
        if "author" in jso:
            author=jso["author"]
            embe.set_author(name=author[0],url=author[1])
        if "image" in jso:
            embe.set_image(url=jso["image"])
        if "add_field" in jso:
            for i,j,k in jso["add_field"]:
                embe.add_field(i,j,inline=k)
    await kwargs["ctx"].response.send_message(message,embed=embe)
    return ''

@xfox.addfunc(xfox.funcs)
async def edit_response(message:str,col:int=-1, *args,**kwargs):
    if col == -1:
        embe=MISSING
    else:
        jso=dict(json.loads(getattr(kwargs[f'embed'],f'{col}_embed'))) 
        embe=disnake.Embed()
        if "title" in jso:
            embe.title=jso["title"]
        if "description" in jso:
            embe.description=jso["description"]
        if "color" in jso:
            try:
                embe.colour=int(float(jso["color"]))
            except: 
                embe.color=disnake.Color.from_rgb(*jso["color"])
        if "footer" in jso:
            footer=jso["footer"]
            embe.set_footer(text=footer[0],icon_url=footer[1])
        if "thumbnail" in jso:
            embe.set_thumbnail(jso["thumbnail"])
        if "author" in jso:
            author=jso["author"]
            embe.set_author(name=author[0],url=author[1])
        if "image" in jso:
            embe.set_image(url=jso["image"])
        if "add_field" in jso:
            for i,j,k in jso["add_field"]:
                embe.add_field(i,j,inline=k)
    await kwargs["ctx"].edit_original_message(message,embed=embe)
    return ''

class activity():
    def __init__(self,message:str,activity:int=0):
        if activity == 0:
            self.__a = disnake.Activity(type=disnake.ActivityType.playing, name=message)
        elif activity == 1:
            self.__a = disnake.Activity(type=disnake.ActivityType.watching, name=message)
        elif activity == 2:
            self.__a = disnake.Activity(type=disnake.ActivityType.listening, name=message)
        elif activity == 3:
            self.__a = disnake.Activity(type=disnake.ActivityType.competing, name=message)
        elif activity == 4:
            self.__a = disnake.Activity(type=disnake.ActivityType.streaming, name=message)
        else:
            self.__a = disnake.Activity(type=disnake.ActivityType.playing, name=message)
    def read(self):
        return self.__a

class xcordisnake():
    def __init__(self, intents: dict = ("default",), activity: list = [], activity_second:int=60):
        if intents == "all":
            self.intents=disnake.Intents.all()
        else:
            self.intents=disnake.Intents.default()
        if "message" in self.intents:
            self.intents.message_content = True
        if "members" in self.intents:
            self.intents.members = True
        if "presences" in self.intents:
            self.intents.presences = True
        self.__activity=activity
        self.__activity_second=activity_second
        self.__a=0
        self.__bot=dext.InteractionBot(intents=self.intents)
    
    def onReady(self, code):
        @self.__bot.event
        async def on_ready():
            output=await parse(code=code,bot=self.__bot)
            if not self.__task_act.is_running() and self.__activity!=[]:
                self.__task_act.start()
            if output!='':
                print(output)

    def activity_start(self):
        @deks.loop(seconds=self.__activity_second)
        async def task_act():
            act=self.__activity[self.__a].read()
            act.name=await parse(code=act.name,bot=self.__bot,embed=cache_embed)
            await self.__bot.change_presence(activity=act)
            if self.__a+1==len(self.__activity):
                self.__a=0
            else:
                self.__a+=1
        self.__task_act=task_act

    def command(self,name:str,description:str='-',code:str='''''', commands:list[dict]=[]):
        if commands == []:
            @self.__bot.slash_command(name=name,description=description)
            async def function(ctx):
                output=await parse(code=code,ctx=ctx,bot=self.__bot,embed=cache_embed)
                if output!='':
                    await ctx.channel.send(output)
        else:
            @self.__bot.slash_command(name=name,description=description)
            async def function(ctx, **kwargs):
                output=await parse(code=code,ctx=ctx,bot=self.__bot,embed=cache_embed, **kwargs)
                if output!='':
                    await ctx.channel.send(output)
            for i in commands:
                typ=None
                ch_typ=None
                choices=None
                options=None
                min_value=None
                max_value=None
                min_length=None
                max_length=None
                if i["required"] == "str":
                    typ=disnake.OptionType.string
                    if 'min' in i:
                        min_length=i['min']
                    if 'max' in i:
                        min_length=i['max']
                elif i["required"] == "bool":
                    typ=disnake.OptionType.boolean
                elif i["required"] == "number":
                    typ=disnake.OptionType.number
                    if 'min' in i:
                        min_value=i["min"]
                    if 'max' in i:
                        max_value=i["max"]
                elif i["required"] == "user":
                    typ=disnake.OptionType.user
                elif i["required"] == "mentionable":
                    typ=disnake.OptionType.mentionable
                elif i["required"] == "text_channel":
                    typ=disnake.OptionType.channel
                    ch_typ=[disnake.ChannelType.text]
                elif i["required"] == "voice_channel":
                    typ=disnake.OptionType.channel
                    ch_typ=[disnake.ChannelType.voice]
                elif i["required"] == "category":
                    typ=disnake.OptionType.channel
                    ch_typ=[disnake.ChannelType.category]
                elif i["required"] == "attachment":
                    typ=disnake.OptionType.attachment
                else:
                    typ=disnake.OptionType.string
                    if 'min' in i:
                        min_length=i['min']
                    if 'max' in i:
                        min_length=i['max']
                if "choices" in i:
                    choices=i["choices"]
                function.options.append(disnake.Option(name=i["name"],description=i["description"],required=i["required"],type=typ,channel_types=ch_typ))
    
    def run(self,token):
        self.__bot.run(token)
