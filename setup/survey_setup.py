import logging

from structlog import wrap_logger

from controllers.survey_controller import create_survey, create_survey_classifiers
from utilities.id_generation import create_survey_ref

logger = wrap_logger(logging.getLogger(__name__))


def setup_census_survey(context):
    survey_data = _create_data_for_survey()

    context.survey_ref = survey_data['survey_ref']
    context.legal_basis = survey_data['legal_basis']
    context.short_name = survey_data['short_name']
    context.long_name = survey_data['long_name']
    context.survey_type = survey_data['survey_type']

    context.survey_id = create_survey(context.survey_ref, context.short_name, context.long_name,
                                      context.legal_basis, context.survey_type)['id']
    context.classifier_id = create_survey_classifiers(context.survey_id)['id']


def _create_data_for_survey():
    survey_ref = create_survey_ref()

    return {
        'survey_ref': survey_ref,
        'legal_basis': 'STA1947',
        'short_name': survey_ref,
        'long_name': survey_ref,
        'survey_type': 'Social'
    }
