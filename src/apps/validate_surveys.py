from pathlib import Path
from loguru import logger
from src.mir_survey_utils.survey_validators.condition_survey_validator import ConditionSurveyValidator
from src.mir_survey_utils.utils.build_checkpoint_to_survey_item_map import build_checkpoint_to_survey_item_map
from src.mir_survey_utils.survey_transformers.findings_transformers import (trim_finding_properties,
                                                                            set_checkpoint_group_to_mir_type,
                                                                            replace_findings_severity,
                                                                            set_checkpoint_item_to_checkpoint_group,
                                                                            replace_checkpoint_group_name,
                                                                            remove_findings,
                                                                            remove_property)

if __name__ == '__main__':

    #survey_path = Path("/home/alex/qi3/mir_datasets/surveys/preprocessed/FYS_SURVEY_REPORT_HIRONDELLE_MK2_issue_1.json")
    survey_path = Path("/home/alex/qi3/mir_datasets/surveys/preprocessed/FYS_SURVEY_REPORT_Fountaine-Pajot-Maldives-32_issue_1.json")
    #survey_path = Path(
    #    "/home/alex/qi3/mir_datasets/surveys/preprocessed/catsample.json")

    survey = ConditionSurveyValidator(survey_json_doc=survey_path, validate=True)

    logger.info(f"Survey {survey_path} is valid={survey.is_valid}")

    checkpoint_to_survey_item_map = build_checkpoint_to_survey_item_map(
        path_to_checkpoints=Path("/home/alex/qi3/nv_nlp_utils/checkpoint_json_files"))

    print(checkpoint_to_survey_item_map)

    # fix survey according to mir format
    logger.info(f"Loaded {len(checkpoint_to_survey_item_map)} survey items")

    updated = remove_property(survey, property_name="subtype")
    logger.info(f"Remove attribute 'subtype' from {updated} findings")

    # apply transformations to the valid survey
    trim_finding_properties(survey, finding_properties=['checkpoint_item', 'checkpoint_group'])

    updated = replace_findings_severity(survey=survey, old_severity_value="MEDIUM", new_severity_value="MODERATE")
    updated = replace_findings_severity(survey=survey, old_severity_value="ACCEPTABLE", new_severity_value="MINOR")
    logger.info(f"Updated {updated} severity levels")

    replace_checkpoint_group_name(survey, checkpoint_group_name={'ANCHORS': 'ANCHOR',
                                                                 'CONDITION': 'SEACOCK',
                                                                 'CHAIN_LOCKER_(DRAINAGE)': 'CHAIN_LOCKER_DRAIN',
                                                                 'EXHAUST_SYSTEM': 'ENGINE_EXHAUST',
                                                                 'FILTER/FUEL_CONDITION':'FUEL_FILTER',
                                                                 'CHARGING_SYSTEM_(ALTERNATOR)':'CHARGING_SYSTEM_ALTERNATOR',
                                                                 'RUDDER(S)_MATERIAL': 'RUDDER',
                                                                 'SPREADERS':'MAST_MAST_BEND',
                                                                 'HOSES_AND_CLAMPS': 'HOSE_CLAMPS',
                                                                 'RUDDER_&_STEERING':'RUDDER',
                                                                 'CHAIN_LOCKER_&_BULKHEAD': 'CHAIN_LOCKER_BULKHEAD',
                                                                 'HATCHES,_WINDOWS_&_VENTILATION':'HATCHES_WINDOWS_VENTILATION',
                                                                 'BAILING_/_BILGE_PUMPING':'BAILING_BILGE_PUMPING',
                                                                 'ANCHOR_CHAIN_LOCKERS_&_BULKHEADS':'CHAIN_LOCKER_BULKHEAD',
                                                                 'ANCHOR_AND_CHAIN': 'ANCHOR',
                                                                 })

    updated = remove_findings(survey,
                              checkpoint_items=['OTHER'],
                              checkpoint_ids=[8, 22])

    logger.info(f"Removed {updated} findings")

    not_found = set_checkpoint_group_to_mir_type(survey, checkpoint_group_map=checkpoint_to_survey_item_map)

    if len(not_found) != 0:
        logger.warning(f"Couldn't find mir survey item for {len(not_found)} checkpoints")
        logger.warning(not_found)

        set_checkpoint_item_to_checkpoint_group(survey=survey,
                                                checkpoint_item_to_checkpoint_group={
                                                    'OIL_COOLERS': 'PROPULSION_MACHINERY',
                                                    'ENGINE_EXHAUST': 'THROUGH_HULL_FITTINGS',
                                                    'ANCHORS': 'DECK_EQUIPMENT',
                                                    'HALYARDS': 'RIG_AND_SAILS',
                                                    'MAST_MAST_BEND': 'RIG_AND_SAILS',
                                                    'ANCHOR': 'DECK_EQUIPMENT',
                                                    'STEM': 'HULL_SHELL',
                                                    'TRANSOM': 'HULL_SHELL',
                                                    'CHAIN_LOCKER_DRAIN': 'DECK_EQUIPMENT',
                                                    'FUEL_FILTER': 'PROPULSION_MACHINERY',
                                                    'BATTERIES': 'ELECTRICAL_AND_ELECTRONICS',
                                                    'CHARGING_SYSTEM_ALTERNATOR': 'ELECTRICAL_AND_ELECTRONICS',
                                                    'RUDDER': 'STEERING',
                                                    'MAST_STEP': 'RIG_AND_SAILS',
                                                    'DODGER': 'DECK_EQUIPMENT',
                                                    'KEEL_EXTERNAL': 'KEELS_BALLAST',
                                                    'HOSE_CLAMPS': 'PROPULSION_MACHINERY',
                                                    'TOPSIDES':'HULL_SHELL',
                                                    'HULL_BELOW_WATERLINE': 'HULL_SHELL',
                                                    'KEELS':'KEELS_BALLAST',
                                                    'SKIN_FITTINGS_AND_VALVES': 'DECK_EQUIPMENT',
                                                    'DECK_MOULDING': 'DECK_EQUIPMENT',
                                                    'CHAIN_LOCKER_BULKHEAD': 'DECK_EQUIPMENT',
                                                    'HATCHES_WINDOWS_VENTILATION': 'DECK_EQUIPMENT',
                                                    'DECK_FITTINGS_AND_EQUIPMENT': 'DECK_EQUIPMENT',
                                                    'RIGGING_CHAIN_PLATES': 'DECK_EQUIPMENT',
                                                    'ANCHOR_AND_CHAIN': 'DECK_EQUIPMENT',
                                                    'LPG_INSTALLATION': 'DOMESTIC_EQUIPMENT',
                                                    'ELECTRICAL_SYSTEM': 'ELECTRICAL_AND_ELECTRONICS',
                                                    'NAVIGATION_LIGHTS': 'ELECTRICAL_AND_ELECTRONICS',
                                                    'BAILING_BILGE_PUMPING': 'BILGE_PUMPS',
                                                    "FRESH_WATER_SYSTEM": "DOMESTIC_EQUIPMENT"
                                                })
    else:
        logger.info("All checkpoints have been identified")

    # save the valid survey
    #filename = survey.filename
    #survey.save(filename=Path(f"/home/alex/qi3/nv_nlp_utils/tmp_files/{filename}"))
