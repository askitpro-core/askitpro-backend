def filter_doubts(doubts, search=None, sort=None, limit=None):
    # Search in text only
    if search:
        needle = search.lower()
        doubts = [
            d for d in doubts
            if needle in d.text.lower()
        ]

    # Sort by upvotes
    if sort == "upvotes":
        doubts = sorted(doubts, key=lambda x: x.upvotes, reverse=True)

    # Limit results
    if limit:
        doubts = doubts[:limit]

    return doubts