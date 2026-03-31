
from better_profanity import profanity
from fastapi import HTTPException


profanity.load_censor_words()
profanity.add_censor_words(["bc", "mc", "chutiya"])  


def validate_content(text: str):
   
    if profanity.contains_profanity(text):
        raise HTTPException(
            status_code=400,
            detail="Inappropriate or vulgar content is not allowed."
        )

def filter_doubts(doubts, search=None, sort=None, limit=None):

    if search:
        doubts = [
            d for d in doubts
            if search.lower() in d["title"].lower()
            or search.lower() in d["description"].lower()
        ]

    if sort == "upvotes":
        doubts = sorted(doubts, key=lambda x: x.get("upvotes", 0), reverse=True)

    if limit:
        doubts = doubts[:limit]

    return doubts