def sanitize_text(raw_text):
    lower_raw_text = raw_text.lower()
    #Changed clean_buffer="" to [] to make it efficiency, this caused changing += character to clean_buffer.append string to list
    clean_buffer = []
    for character in lower_raw_text:
        if character.isalnum() or character in (" ", "-"):
            clean_buffer.append(character)

    clean_text = "".join(clean_buffer)
    word_list = clean_text.split()
    return set(word_list)

if __name__ == "__main__":
    user_jd = input("Paste your Job Description here:")


    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    if not lines:
        print("Error: No input provided")
    else:
        full_jd = " ".join(lines)
        result_set =sanitize_text(full_jd)
        #it might be better when it is on the top?
        STOP_WORDS = {
            "a", "an", "the", "and", "but", "or", "for", "nor", "so", "yet",
            "at", "by", "from", "in", "into", "of", "off", "on", "onto", "out",
            "over", "to", "up", "with", "as", "if", "when", "while", "because",
            "until", "through", "between", "before", "after", "during", "under", "above",
            "i", "me", "my", "mine", "we", "us", "our", "ours", "you", "your",
            "yours", "he", "him", "his", "she", "her", "hers", "it", "its", "they",
            "them", "their", "theirs", "this", "that", "these", "those", "am", "is",
            "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "can", "could", "will",
            "would", "shall", "should", "may", "might", "must",
            "just", "only", "very", "also", "even", "still", "then", "there", "here",
            "who", "what", "where", "when", "why", "how", "which", "all", "any",
            "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "own", "same", "than", "too", "very", "s", "t", "can", "will"
        }
        signal = result_set - STOP_WORDS

        print("\n----- Sanitized Keyword Set ---")
        print(f"Total Unique Keywords: {len(signal)}")
        print(f"keywords: {signal}")
