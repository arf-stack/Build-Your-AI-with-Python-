import json
from difflib import get_close_matches as yakin_sonuclari_getir

def veritabanini_yukle():
    try:
        with open("/Users/arifbayir/Desktop/akıllı chatbot/veritabani.json", "r") as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        print("Veritabanı dosyası bulunamadı.")
        return {"sorular": []}
    except json.JSONDecodeError:
        print("Veritabanı dosyası bozuk.")
        return {"sorular": []}

def veritabanina_yaz(veriler):
    try:
        with open("/Users/arifbayir/Desktop/akıllı chatbot/veritabani.json", "w") as dosya:
            json.dump(veriler, dosya, indent=2)
    except IOError:
        print("Veritabanı dosyasına yazılamadı.")

def yakin_sonuc_bul(soru, sorular):
    eslesen = yakin_sonuclari_getir(soru, sorular, n=1, cutoff=0.6)
    return eslesen[0] if eslesen else None

def cevabini_bul(soru, veritabani):
    for soru_cevaplar in veritabani["sorular"]:
        if soru_cevaplar["soru"] == soru:
            return soru_cevaplar["cevap"]
    return None

def chat_bot():
    veritabani = veritabanini_yukle()

    while True:
        soru = input("Siz: ").strip()

        if not soru:
            print("Lütfen bir soru girin.")
            continue

        if soru.lower() == 'çık':
            break

        gelen_sonuc = yakin_sonuc_bul(soru, [soru_cevaplar["soru"] for soru_cevaplar in veritabani["sorular"]])
        if gelen_sonuc:
            verilecek_cevap = cevabini_bul(gelen_sonuc, veritabani)
            print(f"Bot: {verilecek_cevap}")
        else:
            print("Bot: Bunu nasıl cevaplayacağımı bilmiyorum. Ama bana bunu öğretebilirsin.")
            yeni_cevap = input("Öğretmek için yazabilir veya 'geç' diyebilirsiniz: ").strip()
            if yeni_cevap.lower() != 'geç':
                veritabani["sorular"].append({
                    "soru": soru,
                    "cevap": yeni_cevap
                })
                veritabanina_yaz(veritabani)
                print("Bot: Teşekkürler, sayenizde yeni bir şey öğrendim.")

if __name__ == '__main__':
    chat_bot()