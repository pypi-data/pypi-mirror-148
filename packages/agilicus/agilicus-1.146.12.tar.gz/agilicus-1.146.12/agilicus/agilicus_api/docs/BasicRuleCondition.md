# BasicRuleCondition

A BasicRuleCondition describes an atomic RuleCondition: it matches a 'variable' fact with a desired value. The condition specifies the method of the match (e.g. equality vs set membership). For example, the following condition is true when the country code from where a request originated is equal to CA: ``` variable: source.country_code operator: equals value: CA ```  You will typically specify the variable using a concrete object fully defining its semantics. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**variable** | [**BasicRuleConditionVariable**](BasicRuleConditionVariable.md) |  | 
**operator** | **str** | How to evaluate the variable against the value. - &#x60;equals&#x60;: checks that variable &#x3D;&#x3D; value. - &#x60;greater_than&#x60;: variable &gt; value. - &#x60;less_than&#x60;: checks that variable &lt; value. - &#x60;in&#x60;: set membership. Checks that variable is in value, assuming value is a list. - &#x60;exists&#39;: checks whether variable is defined.    If value is true, then the conditions is true if and only if the variable is defined. Otherwise,    if value is false, then the condition is true if and only if the variable is not defined.  | 
**value** | **bool, date, datetime, dict, float, int, list, str, none_type** | A literal value to match against. Can be any type. Whether the comparison succeeds depends on the type of the &#x60;variable&#x60; and the &#x60;operator&#x60;.  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


