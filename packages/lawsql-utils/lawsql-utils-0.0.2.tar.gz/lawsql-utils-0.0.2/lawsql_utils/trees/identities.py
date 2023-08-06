def set_tree_ids(nodes: list[dict], parent_id: str = "1"):
    """Recursive function updates  nodes in place since list/dicts are mutable. Adds an string id to each deeply nested json whereby each string id is in the following format: "1.1". If node id "1.1" has child nodes, the first child node will be "1.1.1". The root of the tree will always be "1".

    Args:
        nodes (list[dict]): Each dict in the list may have `units` key
        parent_id (str): This is the parent of the node being evaluated
    """
    for counter, node in enumerate(nodes, start=1):
        node["id"] = f"{parent_id}.{str(counter)}"
        if node.get("units", None):
            set_tree_ids(node["units"], node["id"])


def get_tree_node(nodes: list[dict], query_id: str) -> dict | None:
    """Return the first node matching the `query_id`, if it exists

    Args:
        nodes (list[dict]): The deeply nested json list
        query_id (str): The id previously set by `set_tree_ids()`

    Returns:
        dict | None: The first node matching the query_id or None
    """
    for node in nodes:
        if node["id"] == query_id:
            return node
        if units := node.get("units", None):
            if match := get_tree_node(units, query_id):
                return match
