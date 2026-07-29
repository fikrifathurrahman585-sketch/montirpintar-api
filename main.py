from fastapi import FastAPI
from pydantic import BaseModel
import requests
import numpy as np
import os

app = FastAPI(title="MontirPintar API Lite")

# Minta Vercel mengambilkan token dari brankas rahasia
HF_TOKEN = os.environ.get("HF_TOKEN")

# URL API Hugging Face yang benar menggunakan format /models/
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Database Kasus Bengkel
data_bengkel = [
    # ==============================
    # KATEGORI: MOBIL - KAKI-KAKI & KEMUDI (STEERING)
    # ==============================
    {"id": "MBL_KK_01", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Setir atau stir mobil terasa berat saat dibelokkan, kemudi kaku, dan ada bunyi dengung keras saat belok mentok.", "penyebab_utama": "Minyak power steering (hidrolik) habis/bocor, atau motor EPS bermasalah.", "solusi_perbaikan": "Cek kebocoran seal rack steer hidrolik. Jika tipe Elektrik (EPS), perbaiki modul/motor EPS.", "estimasi_biaya": "Rp 500.000 - Rp 3.500.000"},
    {"id": "MBL_KK_02", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Ada bunyi gluduk-gluduk, bletok, atau kasar dari bagian bawah ban saat lewat jalan rusak atau polisi tidur.", "penyebab_utama": "Bushing arm pecah, link stabilizer aus, ball joint oblak, atau karet support shock jebol.", "solusi_perbaikan": "Dongkrak mobil, periksa oblak pada roda. Ganti bushing arm / link stabilizer lalu wajib Spooring.", "estimasi_biaya": "Rp 400.000 - Rp 1.500.000"},
    {"id": "MBL_KK_03", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Setir atau stir getar hebat saat mobil melaju di kecepatan tinggi (di atas 80 km/jam) di jalan tol.", "penyebab_utama": "Roda tidak balance, velg peyang, atau ban sudah benjol/botak tidak rata.", "solusi_perbaikan": "Lakukan Balancing pada keempat roda. Jika velg peyang, lakukan press velg.", "estimasi_biaya": "Rp 100.000 - Rp 400.000"},
    {"id": "MBL_KK_04", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Ban mobil bagian dalam atau bagian luarnya botak duluan (makan sebelah / aus tidak rata).", "penyebab_utama": "Sudut roda (Camber/Toe) berantakan, tie rod bengkok, atau jarang di-spooring.", "solusi_perbaikan": "Perbaiki komponen kaki-kaki yang oblak (tie rod/long tie rod), kemudian wajib lakukan Spooring 3D.", "estimasi_biaya": "Rp 250.000 - Rp 800.000"},
    {"id": "MBL_KK_05", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Mobil terasa limbung, ngayun, atau mantul-mantul terus setelah melewati jalan bergelombang.", "penyebab_utama": "Shockbreaker (peredam kejut) mati, bocor keluar oli, atau per keong sudah lemah.", "solusi_perbaikan": "Ganti shockbreaker sepasang (kiri-kanan) agar seimbang.", "estimasi_biaya": "Rp 800.000 - Rp 2.500.000"},
    {"id": "MBL_KK_06", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Bunyi mendengung (ngiung) dari arah roda mobil saat jalan kencang, makin kencang makin berisik.", "penyebab_utama": "Bearing roda (lakher) sudah aus, kering, atau pelornya hancur.", "solusi_perbaikan": "Dongkrak ban dan putar. Ganti bearing roda yang mendengung (biasanya dipress hidrolik).", "estimasi_biaya": "Rp 300.000 - Rp 900.000"},

    # ==============================
    # KATEGORI: MOBIL - TRANSMISI & PENGGERAK
    # ==============================
    {"id": "MBL_TR_01", "kategori_kendaraan": "Mobil_Matic", "gejala_masalah": "Mobil matic terasa jedug, nyentak kasar, atau nabrak saat pindah/masuk gigi dari P ke D atau N ke R.", "penyebab_utama": "Oli transmisi (ATF/CVTF) sudah jelek, berkurang, body valve kotor, atau solenoid mampet.", "solusi_perbaikan": "Kuras/Flushing oli matic. Jika masih jedug, perlu scan ECU dan kalibrasi solenoid valve.", "estimasi_biaya": "Rp 800.000 - Rp 2.500.000"},
    {"id": "MBL_TR_02", "kategori_kendaraan": "Mobil_Manual", "gejala_masalah": "Mobil manual bau sangit, bau gosong, atau bau hangus dari kap mesin saat lewat tanjakan dan tenaga ngempos.", "penyebab_utama": "Kampas kopling (matahari/dekrup) gosong karena sering gantung kopling atau sudah tipis aus.", "solusi_perbaikan": "Turun transmisi, ganti plat kopling, dekrup, dan bearing release satu set.", "estimasi_biaya": "Rp 1.500.000 - Rp 3.500.000"},
    {"id": "MBL_TR_03", "kategori_kendaraan": "Mobil_Manual", "gejala_masalah": "Gigi persneling mobil manual susah masuk, kaku, alot, atau bunyi krek saat dioper.", "penyebab_utama": "Master kopling atas/bawah bocor, angin palsu di saluran kopling, atau sinkromes aus.", "solusi_perbaikan": "Cek kebocoran master kopling, bleeding minyak kopling. Jika aman, bongkar transmisi (sinkromes).", "estimasi_biaya": "Rp 300.000 - Rp 2.500.000"},
    {"id": "MBL_TR_04", "kategori_kendaraan": "Mobil_Matic", "gejala_masalah": "Mobil matic digas tapi ngempos tidak mau jalan (slip), rpm mesin naik tapi kecepatan tertahan.", "penyebab_utama": "Kampas kopling matic selip, oli transmisi sangat kotor (lumpur), atau seal pompa oli matic bocor.", "solusi_perbaikan": "Overhaul transmisi matic, ganti seal kit dan kampas matic, kuras oli CVT/ATF.", "estimasi_biaya": "Rp 3.500.000 - Rp 8.000.000"},
    {"id": "MBL_TR_05", "kategori_kendaraan": "Mobil_Kaki", "gejala_masalah": "Ada bunyi kletek-kletek berirama dari ban/roda depan saat mobil belok patah ke kanan atau kiri.", "penyebab_utama": "CV Joint (As Roda / Kokel) bagian luar (Outer) sudah aus atau pelornya hancur, karet boot sobek.", "solusi_perbaikan": "Ganti CV Joint luar, pastikan karet boot baru dan diberi gemuk (grease) khusus.", "estimasi_biaya": "Rp 400.000 - Rp 1.200.000"},
    {"id": "MBL_TR_06", "kategori_kendaraan": "Mobil_Matic", "gejala_masalah": "Tuas transmisi matic nyangkut, terkunci, susah digeser dari posisi P meskipun rem sudah diinjak.", "penyebab_utama": "Switch rem (brake switch) mati atau solenoid pengunci tuas transmisi rusak.", "solusi_perbaikan": "Gunakan tombol Shift Lock darurat. Bawa ke bengkel untuk ganti switch pedal rem atau solenoid tuas.", "estimasi_biaya": "Rp 100.000 - Rp 350.000"},
    {"id": "MBL_TR_07", "kategori_kendaraan": "Mobil_Penggerak", "gejala_masalah": "Ada bunyi dengung atau dengkur (ngiung) dari bagian bawah belakang mobil RWD saat lari kencang.", "penyebab_utama": "Gardan (Differential) kekurangan oli, oli gardan campur air, atau gear gardan sudah aus/rompal.", "solusi_perbaikan": "Kuras dan ganti oli gardan. Jika masih dengung, perlu setel ulang celah gigi gardan (backlash).", "estimasi_biaya": "Rp 250.000 - Rp 3.000.000"},

    # ==============================
    # KATEGORI: MOBIL - MESIN & KELISTRIKAN
    # ==============================
    {"id": "MBL_MS_01", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Mesin mobil brebet, nyendat-nyendat saat digas, pincang, dan tarikan berat.", "penyebab_utama": "Busi mati/lemah, koil pengapian bocor arus, atau filter bensin kotor (Fuel pump lemah).", "solusi_perbaikan": "Cek dan ganti busi satu set, periksa kebocoran arus koil, dan bersihkan injektor/filter bensin.", "estimasi_biaya": "Rp 250.000 - Rp 1.200.000"},
    {"id": "MBL_MS_02", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Mesin mobil ngelitik (suara tek-tek halus / kletek) saat nanjak atau digas (Engine Knocking).", "penyebab_utama": "Bahan bakar oktan rendah, ruang bakar banyak kerak karbon, atau timing pengapian tidak pas.", "solusi_perbaikan": "Lakukan Gurah Mesin (Carbon Clean), gunakan bensin oktan tinggi (Pertamax), dan bersihkan throttle.", "estimasi_biaya": "Rp 250.000 - Rp 500.000"},
    {"id": "MBL_MS_03", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Mesin mobil overheat (suhu indikator H naik drastis), ada uap panas atau air mendidih di kap mesin.", "penyebab_utama": "Air radiator habis/bocor, motor kipas (extra fan) mati, waterpump bocor, atau thermostat macet.", "solusi_perbaikan": "Ganti motor kipas radiator, cek kebocoran selang, ganti thermostat, dan isi cairan Coolant.", "estimasi_biaya": "Rp 400.000 - Rp 1.500.000"},
    {"id": "MBL_MS_04", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Mobil susah distarter saat pagi hari, suara dinamo lemah (ngek-ngek) tapi indikator dashboard nyala.", "penyebab_utama": "Aki (Accu) sudah tekor/soak/lemah, dinamo starter kotor arangnya, atau alternator tidak mengisi.", "solusi_perbaikan": "Jumper aki. Jika aki sudah lebih dari 2 tahun, ganti baru. Servis dinamo starter jika aki normal.", "estimasi_biaya": "Rp 700.000 - Rp 1.500.000"},
    {"id": "MBL_MS_05", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Lampu indikator Check Engine warna kuning menyala terus menerus di speedometer mobil.", "penyebab_utama": "Sensor O2 kotor/rusak, Mass Air Flow (MAF) sensor bermasalah, atau ada misfire di busi.", "solusi_perbaikan": "Wajib colok Scanner OBD2 di bengkel untuk membaca kode error, lalu bersihkan atau ganti sensor terkait.", "estimasi_biaya": "Rp 150.000 - Rp 1.500.000"},
    {"id": "MBL_MS_06", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "RPM mesin mobil naik turun sendiri saat AC nyala (hunting), idle gas tidak stabil, kadang mau mati.", "penyebab_utama": "Throttle body kotor, Idle Speed Control (ISC) bermasalah, atau ada selang vacuum bocor.", "solusi_perbaikan": "Bersihkan throttle body dan kalibrasi ulang ISC. Cek dan ganti karet selang vacuum yang getas.", "estimasi_biaya": "Rp 150.000 - Rp 350.000"},
    {"id": "MBL_MS_07", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Ada bunyi decit nyaring kencang (ciiiit) dari ruang mesin saat baru dihidupkan atau kena genangan air.", "penyebab_utama": "Fan belt / V-Belt alternator atau belt AC sudah kendur, kering, atau retak-retak.", "solusi_perbaikan": "Setel ketegangan tali kipas (belt) jika masih tebal. Jika sudah retak/getas, segera ganti baru.", "estimasi_biaya": "Rp 150.000 - Rp 350.000"},
    {"id": "MBL_MS_08", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Ada tetesan cairan oli warna hitam atau coklat di lantai garasi tepat di bawah mesin mobil.", "penyebab_utama": "Oli mesin bocor karena Seal Kruk As (Crankshaft) atau paking karter bak oli sudah getas/jebol.", "solusi_perbaikan": "Cari sumber rembes. Ganti seal kruk as (depan/belakang) atau lem ulang paking karter bak oli.", "estimasi_biaya": "Rp 300.000 - Rp 1.500.000"},
    {"id": "MBL_MS_09", "kategori_kendaraan": "Mobil_Mesin", "gejala_masalah": "Knalpot mobil mengeluarkan asap putih tebal (ngebul) saat mesin dipanaskan atau digas kencang.", "penyebab_utama": "Oli mesin ikut terbakar di ruang bakar karena ring piston baret, silinder aus, atau seal klep bocor.", "solusi_perbaikan": "Lakukan turun mesin (overhaul) setengah atau penuh. Ganti ring piston, cek blok silinder, ganti seal klep.", "estimasi_biaya": "Rp 3.000.000 - Rp 8.000.000"},

    # ==============================
    # KATEGORI: MOBIL - REM (BRAKE SYSTEM)
    # ==============================
    {"id": "MBL_RM_01", "kategori_kendaraan": "Mobil_Rem", "gejala_masalah": "Ada bunyi decit kencang (srek-srek / cicit) dari ban depan saat pedal rem mobil diinjak.", "penyebab_utama": "Kampas rem sudah sangat tipis bergesekan dengan plat, atau ada batu terjepit di cakram.", "solusi_perbaikan": "Segera ganti kampas rem depan (brake pad). Jika piringan cakram baret dalam, lakukan bubut cakram.", "estimasi_biaya": "Rp 250.000 - Rp 600.000"},
    {"id": "MBL_RM_02", "kategori_kendaraan": "Mobil_Rem", "gejala_masalah": "Pedal rem mobil terasa bergetar naik-turun atau ndut-ndutan saat diinjak di kecepatan tinggi.", "penyebab_utama": "Piringan cakram (Rotor) sudah melengkung, bergelombang karena panas, atau tipis tidak rata.", "solusi_perbaikan": "Lepas piringan cakram dan bawa ke tukang bubut (bubut on-car), atau ganti piringan cakram baru.", "estimasi_biaya": "Rp 350.000 - Rp 1.200.000"},
    {"id": "MBL_RM_03", "kategori_kendaraan": "Mobil_Rem", "gejala_masalah": "Pedal rem terasa dalam, ngempos, blong, atau harus dikocok berkali-kali baru bisa pakem.", "penyebab_utama": "Minyak rem bocor/habis, ada angin palsu terjebak di sistem rem, atau master rem sentral jebol.", "solusi_perbaikan": "Cari titik kebocoran di selang, ganti seal master rem, lalu lakukan bleeding (buang angin) minyak rem.", "estimasi_biaya": "Rp 200.000 - Rp 800.000"},
    {"id": "MBL_RM_04", "kategori_kendaraan": "Mobil_Rem", "gejala_masalah": "Rem mobil menarik atau membanting ke satu sisi (kiri atau kanan) saat pedal rem diinjak mendadak.", "penyebab_utama": "Piston kaliper rem macet di satu sisi, selang rem mampet, atau kampas rem aus tidak rata.", "solusi_perbaikan": "Bongkar dan bersihkan piston kaliper rem, lumasi pin slide kaliper dengan gemuk khusus rem.", "estimasi_biaya": "Rp 150.000 - Rp 350.000"},

    # ==============================
    # KATEGORI: MOBIL - AC (PENDINGIN)
    # ==============================
    {"id": "MBL_AC_01", "kategori_kendaraan": "Mobil_AC", "gejala_masalah": "AC mobil tidak dingin sama sekali, hanya keluar angin panas/biasa, siang hari terasa gerah.", "penyebab_utama": "Freon AC habis/bocor, magnetic clutch mati, atau motor kipas kondensor (extra fan) mati.", "solusi_perbaikan": "Cari kebocoran pakai air sabun, ganti part bocor, vakum instalasi, lalu isi ulang freon dan oli kompresor.", "estimasi_biaya": "Rp 350.000 - Rp 1.500.000"},
    {"id": "MBL_AC_02", "kategori_kendaraan": "Mobil_AC", "gejala_masalah": "AC mobil bau apek, asam, bau kecut, atau bau debu yang menyengat saat pertama kali dinyalakan.", "penyebab_utama": "Filter kabin AC kotor/berjamur, atau Evaporator sangat kotor dan berlendir menumpuk kuman.", "solusi_perbaikan": "Ganti filter kabin AC (di bawah dashboard). Lakukan cuci evaporator tanpa bongkar (AC bersin).", "estimasi_biaya": "Rp 150.000 - Rp 800.000"},
    {"id": "MBL_AC_03", "kategori_kendaraan": "Mobil_AC", "gejala_masalah": "Ada bunyi ngorok kasar (grok-grok) dari arah kap mesin yang muncul hanya saat AC dihidupkan.", "penyebab_utama": "Kompresor AC mulai aus, bearing kompresor oblak, atau oli kompresor sudah kering/habis.", "solusi_perbaikan": "Segera tambah oli kompresor (flushing) jika belum parah. Jika sudah jebol ngorok keras, ganti kompresor.", "estimasi_biaya": "Rp 500.000 - Rp 2.500.000"},

    # ==============================
    # KATEGORI: MOTOR - KAKI-KAKI, KEMUDI & REM
    # ==============================
    {"id": "MTR_KK_01", "kategori_kendaraan": "Motor_Kaki", "gejala_masalah": "Stang, stir, atau kemudi motor terasa berat sebelah, kaku susah dibelokkan, atau bunyi jeglek saat direm.", "penyebab_utama": "Komstir (steering cone) aus, kendor, oblak, atau pelor bearing komstir ada yang hancur.", "solusi_perbaikan": "Bongkar body depan, setel ulang/kencangkan komstir. Jika mangkok/pelor aus baret, ganti komstir baru.", "estimasi_biaya": "Rp 150.000 - Rp 350.000"},
    {"id": "MTR_KK_02", "kategori_kendaraan": "Motor_Kaki", "gejala_masalah": "Shockbreaker (shock) depan motor terasa sangat keras mentok nabrak besi atau bocor keluar oli.", "penyebab_utama": "Seal shock bocor sehingga oli habis kering, per patah, atau as shock baret/bengkok.", "solusi_perbaikan": "Bongkar shock depan, ganti seal shock, kuras dan isi ulang oli shockbreaker sesuai takaran pabrik.", "estimasi_biaya": "Rp 80.000 - Rp 200.000"},
    {"id": "MTR_KK_03", "kategori_kendaraan": "Motor_Kaki", "gejala_masalah": "Ban motor belakang terasa goyang, geol-geol, oleng, atau megal-megol saat jalan di kecepatan lambat/sedang.", "penyebab_utama": "Bearing (lakher) roda belakang hancur/oblak, ban benjol, atau velg peyang habis hajar lubang.", "solusi_perbaikan": "Dongkrak tengah, goyangkan roda. Ganti bearing (lakher) roda dan cek alur ban/velg.", "estimasi_biaya": "Rp 50.000 - Rp 150.000"},
    {"id": "MTR_KK_04", "kategori_kendaraan": "Motor_Kaki", "gejala_masalah": "Saat motor boncengan, bagian belakang terasa mentok (amblas) dan tidak mantul empuk, terasa keras.", "penyebab_utama": "Shockbreaker belakang (Monoshock/Dualshock) bocor, sil pecah, atau per-nya sudah mati/lemah.", "solusi_perbaikan": "Suntik ulang oli shock belakang (rekondisi) atau ganti shockbreaker tabung yang baru.", "estimasi_biaya": "Rp 250.000 - Rp 600.000"},
    {"id": "MTR_RM_01", "kategori_kendaraan": "Motor_Rem", "gejala_masalah": "Roda motor terasa seret putarannya berat, rem cakram depan mengunci dan velg cepat panas.", "penyebab_utama": "Piston kaliper rem macet tidak balik karena karat/kotoran lumpur, atau master rem mampet.", "solusi_perbaikan": "Bongkar kaliper rem, bersihkan piston dari karat dengan amplas halus, lumasi pakai stempel/gemuk khusus.", "estimasi_biaya": "Rp 50.000 - Rp 100.000"},
    {"id": "MTR_RM_02", "kategori_kendaraan": "Motor_Rem", "gejala_masalah": "Saat ngerem depan/belakang (cakram), tuas rem motor terasa berdenyut, membal, atau bergetar ke tangan.", "penyebab_utama": "Piringan cakram (Disk Brake) sudah bengkok/bergelombang akibat suhu panas ekstrem (disiram saat panas).", "solusi_perbaikan": "Cek ketebalan cakram, jika masih tebal bisa dipress/bubut. Jika sudah tipis parah, wajib ganti piringan cakram.", "estimasi_biaya": "Rp 150.000 - Rp 300.000"},

    # ==============================
    # KATEGORI: MOTOR - MATIC (CVT)
    # ==============================
    {"id": "MTR_CV_01", "kategori_kendaraan": "Motor_Matic", "gejala_masalah": "Tarikan awal motor matic terasa gredek parah, bergetar kencang dari blok CVT saat selongsong gas baru ditarik.", "penyebab_utama": "Mangkok kampas ganda kotor penuh debu, kampas ganda tipis/slip, atau karet dumper aus.", "solusi_perbaikan": "Servis CVT rutin, bersihkan mangkok ganda. Bisa lakukan modif kartel tipis pada mangkok/bolongi mangkok.", "estimasi_biaya": "Rp 50.000 - Rp 250.000"},
    {"id": "MTR_CV_02", "kategori_kendaraan": "Motor_Matic", "gejala_masalah": "Tenaga motor matic ngempos, gas ditarik putaran tinggi meraung tapi lari motor pelan/kecepatan tertahan.", "penyebab_utama": "V-Belt sudah retak, mulur, aus, atau roller sudah gepeng/peyang. Bisa juga per CVT lembek.", "solusi_perbaikan": "Buka blok CVT. Ganti V-Belt dan Roller satu set original. Cek juga tingkat keausan pully depan.", "estimasi_biaya": "Rp 150.000 - Rp 350.000"},
    {"id": "MTR_CV_03", "kategori_kendaraan": "Motor_Matic", "gejala_masalah": "Ada suara klotok-klotok, tek-tek kasar di bagian CVT saat motor langsam (idle), hilang halus saat digas.", "penyebab_utama": "Slider piece (karet bantalan tutup rumah roller) sudah longgar/aus atau rumah roller oblak parah.", "solusi_perbaikan": "Ganti karet slider piece (murah). Jika tiang rumah roller (drive pulley) aus, ganti rumah roller assy.", "estimasi_biaya": "Rp 35.000 - Rp 250.000"},
    {"id": "MTR_CV_04", "kategori_kendaraan": "Motor_Matic", "gejala_masalah": "Bunyi mendesing bersiul seperti suara pesawat terbang (ngiiing) dari area roda belakang saat motor jalan kencang.", "penyebab_utama": "Bearing rasio (gigi transmisi) di dalam gearbox gardan aus beradu, atau oli gardan habis/tercampur air banjir.", "solusi_perbaikan": "Bongkar gearbox belakang, ganti bearing rasio yang rusak, dan kuras oli gardan baru.", "estimasi_biaya": "Rp 150.000 - Rp 350.000"},
    {"id": "MTR_CV_05", "kategori_kendaraan": "Motor_Matic", "gejala_masalah": "Motor matic tiba-tiba mati total di tengah jalan, tidak bisa jalan sama sekali, terdengar suara tarikan lepas.", "penyebab_utama": "V-Belt CVT putus total di dalam blok karena sudah terlalu aus dan lama tidak diganti.", "solusi_perbaikan": "Panggil bengkel terdekat, bongkar blok CVT, bersihkan sisa serpihan karet, lalu pasang V-belt baru.", "estimasi_biaya": "Rp 200.000 - Rp 400.000"},

    # ==============================
    # KATEGORI: MOTOR - MESIN & KELISTRIKAN
    # ==============================
    {"id": "MTR_MS_01", "kategori_kendaraan": "Motor_Mesin", "gejala_masalah": "Knalpot motor mengeluarkan asap putih tipis atau tebal secara terus menerus (ngebul).", "penyebab_utama": "Oli mesin lolos masuk ke ruang bakar. Ring piston baret, dinding silinder (boring) aus, atau seal klep bocor.", "solusi_perbaikan": "Lakukan turun mesin atas (Korter/Bore up). Ganti ring piston, piston kit, dan pasang seal klep baru.", "estimasi_biaya": "Rp 800.000 - Rp 1.500.000"},
    {"id": "MTR_MS_02", "kategori_kendaraan": "Motor_Mesin", "gejala_masalah": "Suara mesin motor bunyi tek-tek-tek berisik dan kasar mirip mesin jahit saat posisi langsam/idle.", "penyebab_utama": "Setelan celah klep (valve clearance) terlalu renggang, atau rantai keteng (cam chain) kendor/aus.", "solusi_perbaikan": "Bongkar head, setel ulang celah klep pakai filler gauge. Jika rantai keteng aus, ganti rantai keteng+tensionernya.", "estimasi_biaya": "Rp 50.000 - Rp 300.000"},
    {"id": "MTR_MS_03", "kategori_kendaraan": "Motor_Mesin", "gejala_masalah": "Knalpot motor sering nembak-nembak (dor-dor) saat turun gas, mbrebet, dan boros bensin.", "penyebab_utama": "Knalpot bocor di bagian leher paking, busi mau mati, atau setelan injeksi/karbu kotor (campuran udara miskin).", "solusi_perbaikan": "Ganti paking leher knalpot, bersihkan karburator / injektor, dan cek kebersihan filter udara.", "estimasi_biaya": "Rp 50.000 - Rp 150.000"},
    {"id": "MTR_MS_04", "kategori_kendaraan": "Motor_Mesin", "gejala_masalah": "Motor sering mati mendadak saat berhenti di lampu merah atau saat rpm diturunkan (tidak bisa langsam).", "penyebab_utama": "Setelan klep terlalu rapat, busi lemah, throttle body sangat kotor, atau sensor IACV kotor/mati.", "solusi_perbaikan": "Bongkar head silinder, kalibrasi ulang setelan klep, semprot pembersih (injector cleaner) ke throttle body.", "estimasi_biaya": "Rp 75.000 - Rp 200.000"},
    {"id": "MTR_MS_05", "kategori_kendaraan": "Motor_Manual", "gejala_masalah": "Gigi persneling motor manual susah dioper (keras), netralnya alot, dan tarikan kopling selip.", "penyebab_utama": "Kampas kopling (clutch plate) sudah tipis, plat gesek hangus terbakar, atau kabel kopling berkarat.", "solusi_perbaikan": "Bongkar bak kopling, ganti kampas kopling satu set. Cek per kopling, lumasi/ganti kabel kopling yang seret.", "estimasi_biaya": "Rp 150.000 - Rp 450.000"},
    {"id": "MTR_MS_06", "kategori_kendaraan": "Motor_Mesin", "gejala_masalah": "Oli mesin motor (terutama motor radiator) tiba-tiba berubah warna menjadi keputihan seperti susu (kopi susu).", "penyebab_utama": "Air radiator bocor dan menyebrang masuk ke ruang mesin akibat Seal Waterpump jebol.", "solusi_perbaikan": "Segera bongkar, ganti seal waterpump satu set, kuras (flushing) oli mesin 2-3 kali sampai bersih total dari air.", "estimasi_biaya": "Rp 250.000 - Rp 500.000"},
    {"id": "MTR_KL_01", "kategori_kendaraan": "Motor_Kelistrikan", "gejala_masalah": "Tombol stater ditekan cuma bunyi cetek-cetek, dinamo starter diam tidak mau muter menghidupkan mesin.", "penyebab_utama": "Aki drop, atau Bendik Starter (Relay Starter) sudah konslet/mati/kotor dalamnya.", "solusi_perbaikan": "Cek tegangan aki. Jika aki sehat normal (12V), masalah fix ada di Bendik Starter. Ganti bendik baru.", "estimasi_biaya": "Rp 60.000 - Rp 150.000"},
    {"id": "MTR_KL_02", "kategori_kendaraan": "Motor_Kelistrikan", "gejala_masalah": "Aki motor selalu tekor dan ngedrop terus meskipun aki tersebut baru saja diganti dengan yang baru.", "penyebab_utama": "Kiprok (Regulator/Rectifier) mati, atau spul motor gosong/putus sehingga tidak ada arus pengisian ke aki.", "solusi_perbaikan": "Cek voltase aki saat mesin digas, jika angka tidak naik ke 13.5V - 14V berarti pengisian mati. Ganti kiprok/spul.", "estimasi_biaya": "Rp 150.000 - Rp 400.000"},
    {"id": "MTR_KL_03", "kategori_kendaraan": "Motor_Kelistrikan", "gejala_masalah": "Motor mati mendadak di jalan atau lampu merah, tombol stater ditekan cuma bunyi cetek-cetek, dinamo starter diam tidak mau muter, dan klakson nyala redup.", "penyebab_utama": "Aki drop, atau Bendik Starter (Relay Starter) sudah konslet/mati/kotor dalamnya.", "solusi_perbaikan": "Cek tegangan aki. Jika aki sehat normal (12V), masalah fix ada di Bendik Starter. Ganti bendik baru.", "estimasi_biaya": "Rp 60.000 - Rp 150.000"},
]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}
GLOBAL_EMBEDDINGS = None

def get_embedding(text_list):
    response = requests.post(API_URL, headers=headers, json={"inputs": text_list})
    if response.status_code == 200:
        return np.array(response.json())
    else:
        raise Exception(f"Gagal memanggil HF API: {response.text}")

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class KeluhanInput(BaseModel):
    keluhan: str

@app.get("/")
def home():
    return {"status": "aktif", "pesan": "Server MontirPintar siap melayani!"}

@app.post("/diagnosa")
def diagnosa_ai(data: KeluhanInput):
    global GLOBAL_EMBEDDINGS
    try:
        if GLOBAL_EMBEDDINGS is None:
            gejala_list = [item["gejala_masalah"] for item in data_bengkel]
            GLOBAL_EMBEDDINGS = get_embedding(gejala_list)

        input_embedding = get_embedding([data.keluhan])[0]
        
        best_match_idx = -1
        best_score = -1.0
        
        for i, db_emb in enumerate(GLOBAL_EMBEDDINGS):
            score = cos_sim(input_embedding, db_emb)
            if score > best_score:
                best_score = score
                best_match_idx = i
                
        if best_score > 0.4:
            hasil = data_bengkel[best_match_idx]
            return {
                "status": "success",
                # 🛠️ DISESUAIKAN DENGAN KEY DIATAS ("penyebab_utama" & "solusi_perbaikan")
                "diagnosa_ai": hasil["penyebab_utama"],
                "solusi": hasil["solusi_perbaikan"],
                "estimasi_biaya": hasil["estimasi_biaya"],
                "akurasi": round(float(best_score) * 100, 2)
            }
        else:
            return {"status": "error", "pesan": "Keluhan belum dikenali."}
            
    except Exception as e:
        return {"status": "error", "pesan": str(e)}

@app.post("/lapor_error")
def lapor_error(data: dict):
    return {"status": "success"}
