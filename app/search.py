import difflib

def semantic_search(normalized_input: str, database: list, lang: str):
    best_match = None
    highest_score = 0.0
    
    for item in database:
        # Ambil daftar gejala berdasarkan bahasa yang terdeteksi
        symptoms = item.get("language", {}).get(lang, {}).get("symptoms", [])
        
        for symptom in symptoms:
            # 1. Hitung kemiripan urutan kata (Sequence Matcher)
            seq_score = difflib.SequenceMatcher(None, normalized_input, symptom).ratio()
            
            # 2. Hitung jumlah kata kunci yang cocok (Keyword Matcher)
            input_words = set(normalized_input.split())
            symp_words = set(symptom.split())
            common_words = input_words.intersection(symp_words)
            kw_score = len(common_words) / max(len(input_words), 1)
            
            # Gabungkan skor (Lebih menitikberatkan pada kata kunci)
            total_score = (seq_score * 0.4) + (kw_score * 0.6)
            
            if total_score > highest_score:
                highest_score = total_score
                best_match = item
                
    return best_match, highest_score
