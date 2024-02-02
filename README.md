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
    return type, args

@xfox.addfunc(xfox.funcs)
async def function2(item:str, *args, **kwargs):
    await xfox.isempty(item)
    return eval(item)

@xfox.addfunc(xfox.funcs)
async def inside(item:str, type:bool=False,*args, **kwargs):
    return type

@xfox.addfunc(xfox.funcs, 'usefunc')
async def functest(func:xfox.AnonFunction,*args, **kwargs):
    return (await func.compile(), func.name)

# Sync Parsing
print(asyncio.run(xfox.parse("""
// TRASH (xd) //
$test_func[$test_func[sfsaf]]
$function1[1;$inside[true];$sadsadsdsd[]] $onlyif[1<2;ONLYIF]
$function2[1+2;dsadasd] sometext
$function4[]
$function1[1;$inside[fsfdfd;true];$sadsadsdsd[]]
$sdasdasd[sadsadsad]
sdasdsa $exec[true;print(1+231321, end='')] $exec[true;print(1+231321, end='')] $exec[true;print(1+231321, end='')]

// Let/Get //
$let[test;good]
$get[test]

// Internal Functions Test //
$usefunc[$def[$print[hello!]]]
$Test[]
$def[$print[hello!];Test]
$Test[] 
                             
// While Test //
$let[a;0]
$while[$math[$get[a]<=15];$let[a;$math[$get[a]+1]]]
$get[a]

// For Test //
$for[1..5;$get[i]]
$for[5;$get[i]]

// Try Test //
$try[ERROR EXT $get[_];$function1[]] 
$try[$print[$get[_]];$function2[]]

// a Comment // | /&/ Not a Comment /&/
""", ctx="asdsdsdasds")))
```

Output:
```
----- {'ctx': 'asdsdsdasds'}
----- {'ctx': 'asdsdsdasds'}
[LOG] hello!
[LOG] hello!
[LOG] Mising var item in function2
None
(False, ('$sadsadsdsd[]',))
3 sometext
FOX
(True, ('$sadsadsdsd[]',))
$sdasdasd[sadsadsad]
sdasdsa 231322 231322 231322



good

('', '70e5df')
$Test[]






16


12345
01234


ERROR EXT Mising var type in function1


 | /&/ Not a Comment /&/
```

# Examples

[package for creation Discord bots (beta)](https://github.com/play-go/xfox-code/tree/main/example/discord)
