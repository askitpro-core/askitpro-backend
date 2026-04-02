from sentence_transformers import SentenceTransformer, util
import uuid
import torch

# 1. LOAD ONCE: This stays awake in the server's RAM
print("🧠 Waking up Local NLP Engine...")
model = SentenceTransformer('all-MiniLM-L6-v2')
THRESHOLD = 0.55

# --- NEW: AUTO-TAGGER SYSTEM ---
# 1. Define your categories
AVAILABLE_TAGS = [
    # Core Academics (CSE AIML & Tech)
    "Python", "C++", "DSA", "Machine Learning", "Web Dev", "UI/UX", 
    
    # The Grind
    "Placements", "Internships", "Exams", "Assignments", "Attendance",
    
    # Campus & Events
    "Converge", "Kurukshetra", "Campus Life", "General"
]

# 2. Pre-load the tag brain (Do this once so it's lightning fast)
print("🏷️ Loading Tag Embeddings...")
tag_embeddings = model.encode(AVAILABLE_TAGS)

def generate_auto_tag(doubt_text: str) -> str:
    """
    Compares the doubt against our list of tags and returns the best match.
    """
    doubt_embedding = model.encode(doubt_text)
    
    # Compare the doubt against ALL tags at the exact same time
    scores = util.cos_sim(doubt_embedding, tag_embeddings)[0]
    
    # Find the index of the highest score
    best_match_idx = torch.argmax(scores).item()
    best_score = scores[best_match_idx].item()
    
    # If the score is too low, it means it doesn't match any of our tags well
    if best_score < 0.30:  # Lower threshold because comparing a sentence to a single word is harder
        return "General"
        
    return AVAILABLE_TAGS[best_match_idx]

def find_cluster_for_doubt(new_doubt_text: str, existing_room_doubts: list) -> str:
    """
    Reads a new doubt and compares it against existing doubts.
    Returns an existing cluster_id if it matches, or generates a new one.
    """
    if not existing_room_doubts:
        return str(uuid.uuid4())

    print(f"Analyzing: '{new_doubt_text}'...")
    new_embedding = model.encode(new_doubt_text)

    # Check against existing doubts
    for doubt in existing_room_doubts:
        # FIXED: Changed doubt.text to doubt.description to match your Database
        existing_embedding = model.encode(doubt.description) 
        score = util.cos_sim(new_embedding, existing_embedding)[0][0].item()
        
        if score >= THRESHOLD:
            print(f"🔥 Match found! Score: {score:.2f} (Matched with: '{doubt.description}')")
            return doubt.cluster_id

    print("New topic detected.")
    return str(uuid.uuid4())