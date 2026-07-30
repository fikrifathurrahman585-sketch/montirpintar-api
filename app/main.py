from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import difflib
import logging
import os
import requests

# Konfigurasi Logging Server
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MontirPintarAPI")

app = FastAPI(title="MontirPintar API Global Enterprise")

# =====================================================================
# DATABASE KASUS BENGKEL BILINGUAL (LENGKAP & USER-CENTRIC)
# =====================================================================
data_bengkel = [
    # ==============================
    # KATEGORI: MOBIL - KAKI-KAKI & KEMUDI (STEERING)
    # ==============================
    {
        "id": "MBL_KK_01",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Setir atau stir mobil terasa berat saat dibelokkan, kemudi kaku, dan ada bunyi dengung keras saat belok mentok.",
        "masalah_id": "Minyak power steering hidrolik habis atau bocor, atau motor EPS (Electric Power Steering) mengalami gangguan.",
        "tindakan_id": "Jangan paksakan memutar setir saat parkir tanpa tenaga mesin menyala agar tidak merusak komponen.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek selang dan seal power steering apakah ada yang bocor, atau cek sekring dan modul EPS-nya.'",
        "gejala_en": "Steering wheel feels heavy when turning, stiff steering, and loud humming noise when turned to full lock.",
        "masalah_en": "Hydraulic power steering fluid is low/leaking, or the EPS motor is malfunctioning.",
        "tindakan_en": "Avoid forcing the steering wheel when parked without the engine running to prevent further damage.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the hydraulic hoses and seals for leaks, or inspect the EPS fuse and module.'",
        "estimasi_biaya": "Rp 500.000 - Rp 3.500.000 | $35 - $220"
    },
    {
        "id": "MBL_KK_02",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Ada bunyi gluduk-gluduk, bletok, atau kasar dari bagian bawah ban saat lewat jalan rusak atau polisi tidur.",
        "masalah_id": "Komponen kaki-kaki aus, seperti bushing arm pecah, link stabilizer aus, ball joint oblak, atau karet support shock jebol.",
        "tindakan_id": "Kurangi kecepatan secara drastis saat melintasi jalan berlubang atau polisi tidur.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong dongkrak mobilnya, cek bagian bushing arm, link stabilizer, dan ball joint mana yang sudah oblak.'",
        "gejala_en": "Clunking or knocking noises from the lower front wheels when driving over rough roads or speed bumps.",
        "masalah_en": "Worn suspension parts such as cracked arm bushings, worn stabilizer links, loose ball joints, or broken shock mounts.",
        "tindakan_en": "Reduce speed significantly when passing over potholes or speed bumps.",
        "tips_bengkel_en": "Tell the mechanic: 'Please jack up the car and inspect the bushing arms, stabilizer links, and ball joints for play.'",
        "estimasi_biaya": "Rp 400.000 - Rp 1.500.000 | $25 - $100"
    },
    {
        "id": "MBL_KK_03",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Setir atau stir getar hebat saat mobil melaju di kecepatan tinggi (di atas 80 km/jam) di jalan tol.",
        "masalah_id": "Roda tidak balance, velg peyang, atau ban sudah benjol dan botak tidak rata.",
        "tindakan_id": "Turunkan kecepatan kendaraan di bawah 80 km/jam demi keselamatan berkendara di jalan tol.",
        "tips_bengkel_id": "Sampaikan ke bengkel ban: 'Tolong lakukan balancing keempat roda dan cek apakah ada velg yang peyang.'",
        "gejala_en": "Steering wheel shakes violently when driving at high speeds (above 80 km/h) on the highway.",
        "masalah_en": "Unbalanced wheels, bent rims, or unevenly worn/bulged tires.",
        "tindakan_en": "Reduce speed below 80 km/h for safety while driving on the highway.",
        "tips_bengkel_en": "Tell the tire shop: 'Please perform wheel balancing on all four wheels and check if any rims are bent.'",
        "estimasi_biaya": "Rp 100.000 - Rp 400.000 | $7 - $25"
    },
    {
        "id": "MBL_KK_04",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Ban mobil bagian dalam atau bagian luarnya botak duluan (makan sebelah / aus tidak rata).",
        "masalah_id": "Sudut roda (Camber/Toe) berantakan, tie rod bengkok, atau jarang melakukan spooring.",
        "tindakan_id": "Segera jadwalkan penyetelan kaki-kaki agar ban tidak semakin parah ausnya.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek tie rod dan long tie rod, lalu lakukan Spooring 3D presisi.'",
        "gejala_en": "Car tires are balding unevenly on the inner or outer edges (uneven wear).",
        "masalah_en": "Misaligned wheel angles (Camber/Toe), bent tie rods, or lack of regular wheel alignment.",
        "tindakan_en": "Schedule a suspension adjustment soon to prevent further tire wear.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the tie rods and perform a 3D wheel alignment (spooring).'",
        "estimasi_biaya": "Rp 250.000 - Rp 800.000 | $15 - $50"
    },
    {
        "id": "MBL_KK_05",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Mobil terasa limbung, ngayun, atau mantul-mantul terus setelah melewati jalan bergelombang.",
        "masalah_id": "Shockbreaker (peredam kejut) sudah mati, bocor keluar oli, atau per keong melemah.",
        "tindakan_id": "Waspada saat menikung tajam karena mobil kurang stabil dan mudah limbung.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek kondisi shockbreaker depan dan belakang, sepertinya sudah mati dan perlu diganti sepasang.'",
        "gejala_en": "The car feels floaty, bounces excessively, or rocks after passing over bumps or undulating roads.",
        "masalah_en": "Worn out or leaking shock absorbers, or weakened coil springs.",
        "tindakan_en": "Drive cautiously around sharp turns as vehicle stability is reduced.",
        "tips_bengkel_en": "Tell the mechanic: 'Please inspect the front and rear shock absorbers; they seem dead and need pair replacement.'",
        "estimasi_biaya": "Rp 800.000 - Rp 2.500.000 | $50 - $160"
    },
    {
        "id": "MBL_KK_06",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Bunyi mendengung (ngiung) dari arah roda mobil saat jalan kencang, makin kencang makin berisik.",
        "masalah_id": "Bearing roda (lakher) sudah aus, kering, atau pelor di dalamnya hancur.",
        "tindakan_id": "Hindari perjalanan jauh berkecepatan tinggi karena bearing roda yang hancur bisa mengunci.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong dongkrak dan putar roda untuk mengecek bearing roda mana yang berdengung, lalu press ganti baru.'",
        "gejala_en": "A humming or whining noise coming from the wheels when driving fast, getting louder with speed.",
        "masalah_en": "Wheel bearings are worn out, dry, or damaged internally.",
        "tindakan_en": "Avoid long high-speed trips as a failed wheel bearing can seize up.",
        "tips_bengkel_en": "Tell the mechanic: 'Please jack up and spin the wheels to identify the noisy bearing, then press in a new one.'",
        "estimasi_biaya": "Rp 300.000 - Rp 900.000 | $20 - $60"
    },

    # ==============================
    # KATEGORI: MOBIL - TRANSMISI & PENGGERAK
    # ==============================
    {
        "id": "MBL_TR_01",
        "kategori_kendaraan": "Mobil_Matic",
        "gejala_id": "Mobil matic terasa jedug, nyentak kasar, atau nabrak saat pindah/masuk gigi dari P ke D atau N ke R.",
        "masalah_id": "Kualitas oli transmisi (ATF/CVTF) sudah jelek/berkurang, atau body valve kotor dan solenoid mampet.",
        "tindakan_id": "Kendarai mobil dengan pelan dan halus, hindari menginjak gas secara spontan atau kasar.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Mas, maticnya jedug, tolong cek kualitas oli matic-nya dulu, apakah cukup dikuras (flushing) atau perlu scan ECU.'",
        "gejala_en": "Automatic transmission jerks, shifts roughly, or clunks when shifting from P to D or N to R.",
        "masalah_en": "Degraded or low transmission fluid, dirty valve body, or clogged solenoid valves.",
        "tindakan_en": "Drive gently and avoid sudden acceleration.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the transmission fluid quality first, whether it needs flushing or an ECU scan.'",
        "estimasi_biaya": "Rp 800.000 - Rp 2.500.000 | $50 - $160"
    },
    {
        "id": "MBL_TR_02",
        "kategori_kendaraan": "Mobil_Manual",
        "gejala_id": "Mobil manual bau sangit, bau gosong, atau bau hangus dari kap mesin saat lewat tanjakan dan tenaga ngempos.",
        "masalah_id": "Kampas kopling (matahari/dekrup) gosong karena sering gantung kopling atau sudah tipis aus.",
        "tindakan_id": "Jangan dipaksa menanjak curam atau membawa beban berat agar mobil tidak kehilangan tenaga total.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Sepertinya kampas kopling saya habis atau gosong, tolong turun transmisi dan ganti satu set.'",
        "gejala_en": "Manual car smells burnt or emits a scorched odor from the engine bay on steep hills with weak acceleration.",
        "masalah_en": "Clutch disc and pressure plate are burnt due to clutch slipping or normal wear and tear.",
        "tindakan_en": "Avoid steep hills or heavy loads to prevent total power loss.",
        "tips_bengkel_en": "Tell the mechanic: 'The clutch seems burned; please drop the transmission and replace the clutch set.'",
        "estimasi_biaya": "Rp 1.500.000 - Rp 3.500.000 | $100 - $230"
    },
    {
        "id": "MBL_TR_03",
        "kategori_kendaraan": "Mobil_Manual",
        "gejala_id": "Gigi persneling mobil manual susah masuk, kaku, alot, atau bunyi krek saat dioper.",
        "masalah_id": "Master kopling atas atau bawah bocor, ada angin palsu di saluran kopling, atau sinkromes aus.",
        "tindakan_id": "Injak pedal kopling secara penuh hingga ke lantai saat hendak memindahkan gigi persneling.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek master kopling dan lakukan bleeding minyak kopling, atau periksa sinkromes transmisi.'",
        "gejala_en": "Manual transmission gears are hard to shift, stiff, rigid, or make a crunching sound when shifting.",
        "masalah_en": "Leaking upper/lower clutch master cylinders, air in the clutch lines, or worn synchronizers.",
        "tindakan_en": "Press the clutch pedal fully to the floor when shifting gears.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the clutch master cylinders, bleed the clutch fluid, or inspect the synchronizers.'",
        "estimasi_biaya": "Rp 300.000 - Rp 2.500.000 | $20 - $160"
    },
    {
        "id": "MBL_TR_04",
        "kategori_kendaraan": "Mobil_Matic",
        "gejala_id": "Mobil matic digas tapi ngempos tidak mau jalan (slip), rpm mesin naik tapi kecepatan tertahan.",
        "masalah_id": "Kampas kopling matic selip, oli transmisi sangat kotor (lumpur), atau seal pompa oli matic bocor.",
        "tindakan_id": "Jangan memaksa menginjak gas dalam-dalam karena akan memperparah keausan komponen internal transmisi.",
        "tips_bengkel_id": "Sampaikan ke spesialis matic: 'Mobil matic saya slip dan ngempos, tolong cek apakah perlu overhaul transmisi matic.'",
        "gejala_en": "Automatic car revs up when accelerator is pressed but vehicle doesn't move well (slipping), RPM rises while speed lags.",
        "masalah_en": "Slipping automatic clutch plates, severely contaminated transmission fluid, or leaking oil pump seals.",
        "tindakan_en": "Do not force the accelerator pedal as it worsens internal transmission wear.",
        "tips_bengkel_en": "Tell the transmission specialist: 'My automatic car is slipping, please check if a transmission overhaul is necessary.'",
        "estimasi_biaya": "Rp 3.500.000 - Rp 8.000.000 | $230 - $520"
    },
    {
        "id": "MBL_TR_05",
        "kategori_kendaraan": "Mobil_Kaki",
        "gejala_id": "Ada bunyi kletek-kletek berirama dari ban/roda depan saat mobil belok patah ke kanan atau kiri.",
        "masalah_id": "CV Joint (As Roda / Kokel) bagian luar sudah aus, pelor hancur, atau karet boot sobek.",
        "tindakan_id": "Hindari membelokkan setir secara patah atau mendadak terlalu keras.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek CV Joint roda depan, sepertinya as roda luar sudah kena dan karet boot-nya sobek.'",
        "gejala_en": "Rhythmic clicking or popping noises from the front wheels when turning sharply right or left.",
        "masalah_en": "Worn outer CV joint, broken bearings, or torn boot cover.",
        "tindakan_en": "Avoid turning the steering wheel sharply or too aggressively.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the front CV joint, the outer axle seems worn and the boot is torn.'",
        "estimasi_biaya": "Rp 400.000 - Rp 1.200.000 | $25 - $80"
    },
    {
        "id": "MBL_TR_06",
        "kategori_kendaraan": "Mobil_Matic",
        "gejala_id": "Tuas transmisi matic nyangkut, terkunci, susah digeser dari posisi P meskipun rem sudah diinjak.",
        "masalah_id": "Switch rem (brake switch) mati atau solenoid pengunci tuas transmisi mengalami kerusakan.",
        "tindakan_id": "Gunakan tombol Shift Lock darurat pada konsol tuas matic untuk memindahkan gigi.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek switch pedal rem atau solenoid pengunci tuas transmisinya.'",
        "gejala_en": "Automatic transmission shifter is stuck, locked, and hard to move out of P even when the brake is pressed.",
        "masalah_en": "Faulty brake light switch or broken transmission shift lock solenoid.",
        "tindakan_en": "Use the emergency Shift Lock button on the shifter console to move gears.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the brake pedal switch or the shifter lock solenoid.'",
        "estimasi_biaya": "Rp 100.000 - Rp 350.000 | $7 - $23"
    },
    {
        "id": "MBL_TR_07",
        "kategori_kendaraan": "Mobil_Penggerak",
        "gejala_id": "Ada bunyi dengung atau dengkur (ngiung) dari bagian bawah belakang mobil RWD saat lari kencang.",
        "masalah_id": "Gardan (Differential) kekurangan oli, oli gardan tercampur air, atau gear gardan aus dan rompal.",
        "tindakan_id": "Kurangi kecepatan kendaraan untuk mencegah kerusakan komponen gardan yang lebih parah.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong kuras dan cek oli gardan belakang, serta setel ulang celah gigi gardannya.'",
        "gejala_en": "Humming or whining noise from the lower rear area of an RWD car when driving fast.",
        "masalah_en": "Low differential fluid, water-contaminated gear oil, or worn/chipped differential gears.",
        "tindakan_en": "Reduce vehicle speed to prevent severe differential damage.",
        "tips_bengkel_en": "Tell the mechanic: 'Please drain and check the rear differential oil, and adjust the backlash if needed.'",
        "estimasi_biaya": "Rp 250.000 - Rp 3.000.000 | $15 - $200"
    },

    # ==============================
    # KATEGORI: MOBIL - MESIN & KELISTRIKAN
    # ==============================
    {
        "id": "MBL_MS_01",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Mesin mobil brebet, nyendat-nyendat saat digas, pincang, dan tarikan berat.",
        "masalah_id": "Busi mati atau lemah, koil pengapian bocor arus, atau filter bensin/fuel pump lemah.",
        "tindakan_id": "Gunakan mobil dengan kecepatan stabil dan hindari akselerasi mendadak.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek busi dan koil pengapiannya, serta periksa tekanan fuel pump.'",
        "gejala_en": "Car engine is sputtering, hesitating during acceleration, misfiring, or feels sluggish.",
        "masalah_en": "Worn spark plugs, leaking ignition coils, or a weak fuel pump/filter.",
        "tindakan_en": "Drive at a stable speed and avoid sudden acceleration.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the spark plugs, ignition coils, and inspect the fuel pump pressure.'",
        "estimasi_biaya": "Rp 250.000 - Rp 1.200.000 | $15 - $80"
    },
    {
        "id": "MBL_MS_02",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Mesin mobil ngelitik (suara tek-tek halus / kletek) saat nanjak atau digas (Engine Knocking).",
        "masalah_id": "Bahan bakar beroktan rendah, ruang bakar banyak kerak karbon, atau timing pengapian tidak pas.",
        "tindakan_id": "Segera ganti bahan bakar dengan oktan yang lebih tinggi dan hindari beban mesin berat.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong lakukan gurah mesin (carbon clean) dan bersihkan throttle body.'",
        "gejala_en": "Engine knocking or pinging noise (subtle tapping sound) when climbing hills or accelerating.",
        "masalah_en": "Low octane fuel, heavy carbon buildup in the combustion chamber, or incorrect ignition timing.",
        "tindakan_en": "Switch to higher octane fuel immediately and avoid heavy engine loads.",
        "tips_bengkel_en": "Tell the mechanic: 'Please perform a carbon clean and clean the throttle body.'",
        "estimasi_biaya": "Rp 250.000 - Rp 500.000 | $15 - $35"
    },
    {
        "id": "MBL_MS_03",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Mesin mobil overheat (suhu indikator H naik drastis), ada uap panas atau air mendidih di kap mesin.",
        "masalah_id": "Air radiator habis atau bocor, motor kipas extra fan mati, waterpump bocor, atau thermostat macet.",
        "tindakan_id": "Segera tepikan kendaraan di tempat aman, matikan mesin, dan jangan langsung buka tutup radiator saat panas.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Mobil saya overheat, tolong cek sistem pendingin: kipas radiator, selang, waterpump, dan coolant.'",
        "gejala_en": "Engine overheats (temperature gauge spikes to H), hot steam or boiling water visible under the hood.",
        "masalah_en": "Low/leaking radiator coolant, dead cooling fan, leaking water pump, or stuck thermostat.",
        "tindakan_en": "Pull over safely, turn off the engine, and do not open the radiator cap while hot.",
        "tips_bengkel_en": "Tell the mechanic: 'My car overheated, please check the cooling system: radiator fan, hoses, water pump, and coolant.'",
        "estimasi_biaya": "Rp 400.000 - Rp 1.500.000 | $25 - $100"
    },
    {
        "id": "MBL_MS_04",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Mobil susah distarter saat pagi hari, suara dinamo lemah (ngek-ngek) tapi indikator dashboard nyala.",
        "masalah_id": "Aki (Accu) sudah tekor/soak/lemah, dinamo starter kotor arangnya, atau alternator tidak mengisi.",
        "tindakan_id": "Coba lakukan jumper aki darurat atau dorong mobil bagi transmisi manual.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek tegangan aki dan sistem pengisian alternator, atau servis dinamo starter.'",
        "gejala_en": "Car is hard to start in the morning, starter motor sounds weak while dashboard lights are working.",
        "masalah_en": "Weak or dead battery, dirty starter motor brushes, or failing alternator charging.",
        "tindakan_en": "Try a temporary battery jump start or push-start for manual transmissions.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the battery voltage, alternator charging system, or service the starter motor.'",
        "estimasi_biaya": "Rp 700.000 - Rp 1.500.000 | $45 - $100"
    },
    {
        "id": "MBL_MS_05",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Lampu indikator Check Engine warna kuning menyala terus menerus di speedometer mobil.",
        "masalah_id": "Sensor O2 kotor/rusak, Mass Air Flow sensor bermasalah, atau terjadi misfire di ruang bakar.",
        "tindakan_id": "Kendaraan masih bisa dikendarai, namun segera periksakan agar konsumsi bensin tidak boros.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong colok scanner OBD2 untuk membaca kode error Check Engine.'",
        "gejala_en": "Check Engine warning light stays illuminated on the car's dashboard.",
        "masalah_en": "Dirty/faulty O2 sensor, problematic Mass Air Flow sensor, or engine misfire.",
        "tindakan_en": "Vehicle is still drivable, but get it checked soon to avoid poor fuel economy.",
        "tips_bengkel_en": "Tell the mechanic: 'Please plug in the OBD2 scanner to read the Check Engine error code.'",
        "estimasi_biaya": "Rp 150.000 - Rp 1.500.000 | $10 - $100"
    },
    {
        "id": "MBL_MS_06",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "RPM mesin mobil naik turun sendiri saat AC nyala (hunting), idle gas tidak stabil, kadang mau mati.",
        "masalah_id": "Throttle body kotor, Idle Speed Control (ISC) bermasalah, atau ada selang vacuum yang bocor/getas.",
        "tindakan_id": "Nyalakan AC dengan stabil dan hindari melepas gas secara mendadak di kemacetan.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong bersihkan throttle body dan kalibrasi ulang ISC-nya.'",
        "gejala_en": "Engine RPM fluctuates up and down when AC is on (hunting), unstable idling, sometimes stalling.",
        "masalah_en": "Dirty throttle body, faulty Idle Speed Control (ISC), or leaking vacuum hoses.",
        "tindakan_en": "Keep AC running stably and avoid sudden throttle releases in traffic.",
        "tips_bengkel_en": "Tell the mechanic: 'Please clean the throttle body and recalibrate the ISC valve.'",
        "estimasi_biaya": "Rp 150.000 - Rp 350.000 | $10 - $25"
    },
    {
        "id": "MBL_MS_07",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Ada bunyi decit nyaring kencang (ciiiit) dari ruang mesin saat baru dihidupkan atau kena genangan air.",
        "masalah_id": "Fan belt / V-Belt alternator atau belt AC sudah kendur, kering, atau retak-retak.",
        "tindakan_id": "Hindari melintasi genangan air tinggi yang dapat membasahi tali kipas.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek ketegangan fan belt, kalau sudah getas tolong ganti baru.'",
        "gejala_en": "Loud squealing noise from the engine bay when first started or after driving through puddles.",
        "masalah_en": "Loose, dry, or cracked alternator fan belt or AC belt.",
        "tindakan_en": "Avoid driving through deep water puddles that could soak the belt.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the fan belt tension, and replace it if it's cracked or worn.'",
        "estimasi_biaya": "Rp 150.000 - Rp 350.000 | $10 - $25"
    },
    {
        "id": "MBL_MS_08",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Ada tetesan cairan oli warna hitam atau coklat di lantai garasi tepat di bawah mesin mobil.",
        "masalah_id": "Oli mesin bocor karena Seal Kruk As (Crankshaft) atau paking karter bak oli sudah getas/jebol.",
        "tindakan_id": "Rutin cek level dipstick oli mesin agar tidak kehabisan oli di jalan.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek sumber rembesan oli, ganti seal kruk as atau lem ulang paking karter.'",
        "gejala_en": "Black or brown oil droplets on the garage floor directly under the engine.",
        "masalah_en": "Engine oil leak due to hardened or broken crankshaft seals or oil pan gasket.",
        "tindakan_en": "Regularly check the engine oil dipstick level to prevent running out of oil.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the oil leak source, replace the crankshaft seal or reseal the oil pan gasket.'",
        "estimasi_biaya": "Rp 300.000 - Rp 1.500.000 | $20 - $100"
    },
    {
        "id": "MBL_MS_09",
        "kategori_kendaraan": "Mobil_Mesin",
        "gejala_id": "Knalpot mobil mengeluarkan asap putih tebal (ngebul) saat mesin dipanaskan atau digas kencang.",
        "masalah_id": "Oli mesin ikut terbakar di ruang bakar karena ring piston baret, silinder aus, atau seal klep bocor.",
        "tindakan_id": "Pantau level oli mesin secara berkala agar mesin tidak mengalami kerusakan fatal akibat kehabisan oli.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Knalpot ngebul putih, tolong cek kondisi ring piston dan seal klep, apakah perlu turun mesin.'",
        "gejala_en": "Car exhaust emits thick white smoke when the engine is warmed up or accelerated hard.",
        "masalah_en": "Engine oil burning in the combustion chamber due to scratched piston rings, worn cylinder, or leaking valve seals.",
        "tindakan_en": "Monitor engine oil levels regularly to prevent catastrophic engine failure from oil starvation.",
        "tips_bengkel_en": "Tell the mechanic: 'The exhaust is smoking white, please check piston rings and valve seals for an overhaul.'",
        "estimasi_biaya": "Rp 3.000.000 - Rp 8.000.000 | $200 - $520"
    },

    # ==============================
    # KATEGORI: MOBIL - REM (BRAKE SYSTEM)
    # ==============================
    {
        "id": "MBL_RM_01",
        "kategori_kendaraan": "Mobil_Rem",
        "gejala_id": "Ada bunyi decit kencang (srek-srek / cicit) dari ban depan saat pedal rem mobil diinjak.",
        "masalah_id": "Kampas rem sudah sangat tipis bergesekan dengan plat, atau terdapat batu kecil terjepit di cakram.",
        "tindakan_id": "Kurangi kecepatan berkendara karena pengereman bisa sedikit berkurang kepakemannya.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek kampas rem depan, apakah sudah tipis dan perlu diganti atau dibubut cakramnya.'",
        "gejala_en": "Loud squealing or scraping noise from the front wheels when pressing the car brake pedal.",
        "masalah_en": "Brake pads are severely worn down rubbing against the rotor, or a small stone is trapped.",
        "tindakan_en": "Reduce driving speed as braking efficiency may be slightly reduced.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the front brake pads; they seem thin and need replacement or rotor resurfacing.'",
        "estimasi_biaya": "Rp 250.000 - Rp 600.000 | $15 - $40"
    },
    {
        "id": "MBL_RM_02",
        "kategori_kendaraan": "Mobil_Rem",
        "gejala_id": "Pedal rem mobil terasa bergetar naik-turun atau ndut-ndutan saat diinjak di kecepatan tinggi.",
        "masalah_id": "Piringan cakram (Rotor) sudah melengkung, bergelombang karena panas berlebih, atau tipis tidak rata.",
        "tindakan_id": "Hindari melakukan pengereman mendadak dari kecepatan tinggi secara beruntun.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek piringan cakramnya, apakah sudah bergelombang dan perlu dibubut.'",
        "gejala_en": "Brake pedal vibrates up and down or pulsates when pressed at high speeds.",
        "masalah_en": "Brake rotors are warped, uneven due to overheating, or worn unevenly.",
        "tindakan_en": "Avoid consecutive hard braking from high speeds.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the brake rotors for warping and machine/resurface them.'",
        "estimasi_biaya": "Rp 350.000 - Rp 1.200.000 | $23 - $80"
    },
    {
        "id": "MBL_RM_03",
        "kategori_kendaraan": "Mobil_Rem",
        "gejala_id": "Pedal rem terasa dalam, ngempos, blong, atau harus dikocok berkali-kali baru bisa pakem.",
        "masalah_id": "Minyak rem bocor atau habis, terdapat angin palsu di selang rem, atau master rem sentral jebol.",
        "tindakan_id": "BAHAYA! Jangan lanjutkan perjalanan jika rem blong. Segera gunakan rem tangan secara perlahan untuk berhenti darurat.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Rem saya ngempos/blong, tolong cek kebocoran minyak rem, master rem, dan buang angin (bleeding).'",
        "gejala_en": "Brake pedal feels soft, sinks low, fails, or needs to be pumped multiple times to grip.",
        "masalah_en": "Brake fluid leak, air trapped in brake lines, or master cylinder failure.",
        "tindakan_en": "DANGER! Do not continue driving if brakes fail. Use the emergency handbrake gently to stop safely.",
        "tips_bengkel_en": "Tell the mechanic: 'My brakes feel spongy/failed, please check for fluid leaks, master cylinder, and bleed the system.'",
        "estimasi_biaya": "Rp 200.000 - Rp 800.000 | $13 - $50"
    },
    {
        "id": "MBL_RM_04",
        "kategori_kendaraan": "Mobil_Rem",
        "gejala_id": "Rem mobil menarik atau membanting ke satu sisi (kiri atau kanan) saat pedal rem diinjak mendadak.",
        "masalah_id": "Piston kaliper rem macet di satu sisi, selang rem mampet, atau kampas rem aus tidak rata.",
        "tindakan_id": "Pegang setir dengan kuat saat melakukan pengereman darurat agar mobil tidak membanting arah.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Mobil lari ke samping saat direm, tolong cek piston kaliper dan bersihkan pin slide rem.'",
        "gejala_en": "Car pulls or swerves to one side (left or right) when the brakes are applied suddenly.",
        "masalah_en": "Brake caliper piston stuck on one side, blocked brake hose, or uneven brake pad wear.",
        "tindakan_en": "Hold the steering wheel firmly during emergency braking to prevent veering.",
        "tips_bengkel_en": "Tell the mechanic: 'The car pulls to one side when braking, please inspect the caliper piston and slide pins.'",
        "estimasi_biaya": "Rp 150.000 - Rp 350.000 | $10 - $25"
    },

    # ==============================
    # KATEGORI: MOBIL - AC (PENDINGIN)
    # ==============================
    {
        "id": "MBL_AC_01",
        "kategori_kendaraan": "Mobil_AC",
        "gejala_id": "AC mobil tidak dingin sama sekali, hanya keluar angin panas/biasa, siang hari terasa gerah.",
        "masalah_id": "Freon AC habis karena bocor, magnetic clutch kompresor mati, atau motor kipas kondensor (extra fan) mati.",
        "tindakan_id": "Buka sedikit kaca jendela agar sirkulasi udara kabin tetap terjaga.",
        "tips_bengkel_id": "Sampaikan ke bengkel AC: 'Tolong cek kebocoran freon, periksa magnetic clutch, dan kipas kondensor AC.'",
        "gejala_en": "Car AC blows only warm air and is not cold at all, making it stuffy during the day.",
        "masalah_en": "Refrigerant leak, faulty compressor magnetic clutch, or dead condenser cooling fan.",
        "tindakan_en": "Roll down windows slightly to maintain cabin air ventilation.",
        "tips_bengkel_en": "Tell the AC shop: 'Please check for refrigerant leaks, inspect the magnetic clutch, and test the condenser fan.'",
        "estimasi_biaya": "Rp 350.000 - Rp 1.500.000 | $23 - $100"
    },
    {
        "id": "MBL_AC_02",
        "kategori_kendaraan": "Mobil_AC",
        "gejala_id": "AC mobil bau apek, asam, bau kecut, atau bau debu yang menyengat saat pertama kali dinyalakan.",
        "masalah_id": "Filter kabin AC sudah kotor berjamur, atau Evaporator sangat kotor dan berlendir menumpuk kuman.",
        "tindakan_id": "Matikan tombol AC beberapa menit sebelum mesin dimatikan untuk mengurangi kelembapan evaporator.",
        "tips_bengkel_id": "Sampaikan ke bengkel AC: 'Tolong ganti filter kabin dan cuci evaporator AC tanpa bongkar dashboard.'",
        "gejala_en": "Car AC smells musty, sour, or like trapped dust when first turned on.",
        "masalah_en": "Dirty/moldy cabin air filter, or extremely dirty and slimy evaporator breeding bacteria.",
        "tindakan_en": "Turn off the AC switch a few minutes before shutting down the engine to reduce evaporator moisture.",
        "tips_bengkel_en": "Tell the AC shop: 'Please replace the cabin air filter and clean the AC evaporator.'",
        "estimasi_biaya": "Rp 150.000 - Rp 800.000 | $10 - $50"
    },
    {
        "id": "MBL_AC_03",
        "kategori_kendaraan": "Mobil_AC",
        "gejala_id": "Ada bunyi ngorok kasar (grok-grok) dari arah kap mesin yang muncul hanya saat AC dihidupkan.",
        "masalah_id": "Kompresor AC mulai aus, bearing kompresor oblak, atau oli kompresor sudah kering/habis.",
        "tindakan_id": "Matikan AC sementara waktu jika bunyi dirasa semakin kasar untuk mencegah kompresor macet total.",
        "tips_bengkel_id": "Sampaikan ke bengkel AC: 'Ada suara ngorok saat AC menyala, tolong cek kompresor dan bearing-nya.'",
        "gejala_en": "A rough growling or rattling noise from the engine bay that appears only when the AC is turned on.",
        "masalah_en": "AC compressor starting to wear out, loose compressor bearing, or dry/depleted compressor oil.",
        "tindakan_en": "Turn off the AC temporarily if the noise gets louder to prevent total compressor seizure.",
        "tips_bengkel_en": "Tell the AC shop: 'There is a growling noise when AC is on, please inspect the compressor and bearings.'",
        "estimasi_biaya": "Rp 500.000 - Rp 2.500.000 | $35 - $160"
    },

    # ==============================
    # KATEGORI: MOTOR - KAKI-KAKI, KEMUDI & REM
    # ==============================
    {
        "id": "MTR_KK_01",
        "kategori_kendaraan": "Motor_Kaki",
        "gejala_id": "Stang, stir, atau kemudi motor terasa berat sebelah, kaku susah dibelokkan, atau bunyi jeglek saat direm.",
        "masalah_id": "Komstir (steering cone) aus, kendor, oblak, atau pelor bearing komstir ada yang hancur.",
        "tindakan_id": "Berhati-hatilah saat berkendara di tikungan karena kestabilan kemudi motor berkurang.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong setel ulang atau ganti komstir motor karena sudah berat dan oblak.'",
        "gejala_en": "Motorcycle handlebars feel heavy on one side, stiff, hard to steer, or make a clunking noise when braking.",
        "masalah_en": "Worn, loose, or damaged steering cone bearings.",
        "tindakan_en": "Be careful when cornering as motorcycle steering stability is compromised.",
        "tips_bengkel_en": "Tell the mechanic: 'Please readjust or replace the steering cone bearings as they feel heavy and loose.'",
        "estimasi_biaya": "Rp 150.000 - Rp 350.000 | $10 - $25"
    },
    {
        "id": "MTR_KK_02",
        "kategori_kendaraan": "Motor_Kaki",
        "gejala_id": "Shockbreaker (shock) depan motor terasa sangat keras mentok nabrak besi atau bocor keluar oli.",
        "masalah_id": "Seal shock bocor sehingga oli habis kering, per patah, atau as shock baret/bengkok.",
        "tindakan_id": "Kurangi kecepatan saat melewati jalan berlubang agar tidak merusak velg motor.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong bongkar shock depan, ganti seal shock, dan isi ulang oli shock-nya.'",
        "gejala_en": "Front motorcycle shock absorbers feel extremely hard bottoming out or are leaking oil.",
        "masalah_en": "Leaking shock seals draining the oil, broken springs, or scratched/bent shock tubes.",
        "tindakan_en": "Slow down when riding over potholes to avoid damaging motorcycle rims.",
        "tips_bengkel_en": "Tell the mechanic: 'Please overhaul the front shocks, replace the seals, and refill the shock oil.'",
        "estimasi_biaya": "Rp 80.000 - Rp 200.000 | $5 - $13"
    },
    {
        "id": "MTR_KK_03",
        "kategori_kendaraan": "Motor_Kaki",
        "gejala_id": "Ban motor belakang terasa goyang, geol-geol, oleng, atau megal-megol saat jalan di kecepatan lambat/sedang.",
        "masalah_id": "Bearing (lakher) roda belakang hancur/oblak, ban benjol, atau velg peyang habis hajar lubang.",
        "tindakan_id": "Kurangi kecepatan dan hindari manuver tajam karena motor tidak stabil.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek bearing roda belakang dan velg motor, sepertinya sudah oblak.'",
        "gejala_en": "Rear motorcycle tire feels unstable, wobbling, or swaying at low to medium speeds.",
        "masalah_en": "Destroyed/loose rear wheel bearings, bulged tire, or bent rim from potholes.",
        "tindakan_en": "Reduce speed and avoid sharp maneuvers due to instability.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the rear wheel bearings and rim, they feel loose and wobbly.'",
        "estimasi_biaya": "Rp 50.000 - Rp 150.000 | $3 - $10"
    },
    {
        "id": "MTR_KK_04",
        "kategori_kendaraan": "Motor_Kaki",
        "gejala_id": "Saat motor boncengan, bagian belakang terasa mentok (amblas) dan tidak mantul empuk, terasa keras.",
        "masalah_id": "Shockbreaker belakang (Monoshock/Dualshock) bocor, sil pecah, atau per sudah lemah.",
        "tindakan_id": "Kurangi beban bawaan atau hindari jalanan rusak saat berboncengan.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek shock belakang, apakah bisa disuntik oli ulang atau harus diganti baru.'",
        "gejala_en": "When carrying a passenger, the rear suspension bottoms out (sags) and feels harsh instead of smooth.",
        "masalah_en": "Leaking rear shock absorbers, broken seals, or weakened springs.",
        "tindakan_en": "Reduce passenger load or avoid rough roads when riding two-up.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the rear shock, whether it can be reconditioned or needs replacement.'",
        "estimasi_biaya": "Rp 250.000 - Rp 600.000 | $15 - $40"
    },
    {
        "id": "MTR_RM_01",
        "kategori_kendaraan": "Motor_Rem",
        "gejala_id": "Roda motor terasa seret putarannya berat, rem cakram depan mengunci dan velg cepat panas.",
        "masalah_id": "Piston kaliper rem macet karena karat/lumpur, atau lubang master rem mampet.",
        "tindakan_id": "Jangan dipaksakan jalan jauh karena rem yang mengunci bisa membuat ban terbakar.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong bersihkan kaliper dan piston rem depan dari karat karena roda seret.'",
        "gejala_en": "Motorcycle wheel feels draggy and heavy, front disc brake is locking up and rim gets hot quickly.",
        "masalah_en": "Caliper piston stuck due to rust/dirt, or master cylinder port blocked.",
        "tindakan_en": "Do not ride long distances as a locking brake can overheat the tire.",
        "tips_bengkel_en": "Tell the mechanic: 'Please clean the front brake caliper and piston from rust as the wheel is dragging.'",
        "estimasi_biaya": "Rp 50.000 - Rp 100.000 | $3 - $7"
    },
    {
        "id": "MTR_RM_02",
        "kategori_kendaraan": "Motor_Rem",
        "gejala_id": "Saat ngerem depan/belakang (cakram), tuas rem motor terasa berdenyut, membal, atau bergetar ke tangan.",
        "masalah_id": "Piringan cakram (Disk Brake) sudah bengkok/bergelombang akibat panas ekstrem (disiram saat panas).",
        "tindakan_id": "Hindari menyiram piringan cakram dengan air saat kondisi masih sangat panas.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek piringan cakram motor, sepertinya sudah bergelombang dan bergetar saat direm.'",
        "gejala_en": "When braking, the motorcycle brake lever pulses, rebounds, or vibrates in your hand.",
        "masalah_en": "Brake disc rotor is warped or uneven due to extreme heat.",
        "tindakan_en": "Avoid spraying water directly onto hot brake rotors.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the brake disc rotor, it feels warped and vibrates when braking.'",
        "estimasi_biaya": "Rp 150.000 - Rp 300.000 | $10 - $20"
    },

    # ==============================
    # KATEGORI: MOTOR - MATIC (CVT)
    # ==============================
    {
        "id": "MTR_CV_01",
        "kategori_kendaraan": "Motor_Matic",
        "gejala_id": "Tarikan awal motor matic terasa gredek parah, bergetar kencang dari blok CVT saat selongsong gas baru ditarik.",
        "masalah_id": "Mangkok kampas ganda kotor penuh debu, kampas ganda tipis/slip, atau karet dumper aus.",
        "tindakan_id": "Lakukan servis rutin pembersihan CVT secara berkala.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Mas, tolong servis CVT dan bersihkan mangkok kampas gandanya dari debu.'",
        "gejala_en": "Scooter CVT shakes severely or chatters during initial acceleration from a stop.",
        "masalah_en": "Clutch housing is dirty with dust, thin/slipping clutch pads, or worn damper rubber.",
        "tindakan_en": "Perform routine CVT cleaning maintenance regularly.",
        "tips_bengkel_en": "Tell the mechanic: 'Please service the CVT block and clean the clutch housing from dust.'",
        "estimasi_biaya": "Rp 50.000 - Rp 250.000 | $3 - $15"
    },
    {
        "id": "MTR_CV_02",
        "kategori_kendaraan": "Motor_Matic",
        "gejala_id": "Tenaga motor matic ngempos, gas ditarik putaran tinggi meraung tapi lari motor pelan/kecepatan tertahan.",
        "masalah_id": "V-Belt sudah retak, mulur, aus, atau roller sudah gepeng/peyang. Per CVT juga bisa sudah lembek.",
        "tindakan_id": "Jangan geber motor terlalu kencang untuk menghindari V-Belt putus mendadak.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong bongkar CVT, cek kondisi V-Belt dan roller apakah sudah aus atau peyang.'",
        "gejala_en": "Scooter loses power, engine revs high when gas is pulled but acceleration lags and speed is restricted.",
        "masalah_en": "Cracked, stretched, or worn V-Belt, flat-spotted rollers, or soft CVT spring.",
        "tindakan_en": "Avoid revving the engine too high to prevent sudden V-Belt snap.",
        "tips_bengkel_en": "Tell the mechanic: 'Please open the CVT, check the V-belt and rollers for wear or flat spots.'",
        "estimasi_biaya": "Rp 150.000 - Rp 350.000 | $10 - $25"
    },
    {
        "id": "MTR_CV_03",
        "kategori_kendaraan": "Motor_Matic",
        "gejala_id": "Ada suara klotok-klotok, tek-tek kasar di bagian CVT saat motor langsam (idle), hilang halus saat digas.",
        "masalah_id": "Slider piece (karet bantalan tutup rumah roller) sudah longgar/aus atau rumah roller oblak parah.",
        "tindakan_id": "Segera periksakan sebelum merusak jalur rumah roller.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek slider piece dan rumah roller CVT yang bunyi klotok-klotok.'",
        "gejala_en": "Clattering or rough tapping noises from the CVT area at idle, disappearing when accelerated.",
        "masalah_en": "Worn slider pieces (roller cover dampers) or loose roller housing.",
        "tindakan_en": "Get it inspected soon before it damages the roller housing tracks.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the slider pieces and roller housing making clattering noises.'",
        "estimasi_biaya": "Rp 35.000 - Rp 250.000 | $2 - $15"
    },
    {
        "id": "MTR_CV_04",
        "kategori_kendaraan": "Motor_Matic",
        "gejala_id": "Bunyi mendesing bersiul seperti suara pesawat terbang (ngiiing) dari area roda belakang saat motor jalan kencang.",
        "masalah_id": "Bearing rasio (gigi transmisi) di dalam gearbox gardan aus, atau oli gardan habis/tercampur air.",
        "tindakan_id": "Kurangi kecepatan berkendara untuk mencegah gigi rasio rompal.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek gearbox belakang, kuras oli gardan dan ganti bearing rasio yang berdenging.'",
        "gejala_en": "Whining or jet engine-like whistling sound from the rear wheel area when riding fast.",
        "masalah_en": "Worn transmission ratio bearings in the final gear box, or depleted/water-contaminated gear oil.",
        "tindakan_en": "Reduce riding speed to prevent final gear damage.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the rear gearbox, drain gear oil, and replace the noisy ratio bearings.'",
        "estimasi_biaya": "Rp 150.000 - Rp 350.000 | $10 - $25"
    },
    {
        "id": "MTR_CV_05",
        "kategori_kendaraan": "Motor_Matic",
        "gejala_id": "Motor matic tiba-tiba mati total di tengah jalan, tidak bisa jalan sama sekali, terdengar suara tarikan lepas.",
        "masalah_id": "V-Belt CVT putus total di dalam blok karena sudah sangat aus dan terlambat diganti.",
        "tindakan_id": "Tuntun motor ke bengkel terdekat atau gunakan jasa derek motor.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'V-belt motor saya putus di jalan, tolong bongkar CVT, bersihkan sisa serpihan, dan ganti baru.'",
        "gejala_en": "Scooter suddenly dies in the middle of the road, unable to move at all, with a slipping snap sound.",
        "masalah_en": "V-Belt snapped completely inside the CVT case due to severe wear and overdue replacement.",
        "tindakan_en": "Push the scooter to the nearest workshop or use towing services.",
        "tips_bengkel_en": "Tell the mechanic: 'My V-belt snapped, please open the CVT, clean out debris, and install a new one.'",
        "estimasi_biaya": "Rp 200.000 - Rp 400.000 | $13 - $28"
    },

    # ==============================
    # KATEGORI: MOTOR - MESIN & KELISTRIKAN
    # ==============================
    {
        "id": "MTR_MS_01",
        "kategori_kendaraan": "Motor_Mesin",
        "gejala_id": "Knalpot motor mengeluarkan asap putih tipis atau tebal secara terus menerus (ngebul).",
        "masalah_id": "Oli mesin lolos masuk ke ruang bakar akibat ring piston baret, dinding silinder aus, atau seal klep bocor.",
        "tindakan_id": "Cek rutin volume oli mesin agar tidak kehabisan di jalan.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Knalpot motor ngebul putih, tolong cek ring piston, silinder, dan seal klep untuk turun mesin atas.'",
        "gejala_en": "Motorcycle exhaust emits thin or thick continuous white smoke (burning oil).",
        "masalah_en": "Engine oil leaking into combustion chamber due to scratched piston rings, worn cylinder bore, or leaking valve seals.",
        "tindakan_en": "Check engine oil level regularly to avoid running dry.",
        "tips_bengkel_en": "Tell the mechanic: 'Exhaust is smoking white, please check piston rings, cylinder, and valve seals for a top overhaul.'",
        "estimasi_biaya": "Rp 800.000 - Rp 1.500.000 | $50 - $100"
    },
    {
        "id": "MTR_MS_02",
        "kategori_kendaraan": "Motor_Mesin",
        "gejala_id": "Suara mesin motor bunyi tek-tek-tek berisik dan kasar mirip mesin jahit saat posisi langsam/idle.",
        "masalah_id": "Setelan celah klep terlalu renggang, atau rantai keteng (cam chain) kendor dan aus.",
        "tindakan_id": "Hindari menggeber mesin dalam kondisi stasioner terlalu lama.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek dan setel ulang celah klep, serta periksa kondisi rantai keteng beserta tensionernya.'",
        "gejala_en": "Motorcycle engine makes a noisy, harsh ticking sound like a sewing machine at idle.",
        "masalah_en": "Valve clearance is too loose, or the cam chain is loose and worn out.",
        "tindakan_en": "Avoid revving the engine excessively while idling.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check and adjust valve clearance, and inspect the cam chain and tensioner.'",
        "estimasi_biaya": "Rp 50.000 - Rp 300.000 | $3 - $20"
    },
    {
        "id": "MTR_MS_03",
        "kategori_kendaraan": "Motor_Mesin",
        "gejala_id": "Knalpot motor sering nembak-nembak (dor-dor) saat turun gas, mbrebet, dan boros bensin.",
        "masalah_id": "Knalpot bocor di bagian paking leher, busi melemah, atau setelan injeksi/karbu kotor.",
        "tindakan_id": "Kurangi penggunaan kecepatan tinggi sampai sistem pembakaran diservis.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek paking leher knalpot yang bocor dan bersihkan injektor atau karburator.'",
        "gejala_en": "Motorcycle exhaust backfires (pops) when decelerating, sputters, and consumes excess fuel.",
        "masalah_en": "Exhaust leak at the header gasket, weak spark plug, or dirty fuel injection/carburetor.",
        "tindakan_en": "Avoid high speed riding until the combustion system is serviced.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check for exhaust header gasket leaks and clean the injector or carburetor.'",
        "estimasi_biaya": "Rp 50.000 - Rp 150.000 | $3 - $10"
    },
    {
        "id": "MTR_MS_04",
        "kategori_kendaraan": "Motor_Mesin",
        "gejala_id": "Motor sering mati mendadak saat berhenti di lampu merah atau saat rpm diturunkan (tidak bisa langsam).",
        "masalah_id": "Setelan klep terlalu rapat, busi lemah, throttle body sangat kotor, atau sensor IACV kotor/mati.",
        "tindakan_id": "Jaga sedikit putaran gas saat berhenti agar motor tidak mati mendadak.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Motor sering mati saat gas ditutup, tolong setel klep dan bersihkan throttle body serta IACV.'",
        "gejala_en": "Motorcycle frequently stalls when stopping at red lights or when RPM drops (cannot idle).",
        "masalah_en": "Valve clearance too tight, weak spark plug, very dirty throttle body, or dirty/dead IACV sensor.",
        "tindakan_en": "Keep slight throttle input when stopping to prevent sudden stalling.",
        "tips_bengkel_en": "Tell the mechanic: 'The bike stalls when closing throttle, please adjust valves and clean the throttle body/IACV.'",
        "estimasi_biaya": "Rp 75.000 - Rp 200.000 | $5 - $13"
    },
    {
        "id": "MTR_MS_05",
        "kategori_kendaraan": "Motor_Manual",
        "gejala_id": "Gigi persneling motor manual susah dioper (keras), netralnya alot, dan tarikan kopling selip.",
        "masalah_id": "Kampas kopling sudah tipis, plat gesek hangus terbakar, atau kabel kopling berkarat dan seret.",
        "tindakan_id": "Tekan kopling sepenuhnya saat memindahkan gigi persneling.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong bongkar bak kopling, ganti kampas kopling satu set, dan cek kabel kopling.'",
        "gejala_en": "Manual motorcycle gears are hard to shift, neutral is stubborn, and clutch slips.",
        "masalah_en": "Worn clutch friction plates, burnt clutch plates, or rusted/sticky clutch cable.",
        "tindakan_en": "Pull the clutch lever fully when shifting gears.",
        "tips_bengkel_en": "Tell the mechanic: 'Please open the clutch cover, replace the clutch plates, and check the clutch cable.'",
        "estimasi_biaya": "Rp 150.000 - Rp 450.000 | $10 - $30"
    },
    {
        "id": "MTR_MS_06",
        "kategori_kendaraan": "Motor_Mesin",
        "gejala_id": "Oli mesin motor (terutama motor berpendingin cairan) tiba-tiba berubah warna menjadi keputihan seperti susu.",
        "masalah_id": "Air radiator bocor dan menyeberang masuk ke ruang mesin akibat seal waterpump jebol.",
        "tindakan_id": "Jangan nyalakan mesin agar komponen dalam mesin tidak tergerus air radiator.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Oli jadi seperti susu putih, tolong ganti seal waterpump dan kuras oli mesin berulang kali.'",
        "gejala_en": "Motorcycle engine oil suddenly turns milky white like coffee with milk.",
        "masalah_en": "Coolant leak crossing into the engine crankcase due to a blown water pump seal.",
        "tindakan_en": "Do not start the engine to prevent internal damage from coolant contamination.",
        "tips_bengkel_en": "Tell the mechanic: 'The oil is milky white, please replace the water pump seal and flush the engine oil thoroughly.'",
        "estimasi_biaya": "Rp 250.000 - Rp 500.000 | $15 - $35"
    },
    {
        "id": "MTR_KL_01",
        "kategori_kendaraan": "Motor_Kelistrikan",
        "gejala_id": "Tombol stater ditekan cuma bunyi cetek-cetek, dinamo starter diam tidak mau muter menghidupkan mesin.",
        "masalah_id": "Aki drop, atau Bendik Starter (Relay Starter) sudah konslet/mati/kotor di bagian dalamnya.",
        "tindakan_id": "Gunakan kick starter (celah manual) jika motor Anda memilikinya untuk menyalakan mesin.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek voltase aki, jika normal berarti bendik starter-nya yang rusak, tolong ganti.'",
        "gejala_en": "Pressing the electric starter button only makes clicking sounds, starter motor doesn't spin.",
        "masalah_en": "Weak battery or shorted/faulty starter relay (bendik starter).",
        "tindakan_en": "Use the kick starter if available to start the engine.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check battery voltage, if normal the starter relay is faulty, please replace it.'",
        "estimasi_biaya": "Rp 60.000 - Rp 150.000 | $4 - $10"
    },
    {
        "id": "MTR_KL_02",
        "kategori_kendaraan": "Motor_Kelistrikan",
        "gejala_id": "Aki motor selalu tekor dan ngedrop terus meskipun aki tersebut baru saja diganti dengan yang baru.",
        "masalah_id": "Kiprok (Regulator/Rectifier) mati, atau spul motor gosong/putus sehingga tidak ada arus pengisian.",
        "tindakan_id": "Batasi penggunaan aksesoris kelistrikan tambahan seperti lampu sorot agar aki tidak cepat habis.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek pengisian aki dengan multitester, apakah kiprok atau spul-nya yang mati.'",
        "gejala_en": "Motorcycle battery constantly discharges and goes dead even after being replaced with a new one.",
        "masalah_en": "Faulty regulator/rectifier (kiprok) or burned/broken stator coil (spul) preventing charging.",
        "tindakan_en": "Limit extra electrical accessories like spotlights to prevent fast battery drain.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the charging voltage with a multimeter, whether the regulator or stator coil is dead.'",
        "estimasi_biaya": "Rp 150.000 - Rp 400.000 | $10 - $25"
    },
    {
        "id": "MTR_KL_03",
        "kategori_kendaraan": "Motor_Kelistrikan",
        "gejala_id": "Motor mati mendadak di jalan atau lampu merah, tombol stater ditekan cuma bunyi cetek-cetek, dinamo starter diam tidak mau muter, dan klakson nyala redup.",
        "masalah_id": "Aki drop parah, atau relay starter (bendik) mengalami kerusakan total.",
        "tindakan_id": "Tepikan kendaraan dan gunakan kick starter atau jumper aki.",
        "tips_bengkel_id": "Sampaikan ke mekanik: 'Tolong cek sistem kelistrikan pengisian dan kondisi aki serta bendik starter.'",
        "gejala_en": "Bike dies suddenly on the road, starter makes clicking noise, and horn is dim.",
        "masalah_en": "Severely dropped battery or completely failed starter relay.",
        "tindakan_en": "Pull over and use kick starter or jump start.",
        "tips_bengkel_en": "Tell the mechanic: 'Please check the charging electrical system, battery condition, and starter relay.'",
        "estimasi_biaya": "Rp 60.000 - Rp 150.000 | $4 - $10"
    }
]

class KeluhanInput(BaseModel):
    keluhan: str

class ErrorReportInput(BaseModel):
    keluhan: str
    diagnosa_ai: str

@app.get("/")
def home():
    logger.info("Health check endpoint diakses.")
    return {"status": "aktif", "pesan": "Server Global Enterprise MontirPintar Berjalan Optimal!"}

@app.post("/diagnosa")
def diagnosa_ai(data: KeluhanInput):
    try:
        user_text = data.keluhan.lower()
        logger.info(f"Menerima keluhan diagnosa: {user_text}")
        
        best_match = None
        highest_score = 0.0
        detected_lang = "id" # Default Bahasa Indonesia
        
        for item in data_bengkel:
            # Hitung kecocokan Bahasa Indonesia
            gejala_id = item["gejala_id"].lower()
            sim_id = difflib.SequenceMatcher(None, user_text, gejala_id).ratio()
            
            # Hitung kecocokan Bahasa Inggris
            gejala_en = item["gejala_en"].lower()
            sim_en = difflib.SequenceMatcher(None, user_text, gejala_en).ratio()
            
            # Evaluasi skor tertinggi
            if sim_id > highest_score:
                highest_score = sim_id
                best_match = item
                detected_lang = "id"
                
            if sim_en > highest_score:
                highest_score = sim_en
                best_match = item
                detected_lang = "en"
                
        # Ambang batas kecocokan (Threshold)
        if highest_score > 0.08 and best_match:
            logger.info(f"Diagnosa ditemukan (Bahasa: {detected_lang}) dengan akurasi: {highest_score * 100}%")
            
            if detected_lang == "id":
                return {
                    "status": "success",
                    "bahasa": "id",
                    "diagnosa_ai": best_match["masalah_id"],
                    "saran_tindakan": best_match["tindakan_id"],
                    "tips_bengkel": best_match["tips_bengkel_id"],
                    "estimasi_biaya": best_match["estimasi_biaya"],
                    "akurasi": round(float(highest_score) * 100, 2)
                }
            else:
                return {
                    "status": "success",
                    "bahasa": "en",
                    "diagnosa_ai": best_match["masalah_en"],
                    "saran_tindakan": best_match["tindakan_en"],
                    "tips_bengkel": best_match["tips_bengkel_en"],
                    "estimasi_biaya": best_match["estimasi_biaya"],
                    "akurasi": round(float(highest_score) * 100, 2)
                }
        else:
            logger.warning("Keluhan pengguna tidak dikenali dalam database.")
            return {
                "status": "success",
                "bahasa": "unknown",
                "diagnosa_ai": "Kerusakan belum teridentifikasi secara spesifik dalam database / Issue not specifically identified.",
                "saran_tindakan": "Berhenti di tempat aman dan hindari memaksakan kendaraan berjalan / Stop safely and avoid forcing the vehicle.",
                "tips_bengkel": "Bawa kendaraan ke bengkel terdekat untuk pemeriksaan manual oleh mekanik / Visit the nearest workshop for manual inspection.",
                "estimasi_biaya": "Estimasi bervariasi / Varies",
                "akurasi": 0.0
            }
            
    except Exception as e:
        logger.error(f"Error pada endpoint /diagnosa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lapor_error")
def lapor_error(data: ErrorReportInput):
    try:
        logger.warning(f"⚠️ LAPORAN DARI USER -> Keluhan: {data.keluhan} | Diagnosa Salah: {data.diagnosa_ai}")
        
        # ⚠️ TES HARDCODE: Masukkan langsung string token Anda di sini
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","8739496643:AAFRM2JtXrPe2s5DRwTPM-sceC6ctah2Jsg") 
        chat_id = os.environ.get("TELEGRAM_CHAT_ID","8875393494")
        
       if bot_token and chat_id:
            text = f"🚨 LAPORAN DIAGNOSA MELESET\n\nKeluhan: {data.keluhan}\nDiagnosa AI: {data.diagnosa_ai}"
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(telegram_url, json={"chat_id": chat_id, "text": text}, timeout=3)
            logger.info("Notifikasi error berhasil dikirim ke Telegram.")
            
        return {"status": "success", "pesan": "Terima kasih, laporan Anda telah masuk ke sistem evaluasi."}
    except Exception as e:
        logger.error(f"Gagal memproses lapor_error: {str(e)}")
        return {"status": "error", "pesan": str(e)}
