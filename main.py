from lib.doubleLinkedList import DoubleLinkedList

if __name__ == '__main__':
    try:
        ls = DoubleLinkedList('./db/data.json')
        ls.menu()
    except KeyboardInterrupt:
        ls.keluar()