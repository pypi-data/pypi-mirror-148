import urllib.parse
import sys

def main():

    if(sys.argv[1] == "-e"):
        print(urllib.parse.quote(str(sys.argv[2])))

    if (sys.argv[1] == "-d"):
        print(urllib.parse.unquote(str(sys.argv[2])))

if __name__ == '__main__':
    #main()
