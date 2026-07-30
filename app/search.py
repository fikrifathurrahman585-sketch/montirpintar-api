from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Inisialisasi vectorizer (Mesin pengubah teks ke angka)
vectorizer = TfidfVectorizer()

def semantic_search(normalized_input: str, database: list, lang: str):
    best_match = None
    highest_score = 0.0
    
    # 1. Kumpulkan semua gejala dari database ke dalam satu list
    corpus = []
    mapping = []  # Menyimpan index agar tahu gejala ini milik data yang mana
    
    for idx, item in enumerate(database):
        symptoms = item.get("language", {}).get(lang, {}).get("symptoms", [])
        for symptom in symptoms:
            corpus.append(symptom)
            mapping.append(idx)
            
    # Jika corpus kosong, langsung kembalikan
    if not corpus:
        return None, 0.0

    # 2. Tambahkan input user ke akhir corpus agar ikut dipelajari mesin
    corpus.append(normalized_input)
    
    # 3. Ubah semua teks menjadi matriks angka (Vektorisasi)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # 4. Ambil vektor input user (posisi paling akhir)
    user_vector = tfidf_matrix[-1]
    
    # 5. Ambil vektor data bengkel (semua kecuali yang terakhir)
    db_vectors = tfidf_matrix[:-1]
    
    # 6. Hitung kemiripan sudut (Cosine Similarity) antara input user vs database
    similarities = cosine_similarity(user_vector, db_vectors)[0]
    
    # 7. Cari skor tertinggi
    if len(similarities) > 0:
        max_idx = np.argmax(similarities)
        highest_score = similarities[max_idx]
        
        # Ambil data asli berdasarkan index mapping
        if highest_score > 0.0:
            db_index = mapping[max_idx]
            best_match = database[db_index]

    return best_match, highest_score
