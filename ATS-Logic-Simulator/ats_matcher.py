#adding UI build
import streamlit as st
from pypdf import PdfReader
#imported package
from collections import Counter
import re


#re=regular Expression

#Today(4/17): Finally it is friday so that I can use claude agent to fix this for free! yay!
#progress: polishing sanitize_text, there were some dead code. fixed indentation. delete get_user_input function since it is no longer used.
#polished following: word_to_num, double extration on pdf, duplicated and consusion on the stop words, UI text typo


#Constant=fixed
#stop words contains articles, verbs, some common words, famous company, job platform...etc.
STOP_WORDS = {
    "a", "about", "above", "across", "action", "adobe", "affirmative", "after", "afterwards",
    "again", "against", "airbnb", "all", "almost", "alone", "along", "already", "also",
    "although", "always", "am", "amazon", "among", "amongst", "amount", "an", "and",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "apple", "approach",
    "are", "around", "as", "at", "back", "bachelors", "be", "became", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below",
    "benefit", "beside", "besides", "between", "beyond", "both", "bottom", "brief",
    "build", "business", "but", "by", "can", "candidate", "certain", "certainly",
    "could", "degree", "deliver", "did", "disability", "do", "does", "done", "drive",
    "during", "each", "either", "else", "elsewhere", "employer", "employment", "empty",
    "enough", "equal", "equivalent", "even", "ever", "every", "everyone", "everything",
    "everywhere", "except", "experience", "facebook", "few", "field", "for", "from",
    "further", "get", "give", "go", "google", "had", "hardly", "has", "hasnt", "have",
    "he", "help", "hence", "her", "here", "hereupon", "hers", "herself", "him",
    "himself", "his", "how", "howbeit", "however", "i", "ie", "if", "igt", "impact",
    "in", "inc", "indeed", "instagram", "into", "is", "it", "its", "just", "latter",
    "latterly", "least", "less", "linkedin", "ltd", "masters", "may", "maybe", "me",
    "meantime", "meanwhile", "meta", "microsoft", "might", "minimum", "mission",
    "more", "moreover", "most", "mostly", "must", "my", "mine", "namely", "neither",
    "netflix", "never", "nevertheless", "next", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "nowhere", "of", "off", "often", "on", "only", "onto",
    "opportunity", "or", "other", "otherwise", "our", "ours", "out", "over", "own",
    "partner", "people", "perhaps", "phd", "practical", "preferred", "product",
    "qualification", "qualified", "rather", "re", "relevant", "requirement",
    "responsibility", "role", "s", "said", "salesforce", "same", "see", "seem",
    "seemed", "seeming", "seems", "serious", "several", "shall", "she", "should",
    "since", "so", "some", "somewhere", "still", "strategy", "such", "support",
    "t", "team", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "thence", "there", "thereafter", "thereby", "therefore", "therein",
    "thereupon", "these", "they", "this", "those", "through", "tiktok", "to",
    "together", "too", "towards", "twitter", "uber", "under", "until", "up",
    "upon", "very", "via", "vision", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "why", "will", "with", "work", "would", "yet", "you",
    "your", "yours", "veteran"
}
#Some common legal terms that appears in JD, for right now I have separated from the list
HR_LEGAL_FLUFF = {
    "gender", "compensation", "accommodation", "applicable", "understand",
    "identify", "influence", "insight", "development", "disability",
    "orientation", "sexual", "identity", "protected", "status", "benefit",
    "equal", "opportunity", "opportunities", "employer", "veteran", "law", "regulation",
    "salary", "bonus", "equity", "health", "dental", "vision", "inclusive",
    "diverse", "environment", "culture", "background", "employee"
}

GAME_JD_FLUFF = {
    "bring", "big", "test", "class", "information", "creating","www"
}
STOP_WORDS.update(GAME_JD_FLUFF)

STOP_WORDS.update(HR_LEGAL_FLUFF)
#Add more vocabs in stem_exclusions to prevent chopping all the words! I tried to put
#elif word.endswith("es") and len(word) > 4: stemmed_list.append(word[:-3] + "y") this ends up creating businesy
#wonder if there is better logic?
STEM_EXCLUSION = {
    "analysis", "analytics", "bias", "calculus", "corpus", "census",
    "status", "process", "success", "access", "physics", "mathematics", "statistics", "focus",
    "class", "address", "addressing", "alias", "atlas", "canvas", "chaos", "crisis", "electronics",
    "ethics", "gas", "glass", "graphics", "hypothesis", "iris", "lens", "loss", "mass", "minus",
    "pass", "plus", "progress", "radius", "stress", "thesis", "witness", "wellness", "fitness",
    "languages",
    "database", "expertise", "compliance", "governance", "aws", "os", "ios", "macos", "jenkins",
    "pandas", "keras", "redis", "postgres", "kubernetes",
    "business", "businesses", "technology", "technologies", "series", "species"
}

word_to_num = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"
}

#Function=fixed

def sanitize_text(raw_text):
    clean_input = raw_text.lower()
    word_list = re.split(r"[^a-zA-Z0-9]+", clean_input)

    stemmed_list = []
    for word in word_list:
        if len(word)<2:
            continue

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
    resume_file = st.file_uploader("Upload your Resume here", type=['pdf', 'txt'])
    st.markdown("""
    <style>
    
    [data-testid = "stFileUploader"] section{
        padding: 215px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if jd_text and resume_file:
    years_req = 0
    match_score = 0
    if resume_file.name.endswith(".pdf"):
        pdf_reader = PdfReader(resume_file)
        resume_text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                resume_text += content
    else:
        resume_text = resume_file.read().decode("utf-8")
    #resume cleaner
    resume_words = sanitize_text(resume_text)
    resume_counts = Counter(resume_words)
    resume_signal = set(resume_counts.keys())
    #add word=number converter
    processed_resume = resume_text.lower()
    for word, digit in word_to_num.items():
        processed_resume = re.sub(r'\b'+ word + r'\b', digit, processed_resume)

    #experience detector
    resume_years_detected = extract_experience(processed_resume)
    if resume_years_detected:
        years_candidate = max([int(y) for y in resume_years_detected])
    else: years_candidate = 0

    #JD related.
    jd_years_req = extract_experience(jd_text)
    jd_words = sanitize_text(jd_text)
    jd_counts = Counter(jd_words)
    clean_counts = Counter({k: v for k, v in jd_counts.items() if k not in STOP_WORDS})
    jd_signal = set(clean_counts.keys())

    if jd_years_req:
        years_req = max([int(y) for y in jd_years_req])

    exp_delta = years_candidate - years_req

    matched_keywords = jd_signal & resume_signal
    missing_keywords = jd_signal - matched_keywords
    total_weight = sum(clean_counts.values())
    match_weight = sum(clean_counts[word] for word in matched_keywords)

    match_score = (match_weight / total_weight) * 100 if jd_signal else 0

    with topcol1:
        st.metric(label="Match Score", value=f"{match_score: .2f}%")
    with topcol2:
        st.metric(label="Required Experience", value=f"{years_req}")
    # no logic yet
    with topcol3:
        st.metric(label="Candidate Experience", value=f"{years_candidate}yrs", delta=f"{exp_delta}yrs" if exp_delta != 0 else None)
else:
    topcol1.metric(label="Match Score", value ="0%")
    topcol2.metric(label="Required Experience", value ="0 yrs")
    topcol3.metric(label="Candidate Experience", value = "0 yrs")
#line below the column
st.divider()

if jd_text and resume_file:
    st.subheader("Missing Keywords (To boost your score)")

    high_value_missing = sorted(missing_keywords, key=lambda x: clean_counts[x], reverse=True)[:10]

    if high_value_missing:
        cols = st.columns(5)
        for i, word in enumerate(high_value_missing):
            cols[i % 5].info(f"**{word}**")
    else:
        st.success("You've captured all critical keywords! Perfect match! :D")







