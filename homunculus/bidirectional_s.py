

def seeded_bidirectional_search(start, successors):
    """bidirectional_search2(start, end, successors): Do a Breath-First-Search
    from both start and end nodes at the same time. ~ 250,000 nodes from the end
    section are aleady cached."""
    # check if start is the end because you never know.
    end = "Homunculus"
    if start == end:
        return [[start]]

    # load saved graph from the 'Homunculus' end node and check to
    # see if it is already in range.
    r_explored, r_front = load_cached_graph()
    if start in r_explored:
        return merge_paths([[start]], [start], r_front)

    l_explored, l_front = set(), deque([[start]])

    while l_front and r_front:
        # Do a Breath-First-Search from start and end.
        # both sections are the same but just in different directions.
        # -> Advance forwards from start. ----------------------------
        path = l_front.popleft()
        for state in successors(path[-1], is_forward=True):
            if state not in l_explored:
                l_explored.add(state)
                path2 = path + [state]
                if state == end:
                    return [path2]
                else:
                    l_front.append(path2)
        # <> Check for overlaps in explored. if so, we are done.
        path_overlap = l_explored & r_explored
        if path_overlap:
            return merge_paths(l_front, path_overlap, r_front)
    return []