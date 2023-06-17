from typing import Union


def get_object_phrase(doc) -> Union[str, None]:
    """Get the first identified subject from the given doc.

    Parameters
    ----------
    doc

    Returns
    -------

    """
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]
    return None


def get_subject_phrase(doc):
    """

    Parameters
    ----------
    doc

    Returns
    -------

    """
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def has_verb(doc):
    for token in doc:
        if token.pos_ == "VERB":
            return True, token

    return False, None