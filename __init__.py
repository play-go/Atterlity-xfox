import re,asyncio,inspect,json,io,contextlib,traceback
import random,time
import nest_asyncio
class funcs:
    def __init__(self) -> None:
        pass

class CacheData:
    pass

cache=CacheData()
class Empty(Exception):
    def __init__(self, text):
        super().__init__(text)
        
class OnlyIf(Exception):
    def __init__(self, text):
        super().__init__(text)

class WrongAnnotation(Exception):
    def __init__(self, text):
        super().__init__(text)

DNTl=["xfexec",'try','if','for']

async def isempty(item, count=-1):
    fname=traceback.extract_stack()[-2][2]
    fvar=list(inspect.currentframe().f_back.f_locals.items())
    if item == '': raise Empty(f"Mising var {fvar[0][0]} in {fname}")
    elif len(item)<count or count!=-1: raise Empty(f"Mising vars in {fname}")
    return False

def isindclass(a,b):
    if a is b:
        return True
    else:
        return False

def addfunc(clas, name=None):
    def wrapper(func):
        if name == None:
            setattr(clas, func.__name__, func)
            return func
        setattr(clas, name, func)
        return func
    return wrapper

@addfunc(funcs, 'exec')
async def pyexec(back:bool,*args, **kwargs):
    str_obj = io.StringIO()
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        with contextlib.redirect_stdout(str_obj):
            async def execd():
                exec(args[0])
            loop.run_until_complete(execd())
            loop.close()
    except Exception as e:
        return e
    ret=str_obj.getvalue()
    str_obj.close()
    if back:
        return ret
    else: return ""

@addfunc(funcs, 'input')
async def pinput(text: str, *args, **kwargs):
    return input(text)

@addfunc(funcs, 'print')
async def console(*args, **kwargs):
    print("[LOG]","\n".join(args))
    return ''

@addfunc(funcs, 'xfexec')
async def xfexec(back:bool,*args, **kwargs):
    try:
        a = await parse_code(args[0], **kwargs)
    except Exception as e:
        return e
    if back == True:
        return a

@addfunc(funcs, 'onlyif')
async def onlyif(item: str, message: str, *args, **kwargs):
    if eval(item):
        return ""
    else:
        raise OnlyIf(message)
    
@addfunc(funcs, 'math')
async def math(item:str, *args, **kwargs):
    return eval(item)

@addfunc(funcs, 'let')
async def let(name:str, value, *args, **kwargs):
    setattr(cache, name, value)
    return ""
@addfunc(funcs, 'get')
async def get(name:str, *args, **kwargs):
    return getattr(cache, name)

@addfunc(funcs, 'try')
async def xftry(onerror:str, *args, **kwargs):
    try:
        return await parse_code(args[0], **kwargs)
    except Exception as e:
        await let("_",e)
        return onerror
    
@addfunc(funcs, 'random')
async def xfrandom(x:int, y:int, *args, **kwargs):
    return random.randint(x,y)

@addfunc(funcs, "if")
async def xfif(*args, **kwargs):
    if len(args)%2==0:
        for i in range(0,len(args),2):
            if eval(await parse(args[i], **kwargs)):
                return await parse(args[i+1], **kwargs)
    elif len(args)%2==1:
        for i in range(0,len(args[:-1]),2):
            if eval(await parse(args[i], **kwargs)):
                return await parse(args[i+1], **kwargs)
        else:
            return await parse(args[::-1][0], **kwargs)

@addfunc(funcs, "for")
async def xffor(item, code:str,*args, **kwargs):
    item=await parse(item, **kwargs)
    try:
        for i,j in dict(json.loads(item)).items():
            await let("i",i)
            await let("j",j)
            await parse(code, **kwargs)
    except TypeError as e:
        if e.args[0]=="cannot convert dictionary update sequence element #0 to a sequence":
            for i in list(json.loads(item)):
                await let("i",i)
                await parse(code, **kwargs)
        else:
            for i in range(int(item)):
                await let("i",i)
                await parse(code, **kwargs)
    return ''
                
@addfunc(funcs, "len")
async def xflen(item,*args, **kwargs):
    try:
        return len(dict(json.loads(item)).items())
    except TypeError as e:
        if e.args[0]=="cannot convert dictionary update sequence element #0 to a sequence":
            return len(list(json.loads(item)))
        else: return len(item)

@addfunc(funcs, "reverse")
async def xfreverse(item:str,*args, **kwargs):
    try:
        return list(json.loads(item))[::-1]
    except TypeError as e:
        return item[::-1]

@addfunc(funcs, "round")
async def xfround(item:float,col:int=0,*args, **kwargs):
    if col == 0:
        return int(round(item,col))
    else:
        return round(item,col)

@addfunc(funcs, "lower")
async def xflower(item:str,*args, **kwargs):
    return item.lower()

@addfunc(funcs, "upper")
async def xfupper(item:str,*args, **kwargs):
    return item.upper()

@addfunc(funcs, "randomtextlist")
async def xfrandomtext(item:list,col:int=1,*args, **kwargs):
    return random.choices(item,k=col)

@addfunc(funcs, "randomtext")
async def xfrandomtext(*args, col:int=1, **kwargs):
    return random.choices(args[:-1],k=col)

@addfunc(funcs, "time")
async def xftimestamp(item:str,*args, **kwargs):
    return time.time()

@addfunc(funcs, "fetch")
async def xffetch(name:str,item:str,*args, **kwargs):
    await let(name,json.loads(item))
    return ''
#parser
async def parse_argument(arg):
    return re.sub(r"(?<!\\)\;", '%#*()', arg).replace("\\",'').split('%#*()')
async def parse_code(code: str, autostr: bool | None = True, **kwargs):
    try:
        while True:
            enn=re.search(r'(?<!\&\&)\$(\w+)\[',code.lower())
            en_s=enn.start()
            if int(en_s)>len(code):
                raise AttributeError("ERROR")
            en_e=enn.end()
            en=enn.end()
            ens=1
            function=code[en_s:en_e][1:-1]
            if hasattr(funcs,function.lower()):
                while ens>0:
                    if code[en]=="[":
                        ens+=1
                    elif code[en]==']':
                        ens-=1
                    elif en>len(code):
                        raise AttributeError("error")
                    en+=1
                argument=code[en_e:en][:-1]
                if function in DNTl:
                    argument=await parse_argument(argument)
                elif argument=='': argument=['']
                else:
                    argument=await parse_argument(await parse_code(argument, **kwargs))
                fun=getattr(funcs, function)
                insp=inspect.getfullargspec(fun).args
                insp_l=len(insp)
                for i in insp:
                    if not inspect.signature(fun).parameters[i].default is inspect._empty:
                        insp_l-=1
                if len(argument) >= insp_l:
                    sgin=inspect.signature(fun)
                    for i,k in zip(insp,argument):
                        isdnsd=sgin.parameters[i].annotation
                        if isindclass(isdnsd, str) or isindclass(isdnsd, inspect._empty):
                            if k == '':
                                raise Empty(f"Mising var {i} in {fun.__name__}")
                        elif isindclass(isdnsd, int):
                            if k.isdigit():
                                argument[argument.index(k)]=int(k)
                            else:
                                if k.count('.') == 1:
                                    s = k.replace('.', '')
                                    if s.isdigit():
                                        argument[argument.index(k)]=int(k)
                                    else:
                                        raise WrongAnnotation(f"Wrong varible {i} type in {fun.__name__}. Need {isdnsd}")
                                else:
                                    raise WrongAnnotation(f"Wrong varible {i} type in {fun.__name__}. Need {isdnsd}")
                        elif isindclass(isdnsd, float):
                            try:
                                argument[argument.index(k)]=float(k)
                            except: raise WrongAnnotation(f"Wrong varible {i} type in {fun.__name__}. Need {isdnsd}")
                        elif isindclass(isdnsd, list) or isindclass(isdnsd, dict):
                            try: argument[argument.index(k)]=json.loads(k)
                            except: raise WrongAnnotation(f"Wrong varible {i} type in {fun.__name__}. Need {isdnsd}")
                        elif isindclass(isdnsd, bool):
                            if k.lower()=="true": 
                                argument[argument.index(k)]=True
                            elif k.lower()=="false":
                                argument[argument.index(k)]=False
                            else:
                                raise WrongAnnotation(f"Wrong varible {i} type in {fun.__name__}. Need {isdnsd}")
                        else:
                            raise WrongAnnotation(f"Wrong varible {i} type in {fun.__name__}. Need {isdnsd}")
                    if autostr == True:
                        code=code.replace(code[en_s:en], str(await fun(*argument,**kwargs)),1)
                    elif autostr == False:
                        code=code.replace(code[en_s:en], await fun(*argument,**kwargs),1)
                    elif autostr == None:
                        pass
                else:
                    raise Empty(f"Mising var {insp[len(argument)]} in {fun.__name__}")
            else:
                code=re.sub(fr"(?<!\&\&)\$(\w+)\[", "&&"+code[en_s:en],code,count=1)
    except AttributeError as e:
        pass
    except OnlyIf as e:
        return e.args[0] 
    return code.strip()
async def parse(code: str, autostr: bool | None = True, clear_output:bool=True,**kwargs):
    output=await parse_code(code, autostr,**kwargs)
    if clear_output:
        return output.replace("&&",'')
    else:
        return output
