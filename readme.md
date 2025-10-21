Sistem otorisasi berbasis Flask yang mengimplementasikan Role-Based Access Control (RBAC) dengan JWT Authentication.
Proyek ini dikembangkan untuk memenuhi tugas Automatic Learning Project (ALP) pada topik Demo Sistem Otorisasi.

🚀 Fitur Utama
🔐 Login Sistem menggunakan username dan password
🧾 Akses Dokumen berdasarkan peran pengguna (Admin / User)
⚙️ JWT Authentication untuk keamanan API
🚫 Middleware Authorization untuk memvalidasi token dan hak akses
🌐 Frontend UI sederhana (HTML + Bootstrap)
🧠 Aturan Access Policy berbasis peran dan atribut pengguna
🧱 Struktur Folder

⚖️ Daftar Access Policy
Role	Resource	Action	Condition / Attribute
Admin	/api/documents	GET, POST, DEL	Semua dokumen diizinkan
User	/api/documents	GET	Hanya dokumen miliknya
User	/api/documents	POST	Tidak diizinkan
Guest	/api/login	POST	Hanya untuk autentikasi awal

💻 Cara Menjalankan Proyek
1️⃣ Clone Repository
git clone https://github.com/username/alp-otorisasi.git
cd alp-otorisasi

2️⃣ Buat Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependensi
pip install -r requirements.txt

4️⃣ Jalankan Aplikasi
flask run --app app --debug

5️⃣ Akses di Browser
Buka: 👉 http://127.0.0.1:5000

🧠 Teknologi yang Digunakan
Python 3.12
Flask
Flask-JWT-Extended
HTML, CSS (Bootstrap)
SQLite
