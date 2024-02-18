import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame.mixer
import time
import random


class Kullanici:
    def __init__(self, eposta, sifre, ad, soyad):
        self.eposta = eposta
        self.sifre = sifre
        self.ad = ad
        self.soyad = soyad

class Kutuphane:
    def __init__(self):
        self.kitaplar = []

    def kitap_ekle(self, baslik, yazar, yil, sayfa):
        kitap = {
            "ID": len(self.kitaplar) + 1,
            "Başlık": baslik,
            "Yazar": yazar,
            "Yıl": yil,
            "Sayfa Sayısı": sayfa
        }
        self.kitaplar.append(kitap)
        self.kitapları_dosyaya_kaydet()

    def kitapları_dosyaya_kaydet(self):
        with open("kitaplar.txt", "w") as dosya:
            for kitap in self.kitaplar:
                dosya.write(f"{kitap['ID']},{kitap['Başlık']},{kitap['Yazar']},{kitap['Yıl']},{kitap['Sayfa Sayısı']}\n")

    def kitap_sil(self, kitap_id):
        for kitap in self.kitaplar:
            if str(kitap["ID"]) == kitap_id:
                self.kitaplar.remove(kitap)
                self.kitapları_dosyaya_kaydet()

    def kitaplari_listele(self, ust):
        etiket = tk.Label(ust, text="*** KİTAPLAR ***")
        etiket.pack()
        
        for kitap in self.kitaplar:
            bilgi = f"ID: {kitap['ID']}, Başlık: {kitap['Başlık']}, Yazar: {kitap['Yazar']}, Yıl: {kitap['Yıl']}, Sayfa Sayısı: {kitap['Sayfa Sayısı']}"
            etiket = tk.Label(ust, text=bilgi)
            etiket.pack()
        
class KutuphaneYonetimSistemi:
    def temizle_ekran(self):
     for widget in self.ust.winfo_children():
        widget.destroy()
     for widget in self.ust.winfo_children():
        
        if widget != self.arka_plan:
            widget.destroy()
    def __init__(self, ust):
        self.ust = ust
        ust.title("Kütüphane Yönetim Sistemi")
        self.arka_plan = None
        self.muzik_acik = True
        self.muzik_index = 0
        self.muzikler = []
        self.muzikler = ["klasik1.mp3", "klasik2.mp3", "klasik3.mp3","klasik4.mp3","klasik5.mp3"]
        self.arka_plan_tk = None
        self.yukle_arka_plan()
        
        
        self.etiket = tk.Label(ust, text="*** MENÜ ***")
        self.etiket.pack()

        
        self.liste_butonu = tk.Button(ust, text="Kitapları Listele", command=self.kitaplari_listele)
        self.liste_butonu.pack()

        self.ekle_butonu = tk.Button(ust, text="Kitap Ekle", command=self.kitap_ekle)
        self.ekle_butonu.pack()

        self.sil_butonu = tk.Button(ust, text="Kitap Sil", command=self.kitap_sil)
        self.sil_butonu.pack()

        self.arama_butonu = tk.Button(ust, text="Kitap Ara", command=self.kitap_ara)
        self.arama_butonu.pack()


        self.cikis_butonu = tk.Button(ust, text="Çıkış", command=ust.quit)
        self.cikis_butonu.pack()

        self.kutuphane = Kutuphane()

    def yukle_arka_plan(self):
        try:
            self.arka_plan_resmi = Image.open("arkaplan.jpg")
            self.arka_plan_resmi = self.arka_plan_resmi.resize((800, 600), Image.BILINEAR)
            self.arka_plan_tk = ImageTk.PhotoImage(self.arka_plan_resmi)
            self.arka_plan = tk.Label(self.ust, image=self.arka_plan_tk)
            self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Arka plan resmi yüklenirken hata oluştu!")

    
    def kitap_ara(self):
            self.temizle_ekran()
    
    # Arka planı tekrar yerleştir
            self.arka_plan = tk.Label(self.ust, image=self.arka_plan_tk)
            self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)

    # Kitap ara uı
            self.kitap_adi_etiket = tk.Label(self.ust, text="Aranacak Kitap Adı:")
            self.kitap_adi_etiket.place(relx=0.5, rely=0.3, anchor="center")
            self.kitap_adi_giris = tk.Entry(self.ust)
            self.kitap_adi_giris.place(relx=0.5, rely=0.35, anchor="center")
            
            self.ara_butonu = tk.Button(self.ust, text="Ara", command=self.kitap_ara_islem)
            self.ara_butonu.place(relx=0.5, rely=0.5, anchor="center")


            self.geri_butonu = tk.Button(self.ust, text="Geri", command=self.geri)
            self.geri_butonu.place(relx=0.05, rely=0.95, anchor="sw")
            self.entegre_muzik_butonlari()
            self.arama_butonu.destroy()
            
    def kitap_ara_islem(self):
        kitap_adi = self.kitap_adi_giris.get()
        if kitap_adi:
            bulundu = False
            with open("kitaplar.txt", "r") as dosya:
                for satir in dosya:
                    veri = satir.strip().split(",")
                    if len(veri) >= 5 and veri[1].strip() == kitap_adi:
                        messagebox.showinfo("Kitap Bulundu", f"{kitap_adi} adlı kitap bulundu.\nYazar: {veri[2]}\nYıl: {veri[3]}\nSayfa Sayısı: {veri[4]}")
                        bulundu = True
                        break
            if not bulundu:
             messagebox.showerror("Hata", f"{kitap_adi} adlı kitap bulunamadı.")
        else:
            messagebox.showerror("Hata", "Lütfen bir kitap adı girin.")


    def muzik_kontrol(self):
        if self.muzik_acik:
            pygame.mixer.music.pause()
            self.muzik_butonu.config(text="Müzik Aç")  # Buton metnini güncelle
            self.muzik_acik = False
        else:
            pygame.mixer.music.unpause()
            self.muzik_butonu.config(text="Müzik Kapat")  # Buton metnini güncelle
            self.muzik_acik = True

    def onceki_muzik(self):
        if self.muzik_index > 0:
            self.muzik_index -= 1
        else:
            self.muzik_index = len(self.muzikler) - 1
    
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.muzikler[self.muzik_index])
        pygame.mixer.music.play(-1)

    def sonraki_muzik(self):
        if self.muzik_index < len(self.muzikler) - 1:
            self.muzik_index += 1
        else:
            self.muzik_index = 0
        
    
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.muzikler[self.muzik_index])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
    
    def entegre_muzik_butonlari(self):
        self.muzik_butonu = tk.Button(self.ust, text="Müzik Kapat", command=self.muzik_kontrol)
        self.muzik_butonu.place(relx=0.95, rely=0.95, anchor="se")

        self.onceki_muzik_butonu = tk.Button(self.ust, text="Önceki Müzik", command=self.onceki_muzik)
        self.onceki_muzik_butonu.place(relx=0.75, rely=0.95, anchor="se")

        self.sonraki_muzik_butonu = tk.Button(self.ust, text="Sonraki Müzik", command=self.sonraki_muzik)
        self.sonraki_muzik_butonu.place(relx=0.85, rely=0.95, anchor="se")


    def kitaplari_listele(self):
        self.etiket.destroy()
        self.liste_butonu.destroy()
        self.ekle_butonu.destroy()
        self.sil_butonu.destroy()
        self.cikis_butonu.destroy()
        self.arama_butonu.destroy()
        
        self.kutuphane.kitaplari_listele(self.ust)

        self.geri_butonu = tk.Button(self.ust, text="Geri", command=self.geri)
        self.geri_butonu.pack()
    
    def kitap_ekle(self):
        self.etiket.destroy()
        self.liste_butonu.destroy()
        self.ekle_butonu.destroy()
        self.sil_butonu.destroy()
        self.cikis_butonu.destroy()
        self.arama_butonu.destroy()
        

        self.baslik_etiket = tk.Label(self.ust, text="Kitap Adı:")
        self.baslik_etiket.pack()
        self.baslik_giris = tk.Entry(self.ust)
        self.baslik_giris.pack()

        self.yazar_etiket = tk.Label(self.ust, text="Yazar:")
        self.yazar_etiket.pack()
        self.yazar_giris = tk.Entry(self.ust)
        self.yazar_giris.pack()

        self.yil_etiket = tk.Label(self.ust, text="Yayın Yılı:")
        self.yil_etiket.pack()
        self.yil_giris = tk.Entry(self.ust)
        self.yil_giris.pack()

        self.sayfa_etiket = tk.Label(self.ust, text="Sayfa Sayısı:")
        self.sayfa_etiket.pack()
        self.sayfa_giris = tk.Entry(self.ust)
        self.sayfa_giris.pack()

        self.ekle_butonu = tk.Button(self.ust, text="Ekle", command=self.kitap_ekle_kutuphane)
        self.ekle_butonu.pack()

        self.geri_butonu = tk.Button(self.ust, text="Geri", command=self.geri)
        self.geri_butonu.pack()

    def kitap_ekle_kutuphane(self):
        baslik = self.baslik_giris.get()
        yazar = self.yazar_giris.get()
        yil = self.yil_giris.get()
        sayfa = self.sayfa_giris.get()
        self.arama_butonu.destroy()
        
        if not baslik or not yazar or not yil or not sayfa:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        self.kutuphane.kitap_ekle(baslik, yazar, yil, sayfa)

        self.baslik_etiket.destroy()
        self.baslik_giris.destroy()
        self.yazar_etiket.destroy()
        self.yazar_giris.destroy()
        self.yil_etiket.destroy()
        self.yil_giris.destroy()
        self.sayfa_etiket.destroy()
        self.sayfa_giris.destroy()
        self.ekle_butonu.destroy()
        self.geri_butonu.destroy()

        self.etiket = tk.Label(self.ust, text="Kitap eklendi.")
        self.etiket.pack()

        self.anamenuye_don_butonu = tk.Button(self.ust, text="Ana Menüye Dön", command=self.anamenuye_don)
        self.anamenuye_don_butonu.pack()

    def kitap_sil(self):
        self.etiket.destroy()
        self.liste_butonu.destroy()
        self.ekle_butonu.destroy()
        self.sil_butonu.destroy()
        self.cikis_butonu.destroy()
        
        self.kutuphane.kitaplari_listele(self.ust)

        self.sil_etiket = tk.Label(self.ust, text="Silmek istediğiniz kitabın ID'sini girin:")
        self.sil_etiket.pack()
        self.sil_giris = tk.Entry(self.ust)
        self.sil_giris.pack()

        self.sil_butonu = tk.Button(self.ust, text="Sil", command=self.kitap_sil_kutuphane)
        self.sil_butonu.pack()

        self.geri_butonu = tk.Button(self.ust, text="Geri", command=self.geri)
        self.geri_butonu.pack()

    def kitap_sil_kutuphane(self):
        kitap_id = self.sil_giris.get()
        self.kutuphane.kitap_sil(kitap_id)
        self.arama_butonu.destroy()
        
        if not kitap_id:
           messagebox.showerror("Hata", "Lütfen bir ID girin.")
           return
        
        if kitap_id not in self.kutuphane.kitaplar:
            messagebox.showerror("Hata", "Bu ID'ye sahip bir kitap bulunamadı.")
            return
        
        self.kutuphane.kitap_sil(kitap_id)
        
        self.sil_etiket.destroy()
        self.sil_giris.destroy()
        self.sil_butonu.destroy()
        self.geri_butonu.destroy()

        self.etiket = tk.Label(self.ust, text="Kitap silindi.")
        self.etiket.pack()

        self.anamenuye_don_butonu = tk.Button(self.ust, text="Ana Menüye Dön", command=self.anamenuye_don)
        self.anamenuye_don_butonu.pack()
    
    
    
    def geri(self):
    # geriye basınca ekrandakileri siler
        self.temizle_ekran()
        self.arama_butonu.destroy()

        try:
         self.arka_plan_resmi = Image.open("arkaplan.jpg")
         self.arka_plan_resmi = self.arka_plan_resmi.resize((800, 600), Image.BILINEAR)
         self.arka_plan_tk = ImageTk.PhotoImage(self.arka_plan_resmi)
         self.arka_plan = tk.Label(self.ust, image=self.arka_plan_tk)
         self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
         print("Arka plan resmi yüklenirken hata oluştu!")
    
      

    # Menü butonlarını geri eklemek için
        self.muzik_butonu = tk.Button(self.ust, text="Müzik Kapat", command=self.muzik_kontrol)
        self.muzik_butonu.place(relx=0.95, rely=0.95, anchor="se")
         
        self.onceki_muzik_butonu = tk.Button(self.ust, text="Önceki Müzik", command=self.onceki_muzik)
        self.onceki_muzik_butonu.place(relx=0.75, rely=0.95, anchor="se")

        self.sonraki_muzik_butonu = tk.Button(self.ust, text="Sonraki Müzik", command=self.sonraki_muzik)
        self.sonraki_muzik_butonu.place(relx=0.85, rely=0.95, anchor="se")
        
        self.etiket = tk.Label(self.ust, text="*** MENÜ ***")
        self.etiket.pack()

        
        self.liste_butonu = tk.Button(self.ust, text="Kitapları Listele", command=self.kitaplari_listele)
        self.liste_butonu.pack()

        self.ekle_butonu = tk.Button(self.ust, text="Kitap Ekle", command=self.kitap_ekle)
        self.ekle_butonu.pack()

        self.sil_butonu = tk.Button(self.ust, text="Kitap Sil", command=self.kitap_sil)
        self.sil_butonu.pack()

        self.liste_butonu = tk.Button(self.ust, text="Kitap Ara", command=self.kitap_ara)
        self.liste_butonu.pack()

        self.cikis_butonu = tk.Button(self.ust, text="Çıkış", command=self.ust.quit)
        self.cikis_butonu.pack()
        
        
        
        if self.arka_plan:
            self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)

        if not hasattr(self, 'muzik_kontrol'):
        # Müzik butonları yoksa oluştur
            self.muzik_butonu = tk.Button(self.ust, text="Müzik Kapat", command=self.muzik_kontrol)
            self.muzik_butonu.place(relx=0.95, rely=0.95, anchor="se")
            self.onceki_muzik_butonu = tk.Button(self.ust, text="Önceki Müzik", command=self.onceki_muzik)
            self.onceki_muzik_butonu.place(relx=0.75, rely=0.95, anchor="se")
            self.sonraki_muzik_butonu = tk.Button(self.ust, text="Sonraki Müzik", command=self.sonraki_muzik)
            self.sonraki_muzik_butonu.place(relx=0.85, rely=0.95, anchor="se")
    
        
    def anamenuye_don(self):
        self.etiket.destroy()
        self.anamenuye_don_butonu.destroy()

        self.etiket = tk.Label(self.ust, text="*** MENÜ ***")
        self.etiket.pack()

        self.liste_butonu = tk.Button(self.ust, text="Kitapları Listele", command=self.kitaplari_listele)
        self.liste_butonu.pack()

        self.ekle_butonu = tk.Button(self.ust, text="Kitap Ekle", command=self.kitap_ekle)
        self.ekle_butonu.pack()

        self.sil_butonu = tk.Button(self.ust, text="Kitap Sil", command=self.kitap_sil)
        self.sil_butonu.pack()

        self.sil_butonu = tk.Button(self.ust, text="Kitap Ara", command=self.kitap_ara)
        self.sil_butonu.pack()

        self.cikis_butonu = tk.Button(self.ust, text="Çıkış", command=self.ust.quit)
        self.cikis_butonu.pack()

class KutuphaneArayuzu:
    def __init__(self, ust):
        self.ust = ust
        self.giris_yapildi = False  # Giriş yapıldı mı?
        self.muzik_index = 0  # Müzik listesi içindeki indeks
        self.muzikler = ["klasik1.mp3", "klasik2.mp3", "klasik3.mp3","klasik4.mp3","klasik5.mp3"]  # Müzik listesi
        self.muzik_acik = True  # Müzik açık mı?
        ust.title("Kütüphane Bilgi Sistemi")

        # Arka plan resmi
        self.arka_plan_resmi = Image.open("arkaplan.jpg")
        self.arka_plan_resmi = self.arka_plan_resmi.resize((800, 600), Image.BILINEAR)
        self.arka_plan_tk = ImageTk.PhotoImage(self.arka_plan_resmi)
        self.arka_plan = tk.Label(ust, image=self.arka_plan_tk)
        self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)

        self.muzik_index = random.randint(0, len(self.muzikler) - 1)

        # Müzik çal
        pygame.mixer.init()
        pygame.mixer.music.load(self.muzikler[self.muzik_index])
        pygame.mixer.music.play(-1)

        # giriş butonu
        self.giris_butonu = tk.Button(ust, text="Giriş Yap", command=self.giris)
        self.giris_butonu.place(relx=0.5, rely=0.4, anchor="center")

        # kayıt butonu
        self.kayit_butonu = tk.Button(ust, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_butonu.place(relx=0.5, rely=0.6, anchor="center")

        # müzik açma/kapatma butonu
        self.muzik_butonu = tk.Button(ust, text="Müzik Kapat", command=self.muzik_kontrol)
        self.muzik_butonu.place(relx=0.95, rely=0.95, anchor="se")
        # önceki butonu
        self.onceki_muzik_butonu = tk.Button(ust, text="Önceki Müzik", command=self.onceki_muzik)
        self.onceki_muzik_butonu.place(relx=0.75, rely=0.95, anchor="se")
        # sonraki butonu
        self.sonraki_muzik_butonu = tk.Button(ust, text="Sonraki Müzik", command=self.sonraki_muzik)
        self.sonraki_muzik_butonu.place(relx=0.85, rely=0.95, anchor="se")

    def giris(self):
        # giriş ekranı bilgileri 
        self.temizle_ekran()

        self.eposta_etiket = tk.Label(self.ust, text="E-posta:")
        self.eposta_etiket.place(relx=0.5, rely=0.35, anchor="center")
        self.eposta_giris = tk.Entry(self.ust)
        self.eposta_giris.place(relx=0.5, rely=0.4, anchor="center")

        self.sifre_etiket = tk.Label(self.ust, text="Şifre:")
        self.sifre_etiket.place(relx=0.5, rely=0.45, anchor="center")
        self.sifre_giris = tk.Entry(self.ust, show="*")
        self.sifre_giris.place(relx=0.5, rely=0.5, anchor="center")

        self.giris_butonu = tk.Button(self.ust, text="Giriş Yap", command=self.giris_kontrol)
        self.giris_butonu.place(relx=0.5, rely=0.6, anchor="center")
        
        self.geri_butonu = tk.Button(self.ust, text="Geri", command=self.geri_giris)
        self.geri_butonu.place(relx=0.05, rely=0.95, anchor="sw")

    def kayit_ol(self):
        # Kayıt ekranı bileşenleri
        self.temizle_ekran()

        self.eposta_etiket = tk.Label(self.ust, text="E-posta:")
        self.eposta_etiket.place(relx=0.5, rely=0.35, anchor="center")
        self.eposta_giris = tk.Entry(self.ust)
        self.eposta_giris.place(relx=0.5, rely=0.4, anchor="center")

        self.sifre_etiket = tk.Label(self.ust, text="Şifre:")
        self.sifre_etiket.place(relx=0.5, rely=0.45, anchor="center")
        self.sifre_giris = tk.Entry(self.ust, show="*")
        self.sifre_giris.place(relx=0.5, rely=0.5, anchor="center")

        self.ad_etiket = tk.Label(self.ust, text="Ad:")
        self.ad_etiket.place(relx=0.5, rely=0.55, anchor="center")
        self.ad_giris = tk.Entry(self.ust)
        self.ad_giris.place(relx=0.5, rely=0.6, anchor="center")

        self.soyad_etiket = tk.Label(self.ust, text="Soyad:")
        self.soyad_etiket.place(relx=0.5, rely=0.65, anchor="center")
        self.soyad_giris = tk.Entry(self.ust)
        self.soyad_giris.place(relx=0.5, rely=0.7, anchor="center")

        self.kayit_butonu = tk.Button(self.ust, text="Kayıt Ol", command=self.kayit_ol_kaydet)
        self.kayit_butonu.place(relx=0.5, rely=0.8, anchor="center")
        
        self.geri_butonu = tk.Button(self.ust, text="Geri", command=self.geri_kayit)
        self.geri_butonu.place(relx=0.05, rely=0.95, anchor="sw")

    def giris_kontrol(self):
        eposta = self.eposta_giris.get()
        sifre = self.sifre_giris.get()

        if eposta == "" or sifre == "":
            messagebox.showerror("Hata", "Lütfen e-posta ve şifre alanlarını doldurun.")
            return

        with open("kullanici_bilgileri.txt", "r") as dosya:
            for satir in dosya:
                veri = satir.strip().split(",")
                if veri[0] == eposta and veri[1] == sifre:
                    messagebox.showinfo("Başarılı", "Giriş başarılı.")
                    self.temizle_ekran()
                    self.kutuphane_arayuzu = KutuphaneYonetimSistemi(self.ust)
                    self.ust.update()
                    self.giris_yapildi = True
                    return

        messagebox.showerror("Hata", "Geçersiz e-posta veya şifre.")

    def kayit_ol_kaydet(self):
        eposta = self.eposta_giris.get()
        sifre = self.sifre_giris.get()
        ad = self.ad_giris.get()
        soyad = self.soyad_giris.get()

        if eposta == "" or sifre == "" or ad == "" or soyad == "":
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        with open("kullanici_bilgileri.txt", "a") as dosya:
            dosya.write(f"{eposta},{sifre},{ad},{soyad}\n")

        messagebox.showinfo("Başarılı", "Kayıt başarıyla tamamlandı.")
        self.temizle_ekran()
        self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)
        self.giris_butonu = tk.Button(self.ust, text="Giriş Yap", command=self.giris)
        self.giris_butonu.place(relx=0.5, rely=0.4, anchor="center")
        self.kayit_butonu = tk.Button(self.ust, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_butonu.place(relx=0.5, rely=0.6, anchor="center")

    def muzik_kontrol(self):
        if self.muzik_acik:
         pygame.mixer.music.pause()
         self.muzik_butonu.config(text="Müzik Aç")
         self.muzik_acik = False
        else:
         pygame.mixer.music.unpause()
         self.muzik_butonu.config(text="Müzik Kapat")
         self.muzik_acik = True

    def onceki_muzik(self):
        if self.muzik_index > 0:
            self.muzik_index -= 1
        else:
             self.muzik_index = len(self.muzikler) - 1
    
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.muzikler[self.muzik_index])
        pygame.mixer.music.play(-1)

    def sonraki_muzik(self):
        if self.muzik_index < len(self.muzikler) - 1:
         self.muzik_index += 1
        else:
         self.muzik_index = 0
    
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.muzikler[self.muzik_index])
        pygame.mixer.music.play(-1)

    
    
    def temizle_ekran(self):
        if hasattr(self, 'eposta_etiket'):
            self.eposta_etiket.destroy()
        if hasattr(self, 'eposta_giris'):
            self.eposta_giris.destroy()
        if hasattr(self, 'sifre_etiket'):
            self.sifre_etiket.destroy()
        if hasattr(self, 'sifre_giris'):
            self.sifre_giris.destroy()
        if hasattr(self, 'ad_etiket'):
            self.ad_etiket.destroy()
        if hasattr(self, 'ad_giris'):
            self.ad_giris.destroy()
        if hasattr(self, 'soyad_etiket'):
            self.soyad_etiket.destroy()
        if hasattr(self, 'soyad_giris'):
            self.soyad_giris.destroy()
        if hasattr(self, 'giris_butonu'):
            self.giris_butonu.destroy()
        if hasattr(self, 'kayit_butonu'):
            self.kayit_butonu.destroy()
        if hasattr(self, 'geri_butonu'):
            self.geri_butonu.destroy()

    def geri_giris(self):
        self.temizle_ekran()
        self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)
        self.giris_butonu = tk.Button(self.ust, text="Giriş Yap", command=self.giris)
        self.giris_butonu.place(relx=0.5, rely=0.4, anchor="center")
        self.kayit_butonu = tk.Button(self.ust, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_butonu.place(relx=0.5, rely=0.6, anchor="center")

    def geri_kayit(self):
        self.temizle_ekran()
        self.arka_plan.place(x=0, y=0, relwidth=1, relheight=1)
        self.giris_butonu = tk.Button(self.ust, text="Giriş Yap", command=self.giris)
        self.giris_butonu.place(relx=0.5, rely=0.4, anchor="center")
        self.kayit_butonu = tk.Button(self.ust, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_butonu.place(relx=0.5, rely=0.6, anchor="center")


pencere = tk.Tk()
pencere.geometry("800x600")


uygulama = KutuphaneArayuzu(pencere)


pencere.mainloop()
