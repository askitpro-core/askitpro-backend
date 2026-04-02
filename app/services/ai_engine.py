from sentence_transformers import SentenceTransformer, util
import uuid

# 1. LOAD ONCE: This stays awake in the server's RAM
print("🧠 Waking up Local NLP Engine...")
model = SentenceTransformer('all-MiniLM-L6-v2')
THRESHOLD = 0.55

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