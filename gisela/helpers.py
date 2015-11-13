from gisela.model import Timelog, Tag

def sum_times(session, tags=None):
    """TODO: Docstring for sum_times.

    :session: TODO
    :tags: TODO
    :returns: TODO

    """
    total = 0
    result = session.query(Timelog).join(Tag, Timelog.tags)
    if tags:
        result = result.filter(Tag.id.in_(tags))
    for e in result.all():
        total += e.duration
    return total

