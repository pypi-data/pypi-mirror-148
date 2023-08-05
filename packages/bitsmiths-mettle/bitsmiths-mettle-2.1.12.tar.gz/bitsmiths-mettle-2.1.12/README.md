# Mettle #

Bitsmiths-Mettle is the supporting code generators and python libraries for the Mettle project.

See our <a href="https://bitbucket.org/bitsmiths_za/mettle.git">repo</a> and main *README* for more details!


## Requirements ##

Python 3.7+


## Installation ##

```console
$ pip install bitsmiths-mettle

---> 100%
```

## Change History ##


### 2.1.12 ###

| Type   | Description |
| ------ | ----------- |
| New    | Python database and braze models can now be generated with (pydantic, or dataclass, or attrs) as an option. |
| New    | Python daatabase and braze models can now toggle (pk, serializer, dav, clear) features an and off. |

### 2.1.11 ###

| Type   | Description |
| ----   | ----------- |
| Bug    | Fixed a refactor of `errCode` to `err_code` that was not rippled through some of the base library code/ |


### 2.1.10 ###

| Type   | Description |
| ----   | ----------- |
| Change | General typing improvements, and minor bug fixes. |


### 2.1.9 ###

| Type   | Description |
| ----   | ----------- |
| Bug    | Changed the mettle python serializer to use '%Y-%m-%d' instead of '%4Y-%m-%d' as the latter is not a standard that is supported for anything other than gcc. |


### 2.1.8 ###

| Type   | Description |
| ----   | ----------- |
| Change | Update the implementation of python databases db connector to not use the deprecated methods. This removes a bunch pytest warnings. |


### 2.1.7 ###

| Type   | Description |
| ----   | ----------- |
| Change | Code generation improved to typescript database structs. These will now generate '|undefined' for null columns. You can also mark braze columsn as null, and the generation will do the same for those. |

### 2.1.6 ###

| Type | Description |
| ---- | ----------- |
| Bug  | Added the `dist` build option back into the angular makefile generator. |


### 2.1.5 ###

| Type | Description |
| ---- | ----------- |
| Bug  | Fixed the braze type script generator to take the casing int account when generatating the marshaller code. |
| Bug  | Fixed the python braze code generator to include all required table imports if multiple tables are used in a braze struct. |


### 2.1.4 ###

| Type | Description |
| ---- | ----------- |
| Bug  | Fixed an issue where some of the python IO serializers were not properly handling None types for JSON fields. |
| Bug  | Fixed the python braze code generator to use None instead of the base type for list types. |


### 2.1.3 ###

| Type | Description |
| ---- | ----------- |
| Bug  | Fixed a problem where the python HTTP reader by was calling the wrong method when reading an error message. |
| Bug  | The python code generation now defaults date types to None instead of datetime.min. |
| Bug  | Fixed an issue where psycopg2 would raises errors with wild card string searches and parameters at the same time. Had to escape the %, how lame. |
| Bug  | Fixed a python code generation bug where the delete_one() method in the main dao class was noy using an await. |


### 2.1.2 ###

| Type | Description |
| ---- | ----------- |
| Bug  | All python database drivers now return empty strings instead of None from null columns. |


### 2.1.1 ###

| Type   | Description |
| ------ | ----------- |
| Bug    | Fixed generated python queries without input parameters not generating exec() methods. |
| Change | The `lock()` methods for database connectors now accept a `Stmnt` object, generated code updated to pass this in. |
| Change | The C++ `connect()` that takes arguments has changed to be more generic. |
| New    | Added `psycopg2` connector. |



## License ##

This project is licensed under the terms of the MIT license.
