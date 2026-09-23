# Hytale-Optimizer

Hytale için platform bağımsız optimizasyon araçları.

Bu proje, oyun dosyalarını daha düşük RAM kullanımı ve daha iyi performans hedefiyle düzenlemeye yardımcı olan Python scriptleri içerir.

> **Durum:** Geliştirme aşamasında. Scriptleri çalıştırmadan önce oyun dosyalarınızın yedeğini alın.

## Özellikler

- Windows, Linux ve macOS üzerinde çalışabilecek Python tabanlı araçlar
- Oyun dosyalarını yedekleyerek güvenli düzenleme yaklaşımı
- Daha düşük RAM kullanımını hedefleyen yapılandırma optimizasyonları
- Geri alınabilir değişiklikler
- Komut satırı üzerinden kolay kullanım

## Gereksinimler

- Python 3.10 veya üzeri
- Hytale'ın kurulu olması
- Oyun dosyalarında değişiklik yapabilmek için gerekli dosya izinleri

## Kurulum

```bash
git clone https://github.com/Enjoyop2/Hytale-Optimizer.git
cd Hytale-Optimizer
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Gerekli bağımlılıklar eklendiğinde:

```bash
python -m pip install -r requirements.txt
```

## Kullanım

Scriptler hazırlandıktan sonra genel kullanım örneği:

```bash
python scripts/optimize.py --backup
```

Kullanılabilir seçenekleri görmek için:

```bash
python scripts/optimize.py --help
```

> Script adı ve seçenekleri proje geliştikçe güncellenecektir. Mevcut scriptler için `scripts/` klasörünü inceleyin.

## Güvenlik ve yedekleme

- Optimizasyon işleminden önce oyun klasörünün yedeğini alın.
- Scriptleri yalnızca güvendiğiniz kaynaklardan edinin.
- Oyun güncellemelerinden sonra yapılandırma dosyalarının formatı değişebileceği için optimizasyonu yeniden kontrol edin.
- Bu proje Hytale veya ilgili hak sahipleriyle bağlantılı değildir.
- Scriptlerin çevrim içi oyunlarda haksız avantaj sağlamak veya anti-cheat sistemlerini aşmak için kullanılması amaçlanmaz.

## Katkıda bulunma

Katkılar memnuniyetle karşılanır. Değişiklik öncesinde bir issue açabilir veya pull request gönderebilirsiniz.

1. Repoyu fork edin.
2. Yeni bir branch oluşturun.
3. Değişikliklerinizi ve testlerinizi ekleyin.
4. Pull request gönderin.

## Lisans

Lisans daha sonra belirlenecektir.
