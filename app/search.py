import difflib

def semantic_search(normalized_input: str, database: list, lang: str):
    best_match = None
    highest_score = 0.0
    
    for item in database:
        symptoms = item.get("language", {}).get(lang, {}).get("symptoms", [])
        
        for symptom in symptoms:
            # 1. Hitung Sequence Matcher
            seq_score = difflib.SequenceMatcher(None, normalized_input, symptom).ratio()
            
            # 2. Hitung Keyword Matcher (Bobot lebih tinggi untuk kecocokan kata kunci)
            input_words = set(normalized_input.split())
            symp_words = set(symptom.split())
            common_words = input_words.intersection(symp_words)
            kw_score = len(common_words) / max(len(input_words), 1)
            
            # Perketat bobot keyword menjadi 70% agar kata spesifik seperti "rem" / "ngempos" lebih dominan
            total_score = (seq_score * 0.3) + (kw_score * 0.7)
            
            if total_score > highest_score:
                highest_score = total_score
                best_match = item
                
    return best_match, highest_score
