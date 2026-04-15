# BMT-408 Dönem Projesi

**Ad Soyad:** Kazybek Kulmatov
**Öğrenci No:** 21181616067
**E-posta:** kazybek.kulmatov@gazi.edu.tr

## Kurulum Adımları
1. AWS EC2 Ubuntu 24.04 LTS sunucusu oluşturuldu ve güvenlik duvarı (Security Group) yapılandırıldı.
2. Sunucu içi hardening işlemleri yapıldı (gazi kullanıcısı açıldı, root girişi kapatıldı, SSH key yetkilendirildi).
3. Gerekli paketler (Docker, Nginx, Ufw/Nftables) kuruldu.
4. Proje dosyaları sunucuya çekildi (`git clone`).
5. `docker compose up -d` komutu ile servisler ayağa kaldırıldı.

## Test Adımları
1. Tarayıcıdan `http://<SUNUCU_IP>` adresine gidildiğinde FastAPI uygulamasının çalıştığı doğrulanır.
2. `http://<SUNUCU_IP>/docs` adresine gidilerek Swagger UI üzerinden veritabanı CRUD işlemleri test edilebilir.
3. Cronjob ile yedekleme senaryosunun çalıştığı sunucu loglarından doğrulanır.

## Endpoint Listesi
* **GET `/health`** : Sistem sağlık durumu kontrolü.
* **POST `/items`** : Yeni kayıt ekleme (Create).
* **GET `/items`** : Tüm kayıtları listeleme (Read).
* **GET `/items/{id}`** : Belirli bir kaydı getirme.
* **PUT `/items/{id}`** : Kayıt güncelleme (Update).
* **DELETE `/items/{id}`** : Kayıt silme (Delete).
