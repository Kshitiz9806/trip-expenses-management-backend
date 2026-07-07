from enum import Enum

class CategoryEnum(str, Enum):
    FOOD = "food"
    CABS = "cabs"
    INCIDENTAL = "incidental"


class PaymentTypeEnum(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    FOREX_CARD = "forex_card"