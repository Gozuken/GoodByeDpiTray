# GoodByeDPI Tray

GoodbyeDPI'yi sistem tepsi alanında (system tray) çalıştırarak arka planda yönetmenizi sağlayan basit bir Windows uygulaması.

## Özellikler

- GoodbyeDPI'yi otomatik olarak arka planda başlatır (varsayılan: TTL 3)
- Sistem tepsisinde simge olarak gösterilir, durum (çalışıyor/durdu) ipucunda görünür
- **Mod Seçimi:** Sağ tık menüsünden farklı GoodbyeDPI modları arasında geçiş yapabilirsiniz (TTL 3/7, Auto TTL, Fake-SND, Desync, Disorder)
- **Başlat / Durdur / Yeniden Başlat** kontrolleri sağ tık menüsünden yapılabilir
- Tek instance kontrolü (çift çalışmayı engeller)
- Konsol penceresi açılmaz

## Kullanım

1. [GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI) indirip `.exe` dosyasını bu uygulamanın bulunduğu klasöre koyun
2. `goodbyedpiTray.exe` dosyasını çalıştırın
3. Sağ tık menüsünden "Çıkış" ile kapatabilirsiniz

## Gereksinimler

- Windows 10/11
- [GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI) (`goodbyedpi.exe`)

## Geliştirme

Geliştirme ortamı için gerekli paketler:

```bash
pip install pystray Pillow
```

PyInstaller ile `.exe` oluşturmak için:

```bash
pyinstaller goodbyedpiTray.spec
```

## Lisans

[MIT](LICENSE)
