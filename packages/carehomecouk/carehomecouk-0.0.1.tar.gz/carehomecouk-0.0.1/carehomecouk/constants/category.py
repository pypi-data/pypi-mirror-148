from enum import Enum

__all__ = ('Category',)


class Category(Enum):

    GENERAL_ENQUIRY = 1
    BROCHURE_REQUEST = 2
    CARE_ENQUIRY = 4
    JOB_ENQUIRY = 5
    ONSITE_TOUR_BOOKING = 20
    REMOTE_TOUR_BOOKING = 21
