Filter Engine and Database organisation
#######################################

Purpose of this page is to keep a trace of all technical issues, fixes, decision took regarding the filter engine
 * Features : features that (shall) support (or not) the engine, and why.
 * Database schema : design of the database, technical choices, optimisations, ...
 * Technical points : list of hard point and what have been done



Features
========
Functional features :
---------------------
 * User shall be able to select which annotation's fields he want to see
 * User shall be able to compose any filter
    * Basics conditions : ==, !=, >, <, <=, >=
    * Logic operators : AND, OR
    * Set condition : IN, NOT IN
       * Set's operators shall support 2 kinds of research : by variant (chr, ops, ref, alt) or by site (chr, pos)
       * Set's operators shall support 3 kinds of sets : over Sample, over Attribute (= group of sample) and over saved filter
 * User shall be able to save its filters and used them in other filters (as subset of variant)
 * User shall be able to do set-operation over sets like sample, saved filter or group of sample (see attribute notion)
 * Engine shall support pagination of results
 * In the context of an analysis, the user shall be able to rename sample (to have more human friendly names)
 * Current work shall be automatically saved to allow user to retrieve its work in case of problem
 * Result shall be presented in an human friendly way. That's means :
    * No duplicate entries
    * Possibility to group results. By example having at firt level all distinct site (chr-pos), and then, by sample having variant (ref-alt) with associated annotation. Only 2 display modes will be implemented (see abandonned features to see why).
       * Array mode : display all unique entries as a simple table (1 row = 1 entry). That means that if a variant match with several gene's name by example, the user will see several row for the same variant.
       * Variant list : result are grouped by variant. 
    
 * As UI shall be localized. It shall be also the same for annotation's fields names and description


Abandonned features :
---------------------
 * Set condition : XOR (exclusive or). Because of the hight complexity to implement this condition, we decide to posponed it to a future version
 * Custom group for result : Having a generic system to allow user to choose how results shall be grouped is very complex both for the UI and the Engine. There is also lot of case where grouping is more confusing than helpfull. By example if you group by gene, a same variant can be present in several groups, and mixing several grouping like that will do the mess. So only 2 display modes will be implemented (see implemented features). For complex presentation the report generator feature will allow users to do all they want (python module).








Database schema
===============
Topic to read about postgresql :
 * Available Data types - https://www.postgresql.org/docs/9.5/static/datatype.html :
    * Array Type : To avoid. _Arrays are not sets; searching for specific array elements can be a sign of database misdesign. Consider using a separate table with a row for each item that would be an array element. This will be easier to search, and is likely to scale better for a large number of elements._
    * JSON Type : Usefull only if we need to make query inside JSON data. Prefer simple text or varchar type if just need to store json for the client.
    * Enum Type : To simplify import of tierce database, consider their enum as simple text (carachter varia
    * Range Type : Prefer this type for location's (start-end) annotations.

 * Pagination/ OFFSET over big data : http://stackoverflow.com/questions/34110504/optimize-query-with-offset-on-large-table/34291099#34291099
 
 * Count total & Select subset in the same query : http://stackoverflow.com/questions/156114/best-way-to-get-result-count-before-limit-was-applied





Technical points
================
 * 
