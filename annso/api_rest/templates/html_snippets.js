



var sample_selection_table_header   = "<table id=\"browser_samples_table\" class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"100%\" style=\"margin:0;\"><thead><tr><th style=\"width:75px;\"></th><th>Sample</th></tr></thead><tbody></tbody></table>";
var sample_selection_table_row      = "<tr id=\"browser_samples_table_{0}\"><td><input type=\"checkbox\" value=\"{0}\" checked/></td><td>{1}</td></tr>";
var sample_selection_table_row_nick = "<tr id=\"browser_samples_table_{0}\"><td><button class=\"fa edit\">&nbsp;</button> &nbsp; <button class=\"fa delete\">&nbsp;</button></td><td>{2} - <span style=\"color:#999; font-style:italic;\">{1}</span></td></tr>";

var analysis_title_template = "<i class=\"fa fa-folder-o\" style=\"width:20px; text-align:center; margin-right:20px;\" aria-hidden=\"true\"></i>{0}";






// filter_condition_template.format('check', 'DP > 400');
var filter_condition_template = "<li class=\"condition {0}\">\
    <button onclick=\"javascript:filter_toggle_condition(this);\">\
        <i class=\"fa\" aria-hidden=\"true\">&nbsp;</i>\
        <span>{1}</span>\
    </button>\
    <button class=\"fa delete\" onclick=\"javascript:ui.remove_afilter_condition(this);\">&nbsp;</button>\
    <button class=\"fa edit\" onclick=\"javascript:ui.edit_afilter_condition(this);\">&nbsp;</button>\
    <input type=\"hidden\" value='{2}'' />\
</li>";

// filter_group_template.format('check', 'or', '', 'checked', '', '...');
var filter_group_template = "<li class=\"condition {0}\">\
    <button onclick=\"javascript:filter_toggle_condition(this);\">\
        <i class=\"fa\" aria-hidden=\"true\">&nbsp;</i> \
    </button>\
    <button class=\"fa delete\" onclick=\"javascript:ui.remove_afilter_condition(this);\">&nbsp;</button>\
    <button class=\"fa toggle minus\" onclick=\"javascript:ui.toggle_afilter_condition(this);\">&nbsp;</button>\
    <select name=\"select\" class=\"{1}\" onmouseup=\"javascript:filter_switch_operator(this);\">\
        <option value=\"AND\" {2}>AND</option> \
        <option value=\"OR\" {3}>OR</option>\
        <option value=\"XOR\" {4}>XOR</option>\
    </select>\
    <ul class=\"{1}\">\
        {5}\
        <li class=\"addcondition\">\
            <button href=\"#modal_filter_add_condition\" data-toggle=\"modal\" onclick=\"add_filter_ui_parent_elmt=$(this).parent();\">\
                <b class=\"fa fa-plus\" aria-hidden=\"true\">&nbsp;</b>\
                <span>Add new condition</span>\
            </button>\
        </li>\
    </ul>\
</li>";
