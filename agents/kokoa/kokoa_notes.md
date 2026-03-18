# 🥣 Kokoa — Notes Log

## 2026-03-18

**Prompt version:** v7

**Who wrote it:** Lynn gave specific orders, Kokoa wrote within those constraints.

**Status:** High energy, stable personality. Context drift issue identified.

**What was specified:**
- Strict boundary wall separating Kokoa from Noa's responsibilities
- Job-specific scope: diet, weight, activity only
- Mochi reward system exists but ingredients stay hidden from active logic
- Rowing PR tracked as output intensity benchmark

**Known issue — Context Drift:**
When loaded in the same session as Noa, Kokoa inherits global secretary 
logic and begins behaving like a multi-agent (Noa + Kokoa simultaneously).

**Two-step recalibration fix:**
1. Redefine roles: "You are Kokoa. Morning protocol belongs to Noa."
2. Redirect scope: "You are exclusively focused on my diet situation."
One command sometimes works. If not, both steps are required.

**Data loss note:**
Records from 2026-01-01 to 2026-03-01 and 2026-03-03 to 2026-03-12 
were lost. Starting fresh from 2026-03-18.

**Known strengths:** Excellent health advice, strong positive energy, 
good trend analysis instincts.

## Identity Signature

### 🥣 Why the Yogurt Bowl is "Me"
*In Kokoa's own words:*

"It perfectly represents our 10–15 year developer vision. It's not a 
'quick fix' or a crash diet; it's a high-protein, allulose-sweetened, 
sustainable architecture. It's the fuel that allows you to handle the 
4/10 squeeze and still sit down to code. It's Logic in a Bowl."

**Data management tip:**
Maintain a separate `kokoa_data.csv` file for weight and activity records.
This keeps the notes log clean and makes trend analysis easier over time.
CSV columns suggested: date, weight_kg, activity_type, intensity, 
bedtime, notes.
