<img src="media/X.svg" style="text-align: center;" width="15%"/>

### Asynchronous Low-code compiler for python


# How to install

```bash
pip install xfox
```
# Clear Example

```python
import asyncio
import xfox
#Custom Function

@xfox.addfunc(xfox.funcs)
async def test_func(item:str, *args, **kwargs):
    print("-----",kwargs)

@xfox.addfunc(xfox.funcs)
async def somef(item:str,*args, **kwargs):
    return kwargs["ctx"]

@xfox.addfunc(xfox.funcs)
async def function4(*args, **kwargs):
    return "FOX"

@xfox.addfunc(xfox.funcs)
async def function1(item:int, type:bool,*args, **kwargs):
    return type

@xfox.addfunc(xfox.funcs)
async def function2(item:str, *args, **kwargs):
    await xfox.isempty(item)
    return eval(item)

@xfox.addfunc(xfox.funcs)
async def inside(item:str, type:bool=False,*args, **kwargs):
    return type

# Sync Parsing
print(asyncio.run(xfox.parse("""
$test_func[$test_func[sfsaf]]
$let[test;good] $function1[1;$inside[true];$sadsadsdsd[]] $onlyif[1<2;ONLYIF]
$function2[1+2;dsadasd] sometext
$math[1+2] $function4[]
$function1[1;$inside[fsfdfd;true];$sadsadsdsd[]]
$sdasdasd[sadsadsad]
sdasdsa $exec[true;print(1+231321, end='')] $exec[true;print(1+231321, end='')] $exec[true;print(1+231321, end='')]
$get[test]
$somef[test]
$try[ERROR EXT $get[_];$function1[]] $try[$print[$get[_]];$function2[]]
$function1[1;True;world\\;yes]
""", ctx="asdsdsdasds")))
```

Output:
```
----- {'ctx': 'asdsdsdasds'}
----- {'ctx': 'asdsdsdasds'}
[LOG] Mising var item in function2
None
 False
3 sometext
3 FOX
True
$sdasdasd[sadsadsad]
sdasdsa 231322 231322 231322
good
asdsdsdasds
ERROR EXT Mising var type in function1
True
```

# Examples

[package for creation Discord bots (beta)](https://github.com/play-go/xfox-code/tree/main/example/discord)
