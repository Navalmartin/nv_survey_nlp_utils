from pathlib import Path
from loguru import logger
from src.mir_survey_utils.survey_validators.condition_survey_validator import (
    ConditionSurveyValidator,
)
from src.mir_survey_utils.utils.build_checkpoint_to_survey_item_map import (
    build_checkpoint_to_survey_item_map,
)
from src.mir_survey_utils.survey_transformers.findings_transformers import (
    trim_finding_properties,
    set_checkpoint_group_to_mir_type,
    replace_findings_severity,
    set_checkpoint_item_to_checkpoint_group,
    replace_checkpoint_item_name,
    remove_findings,
    remove_property,
)


ALIGNED_PATH = Path("/home/alex/qi3/mir_datasets/surveys/aligned")

if __name__ == "__main__":


    #survey_path = Path(
    #    "../../data/json_files/preprocessed/FYS_SURVEY_REPORT_Hallberg_Rassy_42_issue_1.json"
    #)

    survey_path = Path(
        #"/home/alex/qi3/mir_datasets/surveys/preprocessed/atlanta.json"
        "/home/alex/qi3/mir_datasets/surveys/preprocessed/coldsample.json"
    )

    survey = ConditionSurveyValidator(survey_json_doc=survey_path, validate=True)

    logger.info(f"Survey {survey_path} is valid={survey.is_valid}")

    checkpoint_to_survey_item_map = build_checkpoint_to_survey_item_map(
        path_to_checkpoints=Path("/home/alex/qi3/mir_datasets/surveys/checkpoint_json_files")
    )

    print(checkpoint_to_survey_item_map)

    # fix survey according to mir format
    logger.info(f"Loaded {len(checkpoint_to_survey_item_map)} survey items")

    updated = remove_property(survey, property_name="subtype")
    logger.info(f"Remove attribute 'subtype' from {updated} findings")

    # replace the checkpoint item name
    # with the specified name
    replace_checkpoint_item_name(
        survey,
        checkpoint_group_name={
            "ANCHORS": "ANCHOR",
            "CONDITION": "SEACOCK",
            "CHAIN LOCKER (DRAINAGE)": "CHAIN_LOCKER_DRAIN",
            "EXHAUST SYSTEM": "ENGINE_EXHAUST",
            "FILTER/FUEL CONDITION": "FUEL_FILTER",
            "CHARGING SYSTEM (ALTERNATOR)": "CHARGING_SYSTEM_ALTERNATOR",
            "CHARGING SYSTEM (BATTERY CHARGER)": "BATTERY_CHARGER",
            "RUDDER(S) MATERIAL": "RUDDER",
            "SPREADERS": "MAST_MAST_BEND",
            "HOSES AND CLAMPS": "HOSE_CLAMPS",
            "HOSES, CLAMPS AND CONNECTORS": "HOSE_CLAMPS",
            "RUDDER & STEERING": "RUDDER",
            "CHAIN LOCKER & BULKHEAD": "CHAIN_LOCKER_BULKHEAD",
            "HATCHES, WINDOWS & VENTILATION": "HATCHES_WINDOWS_VENTILATION",
            "BAILING / BILGE_PUMPING": "BAILING_BILGE_PUMPING",
            "ANCHOR CHAIN LOCKERS & BULKHEADS": "CHAIN_LOCKER_BULKHEAD",
            "ANCHOR AND CHAIN": "ANCHOR",
            "PROPELLER(S)": "PROPELLER",
            "SAT PHONE": "SATCOM",
            "SHAFT BEARING (CUTTLESS BEARING)": "SHAFT_BEARING"
        },
    )

    # apply transformations to the valid survey
    trim_finding_properties(
        survey, finding_properties=["checkpoint_item", "checkpoint_group"]
    )

    updated = replace_findings_severity(
        survey=survey, old_severity_value="MEDIUM", new_severity_value="MODERATE"
    )
    updated = replace_findings_severity(
        survey=survey, old_severity_value="ACCEPTABLE", new_severity_value="MINOR"
    )
    logger.info(f"Updated {updated} severity levels")



    #updated = remove_findings(
    #    survey, checkpoint_items=["OTHER"], checkpoint_ids=[8, 22]
    #)

    #logger.info(f"Removed {updated} findings")

    not_found = set_checkpoint_group_to_mir_type(
        survey, checkpoint_group_map=checkpoint_to_survey_item_map
    )

    if len(not_found) != 0:
        logger.warning(
            f"Couldn't find mir survey item for {len(not_found)} checkpoints"
        )

        logger.warning(f"Checkpoints not found {not_found}")
        logger.warning("Attempting to align these...")

        checkpoint_item_to_checkpoint_group={
                "OIL_COOLERS": "PROPULSION_MACHINERY",
                "ENGINE_EXHAUST": "THROUGH_HULL_FITTINGS",
                "ANCHORS": "DECK_EQUIPMENT",
                "HALYARDS": "RIG_AND_SAILS",
                "MAST_MAST_BEND": "RIG_AND_SAILS",
                "ANCHOR": "DECK_EQUIPMENT",
                "STEM": "HULL_SHELL",
                "TRANSOM": "HULL_SHELL",
                "CHAIN_LOCKER_DRAIN": "DECK_EQUIPMENT",
                "FUEL_FILTER": "PROPULSION_MACHINERY",
                "BATTERIES": "ELECTRICAL_AND_ELECTRONICS",
                "CHARGING_SYSTEM_ALTERNATOR": "ELECTRICAL_AND_ELECTRONICS",
                "BATTERY_CHARGER": "ELECTRICAL_AND_ELECTRONICS",
                "RUDDER": "STEERING",
                "MAST_STEP": "RIG_AND_SAILS",
                "DODGER": "DECK_EQUIPMENT",
                "KEEL_EXTERNAL": "KEELS_BALLAST",
                "HOSE_CLAMPS": "PROPULSION_MACHINERY",
                "TOPSIDES": "HULL_SHELL",
                "HULL_BELOW_WATERLINE": "HULL_SHELL",
                "KEELS": "KEELS_BALLAST",
                "SKIN_FITTINGS_AND_VALVES": "DECK_EQUIPMENT",
                "DECK_MOULDING": "DECK_EQUIPMENT",
                "CHAIN_LOCKER_BULKHEAD": "DECK_EQUIPMENT",
                "HATCHES_WINDOWS_VENTILATION": "DECK_EQUIPMENT",
                "DECK_FITTINGS_AND_EQUIPMENT": "DECK_EQUIPMENT",
                "RIGGING_CHAIN_PLATES": "DECK_EQUIPMENT",
                "ANCHOR_AND_CHAIN": "DECK_EQUIPMENT",
                "LPG_INSTALLATION": "DOMESTIC_EQUIPMENT",
                "ELECTRICAL_SYSTEM": "ELECTRICAL_AND_ELECTRONICS",
                "NAVIGATION_LIGHTS": "ELECTRICAL_AND_ELECTRONICS",
                "BAILING_BILGE_PUMPING": "BILGE_PUMPS",
                "FRESH_WATER_SYSTEM": "DOMESTIC_EQUIPMENT",
                "BLACK_WATER_TANK": "DOMESTIC_EQUIPMENT",
                "ANODES": "CATHODIC_PROTECTION",
                "COCKPIT":"DECK_EQUIPMENT",
                "HULL_INTERNAL_STRUCTURE": "HULL_SHELL",
                "PROPELLER": "PROPULSION_MACHINERY",
                "CHARGING_SYSTEM_(BATTERY_CHARGER)": "ELECTRICAL_AND_ELECTRONICS",
                "TELEVISION(S)": "DOMESTIC_EQUIPMENT",
                "SAT_PHONE": "ELECTRICAL_AND_ELECTRONICS",
                "ENGINE_SYNCHRONIZER": "PROPULSION_MACHINERY",
                "FREEZER": "DOMESTIC_EQUIPMENT",
                "SEA_WATER_ICE_MAKER": "DOMESTIC_EQUIPMENT",
                "BILGE": "BILGE_PUMPS",
                "SHAFT_BEARING": "PROPULSION_MACHINERY",
                "SHORE_POWER_INLET": "ELECTRICAL_AND_ELECTRONICS"
            }

        counter = 0
        not_aligned = []
        for item in not_found:
            if item in checkpoint_item_to_checkpoint_group:
                counter += 1
            else:
                not_aligned.append(item)

        logger.warning(f"Script will align {counter} checkpoints to survey items")
        logger.warning(f"Not aligned checkpoints: {not_aligned}")
        set_checkpoint_item_to_checkpoint_group(
            survey=survey,
            checkpoint_item_to_checkpoint_group=checkpoint_item_to_checkpoint_group,
        )

        logger.warning(f"Could not align {len(not_found) - counter} checkpoints to survey items")
    else:
        logger.info("All checkpoints have been identified")

    # save the valid survey
    filename = survey.filename
    survey.save(filename=ALIGNED_PATH / f"{filename}")
