from collections import Counter
import re

#re=regular Expression
#Today(4/10) We are going to fix following three problems pulled by Dante(Claude): prob 1: stemmer prob 2: minor experience error prob
# 3: Missing keywords output is incomplete
#Progress: create constant STEM_EXCLUSION to prevent aggressive stemming, add the larger filter so that when the experience level is not detected
#this will comeout as no number detected, Added more words in constant, add one more rule with word done with es, changed the output format
#the es stemming rule maybe too aggressive suggestions 1. add some es words like series, aries, species into stop words or 2. maybe other?
#Extension to phase 4 to fix  2. Dashboard UI so that user can use this easier 3. Error Resilieness.
#few question arose: on the job search site how does that 40%, 60% score is possible, what is actual setting for the real company?

#Constant=fixed
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
            "nor", "not", "own", "same", "than", "too", "very", "s", "t", "can", "will",
            "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone",
            "along", "already", "also", "although", "always", "among", "amongst", "amount", "any", "anyhow",
        "anyone", "anything", "anyway", "anywhere", "around", "back", "became", "become", "becomes", "becoming",
        "beforehand", "behind", "being", "below", "beside", "besides", "beyond", "both", "bottom", "brief",
        "certain", "certainly", "done", "during", "each", "either", "else", "elsewhere", "empty", "enough",
        "even", "ever", "every", "everyone", "everything", "everywhere", "except", "further", "get", "give",
        "go", "had", "hardly", "hasnt", "hence", "hereupon", "herself", "himself", "howbeit", "however",
        "ie", "inc", "indeed", "latter", "latterly", "least", "less", "ltd", "maybe", "meantime",
        "meanwhile", "might", "moreover", "mostly", "namely", "neither", "never", "nevertheless", "next", "nobody",
        "none", "noone", "nothing", "nowhere", "often", "otherwise", "perhaps", "rather", "re", "said",
        "see", "seem", "seemed", "seeming", "seems", "serious", "several", "since", "somewhere", "still",
        "thence", "thereafter", "thereby", "therefore", "therein", "thereupon", "together", "towards", "upon", "via"
        }
STEM_EXCLUSION = {
    "analysis", "analytics", "business", "bias", "pandas", "calculus", "corpus", "census",
    "status", "process", "success", "access", "physics", "mathematics", "statistics", "focus",
    "class", "address", "addressing", "alias", "atlas", "canvas", "chaos", "crisis", "electronics",
    "ethics", "gas", "glass", "graphics", "hypothesis", "iris", "lens", "loss", "mass", "minus",
    "pass", "plus", "progress", "radius", "stress", "thesis", "witness", "wellness", "fitness",
    "database", "expertise", "compliance", "governance", "aws", "os", "ios", "macos", "jenkins",
    "pandas", "analysis", "bias", "calculus", "corpus", "census", "languages"
    }
#Function=fixed
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
    stemmed_list = []
    for word in word_list:
        if word in STEM_EXCLUSION:
            stemmed_list.append(word)
        elif word.endswith("es") and len(word) > 4:
            stemmed_list.append(word[:-2])
        elif word.endswith('s') and not word.endswith('ss') and len(word) > 3:
            stemmed_list.append(word[:-1])
        else:
            stemmed_list.append(word)
    return stemmed_list
#New function for years of experience finder
def extract_experience(text):
    exp_pattern = r"(\d+)\+?\s*(?:years?|yrs?)"
    return re.findall(exp_pattern, text, re.IGNORECASE)

#Inputs=variables
if __name__ == "__main__":
    full_jd = get_user_input("Paste your Job Description here")

    if not full_jd.strip():
        print("Error: No input provided")
    else:
        jd_years_req = extract_experience(full_jd)
        if jd_years_req:
            years_req = max([int(y) for y in jd_years_req])
            if years_req != 0:
                print(f"\n Detected Experience Requirement: {years_req}+ years")
            else:
                print("No Experience Requirement")
        else:
            print("No Experience level provided")

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


#Build ATS coverage: modified weighted sums so that it will be more accurate.

            matched_keywords = jd_signal & resume_signal
            missing_keywords = jd_signal - matched_keywords
            total_weight = sum(clean_counts.values())
            match_weight = sum(clean_counts[word] for word in matched_keywords)
            match_score = (match_weight / total_weight) * 100 if jd_signal else 0

#Outputs=The results from running a code
            print(f"\n ***[ATS Analysis Results]***")
            print(f"Match Score {match_score:.2f}%")
#Outputs with sorted
            high_value_missing = sorted(missing_keywords, key=lambda x: clean_counts[x], reverse=True)[:10]

            print(f"\nMatched Keywords({len(matched_keywords)})")
            for word in sorted(matched_keywords):
                print(f" - {word}")

            print(f"\n Top 10 Missing Keywords: ")
            for word in high_value_missing:
                print(f" - {word}: mentioned {clean_counts[word]} times in JD")


