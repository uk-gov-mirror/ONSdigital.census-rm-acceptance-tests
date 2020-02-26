Feature: Handle refusal message

  Scenario: Refusal message results in case excluded from action plan
    Given sample file "sample_for_refusals.csv" is loaded successfully
    When a refusal message for a created case is received
    And set action rule of type "ICL1E" when case event "REFUSAL_RECEIVED" is logged
    Then only unrefused cases appear in "P_IC_ICL1" print files
    And the case is marked as refused
    And a CLOSE action instruction is emitted to FWMT
    And the events logged for the refusal case are [SAMPLE_LOADED,REFUSAL_RECEIVED]