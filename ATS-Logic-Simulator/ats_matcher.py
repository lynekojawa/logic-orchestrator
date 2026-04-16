#adding UI build
import streamlit as st
from pypdf import PdfReader
#imported package
from collections import Counter
import re


#re=regular Expression

#Today(4/15): 1. adding logic gaps in col3 V 2. fixing minor detail 3. add top 10 missed word V 4. adding pdf to txt converter V
#progress: add logic gap, added top tem missing words feature,
#!! my logic cannot detect numbers in words eg: more than six years is not detected. problem resolved
#For categorizing vocabs, so i thought it was inefficient to update those words in stop words with creating new sets and update
#but after I noticed it seems like efficient in control those key words by the types of industry standard, and will help users to get better
#match score. There are two many words I am missing...
#Generally, I just grab any JD from linkedin, and I got one company matched 20.39% so let's see if I am getting a rejection letter from them!


#Constant=fixed
#stop words contains articles, verbs, some common words, famous company, job platform...etc.
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
        "thence", "thereafter", "thereby", "therefore", "therein", "thereupon", "together", "towards", "upon", "via",
        "meta", "google", "amazon", "apple", "netflix", "microsoft", "uber", "airbnb", "igt",
        "linkedin", "tiktok", "twitter", "facebook", "instagram", "adobe", "salesforce",
        "team", "people", "business", "product", "approach", "build", "partner", "help",
        "work", "support", "mission", "vision", "impact", "strategy", "deliver", "drive",
        "opportunity", "requirement", "responsibility", "qualified", "candidate", "role",
        "experience", "preferred", "minimum", "qualification", "equal", "employment",
        "opportunity", "affirmative", "action", "employer", "disability", "veteran",
        "relevant", "field", "equivalent", "practical", "degree", "bachelors", "masters", "phd"
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
def get_user_input(prompt_message):
    print(prompt_message)

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    return " ".join(lines)

#Changed split to re.split
def sanitize_text(raw_text):
    lower_raw_text = raw_text.lower()
    clean_buffer = []
#Change old clean_buffer to one line to be efficient and save line

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
    resume_file = st.file_uploader("Upload your Job Description here", type=['pdf', 'txt'])
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
                resume_text += page.extract_text()
    else:
        resume_text = resume_file.read().decode("utf-8")
    #resume cleaner
    resume_words = sanitize_text(resume_text)
    resume_counts = Counter(resume_words)
    resume_signal = set(resume_counts.keys())
    #add word=number converter
    processed_resume = resume_text.lower()
    for word, digit in word_to_num.items():
        processed_resume = processed_resume.replace(word, digit)

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







