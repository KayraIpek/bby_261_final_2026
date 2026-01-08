# rommenu.py
class MenuSistemi:

    @staticmethod
    def karsilama(program_adi):
        print(f"\n{program_adi} programına hoş geldiniz!\n")

    @staticmethod
    def menuOlustur(menu_map): # menu_map: {"Açıklama": fonksiyon_objesi, ...}
        numbered_options = {}
        for i, (description, func_obj) in enumerate(menu_map.items(), 1):
            print(f"{i}. {description}")
            numbered_options[str(i)] = func_obj

        # Menünün sonuna otomatik olarak "Çıkış" seçeneğini ekle
        cikis_numarasi = str(len(menu_map) + 1)
        print(f"{cikis_numarasi}. Çıkış")

        secim = input("Bir seçenek giriniz: ")

        if secim in numbered_options:
            return numbered_options[secim]
        elif secim == cikis_numarasi:
            # Kullanıcı çıkışı seçtiyse özel bir değer döndür
            return "EXIT"
        else:
            print("Geçersiz bir seçim yaptınız.")
            return None # Geçersiz seçimde None döndür

    @staticmethod
    def menuyuCalistir(menu_map):
        """
        Menüyü sürekli olarak gösterir ve kullanıcı çıkış yapana kadar seçimleri işler.
        """
        while True:
            secim = MenuSistemi.menuOlustur(menu_map)

            if secim == "EXIT":
                print("Programdan çıkılıyor...")
                break
            elif secim: # Eğer geçerli bir fonksiyon seçildiyse (None değilse)
                secim() # Fonksiyonu çağır
                print() # Fonksiyon çalıştıktan sonra bir boşluk bırak
                print("-- Menü ------")
