from loguru import logger


class MIConditionSurveyFormatter(object):

    def __init__(self, survey: dict):
        self.survey = survey

    def format(self):
        pass

    def format_findings(self, checkpoint_to_survey_item_map: dict):
        logger.info("Formatting findings...")
        findings = self.survey['findings_data']

        # assign checkpoints to the
        # right survey item