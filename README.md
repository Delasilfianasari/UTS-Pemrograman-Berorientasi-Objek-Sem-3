# UTS Pemrograman Berorientasi Objek

## Identitas
- NIM: ISI_NIM_ANDA
- Nama: ISI_NAMA_ANDA
- Link GitHub: ISI_LINK_REPOSITORY_ANDA

## Deskripsi
Program Python berbasis OOP untuk membaca dan memproses `employee.json` serta `sensor_logs.json`.

## Struktur
- `main.py`: kelas OOP, aturan bisnis, dan laporan.
- `employee.json`: data karyawan.
- `sensor_logs.json`: data pembacaan sensor.

## Konsep OOP
1. **Inheritance**: `PermanentEmployee` dan `ContractEmployee` mewarisi `Employee`; kelas-kelas sensor mewarisi `Sensor`.
2. **Polymorphism**: `display()` dipanggil pada objek berbeda dan hasilnya mengikuti jenis objek.
3. **Override**: subclass mengubah implementasi `display()`; `ContractEmployee` juga mengubah `calculate_bonus()`.
4. **Rule**:
   - Bonus `PERF2026` = 10% dari gaji pokok.
   - Bonus `SENIOR10` = 10% dari gaji pokok.
   - Bonus `LEAD2026` = 15% dari gaji pokok.
   - Karyawan nonpermanen tidak memperoleh bonus.
   - Status suhu: NORMAL < 60°C; WARNING 60°C sampai kurang dari 85°C; DANGER >= 85°C.
   - Status hasil rule dibandingkan dengan status yang tersimpan pada JSON.
5. **Abstract class**: `Employee` dan `Sensor` menggunakan `ABC` serta `abstractmethod`.

## Cara menjalankan
Pastikan Python 3 sudah terpasang. Buka terminal pada folder proyek, lalu jalankan:

```bash
python main.py
```

Jika perintah tersebut tidak bekerja pada Windows, coba:

```bash
py main.py
```

File JSON harus berada dalam folder yang sama dengan `main.py`.

## Catatan asumsi
Soal menyediakan kode bonus tetapi tidak menjelaskan nilai persentase bonus. Program menggunakan asumsi yang ditulis di atas; sesuaikan jika dosen memberikan rule bonus khusus.
