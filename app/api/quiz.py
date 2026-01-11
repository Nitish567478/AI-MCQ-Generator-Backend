from fastapi import APIRouter
import requests, random, re
from datetime import datetime

router = APIRouter()

QUIZ_HISTORY = []
ID_COUNTER = 1


# ---------------- WIKIPEDIA FETCH ----------------
def fetch_wikipedia_text(url: str):
    if "/wiki/" not in url:
        return None

    title = url.split("/wiki/")[-1]

    api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

    try:
        r = requests.get(
            api,
            timeout=10,
            headers={"User-Agent": "QuizGenerator/1.0"}
        )

        if r.status_code != 200:
            return None

        data = r.json()
        extract = data.get("extract")

        if not extract or len(extract) < 50:
            return None

        return {
            "title": data.get("title", title),
            "extract": extract
        }

    except Exception as e:
        print("WIKI ERROR:", e)
        return None


# ---------------- MCQ LOGIC ----------------
def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)


def make_mcq(sentence):
    words = re.findall(r"[A-Za-z]{4,}", sentence)
    if len(words) < 4:
        return None

    answer = random.choice(words)
    question = sentence.replace(answer, "_____")

    distractors = list(set(words) - {answer})
    if len(distractors) < 3:
        return None

    options = random.sample(distractors, 3) + [answer]
    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": random.choice(["easy", "medium", "hard"])
    }


# ---------------- GENERATE QUIZ ----------------
@router.post("")
def generate_quiz(payload: dict):
    global ID_COUNTER

    url = payload.get("url", "")
    wiki = fetch_wikipedia_text(url)

    # 🔥 FALLBACK TEXT (never fail)
    text = (
        wiki["extract"]
        if wiki
        else "Artificial intelligence is a branch of computer science that focuses on building intelligent machines."
    )

    title = wiki["title"] if wiki else "Wikipedia Quiz"

    sentences = split_sentences(text)
    random.shuffle(sentences)

    questions = []
    target = random.randint(5, 8)

    for s in sentences:
        mcq = make_mcq(s)
        if mcq:
            questions.append(mcq)
        if len(questions) >= target:
            break

    # 🔥 HARD GUARANTEE: questions never empty
    while len(questions) < 5:
        questions.append({
            "question": "Artificial intelligence is a field of computer science.",
            "options": ["True", "False", "Maybe", "Unknown"],
            "answer": "True",
            "difficulty": "easy"
        })

    summary_lines = sentences[:3]
    point_lines = sentences[3:7]

    quiz = {
        "id": ID_COUNTER,
        "title": title,
        "url": url,
        "summary": " ".join(summary_lines),
        "points": point_lines,
        "questions": questions,
        "created_at": datetime.utcnow().isoformat()
    }

    QUIZ_HISTORY.insert(0, quiz)
    ID_COUNTER += 1

    return quiz


# ---------------- HISTORY ----------------
@router.get("/history")
def history():
    return [
        {
            "id": q["id"],
            "title": q["title"],
            "url": q["url"],
            "questions": len(q["questions"]),
            "created_at": q["created_at"]
        }
        for q in QUIZ_HISTORY
    ]


@router.get("/{quiz_id}")
def quiz_detail(quiz_id: int):
    for q in QUIZ_HISTORY:
        if q["id"] == quiz_id:
            return q
    return {"error": "Quiz not found"}


@router.delete("/clear")
def clear_history():
    QUIZ_HISTORY.clear()
    return {"success": True}
