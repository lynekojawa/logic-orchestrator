from collections import Counter

#Today(4/8) we will change the match the with the weighted the keywords.
#problems with s characters

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
    clean_buffer = []
    for character in lower_raw_text:
        if character.isalnum() or character in (" ", "-"):
            clean_buffer.append(character)

    clean_text = "".join(clean_buffer)
    word_list = clean_text.split()
    stemmed_list =[]
    for word in word_list:
        if word.endswith('s') and not word.endswith('ss') and len(word) > 3:
            stemmed_list.append(word[:-1])
        else:
            stemmed_list.append(word)
    return list(word_list)


#Change full_jd = input to full_jd = get_user_input
#It was working well in pycharm's environment, hoewever it may only read first line of JD on the web environment.
if __name__ == "__main__":
    full_jd = get_user_input("Paste your Job Description here")

    if not full_jd.strip():
        print("Error: No input provided")
    else:
        full_resume = get_user_input("---Paste your resume here (Type 'Done' to finish---)")
        if not full_resume.strip():
            print("Error: No resume provided.")
        else:
            jd_words = sanitize_text(full_jd)
            jd_counts= Counter(jd_words)
            #List basket with condition, items not item
            clean_counts = Counter({k: v for k, v in jd_counts.items() if k not in STOP_WORDS})
            jd_signal = set(clean_counts.keys())

            resume_words = sanitize_text(full_resume)
            resume_counts = Counter(resume_words)
            resume_signal = set(resume_counts.keys())

#Build ATS coverage: modified Jaccard |Resume\intersect JD|/|JD|

            matched_keywords = jd_signal & resume_signal
            missing_keywords = jd_signal - matched_keywords
            match_score = (len(matched_keywords) / len(jd_signal)) * 100 if jd_signal else 0

            print(f"Match Score {match_score}%")
            print(f"Matched({len(matched_keywords)}):{matched_keywords}")
            print(f"Missing({len(missing_keywords)}):{missing_keywords}")
            print(f"Top 5 Keywords: {clean_counts.most_common(5)}")


