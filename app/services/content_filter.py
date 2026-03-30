def filter_doubts(doubts, search=None, sort=None, limit=None):
    # Search in title + description
    if search:
        doubts = [
            d for d in doubts
            if search.lower() in d.title.lower()
            or search.lower() in d.description.lower()
        ]

    # Sort by upvotes
    if sort == "upvotes":
        doubts = sorted(doubts, key=lambda x: x.upvotes, reverse=True)

    # Limit results
    if limit:
        doubts = doubts[:limit]

    return doubts