# RuleCondition

A RuleCondition represents a piece of information whose truth is evaluated in order to determine if a rule's action should be executed.   Multiple RuleConditions are typically combined by Rule into a single logical statement. The method by which they are combined (conjunction vs disjunction) depends on the rule itself. The facts evaluated to determine the truth of a RuleCondition and any constraints on those facts are specified by a more concrete type of RuleCondition. Accordingly, each RuleCondition must provide exactly one of the concrete types:  - `http_rule_condition`  - `basic_rule_condition`  - `compound_rule_condition`  A RuleCondition may be `negated`, in which case it will be true if the concrete condition is false. Otherwise the truth of the RuleCondition matches the truth of the concrete condition. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**negated** | **bool** | Whether or not the RuleCondition is true if the concrete condition is. Set to true to have the RuleCondition evaluate to true if and only if the concrete condition is false.  | 
**http_rule_condition** | [**HttpRule**](HttpRule.md) |  | [optional] 
**basic_rule_condition** | [**BasicRuleCondition**](BasicRuleCondition.md) |  | [optional] 
**compound_rule_condition** | [**CompoundRuleCondition**](CompoundRuleCondition.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


