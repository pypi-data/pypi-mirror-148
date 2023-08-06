import datetime
from enum import Enum

from .category import Category
from .member import Member

__all__ = ('Enquiry',)


class Enquiry:

    def __init__(
        self,
        id,
        category,
        member,
        to_email,
        from_email,
        date_time,
        content,
        first_name,
        surname,
        address1,
        address2,
        address3,
        town,
        postcode,
        telephone,
        is_anonymised,
        booking_date=None,
        booking_time=None,
        booking_type=None,
    ):

        self.id = id
        self.category = category
        self.member = member
        self.to_email = to_email
        self.from_email = from_email
        self.date_time = date_time
        self.content = content
        self.first_name = first_name
        self.surname = surname
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.town = town
        self.postcode = postcode
        self.telephone = telephone
        self.is_anonymised = is_anonymised
        self.booking_type = booking_type
        self.booking_date = booking_date
        self.booking_time = booking_time

    def __str__(self):
        return (
            f'[{self.category.name}] for {self.member.name}: '
            f'{self.full_name} (#{self.id})'
        )

    @property
    def full_name(self):
        parts = []

        if self.first_name:
            parts.append(self.first_name)

        if self.surname:
            parts.append(self.surname)

        return ' '.join(parts) or 'Name not given'

    @classmethod
    def from_json_type(cls, obj):

        date_time = datetime.datetime.strptime(
            obj['date'],
            '%Y-%m-%d %H:%M:%S'
        )

        category_specific_data = obj.get('categorySpecificData', {})

        booking_date = None
        if category_specific_data.get('bookingDate'):
            parts = category_specific_data['bookingDate'].split(' ')
            booking_date = datetime.datetime.strptime(
                f'{parts[1][:2]} {parts[2]} {parts[3]}',
                '%d %B %Y'
            ).date()

        booking_time = None
        if category_specific_data.get('bookingTime'):
            booking_date = datetime.datetime.strptime(
                category_specific_data['bookingTime'],
                '%H:%M %p'
            ).time()

        return cls(
            obj['id'],
            Category.from_json_type(obj['category ']),
            Member.from_json_type(obj['member']),
            obj['to'],
            obj['from'],
            date_time,
            obj['content'],
            obj['firstName'],
            obj['surname'],
            obj['address1'],
            obj['address2'],
            obj['address3'],
            obj['town'],
            obj['postcode'],
            obj['telephone'],
            obj['isAnonymised'],
            booking_type=category_specific_data.get('bookingType'),
            booking_date=booking_date,
            booking_time=booking_time
        )

    @classmethod
    def many(
        cls,
        api_client,
        date_time_from=None,
        date_time_to=None,
        exclude_anonymised=None,
        category_id=None
    ):

        params = {}

        if date_time_from is not None:
            params['dateFrom'] = date_time_from.strftime('%Y-%m-%dT%H:%M:%S')

        if date_time_to is not None:
            params['dateTo'] = date_time_to.strftime('%Y-%m-%dT%H:%M:%S')

        if exclude_anonymised is not None:
            params['excludeAnonymised'] \
                    = 'true' if exclude_anonymised else 'false'

        if category_id is not None:
            if isinstance(category_id, Enum):
                category_id = category_id.value
            params['categoryId'] = category_id

        objs = api_client('enquiry', params=params)

        return [cls.from_json_type(obj) for obj in objs['data']]
