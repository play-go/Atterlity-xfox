### Asynchronous Low-code compiler for python

# How to install

```bash
pip install xfox
```
# Clear Example

```python
import asyncio
import xfox,time
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
$while[$eval[$get[a]<=5];$let[a;$eval[$get[a]+1]]]
$get[a]
123 $while[True;$if[$get[a]<15;$let[a;$eval[$get[a]+1]];$break[]] $get[a]]
123 $while[True;$break[]]
$break[]
                             
// For Test //
$for[1..5;$get[i]]
$for[5;$get[i] $break[]]

// Try Test //
$try[ERROR $get[_];$function1[]] 
$try[$print[$get[_]];$function2[]]
$try[$get[_];$raise[name;text]]

// Import usage
$import[ttest]
$functiomm[] <- (custom function from ttest)
//

// Exit - $exit[]//
                                                                    
// a Comment // | &s Not a Comment &s
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


('', 'd489c9')
$Test[]






6
123 789101112131415
123



12345



ERROR Mising var type in function1

[ERROR] name: text



Hello, world!



 | // Not a Comment //
PS C:\Users\user\Documents\xfox> & C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe c:/Users/user/Documents/xfox/test.py
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


('', 'dd6fe4')
$Test[]






6
123 789101112131415
123



12345



ERROR Mising var type in function1

[ERROR] name: text

// Import usage

Hello, world! <- (custom function from ttest)
//



 | // Not a Comment //
```

# Interactive Xfox Interpreter

```bash
python -m xfox
```

Or

```Bash
xfox
```

# Start xfox files

```bash
python -m xfox (filename).xfox
```

Or

```Bash
xfox (filename).xfox
```

# Examples

[package for creation Discord bots (outaded)](https://github.com/play-go/xfox-code/tree/main/example/discord)
