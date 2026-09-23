# Hytale Optimizer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-555?style=for-the-badge" alt="Supported platforms" />
  <img src="https://img.shields.io/badge/Status-Experimental-orange?style=for-the-badge" alt="Experimental" />
</p>

<p align="center">
  <strong>Hytale asset optimization utilities</strong><br />
  <em>Hytale varlık dosyaları için optimizasyon araçları</em>
</p>

<p align="center">
  <a href="#english">English</a> •
  <a href="#türkçe">Türkçe</a>
</p>

---

<a id="english"></a>

## 🇬🇧 English

**Hytale Optimizer** is a collection of small, platform-independent Python utilities for modifying `Assets.zip`. The current tools focus on reducing unnecessary asset data and replacing music assets with a silent audio file.

> ⚠️ **Experimental software:** These scripts directly replace the original `Assets.zip`. Make a backup before running them. Use them at your own risk and verify the result after every Hytale update.

### ✨ Current features

- 🔎 Recursively searches for `Assets.zip` beside the scripts.
- 🧹 Minifies JSON-like files under `Server/` without alphabetically reordering keys.
- 🎵 Replaces `.ogg` files under `Common/Music/` with the bundled `Empty.ogg` file.
- 🧰 Uses a temporary archive in the target directory before replacing the original archive.
- 🖥️ Prints progress, errors, and a completion summary in the terminal.
- 🌍 Uses Python's standard library only; no third-party packages are currently required.

### 📁 Repository contents

| File | Purpose |
| --- | --- |
| [`assets_json_min.py`](assets_json_min.py) | Minifies `.json`, `.particlesystem`, and `.particlespawner` files under `Server/` inside `Assets.zip`. |
| [`assets_clear_music.py`](assets_clear_music.py) | Replaces `.ogg` files under `Common/Music/` with `Empty.ogg`. |
| [`Empty.ogg`](Empty.ogg) | Silent audio source used by the music replacement script. |

### ✅ Requirements

- Python **3.10 or newer**
- A writable Hytale asset directory
- An `Assets.zip` file located in the repository directory or one of its subdirectories
- A complete backup of the original asset archive

No `requirements.txt` file is needed at the moment because the scripts use only Python's built-in modules.

### 🚀 Installation

```bash
git clone https://github.com/Enjoyop2/Hytale-Optimizer.git
cd Hytale-Optimizer
python --version
```

### ▶️ Usage

Place the repository next to the Hytale installation, or ensure that the folder containing `Assets.zip` is inside the repository directory. Then run the desired script:

#### Minify server asset data

```bash
python assets_json_min.py
```

This processes matching files in the `Server/` path inside the archive. Invalid JSON files are left unchanged and reported in the terminal.

#### Silence music assets

```bash
python assets_clear_music.py
```

This replaces matching `.ogg` files in `Common/Music/` with the repository's `Empty.ogg` file.

### ⚠️ Important safety notes

1. Close Hytale before modifying its files.
2. Copy `Assets.zip` to a safe location before running either script.
3. The scripts replace the original archive after processing; the repository does **not** currently create a user-named backup automatically.
4. Restore your backup if Hytale fails to start or assets behave unexpectedly.
5. Hytale updates may change archive paths or file formats, so re-check the scripts after updates.
6. This project is not affiliated with or endorsed by Hytale or its rights holders.
7. The tools are intended for local asset management and accessibility/performance experimentation—not for bypassing anti-cheat or gaining an unfair advantage in online play.

### 🤝 Contributing

Issues and pull requests are welcome.

1. Fork the repository.
2. Create a focused branch.
3. Test against a copy of `Assets.zip`.
4. Document platform-specific behavior or limitations.
5. Open a pull request with a clear description of the change.

### 📄 License

No license has been declared yet. Until a license is added, all rights are reserved by the copyright holder.

---

<a id="türkçe"></a>

## 🇹🇷 Türkçe

**Hytale Optimizer**, `Assets.zip` dosyası üzerinde değişiklik yapmak için hazırlanmış, platform bağımsız küçük Python araçlarından oluşur. Mevcut araçlar gereksiz varlık verilerini azaltmaya ve müzik dosyalarını sessiz bir ses dosyasıyla değiştirmeye odaklanır.

> ⚠️ **Deneysel yazılım:** Scriptler orijinal `Assets.zip` dosyasını doğrudan değiştirir. Çalıştırmadan önce mutlaka yedek alın. Kullanım sorumluluğu size aittir ve her Hytale güncellemesinden sonra sonucu kontrol edin.

### ✨ Mevcut özellikler

- 🔎 Scriptlerin bulunduğu klasörde ve alt klasörlerde `Assets.zip` arar.
- 🧹 `Server/` altındaki JSON benzeri dosyaları anahtarları alfabetik olarak sıralamadan küçültür.
- 🎵 `Common/Music/` altındaki `.ogg` dosyalarını repodaki `Empty.ogg` ile değiştirir.
- 🧰 Orijinal arşivi değiştirmeden önce hedef klasörde geçici bir arşiv oluşturur.
- 🖥️ Terminalde ilerleme, hata ve işlem özeti gösterir.
- 🌍 Şu anda üçüncü taraf paket gerektirmez; yalnızca Python standart kütüphanesini kullanır.

### 📁 Depo içeriği

| Dosya | Açıklama |
| --- | --- |
| [`assets_json_min.py`](assets_json_min.py) | `Assets.zip` içindeki `Server/` klasöründe bulunan `.json`, `.particlesystem` ve `.particlespawner` dosyalarını küçültür. |
| [`assets_clear_music.py`](assets_clear_music.py) | `Common/Music/` altındaki `.ogg` dosyalarını `Empty.ogg` ile değiştirir. |
| [`Empty.ogg`](Empty.ogg) | Müzik değiştirme scriptinin kullandığı sessiz ses dosyasıdır. |

### ✅ Gereksinimler

- **Python 3.10 veya üzeri**
- Yazma izni olan bir Hytale varlık klasörü
- Repo klasöründe veya alt klasörlerinden birinde bulunan `Assets.zip`
- Orijinal arşivin eksiksiz bir yedeği

Scriptler yalnızca Python'ın yerleşik modüllerini kullandığı için şu an `requirements.txt` dosyasına ihtiyaç yoktur.

### 🚀 Kurulum

```bash
git clone https://github.com/Enjoyop2/Hytale-Optimizer.git
cd Hytale-Optimizer
python --version
```

### ▶️ Kullanım

Repo klasörünü Hytale kurulumu ile aynı konuma yerleştirin veya `Assets.zip` dosyasının repo klasörü içinde ya da bir alt klasörde olduğundan emin olun. Ardından istediğiniz scripti çalıştırın:

#### Sunucu varlıklarını küçültme

```bash
python assets_json_min.py
```

Arşiv içindeki `Server/` yoluyla eşleşen dosyaları işler. Geçersiz JSON dosyaları değiştirilmeden bırakılır ve terminalde raporlanır.

#### Müzik dosyalarını susturma

```bash
python assets_clear_music.py
```

`Common/Music/` altında bulunan eşleşen `.ogg` dosyalarını repodaki `Empty.ogg` ile değiştirir.

### ⚠️ Önemli güvenlik notları

1. Dosyaları değiştirmeden önce Hytale'ı kapatın.
2. Scriptleri çalıştırmadan önce `Assets.zip` dosyasını güvenli bir konuma kopyalayın.
3. Scriptler işlem sonunda orijinal arşivin yerine geçer; depo şu anda kullanıcı tarafından belirlenen otomatik bir yedek oluşturmaz.
4. Hytale başlatılamazsa veya varlıklarda sorun oluşursa yedeğinizi geri yükleyin.
5. Hytale güncellemeleri arşiv yollarını veya dosya biçimlerini değiştirebilir; güncellemelerden sonra scriptleri tekrar kontrol edin.
6. Bu proje Hytale veya hak sahipleriyle bağlantılı değildir ve onlar tarafından desteklenmez.
7. Araçlar yerel varlık yönetimi ve erişilebilirlik/performans denemeleri için tasarlanmıştır; anti-cheat sistemlerini aşmak veya çevrim içi oyunda haksız avantaj sağlamak amacı taşımaz.

### 🤝 Katkıda bulunma

Issue ve pull request'ler memnuniyetle karşılanır.

1. Repoyu fork edin.
2. Sadece ilgili değişikliği içeren bir branch oluşturun.
3. Testleri `Assets.zip` kopyası üzerinde yapın.
4. Platforma özel davranışları veya sınırlamaları belgeleyin.
5. Değişikliği açıklayan net bir pull request gönderin.

### 📄 Lisans

Henüz bir lisans belirtilmemiştir. Lisans eklenene kadar tüm haklar telif sahibine aittir.

---

<p align="center">
  <sub>Built for careful local experimentation with Hytale assets • Hytale varlıklarıyla dikkatli yerel denemeler için hazırlanmıştır</sub>
</p>
