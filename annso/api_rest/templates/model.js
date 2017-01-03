


var demo_sample_attributes = {}
var demo_samples = {};
var demo_analysis_id = -1;
var demo_display = "table";
var demo_fields = [2, 4, 5, 6, 7, 8, 9, 11, 22, 16];
var demo_filter = ['AND', [['==',['field',4], ['value', 1]], ['>', ['field', 9], ['value', 50]]]];




function Sample()
{
    this.id = -1;
    this.name = "";
    this.nickname = "";
    this.attributes = {};
}



function Analysis(json)
{
    // Data
    this.id = json["id"];
    this.name = json["name"];
    this.sample = {}
    this.fields = [];
    this.filter = [];
    this.creation_date = json["creation_date"];
    this.update_date = json["update_date"];

    // GUI Data
    this.annotation_display = "table";
}



function Filter(filter)
{
    this.filter = ['AND', [['==',['field',4], ['value', 1]], ['>', ['field', 9], ['value', 50]]]];

}


function FilterOperator(op)
{
    this.operator = op;
}








function OperatorGroup()
{
    this.type = '';
    this.operands = [];
    this.checked = true;


    this.is_valid = function()
    {
        var sub_valid = true;
        // TODO : check that all sub operator are valid

        return (this.type in ['AND', 'OR', 'XOR']) && sub_valid;
    }


    this.toJson = function ()
    {
        return [this.type, this.operands];
    }
}
function Operator_AND() { this.type = 'AND'; }
Operator_AND.prototype = new OperatorGroup;
function Operator_OR()  { this.type = 'OR'; }
Operator_AND.prototype = new OperatorGroup;
function Operator_XOR() { this.type = 'XOR'; }
Operator_AND.prototype = new OperatorGroup;



function Operand()
{
    this.type
}


operator_test  = ['==', '!=', '>', '<', '>=', '<=']







