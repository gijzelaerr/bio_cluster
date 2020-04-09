from oca import Client
from conf import USER, PASSWORD, ENDPOINT


def main():
    client = Client(USER + ':' + PASSWORD, ENDPOINT)
    print(client.version())


if __name__ == '__main__':
    main()
