import json, sys, os, re
from terminaltables import AsciiTable
from colorama import Fore, Style

class Node:
    def __init__(self, info):
        self.info = info
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self, path):
        self.awal = None
        self.akhir = None
        self.path = path
        self.list = {}

        with open(self.path) as json_data:
            data = json.load(json_data)

            for obj in data:
                self.addLast(obj)        

            self.list = data
    
    def clearConsole(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def menu(self):

        def selectMenu():
            opsi = input(f'{Fore.YELLOW}\x1b[1m[ Pilih Salah Satu ]\x1b[0m{Fore.BLUE} >> {Style.RESET_ALL}')

            while opsi == '1' or opsi == '2' or opsi == '3' or opsi == '4' or opsi == '5' or opsi == '6':
                if opsi == '1':
                    self.tambahData()
                    break
                elif opsi == '2':
                    self.editData()
                    break
                elif opsi == '3':
                    self.hapusData()
                    break
                elif opsi == '4':
                    self.tampilData()
                    break
                elif opsi == '5':
                    self.credit()
                    break
                elif opsi == '6':
                    self.keluar()
            else:
                print(f'''\n{Fore.RED}Opsi dengan '{opsi}' tidak valid, pilih salah satu angka di menu!{Style.RESET_ALL}\n''')
                selectMenu()

        data = self.list
        stringMenu = f'''{Fore.WHITE}
# ============================================== #
#    {Fore.RED}        [  Aplikasi Data FILM  ]  {Fore.WHITE}          #
# ============================================== #

{Fore.YELLOW}\x1b[3mInfo : Terdapat {len(data)} film di database.\x1b[0m

{Fore.WHITE}1) {Fore.GREEN}Tambah data FILM
{Fore.WHITE}2) {Fore.GREEN}Edit data FILM
{Fore.WHITE}3) {Fore.GREEN}Hapus data FILM
{Fore.WHITE}4) {Fore.GREEN}Tampilkan FILM yang tersedia
{Fore.LIGHTBLACK_EX}--------------------------------
{Fore.WHITE}5) {Fore.CYAN}Tentang Aplikasi (Credit)
{Fore.WHITE}6) {Fore.RED}Keluar
'''
        self.clearConsole()
        print(stringMenu)
        selectMenu()

        

    def write2json(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=3)

    def tambahData(self):
        
        def confirmAdd():
            apakah = input(Fore.GREEN + '\nApakah anda ingin menambahkan data lagi [Y/T]? ' + Style.RESET_ALL)
            if apakah.upper() == 'N' or apakah.upper() == 'T':
                self.menu()
            elif apakah.upper() == 'Y':
                self.tambahData()
            else:
                print(Fore.RED + f"\ninput dengan kata kunci '{apakah}' tidak valid!")
                confirmAdd()  

        self.clearConsole()
        print(Fore.LIGHTWHITE_EX + '------------ [ TAMBAH DATA ] ------------\n')
        judul           = input(Fore.MAGENTA + 'Masukan judul         : ' + Style.RESET_ALL)
        genre           = input(Fore.MAGENTA + 'Masukan genre         : ' + Style.RESET_ALL)
        sutradara       = input(Fore.MAGENTA + 'Masukan sutradara     : ' + Style.RESET_ALL)
        tanggal_rilis   = input(Fore.MAGENTA + 'Masukan tanggal rilis : ' + Style.RESET_ALL)

        local_dict = {
                'no': self.size() + 1,
                'judul': judul,
                'genre': genre,
                'sutradara': sutradara,
                'tanggal_rilis': tanggal_rilis
            }

        self.addLast(local_dict)
        self.list.append(local_dict)
        self.write2json(self.list)
        self.clearConsole()
        print(f'''{Fore.LIGHTBLUE_EX}Penambahan Data Berhasil!\n''')
        confirmAdd()       

    def urutNomorFilm(self):
        list = []

        for i in range(len(self.list)):
            list.append({
                'no': i+1,
                'judul': self.list[i]['judul'],
                'genre': self.list[i]['genre'],
                'sutradara': self.list[i]['sutradara'],
                'tanggal_rilis': self.list[i]['tanggal_rilis']
            })

        self.list = list

    def editData(self):

        searchKeyword = input(Fore.MAGENTA + '\n[ EDIT DATA ] -> Masukan nomor/judul film : ' + Style.RESET_ALL)

        index = 0

        intSearchKeyword = None

        if re.match('^[-+]?[0-9]+$', searchKeyword):
            intSearchKeyword = int(searchKeyword)

        for i in range(len(self.list)):
            if intSearchKeyword == self.list[i]['no'] or searchKeyword.upper() in self.list[i]['judul'].upper():
                index = self.list[i]['no']

        def confirmUpdate():
            opsi = input(Fore.LIGHTBLUE_EX + f'\nApakah anda ingin mengubah data ini [Y/T]? ' + Style.RESET_ALL)
            
            if opsi.upper() == 'N' or opsi.upper() == 'T':
                return self.menu()
            elif opsi.upper() == 'Y':
                pass
            else:
                print(Fore.RED + f"\ninput dengan kata kunci '{opsi}' tidak valid!")
                confirmUpdate()

        def confirmDataUpdate():
            opsi = input(Fore.LIGHTBLUE_EX + f'\nTerapkan perubahan [Y/T]? ' + Style.RESET_ALL)
            
            if opsi.upper() == 'N' or opsi.upper() == 'T':
                self.clearConsole()
                print(Fore.RED + f'Perubahan data dibatalkan!')
                input(Fore.GREEN + '\n\n[ Kembali ]')
                self.menu()
            elif opsi.upper() == 'Y':
                pass
            else:
                print(Fore.RED + f"\ninput dengan kata kunci '{opsi}' tidak valid!")
                confirmDataUpdate()

                
                
        def successMessage():
            self.urutNomorFilm()
            self.write2json(self.list)
            self.clearConsole()
            print(Fore.CYAN + f'Sukses edit data FILM dengan judul {self.list[index - 1]["judul"]}!')
            input(Fore.GREEN + '\n\n[ Kembali ]')
            self.menu()


        if index != 0:
            table_field = ['No','Judul', 'Genre', 'Sutradara', 'Tanggal Rilis']
            
            table_data_before = [
                table_field
            ]

            table_data_before.append(
                [self.list[index - 1]['no'], self.list[index - 1]['judul'], self.list[index - 1]['genre'], self.list[index - 1]['sutradara'], self.list[index - 1]['tanggal_rilis']] 
            )

            table = AsciiTable(table_data_before, 'Data sebelum update')
            print(Fore.YELLOW + '\n' + table.table)

            confirmUpdate()

            print(Fore.WHITE + '\n------------ [ EDIT DATA ] ------------\n')
            judul           = input(Fore.MAGENTA + 'Masukan judul         : ' + Style.RESET_ALL)
            genre           = input(Fore.MAGENTA + 'Masukan genre         : ' + Style.RESET_ALL)
            sutradara       = input(Fore.MAGENTA + 'Masukan sutradara     : ' + Style.RESET_ALL)
            tanggal_rilis   = input(Fore.MAGENTA + 'Masukan tanggal rilis : ' + Style.RESET_ALL)

            local_dict = {
                    'no': index,
                    'judul': judul,
                    'genre': genre,
                    'sutradara': sutradara,
                    'tanggal_rilis': tanggal_rilis
                }

            
            table_data_after = [
                table_field
            ]

            table_data_after.append(
                    [local_dict['no'], local_dict['judul'], local_dict['genre'], local_dict['sutradara'], local_dict['tanggal_rilis']] 
            )

            table = AsciiTable(table_data_after, 'Data setelah update')
            print(Fore.YELLOW + '\n' + table.table)

            confirmDataUpdate()

            self.list[index - 1] = local_dict
            successMessage()
        else:
            self.clearConsole()
            print(Fore.RED + f"\nData dengan kata kunci '{searchKeyword}' tidak ditemukan!")
            input(Fore.GREEN + '\n\n[ Kembali ]')
            self.menu()

    def hapusData(self):
        searchKeyword = input(Fore.MAGENTA + '\n[ HAPUS DATA ] -> Masukan nomor/judul film : ' + Style.RESET_ALL)
        
        intSearchKeyword = None
        index = 0
        
        if re.match('^[-+]?[0-9]+$', searchKeyword):
            intSearchKeyword = int(searchKeyword)

        for i in range(len(self.list)):
            if intSearchKeyword == self.list[i]['no'] or searchKeyword.upper() in self.list[i]['judul'].upper():
                index = self.list[i]['no']

        temp_list = self.list[len(self.list) - 1]

        def showTable(data):
            table_data = [
                ['No','Judul', 'Genre', 'Sutradara', 'Tanggal Rilis']
            ]

            table_data.append(
                [data['no'], data['judul'], data['genre'], data['sutradara'], data['tanggal_rilis']] 
            )


            table = AsciiTable(table_data)
            print(Fore.YELLOW + '\n' + table.table)

        def confirmDelete():
            
            opsi = input(Fore.LIGHTBLUE_EX + f'\nApakah anda ingin menghapus data ini [Y/T]? ' + Style.RESET_ALL)
            
            if opsi.upper() == 'N' or opsi.upper() == 'T':
                return self.menu()
            elif opsi.upper() == 'Y':
                pass
            else:
                print(Fore.RED + f"\ninput dengan kata kunci '{opsi}' tidak valid!")
                confirmDelete()
                
        def successMessage():
            self.urutNomorFilm()
            self.write2json(self.list)
            self.clearConsole()
            print(Fore.CYAN + f'Sukses hapus data FILM dengan judul {temp_list["judul"]}!')
            input(Fore.GREEN + '\n\n[ Kembali ]')
            self.menu()

        if index != 0:
            if index == 1:
                showTable(self.list[index - 1])
                confirmDelete()
                self.removeFirst()
                self.list.pop()
                successMessage()
            elif index == self.size():
                showTable(self.list[index - 1])
                confirmDelete()
                self.removeLast()
                self.list.pop()
                successMessage()
            else:
                showTable(self.list[index - 1])
                confirmDelete()
                removedNode = self.get(index)
                if removedNode is not None:
                    removedNode.prev.next = removedNode.next
                    removedNode.next.prev = removedNode.prev
                    del removedNode
                    self.list.pop(index - 1)
                    successMessage()
                else:
                    self.clearConsole()
                    print(Fore.RED + f"Hapus data gagal. Nomor {index} tidak ditemukan!")
                    input(Fore.GREEN + '\n\n[ Kembali ]')
                    self.menu()
        else:
            self.clearConsole()
            print(Fore.RED + f"\nData dengan kata kunci '{searchKeyword}' tidak ditemukan!")
            input(Fore.GREEN + '\n\n[ Kembali ]')
            self.menu()
    
    def dictPage(self, page, list):
        result = []
        
        dictSeparate = [list[i:i+10] for i in range(0, len(list), 10)]
        listLength = len(dictSeparate)
        index = page - 1
        if index < listLength and index >= 0:
            result = dictSeparate[index]
        elif index < 0:
            result = []

        return result

    def tampilData(self, page=1):
        table_data = [
            ['No','Judul', 'Genre', 'Sutradara', 'Tanggal Rilis']
        ]

        data = self.dictPage(page, self.list)

        
        for i in range(len(data)):
            table_data.append(
                [data[i]['no'], data[i]['judul'], data[i]['genre'], data[i]['sutradara'], data[i]['tanggal_rilis']] 
            )

        self.clearConsole()
        allPage = len([self.list[i:i+10] for i in range(0, len(self.list), 10)])
        judul = f"[ List Film - Page {page}/{allPage} ]"
        table = AsciiTable(table_data, judul)
        print(Fore.YELLOW + '\n' + table.table)

        pageid = input(f'''\n\n{Fore.BLUE}[ TAMPIL DATA ] Masukan No Page / Enter untuk kembali : {Style.RESET_ALL}''')

        if re.match('^[-+]?[0-9]+$', pageid):
            self.tampilData(int(pageid))
            pass
        else:
            self.menu()
        
    def credit(self):
        self.clearConsole()
        print(f'''{Fore.RED}
# ============================================== #
#            {Fore.LIGHTWHITE_EX}\033[1m[  Tentang Aplikasi  ]\x1b[0m{Fore.RED}              #
#      {Fore.LIGHTWHITE_EX}\x1b[3mLoving yourself will save your soul\x1b[0m{Fore.RED}       #
# ============================================== #
#                                                #
#    {Fore.CYAN}Dibuat Oleh Hanif Ahmad Syauqi - 1012161{Fore.RED}    #
{Fore.WHITE}#          {Fore.GREEN}Teknik Informatika 4 / 2021 {Fore.WHITE}          #
#                                                #
#        {Fore.LIGHTMAGENTA_EX}github.com/MRHRTZ/Crud-Data-Film{Fore.WHITE}        #
#              {Fore.YELLOW}wa.me/6285559038021{Fore.WHITE}               #
#                                                #
# ============================================== # {Style.RESET_ALL}''')
        input(Fore.GREEN + '\n\n[ Kembali ]')
        self.menu()

    def keluar(self):
        print(Fore.YELLOW + '\n\nBye 🤞\n' + Style.RESET_ALL)

        sys.exit(0)
        
    def isEmpty(self):
        return self.awal is None

    def size(self):
        if self.isEmpty():
            banyakNode = 0
        else:
            bantu = self.awal
            banyakNode = 1
            while bantu.next is not None:
                banyakNode = banyakNode + 1
                bantu = bantu.next
        return banyakNode

    def getFirst(self):
        return self.awal

    def getLast(self):
        return self.akhir

    def get(self, index):
        if self.isEmpty() or index<1 or index>self.size():
            return None
        else:
            bantu = self.awal
            posisi = 1
            while posisi<index:
                bantu = bantu.next
                posisi = posisi + 1
            return bantu
            

    def addLast(self, info):
        newNode = Node(info)
        if self.isEmpty():
            self.awal = newNode
            self.akhir = newNode
        else:
            self.akhir.next = newNode
            newNode.prev = self.akhir
            self.akhir = newNode

    def removeFirst(self):
        if self.isEmpty():
            print("Ngak bisa hapus. Data kosong")
        elif self.awal == self.akhir:
            removedNode = self.awal
            self.awal = None
            self.akhir = None
            del removedNode
        else:
            removedNode = self.awal
            self.awal = self.awal.next
            self.awal.prev = None
            del removedNode

    def removeLast(self):
        if self.awal == self.akhir:
            removedNode = self.awal
            self.awal = None
            self.akhir = None
            del removedNode
        else:
            removedNode = self.akhir
            self.akhir = self.akhir.prev
            self.akhir.next = None
            del removedNode
            
    def remove(self, index):
        if index==1:
            self.removeFirst()
        elif index==self.size():
            self.removeLast()
        else:
            removedNode = self.get(index)
            if removedNode is not None:
                removedNode.prev.next = removedNode.next
                removedNode.next.prev = removedNode.prev
                del removedNode