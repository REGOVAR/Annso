


// ------------------------------------------------------------------
// DISPLAY error for the user
function error(json=null)
{
    if (json == null)
    {
        json = {"error_id" : "-", "error_code" : "-1", "error_url" : "#", "msg" : "Unknow error ...."}
    }

    $('#modal_error_id').text(json["error_id"]);
    $('#modal_error_code').text(json["error_code"]);
    $('#modal_error_code').attr('href', json["error_url"]);
    $('#modal_error_msg').text(json["msg"]);
    $('#modal_error').modal('show');
}

var selected_tab = "welcom_toolbar";




// This controler focus on all action that impact the analysis model.
// pure UI variable and method are defined outside of this class
function AnnsoControler () {
    this.analysis = null;

    this.filter_mode = ["quick", "advanced"];
    this.qfilter = [];



    // Check if data model is consistent. Used by ui controler to know if 
    // data can be displayed or not.
    this.is_valid = function()
    {
        return true;
    }


    // ------------------------------------------------------------------
    // New analysis
    this.new_analysis = function (name, template_id)
    {
        $.ajax(
        {
            url: rootURL + "/analysis",
            type: "POST",
            data: "{\"name\" : \""+ analysis_name +"\", \"template_id\" : " + template_id + "}",
            async: false
        }).fail(function() { alert("TODO : network error"); })
        .done(function(data)
        {
            analysis.load_analysis(data);
        });
    };


    // ------------------------------------------------------------------
    // Load an analysis from server
    this.load_analysis = function (id)
    {
        $.ajax({ url: rootURL + "/analysis/" + id, type: "GET", async: false}).fail(function() { alert("TODO : network error"); })
        .done(function(json)
        {
            if (json["success"])
            {
                // Init model
                analysis.analysis = new Analysis(json["data"]);
                analysis.filter_mode = "advanced";
                analysis.qfilter = [];


                // Update view
                ui.start_analysis();
            }
            else
            {
                error(json);
            }
        });
    };


    // ------------------------------------------------------------------
    // Save current analysis settings to the server
    // Settings = samples, attributes, fields, filter, selection
    this.save_analysis = function ()
    {
        alert("TODO : Save current analysis to the server");
    };


    this.add_sample = function (id)
    {

    };

    this.remove_sample = function (id)
    {

    };

    this.set_sample_nickname = function (id, nickname)
    {

    };

    this.set_sample_comments = function (id, comments)
    {

    };

    this.select_field = function (id, position)
    {

    };

    this.remove_field = function (id)
    {

    };

    this.switch_qfilter = function (id)
    {

    };


    this.get_qfilter = function ()
    {

    };

    this.get_afilter = function ()
    {

    };

    this.save_filter = function (name)
    {
        if (this.filter_mode == "quick")
        {

        }
        else
        {

        }

        $.ajax({ url: "{0}/analysis/{1}/savefilter".format(rootURL, id), type: "GET", async: false}).fail(function() { alert("TODO : network error"); })
        .done(function(json)
        {
            if (json["success"])
            {
                // Init model
                analysis.analysis = new Analysis(json["data"]);
                analysis.filter_mode = "advanced";
                analysis.qfilter = [];


                // Update view
                ui.start_analysis();
            }
            else
            {
                error(json);
            }
        });
    };


    this.switch_variant = function (id)
    {

    };

    this.export_selection = function ()
    {

    };


    this.report_selection = function ()
    {

    };

};





var analysis = new AnnsoControler;



function AnnsoUIContoler ()
{

    this.current_tab = "welcom";

    // ------------------------------------------------------------
    // GLOBAL MENUS / TAB NAVIGATION 

    this.select_tab = function(tab_name)
    {
        this.current_tab = tab_name;
        $('#welcom_toolbar').hide();
        $('#sample_toolbar').hide();
        $('#variant_toolbar').hide();
        $('#result_toolbar').hide();
        $('#' + tab_name + '_toolbar').show();

        if (tab_name == "variant")
        {
            // Force refresh of the variant array
            load_variants_array();
        }
    };

    this.select_submenu = function(menu_name)
    {

        if (this.current_tab == "variant")
        {
            $('#filters_panel_menu_quick').hide();
            $('#filters_panel_menu_info').hide();
            $('#filters_panel_menu_filter').hide();
            $('#filters_panel_menu_' + menu_name ).show();
        }
        if (this.current_tab == "result")
        {
            $('#selection_panel_menu_info').hide();
            $('#selection_panel_menu_export').hide();
            $('#selection_panel_menu_report').hide();
            $('#selection_panel_content_info').hide();
            $('#selection_panel_content_export').hide();
            $('#selection_panel_content_report').hide();
            $('#selection_panel_menu_' + menu_name ).show();
            $('#selection_panel_content_' + menu_name ).show();
        }
    };


    // ------------------------------------------------------------
    // TOOLBARS ACTIONS

    this.variant_display = function (display_mode)
    {
        // display_mode = table | list
    };


    this.reset_filter = function ()
    {

    };

    this.apply_filter = function ()
    {
        analysis.analysis.filter = build_filter_json($('#filters_panel_menu_filter_c > ul > li'));
        console.debug(analysis.analysis.filter);

        load_variants_array();
    };

    this.save_filter = function ()
    {
        filter_name = $('#modal_save_filter_name').val();

        // Update data
        analysis.analysis.save_filter(filter_name);

        // Refresh ui
        // TODO
    };



    this.load_sample_database = function ()
    {

    };


    

    this.new_attribute = function(name, samples_values)
    {
        var i = 0;
        $('#browser_samples_table tr').each(function()
        {
            td = (i == 0) ? "th" : "td";
            ph = (i == 0) ? "Attribute name" : "Attribute value";
            $(this).append(sample_selection_table_attribute.format(td, ph, ""));
            i += 1;
        });
    };

    this.validate_attribute = function (elmt)
    {
        var value = $(elmt).val();
        if (!/^[a-z0-9]+$/i.test(value))
        {
            alert('Input is not alphanumeric');
            $(elmt).removeClass("success");
            $(elmt).addClass("error");
        }
        else
        {
            $(elmt).addClass("success");
            $(elmt).removeClass("error");
        }

    };



    // WELCOM PANEL ACTIONS
    this.set_template = function (template_id)
    {

    };


    this.start_analysis = function ()
    {
        /*if (!analysis.is_valid())
        {
            return;
        }*/

        // Reset new analysis form
        $('#modal_new_analysis_name').val("");
        $('#modal_new_analysis').modal('hide');


        // Set main title
        $('#analysis_title').html(analysis_title_template.format(analysis.analysis.name));




        // Reset samples screen
        if (analysis.analysis.samples.length == 0)
        {
            $('#browser_samples').html("<span class=\"maincontent_placeholder\">&#11172; Import and select sample(s) you want to analyse.</span>")
        }
        else
        {
            
            // tHeader
            var html = "";
            $.each(analysis.analysis.attributes, function(id, attr) 
            {
                html += sample_selection_table_attribute.format("th", "Attribute name", attr['name']);
            });
            $('#browser_samples').html(sample_selection_table_header.format(html));


            // tBody (samples values)
            html = "";
            $.each(analysis.analysis.samples, function(id, sp) 
            {
                var attr_html = "";
                var sp_id = id;
                $.each(analysis.analysis.attributes, function(id, attr) 
                {
                    attr_html += sample_selection_table_attribute.format("td", "Attribute value", attr['samples_value'][sp_id]);
                });
                if (sp.nickname == null)
                {
                    html += sample_selection_table_row.format(id, sp.name, attr_html);
                }
                else
                {
                    html += sample_selection_table_row_nick.format(id, sp.name, sp.nickname, attr_html);
                }
            });
            $('#browser_samples_table tbody').append(html);
        }



        // Automaticaly select the Sample section
        $('#nav_project_sample')[0].click(function (e) { e.preventDefault(); $(this).tab('show'); })



        // Reset UI fields
        $('#annotation_fields_list li').each(function(idx) {
            $(this).removeClass('check');
            $(this).addClass('uncheck');
        });
        $.each(analysis.analysis.fields, function(idx, fid) 
        {
            db_id = '#annotation_fields_db_'+ annotation_fields[fid]['db_id'];
            $(db_id).removeClass('uncheck');
            $(db_id).addClass('check');
            $('#annotation_fields_field_'+fid).removeClass('uncheck');
            $('#annotation_fields_field_'+fid).addClass('check');
        });

        // Reset UI filter
        $('#filters_panel_menu_filter_c > ul').html(build_filter_ui(analysis.analysis.filter));
    };



    this.remove_afilter_condition = function(elmt)
    {
        $(elmt).parent().remove();
    };

    this.toggle_afilter_condition = function (elmt)
    {
        if ($(elmt).hasClass('minus'))
        {
            $(elmt).next().next().addClass('collapse');
            $(elmt).removeClass('minus');
            $(elmt).addClass('plus');
        }
        else
        {
            $(elmt).next().next().removeClass('collapse');
            $(elmt).removeClass('plus');
            $(elmt).addClass('minus');
        }
    };


    this.edit_afilter_condition = function (elmt)
    {
        // TODO
    };

}
var ui = new AnnsoUIContoler;











function create_analysis()
{
    var analysis_name = $('#modal_new_analysis_name').val();
    var template_id = -1;

    if (analysis_name != "")
    {
        analysis_controler.new_analysis(analysis_name, template_id);
    }
    else
    {
        alert("Thanks to give a name to your analyse.");
        return;
    }

    if (analysis_controler.is_valid())
    {
        load_analysis();
    }
    else
    {
        alert ("TODO : reset whole IHM");
    }  
};







var filter_operator_display_map = {'==' : '=', '!=' : "&#8800;", '>' : "&gt;", '>=' : "&#8805;", '<' : "&lt;", '<=' : "&#8804;"};
var add_filter_ui_parent_elmt;
function build_filter_ui(json)
{
    if (["AND", "OR", "XOR"].includes(json[0]))
    {
        var operand_html = "";
        $.each(json[1], function(idx, operand) 
        {
            operand_html += build_filter_ui(operand);
        });


        if (json[0] == "AND")
            return filter_group_template.format('check', 'and', 'selected', '', '', operand_html);
        if (json[0] == "OR")
            return filter_group_template.format('check', 'or', '', 'selected', '', operand_html);
        if (json[0] == "XOR")
            return filter_group_template.format('check', 'xor', '', '', 'selected', operand_html);
    }
    else if (json[0] == 'field')
    {
        return annotation_fields[json[1]]['name'];
    }
    else if (json[0] == 'value')
    {
        return json[1];
    }
    else if (['==', '!=', '>', '>=', '<', '<='].includes(json[0]))
    {
        return filter_condition_template.format('check', "{0} {1} {2}".format(build_filter_ui(json[1]), filter_operator_display_map[json[0]], build_filter_ui(json[2])), JSON.stringify(json));
    }
    else if (["IN", "NOTIN"].includes(json[0]))
    {
        return filter_set_template.format('check', "{0} {1}".format(json[1], json[0]), json[2][0], json[2][1], JSON.stringify(json));
    }
    else
    {
        return "TO BE implemented";
    }
}

function add_filter_ui(operator)
{
    var json;
    if (["AND", "OR", "XOR"].includes(operator))
    {
        json = [operator, []];
    }
    else 
    {
        // retrieve operator
        var operator = $('#modal_filter_field_operator').find(":selected").val();

        // retrieve field
        f_id = annotation_fields_autocomplete_info[annotation_fields_autocomplete.indexOf($('#modal_filter_field_name').val())]["id"];
        var op1 = ['field', f_id];
        
        // retrieve value
        var op2 = ['value', $('#modal_filter_field_value').val()];

        json = [operator, op1, op2];
    }
    $(build_filter_ui(json)).insertBefore(add_filter_ui_parent_elmt);
}
function add_filter_ui2(operator)
{
    // retrieve operator
    var operator = $('#modal_filter_variant_operator').find(":selected").val();
    var type = $('#modal_filter_variant_type').find(":selected").val();
    var set = $('#modal_filter_variant_set').find(":selected").val();

    json = [operator, type, [set, $('#modal_filter_variant_setid').val()]];
    


    console.debug(json);

    $(build_filter_ui(json)).insertBefore(add_filter_ui_parent_elmt);
}



function build_filter_json(root_elmt)
{

    // take in account only checked filter condition
    if ($(root_elmt).hasClass("check"))
    {
        if ($(root_elmt).has("select").length == 1)
        {
            var json = [$(root_elmt).find(":selected").val(), []];

            $(root_elmt).find("> ul > li").each(function( index ) 
            {

                var data = build_filter_json($( this ));
                if (data != null)
                {
                    json[1].push(data);
                }
            });

            return json;
        }
        else
        {
            return JSON.parse($(root_elmt).find("> input[type='hidden']").val());
        }
    }

    return null;
}























var substringMatcher = function(strs) 
{
    return function findMatches(q, cb) 
    {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) 
        {
            if (substrRegex.test(str)) 
            {
                matches.push(str);
            }
        });

        cb(matches);
    };
};




































function load_sample_database()
{
    $('#modal_import_sample_db_content').html('<i class="fa fa-refresh fa-spin fa-3x fa-fw" style="margin:200px 250px"></i><span class="sr-only">Loading data from database</span>');
    $.ajax({ url: rootURL + "/sample", type: "GET", async: false}).fail(function()
    {
        alert( "ERROR" );
    }).done(function(json) 
    {
        if (json["success"])
        {
            json = json["data"]
        }
        else
        {
            display_error(json);
            return;
        }
        html="<table class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"100%\" style=\"margin:0\">\
                    <thead>\
                        <tr>\
                            <th style=\"width:20px\"></th>\
                            <th style=\"width:200px\">Sample</th>\
                            <th style=\"width:40px\">Comment</th>\
                            <th style=\"width:100px\">Analyses</th>\
                        </tr>\
                    </thead>\
                    <tbody>\n";

        for (var i=0; i< json.length; i++)
        {
            html += "<tr style=\"cursor: pointer;\" onclick=\"javascript:toggle_select_sample({0}, true);\">\
                            <td><input type=\"checkbox\" value=\"{0}\"/></td>\
                            <td>{1} </td>\
                            <td>{2} </td>\
                            <td>{3} </td>\
                        </tr>".format(json[i]["id"], json[i]["name"], json[i]["comments"], json[i]["analyses"]);
        }

        html += "</tbody></table>";

        $('#modal_import_sample_db_content').html(html);

    });
}


function add_sample_to_analysis(sample)
{

}


function toggle_select_sample( id, clean_list=false)
{
    // check if need to add the table
    if (Object.keys(analysis.analysis.samples).length == 0)
    {
        $('#browser_samples').html(sample_selection_table_header);
    }

    // check if id already in the list
    checked = false;
    if (id in analysis.analysis.samples)
    {
        // update check status
        analysis.analysis.samples[id]["checked"] = !analysis.analysis.samples[id]["checked"];
        $('#browser_samples_table_'+id+ " input").prop('checked', analysis.analysis.samples[id]["checked"]);

        // update model & view
        if (!analysis.analysis.samples[id]["checked"] && clean_list)
        {
            delete(analysis.analysis.samples[id]);
            $('#browser_samples_table_'+id).remove();
        }
    }
    else
    {
        sample = null;
        $.ajax({ url: rootURL + "/sample/" + id, type: "GET", async: false}).done(function(json)
        {
            sample = json["data"];
        });
        analysis.analysis.samples[id] = {"name" : sample["name"], "comments" : sample["comments"], "analyses" : "", "nickname" : "", "attributes" : [], "checked" : true};
        // TODO build row according to existing attributes
        $('#browser_samples_table tbody').append('<tr id="browser_samples_table_{0}"><td><input type=\"checkbox\" value=\"{0}\" checked/></td><td>{1}</td></tr>'.format(id, sample["name"]));
    }
}


function load_variants_array()
{
    // Init the analysis by creating relation between sample, attributes and the analysis
    samples = [];
    $.each(analysis.analysis.samples, function( key, data ) {
        if (data["checked"])
        {
            samples.push({"id" : key, "attributes" : []});
        }
    });
    $('#variants_list').html('<i class="fa fa-refresh fa-spin fa-3x fa-fw" style="display:block;margin:auto;margin-top:200px;"></i><span class="sr-only">Loading data from database</span>');


    // retrieve list of sample
    $.ajax({ 
        url: rootURL + "/analysis/" + analysis.analysis.id + "/filtering", 
        type: "POST",
        data: "{\"mode\" : \"table\", \"filter\" : " + JSON.stringify(analysis.analysis.filter) + ", \"fields\" : " + JSON.stringify(analysis.analysis.fields) + "}",
        async: true}).fail(function()
    {
        display_error();
    }).done(function(json)
    {
        if (json["success"])
        {
            json = json["data"]
        }
        else
        {
            display_error(json);
            return;
        }

        if (  $("#variants_list_table").length )
        {
            update_variants_list(json);
        }
        else
        {
            init_variants_list(json);
        }
    });
}




function init_variants_list(json)
{
    var html = "<table id=\"variants_list_table\" class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"100%\" style=\"margin:0\"><thead><tr><th style=\"width:20px\"></th>";

    for (var i=0; i<analysis.analysis.fields.length; i++)
    {
        html += "<th>{0}</th>".format(annotation_fields[analysis.analysis.fields[i]]["name"]);
    }
    html += "</tr></thead><tbody>";


    var rowhtml = "<tr id=\"variant_{0}\" style=\"cursor: pointer;\"><td><input type=\"checkbox\" value=\"{0}\"/></td>";
    "<td>{1}</td><td>{2}</td><td class=\"pos\">{3}</td><td class=\"seq\">{4}</td><td class=\"seq\">{5}</td></tr>";
    
    $.each(json, function( idx, v ) 
    {

        html += rowhtml.format(v["variant_id"]);
        for (var i=0; i<analysis.analysis.fields.length; i++)
        {
            fid   = analysis.analysis.fields[i];
            ftype = annotation_fields[fid]["type"];

            if (fid in annotation_fields_formaters)
            {
                // use special format method to display this field
                html += annotation_fields_formaters[fid](v[analysis.analysis.fields[i]]);
            }
            else
            {
                // format according to the type
                if (ftype == "int" || ftype == "float")
                    html += annotation_format_number(v[fid]);
                else 
                    html += "<td>{0}</td>".format(v[fid]);
            }
        }
        html += "</tr>";
    });
    $("#variants_list").html(html + "</tbody></table>");
}

function annotation_format_number(value)
{
    var n = value.toString(), p = n.indexOf('.');
    return "<td class=\"number\">{0}</td>".format(
        n.replace(/\d(?=(?:\d{3})+(?:\.|$))/g, function($0, i)
        {
            return p<0 || i<p ? ($0+'&nbsp;') : $0;
        }));
}

function annotation_format_sequence(seq)
{
    map = {'G':'<span class="g">G</span>', 'G':'<span class="g">G</span>', 'G':'<span class="g">G</span>', 'G':'<span class="g">G</span>'}
    max = 10;
    size = seq.length;
    var html = "";
    for (var i=0; i<Math.min(max, seq.length); i++)
    {
        html +='<span class="{0}">{0}</span>'.format(seq[i]);
    } 
    if (seq.length > max)
    {
        html ='<a title="' + seq + '">' + html + '&#8230;</a>';
    }
    return "<td class=\"seq\">{0}</td>".format(html);
}

function annotation_format_sampleid(id)
{
    name = analysis.analysis.samples[id]["nickname"];
    if (name == null)
        name = analysis.analysis.samples[id]["name"];

    return "<td>{0}</td>".format(name);
}

function annotation_format_gt(gt)
{
    return "<td class=\"seq\">{0}</td>".format(['Ref/Ref <span style="font-weight:100">Homo</span>', 'Alt/Alt <span style="font-weight:100">Homo</span>', 'Ref/Alt <span style="font-weight:100">Hetero</span>', 'Alt1/Aly2 <span style="font-weight:100">Hetero</span>'][gt]);
}






function update_variants_list(json)
{

}




function filter_build_tree(json)
{

}





















 
function filter_toggle_field(elmt, f_id)
{
    if ($(elmt).parent().hasClass('check'))
    {
        $(elmt).parent().removeClass('check');
        $(elmt).parent().addClass('uncheck');

        analysis.analysis.fields.splice(analysis.analysis.fields.indexOf(f_id),1);
    }
    else
    {
        $(elmt).parent().addClass('check');
        $(elmt).parent().removeClass('uncheck');

        analysis.analysis.fields.push(f_id);
    }

    load_variants_array();
}
function filter_toggle_field_group(elmt)
{
    if ($(elmt).hasClass('minus'))
    {
        $(elmt).next().next().next().addClass('collapse');
        $(elmt).removeClass('minus');
        $(elmt).addClass('plus');
    }
    else
    {
        $(elmt).next().next().next().removeClass('collapse');
        $(elmt).removeClass('plus');
        $(elmt).addClass('minus');
    }
}


function filter_toggle_condition(elmt)
{
    if ($(elmt).parent().hasClass('check'))
    {
        $(elmt).parent().removeClass('check');
        $(elmt).parent().addClass('uncheck');
    }
    else
    {
        $(elmt).parent().addClass('check');
        $(elmt).parent().removeClass('uncheck');
    }
}

function filter_switch_operator(elmt)
{
    var map = {"AND" : "and", "OR" : "or", "XOR" : "xor"};
    var operator = $(elmt).find(":selected").text();



    $(elmt).removeClass('and');
    $(elmt).removeClass('or');
    $(elmt).removeClass('xor');
    $(elmt).addClass(map[operator]);

    $(elmt).next().removeClass('and');
    $(elmt).next().removeClass('or');
    $(elmt).next().removeClass('xor');
    $(elmt).next().addClass(map[operator]);
}











function fake_rename_sample()
{
    i=0;
    data = ["<i class=\"fa fa-pencil\" aria-hidden=\"true\" style=\"width:20px; text-align:center;\">&nbsp;</i> Dad <span style=\"color:#999\"> - CGH0157</span>", 
            "<i class=\"fa fa-pencil\" aria-hidden=\"true\" style=\"width:20px; text-align:center;\">&nbsp;</i> Mom <span style=\"color:#999\"> - CGH0413</span>", 
            "<i class=\"fa fa-pencil\" aria-hidden=\"true\" style=\"width:20px; text-align:center;\">&nbsp;</i> Son <span style=\"color:#999\"> - CGH0542</span>"];
    data2 = ["Dad", "Mom", "Son"];

    $('#browser_samples_table tr td:nth-child(3)').each(function()
    {
        $(this).html(data[i]);
        i += 1;
    });

    i = 0;

    $('#browser_samples_table tr td:nth-child(2)').each(function()
    {
        $(this).html(data2[i]);
        i += 1;
    });
}







function fake_generate_report()
{
    $.ajax({ url: "http://annso.absolumentg.fr/v1/report", type: "GET", async: false}).done(function(report)
    {
        $('#selection_panel_content_report').html(report);
        
    });
}




























/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* Filter method
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
var total_variants = 0;
var qfilter_warning_warning_msg_tpl = "&nbsp;<i class=\"fa fa-warning\" aria-hidden=\"true\"></i> {0} / {1} variants displayed";
$("#browser_filter_input").keyup(function () 
{ 
    var total_row = 0;
    // Split the current value of searchInput
    var data = this.value.toUpperCase().split(" ");
    // Create a jquery object of the rows
    var jo = $("#browser_files_table > tbody").find("tr");
    if (this.value == "") 
    {
        jo.show();
        $('#qfilter_warning').html("&nbsp;");
        $('#qfilter_message').html("&nbsp;" + total_variants + " variants");
        return;
    }
    // hide all the rows
    jo.hide();
    var displayed_row = 0;
    total_variants = 0;
    //Recusively filter the jquery object to get results.
    jo.filter(function (i, v) 
    {
        var $t = $(this);
        for (var d = 0; d < data.length; ++d) 
        {
            total_variants += 1;
            if ($t.text().toUpperCase().indexOf(data[d]) > -1) 
            {
                displayed_row += 1;
                return true;
            }
        }
        return false;
    })
    //show the rows that match.
    .show();
    $('#qfilter_warning').html(qfilter_warning_warning_msg_tpl.format(displayed_row,total_variants));
    $('#qfilter_message').html("&nbsp;");
});











/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* WEBSOCKETS handler
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

function ws_file_changed(data)
{
    jQuery.each(data, function(index, item) {
        var percentage = (item["upload_offset"] / item["set_notify_all"] * 100).toFixed(2);

        buildProgressBar(percentage, item["status"], "browser_inprogress_pipes_table_td_progress_" + item["id"]);
        var tdElement = $("#run-" + item["id"] + "-status");
        tdElement.html(item["status"]);
    });
    // Todo : update controls
}



function ws_new_pipeline(msg_data)
{

}

function ws_new_run(msg_data)
{   
}

function ws_run_changed(data)
{
    jQuery.each(data, function(index, item) 
    {

        var percentage = (item["progress"]["value"] / item["progress"]["max"] * 100).toFixed(2);

        if (demo_pirus_displayed_run == item["id"])
        {
            update_run_header(item);
        }

        elmt = $('#browser_navpanel_inprogress_run_' + item["id"]);
        if (elmt.length > 0)
        {
            if ($.inArray(item["status"],["ERROR", "CANCELED", "DONE"]) > -1)
            {
                elmt.delete();
            }
            else
            {
                elmt.html("<a onclick=\"javascript:show_tab('browser_run','{0}')\" href=\"#\"><i class=\"fa fa-tasks\" aria-hidden=\"true\"></i> {1} <span>{2}%</span></a>".format(item["id"], item["name"], Math.round(percentage)));
            }
        }
        else
        {
            $('#browser_navpanel_inprogress ul').append("<li id=\"browser_navpanel_inprogress_run_{0}\"><a onclick=\"javascript:show_tab('browser_run','{0}')\" href=\"#\"><i class=\"fa fa-tasks\" aria-hidden=\"true\"></i> {1} <span>{2}%</span></a></li>".format(item["id"], item["name"], percentage));
        }
    });
}







/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* TOOLS
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

function humansize(nbytes)
{
    var suffixes = ['o', 'Ko', 'Mo', 'Go', 'To', 'Po']
    if (nbytes == 0) return '0 o'

    var i = 0
    while (nbytes >= 1024 && i < suffixes.length-1)
    {
        nbytes /= 1024.
        i += 1
    }
    f = Math.round(nbytes * 100) / 100
    return f + " " + suffixes[i]
}

var demo_pirus_extensions = 
{
    "image" :   ["jpg", "jpeg", "gif", "png", "bmp", "tiff"],
    "archive" : ["zip", "tar.gz", "tar", "tar.xz", "gz", "xz", "rar"],
    "code" :    ["html", "htm", "py"],
    "text" :    ["log", "txt", "vcf", "sam"],
    "pdf" :     ["pdf"],
    "excel" :   ["xls", "xlsx"]
};
function get_file_icon(extension)
{
    for (var k in demo_pirus_extensions)
    {
        if (typeof demo_pirus_extensions[k] !== 'function') 
        {
            if ($.inArray(extension,demo_pirus_extensions[k]) > -1)
                return '<i class="fa fa-file-' + k +'-o" aria-hidden="true"></i>';
        }
    }
    return '<i class="fa fa-file-o" aria-hidden="true"></i>'
}