# BasicRuleConditionVariable


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**variable_type** | **str** | The discriminator for the variable. | 
**object_path** | **str** | The object path to the variable to match against. The objects available for comparison depend on the context of the rule evaluation. If an object does not exist, all conditions involving it, other than those using an &#x60;exists&#x60; operator automatically evaluate to false.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


