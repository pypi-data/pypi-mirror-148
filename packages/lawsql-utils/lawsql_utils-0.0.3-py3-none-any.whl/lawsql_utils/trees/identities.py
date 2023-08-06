def set_tree_ids(
    nodes: list[dict],
    parent_id: str = "1",
    child_key: str = "units",
):
    """Recursive function updates nodes in place since list/dicts are mutable. Assumes that the nodes reprsent a deeply nested json, e.g.

    For each node in the `nodes` list, it will add a new `id` key and will increment according to its place in the tree structure.

    If node id "1.1" has child nodes, the first child node will be "1.1.1".

    The root of the tree will always be "1", unless the `parent_id` is set to a different string.

    The child key of the tree will always be "units", unless the `child_key` is set to a different string.

    Args:
        nodes (list[dict]): The list of dicts that
        parent_id (str, optional): The root node id. Defaults to "1".
        child_key (str, optional): The node which represents a list of children nodes. Defaults to "units".

    >>> sample_unit_list_data: list[dict] = [
            {
                "item": "Preliminary Title",
                "units": [
                    {
                        "item": "Chapter 1",
                        "caption": "Effect and Application of Laws",
                        "units": [
                            {
                                "item": "Article 1",
                                "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
                            },
                            {
                                "item": "Article 2",
                                "content": "Laws shall take effect after fifteen days following the completion of their publication either in the Official Gazette or in a newspaper of general circulation in the Philippines, unless it is otherwise provided. (1a)\n",
                            },
                        ],
                    }
                ],
            }
        ]
    >>> set_tree_ids(sample_unit_list_data)
    >>> sample_unit_list_data # note the additional `id` key
        [
            {
                'item': 'Preliminary Title',
                'units': [
                    {'item': 'Chapter 1',
                    'caption': 'Effect and Application of Laws',
                    'units': [
                        {'item': 'Article 1',
                        'content': 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
                        'id': '1.1.1.1'},
                        {'item': 'Article 2',
                        'content': 'Laws shall take effect after fifteen days following the completion of their publication either in the Official Gazette or in a newspaper of general circulation in the Philippines, unless it is otherwise provided. (1a)\n',
                        'id': '1.1.1.2'}
                    ],
                    'id': '1.1.1'}
                ],
                'id': '1.1'
            }
        ]
    """
    if isinstance(nodes, list):
        for counter, node in enumerate(nodes, start=1):
            node["id"] = f"{parent_id}.{str(counter)}"
            if node.get(child_key, None):
                set_tree_ids(node[child_key], node["id"])


def get_tree_node(
    nodes: list[dict],
    query_id: str,
    child_key: str = "units",
) -> dict | None:
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
        if units := node.get(child_key, None):
            if match := get_tree_node(units, query_id):
                return match
