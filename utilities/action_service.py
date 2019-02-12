import requests

from config import Config


def create_action_plan(survey_ref, collection_exercise_id):
    # hard coded until dateutils available and we know more about data randomization
    trigger_date_time = '2019-02-11T11:11:00.000+00:00'

    action_plan_name = survey_ref + ' H 1'
    action_plans = get_action_plans()
    collex_action_plans = [plan for plan in action_plans
                           if plan_for_collection_exercise(plan, collection_exercise_id)]

    action_plan_data = build_combined_action_data(collex_action_plans)
    action_plan_id = action_plan_data[0]['id']

    rule = {
        'actionPlanId': action_plan_id,
        'actionTypeName': 'SOCIALNOT',
        'name': action_plan_name,
        'description': 'myActionPlanDesc',
        'triggerDateTime': trigger_date_time,
        'priority': 3
    }

    action_rules_response = requests.post(f'{Config.ACTION_SERVICE}/actionrules', auth=Config.BASIC_AUTH, json=rule)

    return action_rules_response, action_plan_id


def get_action_plans():
    action_plans_response = requests.get(f'{Config.ACTION_SERVICE}/actionplans', auth=Config.BASIC_AUTH)
    action_plans_response.raise_for_status()
    return action_plans_response.json()


def plan_for_collection_exercise(plan, collection_exercise_id):
    if not plan['selectors']:
        return False
    return plan['selectors']['collectionExerciseId'] == collection_exercise_id


def build_combined_action_data(action_plans):
    action_data = []
    for action_plan in action_plans:
        action_rule_id = action_plan.get('id')
        action_rules = get_action_rules(action_rule_id)
        action_rules = sorted(action_rules, key=lambda k: k['triggerDateTime'])
        action_plan['action_rules'] = action_rules
        action_data.append(action_plan)
    return action_data


def get_action_rules(action_plan_id):
    response = requests.get(f'{Config.ACTION_SERVICE}/actionrules/actionplan/{action_plan_id}', auth=Config.BASIC_AUTH)
    response.raise_for_status()
    return response.json()
