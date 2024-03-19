import xfox
import sys,asyncio
try:
    from termcolor import colored
except:
    def colored(a,b):
        return a
def main():
    global argv
    argv=sys.argv[1:]
    try:
        match argv[0]:
            case "-p":
                try:
                    return asyncio.run(xfox.parse("\n".join(argv[1:])))
                except xfox.Raise as e:
                    print(colored(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}","red"))
            case _:
                try:
                    with open(argv[0], "r") as f:
                        return asyncio.run(xfox.parse("\n".join(f.readlines())))
                except FileNotFoundError as e:
                    print(colored(f"[ERROR] File {argv[0]} not found","red"))
                except xfox.Raise as e:
                    print(colored(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}","red"))
    except IndexError:
        print("Atterlity-xfox "+xfox.VERSION)
        print("Its just a compiller... Type something..")
        while True:
            try:
                a=input(">>> ")
            except KeyboardInterrupt:
                return 0
            try:
                print(asyncio.run(xfox.parse(a)))
            except xfox.Raise as e:
                print(colored(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}","red"))

main()