def collapse_dict(d: dict, parent_key="", sep="."):
    """
    Collapse a nested dictionary into dot notation.

    Args:
        d (dict): The dictionary to be collapsed.
        parent_key (str): The key representing the parent level.
        sep (str): The separator to use between keys in the dot notation.

    Returns:
        dict: The collapsed dictionary.
    """
    try:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(collapse_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    except AttributeError:
        print(f"Error: {d} is not a dictionary.")
        raise
