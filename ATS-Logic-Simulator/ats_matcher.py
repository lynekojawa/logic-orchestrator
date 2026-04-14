#adding UI build
import streamlit as st
#imported package
from collections import Counter
import re

#re=regular Expression
#Today(4/14): new monitor arrived! we are starting phase 4 for building a UI today so that this will look pretty lol.
#progress: install streamlit,
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

#operator for streamlit
st.set_page_config(layout="wide")
st.title("ATS Visual Commander Dashboard")
st.write("ATS logic is now visual.")
#Room first furniture later
topcol1, topcol2, topcol3 = st.columns(3)

left_JD, right_Resume=st.columns(2)
with left_JD:
    jd_text = st.text_area("Paste your Job Description here", height=500)
with right_Resume:
    resume_file = st.file_uploader("Upload your Job Description here", type=['pdf', 'txt'])

if jd_text and resume_file:
    years_req = 0
    match_score = 0
    if resume_file is not None:
        resume_text = resume_file.read().decode("utf-8")

    resume_words = sanitize_text(resume_text)
    resume_counts = Counter(resume_words)
    resume_signal = set(resume_counts.keys())

    jd_years_req = extract_experience(jd_text)
    jd_words = sanitize_text(jd_text)
    jd_counts = Counter(jd_words)
    clean_counts = Counter({k: v for k, v in jd_counts.items() if k not in STOP_WORDS})
    jd_signal = set(clean_counts.keys())
    if jd_years_req:
        years_req = max([int(y) for y in jd_years_req])

    matched_keywords = jd_signal & resume_signal
    missing_keywords = jd_signal - matched_keywords
    total_weight = sum(clean_counts.values())
    match_weight = sum(clean_counts[word] for word in matched_keywords)

    match_score = (match_weight / total_weight) * 100 if jd_signal else 0
    high_value_missing = sorted(missing_keywords, key=lambda x: clean_counts[x], reverse=True)[:10]
    with topcol1:
        st.metric(label="Match Score", value=f"{match_score: .2f}%")
    with topcol2:
        st.metric(label="Required Experience", value=f"{years_req}")
    # no logic yet
    with topcol3:
        st.metric(label="Candidate Experience", value="0")
else:
    topcol1.metric(label="Match Score", value ="0%")
    topcol2.metric(label="Required Experience", value ="0 yrs")
    topcol3.metric(label="Candidate Experience", value = "0 yrs")









