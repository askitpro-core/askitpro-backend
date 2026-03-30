from better_profanity import profanity
from fastapi import HTTPException

# Load default + custom words
profanity.load_censor_words()
profanity.add_censor_words(["bc", "mc", "chutiya"])  


def validate_content(text: str):
   
    if profanity.contains_profanity(text):
        raise HTTPException(
            status_code=400,
            detail="Inappropriate or vulgar content is not allowed."
        )