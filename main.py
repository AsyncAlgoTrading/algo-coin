from exchange import Exchange
from callback import Print


def main():
    ex = Exchange(sandbox=False)
    ex.registerCallback(
        Print(onMatch=True,
              onReceived=False,
              onOpen=False,
              onDone=False,
              onChange=False,
              onError=False))
    ex.run()

if __name__ == '__main__':
    main()
