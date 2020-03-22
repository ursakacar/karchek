from wsgiref.simple_server import make_server
import static

app = static.Cling('_site')

def main():
    make_server('localhost', 8000, static.Cling('_site')).serve_forever()

if __name__=='__main__':
    main()