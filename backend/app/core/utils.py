def escape_search(query: str) -> str:
    """Escape SQL LIKE wildcards to prevent injection."""
    return query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
