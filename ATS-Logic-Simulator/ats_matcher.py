#Fixed Stop_Words
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

#Define new functions so that we won't double the code
def get_user_input(prompt_message):
    print(prompt_message)

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    return " ".join(lines)

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
    full_jd = input("Paste your Job Description here")

    if not full_jd.strip():
        print("Error: No input provided")
    else:
        full_resume = get_user_input("---Paste your resume here (Type 'Done' to finish---)")
        if not full_resume.strip():
            print("Error: No resume provided.")
        else:
            jd_signal = sanitize_text(full_jd) - STOP_WORDS
            resume_signal = sanitize_text(full_resume) - STOP_WORDS
#Build ATS coverage: modified Jaccard |Resume\intersect JD|/|JD|
            #intersection
            matched_keywords = jd_signal & resume_signal
            #difference?
            missing_keywords = jd_signal - matched_keywords
            #score
            match_score = (len(matched_keywords) / len(jd_signal)) * 100 if jd_signal else 0

            print(f"Match Score {match_score}%")
            print(f"Matched({len(matched_keywords)}):{matched_keywords}")
            print(f"Missing({len(missing_keywords)}):{missing_keywords}")



