<img src="media/X.svg" style="text-align: center;" width="15%"/>

### Asynchronous Low-code compiler for python


# How to install

```bash
pip install LATER
```
# Clear Example

```python
import main, asyncio

#Custom Function

@main.addfunc(main.funcs)
async def test_func(item:str, *args, **kwargs):
    print("-----",kwargs)

@main.addfunc(main.funcs)
async def somef(item:str,*args, **kwargs):
    return kwargs["ctx"]

@main.addfunc(main.funcs)
async def function4(*args, **kwargs):
    return "FOX"

@main.addfunc(main.funcs)
async def function1(item:int, type:bool,*args, **kwargs):
    return type

@main.addfunc(main.funcs)
async def function2(item:str, *args, **kwargs):
    await main.isempty(item)
    return eval(item)

@main.addfunc(main.funcs)
async def inside(item:str, type:bool=False,*args, **kwargs):
    return type

# Sync Parsing
print(asyncio.run(main.parse("""
$test_func[$test_func[sfsaf]]
$let[test;good] $function1[1;$inside[true];$sadsadsdsd[]] $onlyif[1<2;XUI]
$function2[1+2;dsadasd] sometext
$math[1+2] $function4[]
$function1[1;$inside[fsfdfd;true];$sadsadsdsd[]]
$sdasdasd[sadsadsad]
sdasdsa $pyexec[true;print(1+231321, end='')] $xfexec[true;]
$get[test]
$somef[test]
$xftry[ERROR EXT $get[_];$function1[]] $xftry[$console[$get[_]];$function2[]]
$function1[1;True;world\\;yes]
""", ctx="asdsdsdasds")))
```

Output:
```
----- {'ctx': 'asdsdsdasds'}
----- {'ctx': 'asdsdsdasds'}
None
 False 
3 sometext
3 FOX
True
$sdasdasd[sadsadsad]
sdasdsa $pyexec[true;print(1+231321, end='')]
good
asdsdsdasds
$xftry[ERROR EXT $get[_];$function1[]] $xftry[$console[$get[_]];$function2[]]
$function1[1;True;world\;yes]
```

# Examples

package for creation Discord bots (beta)
