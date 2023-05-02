import enum
from typing import List

class SurveyItemTypeEnum(enum.Enum):
    INVALID = 0
    ABNORMAL_EVENTS = 1
    CATHODIC_PROTECTION = 9

    DECK_SUPERSTRUCTURE_COCKPIT = 3
    DECK_EQUIPMENT = 4
    DOMESTIC_EQUIPMENT = 11

    KEELS_BALLAST = 5
    MISCELLANEOUS_SYSTEM_EQUIPMENT = 17
    MISCELLANEOUS = 18
    HULL_SHELL = 2
    INTERNAL_STRUCTURE_MEMBERS = 6
    THROUGH_HULL_FITTINGS = 7
    STEERING = 8

    RIG_AND_SAILS = 10
    PROPULSION_MACHINERY = 12
    ELECTRICAL_AND_ELECTRONICS = 13
    BILGE_PUMPS = 14
    SAFETY_EQUIPMENT = 15
    INTERIOR_EXTERIOR_OUTFIT = 16



SURVEY_ITEM_TYPE_STRS = [SurveyItemTypeEnum.CATHODIC_PROTECTION.name.lower(),
                         SurveyItemTypeEnum.DECK_SUPERSTRUCTURE_COCKPIT.name.lower(),
                         SurveyItemTypeEnum.DOMESTIC_EQUIPMENT.name.lower(),
                         SurveyItemTypeEnum.DECK_EQUIPMENT.name.lower(),
                         SurveyItemTypeEnum.SAFETY_EQUIPMENT.name.lower(),
                         SurveyItemTypeEnum.HULL_SHELL.name.lower(),
                         SurveyItemTypeEnum.KEELS_BALLAST.name.lower(),
                         SurveyItemTypeEnum.INTERNAL_STRUCTURE_MEMBERS.name.lower(),
                         SurveyItemTypeEnum.THROUGH_HULL_FITTINGS.name.lower(),
                         SurveyItemTypeEnum.STEERING.name.lower(),
                         SurveyItemTypeEnum.RIG_AND_SAILS.name.lower(),
                         SurveyItemTypeEnum.PROPULSION_MACHINERY.name.lower(),
                         SurveyItemTypeEnum.ELECTRICAL_AND_ELECTRONICS.name.lower(),
                         SurveyItemTypeEnum.BILGE_PUMPS.name.lower(),
                         SurveyItemTypeEnum.SAFETY_EQUIPMENT.name.lower(),
                         SurveyItemTypeEnum.INTERIOR_EXTERIOR_OUTFIT.name.lower()
]


def get_survey_item_strings_human_read() -> List[str]:

    items = []

    for item in SURVEY_ITEM_TYPE_STRS:
        item = item.split("_")
        item = " ".join(item)
        items.append(item)

    return items