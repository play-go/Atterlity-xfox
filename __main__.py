import xfox
import sys,asyncio
argv=sys.argv[1:]
endphase='Bye!'
def main():
    global argv,endphase
    try:
        match argv[0]:
            case "-p":
                try:
                    return asyncio.run(xfox.parse("\n".join(argv[1:])))
                except xfox.Raise as e:
                    print(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}")
            case _:
                try:
                    with open(argv[0], "r") as f:
                        return asyncio.run(xfox.parse("\n".join(f.readlines())))
                except xfox.Raise as e:
                    print(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}")
    except IndexError:
        print("Atterlity-xfox "+xfox.VERSION)
        print("Its just a compiller... Type something..")
        while True:
            try:
                a=input(">>> ")
            except KeyboardInterrupt:
                print(f"\n{endphase}")
                return 0
            try:
                print(asyncio.run(xfox.parse(a)))
            except xfox.Raise as e:
                print(f"[ERROR] {e.args[0]['name']}: {e.args[0]['text']}")

main()