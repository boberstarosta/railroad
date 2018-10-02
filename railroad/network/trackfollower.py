
def follow(segment, t, backwards, break_func, results=None, elapsed_distance=0.0):
    if results is None:
        results = []

    if break_func(segment, t, backwards):
        return results

    if backwards:
        next_node = segment.nodes[0]
        next_elapsed_distance = elapsed_distance + t*segment.length
    else:
        next_node = segment.nodes[1]
        next_elapsed_distance = elapsed_distance + (1 - t)*segment.length
    next_segment = next_node.other_segment(segment)
    if next_segment is None:
        return results + ["end"]
    else:
        if next_node is next_segment.nodes[0]:
            next_t = 0
            next_backwards = False
        else:
            next_t = 1
            next_backwards = True

        return follow(next_segment, next_t, next_backwards, break_func, results)
