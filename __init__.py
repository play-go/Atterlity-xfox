# Говнокод от (меня)
import re,asyncio,inspect,json,io,contextlib,traceback,math,importlib,random,time
import nest_asyncio,uuid
try:
    from termcolor import colored
except:
    def colored(a,b):
        return a

class funcs:
    def __init__(self) -> None:
        pass
class anonfuncs:
    def __init__(self) -> None:
        pass
class CacheData:
    pass
class AnonFunction:
    def __init__(self,name,code):
        self.name=name
        self.__code=code
    async def compile(self):
        return await parse(self.__code)
VERSION="0.1.7"
cache=CacheData()
class StopWord(Exception):
    def __init__(self, text):
        super().__init__(text)
class Empty(Exception):
    def __init__(self, text):
        super().__init__(text)
class OnlyIf(Exception):
    def __init__(self, text):
        super().__init__(text)
class WrongAnnotation(Exception):
    def __init__(self, text):
        super().__init__(text)
class Raise(Exception):
    def __init__(self, text):
        super().__init__(text)

DNTl=["xfexec",'try','if','for','def','while',"dowhile"]
output_rep={"&i":'$',"&j":"&","&k":';',"&s":'//'}

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

def classreturn(self):
    return f"<Class {self.name}>"

def addfunc(clas, name=None):
    def wrapper(func):
        if name == None:
            setattr(clas, func.__name__.lower(), func)
            return func
        setattr(clas, name.lower(), func)
        return func
    return wrapper

@addfunc(funcs, 'exec')
async def pyexec(back:bool,*args, **kwargs):
    "Allows to execute python code."
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

@addfunc(funcs, 'help')
async def phelp(name: str,*args, **kwargs):
    "Allows you to find out the docstring and arguments of a function."
    a=getattr(funcs, name)
    if a.__doc__ == None or a.__doc__ == '':
        return "The function haven't docstring"
    else:
        return a.__doc__

@addfunc(funcs, 'break')
async def pbreak(*args, **kwargs):
    "Why?"
    raise StopWord("Break outside the cycle")

@addfunc(funcs, 'raise')
async def praise(error:str,text:str,*args, **kwargs):
    "Allows you to raise errors."
    raise Raise({"name":error,"text":text})

@addfunc(funcs, 'input')
async def pinput(text: str, *args, **kwargs):
    "Get user input from console."
    return input(text)

@addfunc(funcs, 'print')
async def console(*args, **kwargs):
    "Allows you to send a log message to the console."
    print(colored("[LOG] "+'\n'.join(args),"yellow"))
    return ''

@addfunc(funcs, 'xfexec')
async def xfexec(back:bool,*args, **kwargs):
    "Allows you working with xfox from code."
    try:
        a = await __parse_code(args[0], **kwargs)
    except Exception as e:
        return e
    if back == True:
        return a

@addfunc(funcs, 'onlyif')
async def onlyif(item: str, message: str, *args, **kwargs):
    "Checks the statement and throws an error, if False.."
    if eval(item):
        return ""
    else:
        raise OnlyIf(message)
    
@addfunc(funcs, 'import')
async def importt(item:str, *args, **kwargs):
    "Just... import..."
    importlib.import_module(item, package=None)
    return ''
        
    
@addfunc(funcs, 'eval')
async def mathh(item:str, *args, **kwargs):
    "Just... eval..."
    return eval(item)

@addfunc(funcs, 'let')
async def let(name:str, value, *args, **kwargs):
    "Allows you to store data."
    setattr(cache, name, value)
    return ""
@addfunc(funcs, 'get')
async def get(name:str, *args, **kwargs):
    "Allows you to get data from storage."
    return getattr(cache, name)

@addfunc(funcs, 'try')
async def xftry(onerror:str, *args, **kwargs):
    "Just... 'try' from python..."
    try:
        return await __parse_code(args[0], **kwargs)
    except Exception as e:
        await let("_",e)
        return onerror
    
@addfunc(funcs, 'random')
async def xfrandom(x:int, y:int, *args, **kwargs):
    "Allows  to get random number from X to Y"
    return random.randint(x,y)

@addfunc(funcs, "if")
async def xfif(*args, **kwargs):
    "Just... 'if' from python..."
    if len(args)%2==0:
        for i in range(0,len(args),2):
            if eval(await parse(args[i],in_cycle=True, **kwargs)):
                return await parse(args[i+1],in_cycle=True, **kwargs)
    elif len(args)%2==1:
        for i in range(0,len(args[:-1]),2):
            if eval(await parse(args[i],in_cycle=True, **kwargs)):
                return await parse(args[i+1],in_cycle=True, **kwargs)
        else:
            return await parse(args[::-1][0],in_cycle=True, **kwargs)

@addfunc(funcs, "while")
async def xfwhile(q, code:str,*args, **kwargs):
    "Just... 'while' from python..."
    trash=''
    while eval(await parse(q,in_cycle=True,**kwargs)):
        try:
            a=await parse(code, stop_word=True,in_cycle=True, **kwargs)
        except StopWord:
                break
        trash=trash+a
    return trash

@addfunc(funcs, "dowhile")
async def xfdowhile(q, code:str,*args, **kwargs):
    "do 'do' and check 'while'. If 'while'=True continue doing 'do'"
    trash=await parse(code, stop_word=True,in_cycle=True, **kwargs)
    while eval(await parse(q,in_cycle=True,**kwargs)):
        try:
            a=await parse(code, stop_word=True,in_cycle=True, **kwargs)
        except StopWord:
                break
        trash=trash+a
    return trash


@addfunc(funcs, "for")
async def xffor(item, code:str,*args, **kwargs):
    "Just... 'for' from python..."
    item=await parse(item, **kwargs)
    trash=''
    try:
        for i,j in dict(json.loads(item)).items():
            await let("i",i)
            await let("j",j)
            try:
                trash=trash+str(await parse(code,stop_word=True,in_cycle=True, **kwargs))
            except StopWord:
                break
        return trash
    except TypeError as e:
        if e.args[0]=="cannot convert dictionary update sequence element #0 to a sequence":
            for i in list(json.loads(item)):
                await let("i",i)
                try:
                    trash=trash+str(await parse(code,stop_word=True,in_cycle=True, **kwargs))
                except StopWord:
                    break
            return trash
    except: pass
    if len(item.split(".."))>1:
        a=item.split("..")
        for i in range(int(a[0]),int(a[1])+1):
            await let("i",i)
            try:
                trash=trash+str(await parse(code,stop_word=True,in_cycle=True, **kwargs))
            except StopWord:
                break
        return trash
    else:
        for i in range(int(item)):
            await let("i",i)
            try:
                trash=trash+str(await parse(code,stop_word=True,in_cycle=True, **kwargs))
            except StopWord:
                break
        return trash
                
@addfunc(funcs, "len")
async def xflen(item,*args, **kwargs):
    "Allows to get string lenght."
    try:
        return len(dict(json.loads(item)).items())
    except TypeError as e:
        if e.args[0]=="cannot convert dictionary update sequence element #0 to a sequence":
            return len(list(json.loads(item)))
        else: return len(item)

@addfunc(funcs, "reverse")
async def xfreverse(item:str,*args, **kwargs):
    "Allows to get reversed string."
    try:
        return list(json.loads(item))[::-1]
    except TypeError as e:
        return item[::-1]

@addfunc(funcs, "round")
async def xfround(item:float,col:int=0,*args, **kwargs):
    "Allows to get round number."
    if col == 0:
        return int(round(item,col))
    else:
        return round(item,col)

@addfunc(funcs, "lower")
async def xflower(item:str,*args, **kwargs):
    "Allows to get lowercase string."
    return item.lower()

@addfunc(funcs, "exit")
async def pyexit(*args, **kwargs):
    "Just... 'exit' from python..."
    exit()

@addfunc(funcs, "upper")
async def xfupper(item:str,*args, **kwargs):
    "Allows to get uppercase string."
    return item.upper()

@addfunc(funcs, "randomtextlist")
async def xfrandomtext(item:list,col:int=1,*args, **kwargs):
    "Allows to get random text from list."
    return random.choices(item,k=col)

@addfunc(funcs, "randomtext")
async def xfrandomtext(col:int=1, *args, **kwargs):
    "Allows to get random text from args."
    return random.choices(args[:-1],k=col)

@addfunc(funcs, "time")
async def xftimestamp(*args, **kwargs):
    "Allows to get timestamp."
    return time.time()

@addfunc(funcs, "fetch")
async def xffetch(item:str,name:str=None,*args, **kwargs):
    "Fetching data and store in storage."
    if name == None:
        await let("_",json.loads(item))
        return "$get[_]"
    else: 
        await let(name,json.loads(item))
        return f"$get[{name}]"

@addfunc(funcs, "def")
async def deffunc(code:str, name:str=None,*args, **kwargs):
    "Allows to create anonymous (or not) function."
    if name == None:
        name=str(uuid.uuid4())[:6]
        await let(name,code)
        return f"<Function {name}>"
    else:
        @addfunc(anonfuncs, name)
        async def anonf(*args,**kwargs):
            return await parse(code)
        return ''
#parser
async def parse_argument(arg):
    return re.sub(r"(?<!\\)\;", '%#*()', arg).replace("\\",'').split('%#*()')
async def parse_argument_DNT(arg:str):
    code=arg
    while True:
            enn=re.search(r'\$(\w+)\[',code.lower())
            if enn==None:
                break
            en_s=enn.start()
            if int(en_s)>len(code):
                break
            en_e=enn.end()
            en=enn.end()
            ens=1
            function=code[en_s:en_e][1:-1].lower()
            if hasattr(funcs,function) or hasattr(anonfuncs,function):
                try:
                    while ens>0:
                        if code[en]=="[":
                            ens+=1
                        elif code[en]==']':
                            ens-=1
                        elif en>len(code):
                            raise AttributeError("error")
                        en+=1
                except IndexError:
                    raise IndexError(f"Out of range in '{function}'")
            code=code.replace(code[en_s:en],'&i'+code[en_s:en][1:].replace(";",'\\;'),1)
    return re.sub(r"(?<!\\)\;", '%#*()', code).replace("\\",'').replace("&i",'$').split('%#*()')
async def __parse_code(code: str, stop_word:bool=False, in_cycle:bool=False, **kwargs):
    try:
        while True:
            enn=re.search(r'\$(\w+)\[',code.lower())
            en_s=enn.start()
            if int(en_s)>len(code):
                raise AttributeError("ERROR")
            en_e=enn.end()
            en=enn.end()
            ens=1
            function=code[en_s:en_e][1:-1].lower()
            if hasattr(funcs,function) or hasattr(anonfuncs,function):
                try:
                    while ens>0:
                        if code[en]=="[":
                            ens+=1
                        elif code[en]==']':
                            ens-=1
                        elif en>len(code):
                            raise AttributeError("error")
                        en+=1
                except IndexError:
                    raise IndexError(f"Out of range in '{function}'")
                argument=code[en_e:en][:-1]
                if function in DNTl:
                    argument=await parse_argument_DNT(argument)
                elif argument=='': argument=['']
                else:
                    argument=await parse_argument(await __parse_code(argument,in_cycle=in_cycle, **kwargs))
                if hasattr(funcs,function):
                    fun=getattr(funcs, function)
                elif hasattr(anonfuncs,function):
                    fun=getattr(anonfuncs, function)
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
                        elif isindclass(isdnsd, AnonFunction):
                            x=re.search(r"<Function (\w+)>", k)
                            if x:
                                argument[argument.index(k)]=AnonFunction(x.groups()[0],await get(x.groups()[0]))
                            else:
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
                    output=''
                    try:
                        output=await fun(*argument,**kwargs)
                    except StopWord:
                        if stop_word==True or in_cycle == True:
                            raise StopWord("0_0")
                    code=code.replace(code[en_s:en], str(output),1)
                else:
                    raise Empty(f"Mising var {insp[len(argument)]} in {fun.__name__}")
            else:
                code=re.sub(r"\$(\w+)\[", "&i"+code[en_s+1:en].replace(";",'&k'),code,count=1)
    except AttributeError as e:
        pass
    except OnlyIf as e:
        return e.args[0]
    except Raise as e:
        raise Raise(colored(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}","red"))
    return code.strip()
async def parse(code: str,del_empty_lines:bool=False,clear_output:bool=True,stop_word:bool=False,in_cycle:bool=False,**kwargs):
    "Parser for xfox code!"
    output=await __parse_code(re.sub('\/\/.*?\/\/', '', code, flags=re.DOTALL),stop_word=stop_word,in_cycle=in_cycle,**kwargs)
    output=output.strip()
    if clear_output:
        for i,j in output_rep.items():
            output=re.sub(i,j,output)
        output=output
    if del_empty_lines:
        output='\n'.join([line for line in output.splitlines() if line.strip() != ''])
    return output
