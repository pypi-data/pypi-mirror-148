
__all__ = ('Member',)


class Member:
    """
    The member (e.g care home) an enquiry is associated with.
    """

    def __init__(self, id, name, postcode):

        self.id = id
        self.name = name
        self.postcode = postcode

    def __str__(self):
        return f'{self.name} @ {self.postcode} (#{self.id})'

    @classmethod
    def from_json_type(cls, obj):
        return cls(obj['id'], obj['name'], obj['postcode'])
