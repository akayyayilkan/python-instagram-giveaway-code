import os
import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# =========================================================
# 🎯 BİLGİLERİN VE AYARLARIN
# =========================================================
INSTAGRAM_USER = "kullanici_adi"
INSTAGRAM_PASS = "hesap_şifre"
POST_URL = "çekiliş_url"
DOSYA_YOLU = "kullanicilar.txt"
TOTAL_COMMENTS = 100  # 🎯 SINIR 100 YORUM YAPILDI

def ekrani_temizle():
    os.system('clear')

def banner_yazdir():
    print("=" * 60)
    print("  INSTAGRAM 3'LÜ GERÇEK HESAP ETIKETLEME (100 YORUM MODU)")
    print("=" * 60)

def instagram_3lu_post_botu():
    ekrani_temizle()
    banner_yazdir()

    if not os.path.exists(DOSYA_YOLU):
        print(f"[HATA] '{DOSYA_YOLU}' bulunamadı!")
        print("Lütfen 'kullanicilar.txt' dosyasının botla aynı klasörde olduğundan emin ol.")
        input("\nDevam etmek için ENTER'a basın...")
        return

    with open(DOSYA_YOLU, "r", encoding="utf-8") as f:
        user_pool = [line.strip().replace("@", "") for line in f.readlines() if line.strip()]

    if len(user_pool) < 3:
        print(f"\n[!] 'kullanicilar.txt' içinde en az 3 gerçek kullanıcı olmalıdır.")
        input("\nDevam etmek için ENTER'a basın...")
        return

    messages = ["Harika bir çekiliş", "Umarım bana çıkar", "Kazanmayı çok istiyorum", "Süper fırsat", "Katıldım", "Harika hediye"]
    emojis = ["🔥", "✨", "🎉", "👏", "🙌", "💯", "🚀", "😍", "🎁", "🍀"]

    print(f"[+] Toplam {len(user_pool)} adet GERÇEK kullanıcı listeden yüklendi.")
    print(f"[+] Toplam {TOTAL_COMMENTS} adet 3'lü yorum atılacak.")
    print("[+] Chrome başlatılıyor...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    
    # 1. Instagram Giriş Sayfası
    print("[+] Instagram giriş sayfasına gidiliyor...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    try:
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(INSTAGRAM_USER)
        password_input.send_keys(INSTAGRAM_PASS)
        password_input.send_keys(Keys.ENTER)
        time.sleep(6)
    except Exception:
        print(f"[!] Otomatik giriş adımı atlandı.")

    print("\n---------------------------------------------------------")
    print("👉 Açılan Chrome penceresinden hesabına giriş yapıldığından emin ol.")
    print("👉 Ana sayfaya ulaştıysan BURAYA DÖNÜP ENTER'A BAS!")
    print("---------------------------------------------------------\n")
    input("Giriş yapıldıysa ENTER'a bas kardo...")

    # 2. Çekiliş Gönderisine Git
    print(f"\n[+] Çekiliş gönderisine gidiliyor: {POST_URL}")
    driver.get(POST_URL)
    time.sleep(5)

    # 3. Yorum YAZMA VE POST ETME Döngüsü (100 Yorum)
    for i in range(TOTAL_COMMENTS):
        selected_users = random.sample(user_pool, 3)
        tagged_string = " ".join([f"@{u}" for u in selected_users])
        random_msg = random.choice(messages)
        random_emojis = "".join(random.sample(emojis, 2))
        
        comment_text = f"{random_msg} {tagged_string} {random_emojis}"

        try:
            comment_box = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Yorum ekle...' or @placeholder='Add a comment...']"))
            )
            comment_box.click()
            time.sleep(1)

            driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                comment_box,
                comment_text
            )
            time.sleep(1.5)

            comment_box.send_keys(" ")
            time.sleep(0.5)
            comment_box.send_keys(Keys.ENTER)
            time.sleep(2)

            try:
                post_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Paylaş') or contains(text(), 'Post') or contains(text(), 'Publish')]")
                driver.execute_script("arguments[0].click();", post_button)
                time.sleep(2)
            except Exception:
                pass

            print(f"[{i+1}/{TOTAL_COMMENTS}] Yorum 3 Kişi Etiketlenerek POST EDİLDİ:\n -> {comment_text}")

        except Exception as e:
            print(f"[{i+1}/{TOTAL_COMMENTS}] Hata oluştu: {e}")

        # Spam Engeli Beklemesi (45-80sn)
        wait_time = random.randint(45, 80)
        print(f" -> Spam riski yememek için {wait_time} saniye bekleniyor...\n")
        time.sleep(wait_time)

    print("\n[BAŞARILI] 100 adet 3'lü etiketli yorum başarıyla post edildi!")
    input("\nKapatmak için ENTER'a basın...")

if __name__ == "__main__":
    instagram_3lu_post_botu()
