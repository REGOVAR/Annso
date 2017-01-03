


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





function AnnsoControler () {
    this.model = "";
    this.selected_tab = "welcom_toolbar";






    // ------------------------------------------------------------------
    // MODEL CREATE a new empty analysis
    this.new_empty = function ()
    {
        error({"msg" : "not yet implemented"});
    }




    // ------------------------------------------------------------------
    // MODEL CREATE a new analysis based on a template id
    this.new_from_template = function (template_id)
    {

    }


    // ------------------------------------------------------------------
    // MODEL LOAD an analysis from server
    this.load = function (id)
    {
        $.ajax({ url: rootURL + "/analysis/" + id, type: "GET", async: false}).fail(function()
        {
            this.error();
        }).done(function(json) 
        {
            if (json["success"])
            {
                this.analysis = new Analysis(json["data"]);
            }
            else
            {
                error(json);
            }
        });
    }
}







var controler = new AnnsoControler;














function select_tab(tab_name)
{
    $('#welcom_toolbar').hide();
    $('#sample_toolbar').hide();
    $('#variant_toolbar').hide();
    $('#result_toolbar').hide();
    $('#' + tab_name + '_toolbar').show();

    if (tab_name == "variant")
    {
        // Try to load variant according to the samples and filter
        load_variants_array();
    }
}


function create_analysis()
{
    var analysis_name = $('#modal_new_analysis_name').val();
    var template_id = -1;

    if (analysis_name != "")
    {
        $.ajax(
        {
            url: rootURL + "/analysis",
            type: "POST",
            data: "{\"name\" : \""+ analysis_name +"\", \"template_id\" : " + template_id + "}",
            async: false
        }).fail(function()
        {
            alert( "ERROR" );
        }).done(function(json)
        {
            load_analysis(json);
        });
    }
    else
    {
        alert("Thanks to give a name to your analyse.");
    }
}

function start_analysis(id)
{
    $.ajax({ url: rootURL + "/analysis/" + id, type: "GET", async: false}).fail(function()
    {
        alert( "ERROR" );
    }).done(function(json) 
    {
        load_analysis(json);
    });
}



function load_analysis(json)
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

    // Reset new analysis form
    $('#modal_new_analysis_name').val("");
    $('#modal_new_analysis').modal('hide');


    // Set main title
    $('#analysis_title').html(analysis_title_template.format(json["name"]));
    demo_analysis_id = json["id"];

    // Apply analysis settings
    // TODO load from json["setting"]
    demo_sample_attributes = {}
    demo_samples = {1:{"name":"B00H79Q.HC", "nickname":"Olivier"}};
    demo_fields = [2, 4, 5, 6, 7, 8, 9, 11, 22, 16];
    demo_filter = ['AND', [['==',['field',4], ['value', 1]], ['>', ['field', 9], ['value', 50]]]];


    // Todo : reset samples screen, filters, reports, ...
    $('#browser_samples').html("<span class=\"maincontent_placeholder\">&#11172; Import and select sample(s) you want to analyse.</span>")
    // Automaticaly select the Sample section
    $('#nav_project_sample')[0].click(function (e) { e.preventDefault(); $(this).tab('show'); })


    // Reset UI field list
    $('#annotation_fields_list li').each(function(idx) {
        $(this).removeClass('check');
        $(this).addClass('uncheck');
    });
    $.each(demo_fields, function(idx, fid) 
    {
        db_id = '#annotation_fields_db_'+ annotation_fields[fid]['db_id'];
        $(db_id).removeClass('uncheck');
        $(db_id).addClass('check');
        $('#annotation_fields_field_'+fid).removeClass('uncheck');
        $('#annotation_fields_field_'+fid).addClass('check');
    });

    // Reset UI filter
    $('#filters_panel_menu_filter_c > ul').html(build_filter_ui(demo_filter));
}

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
    else
    {
        return "TO BE implemented";
    }
}

var filter_operator_display_map = {'==' : '=', '!=' : "&#8800;", '>' : "&gt;", '>=' : "&#8805;", '<' : "&lt;", '<=' : "&#8804;"};
var add_filter_ui_parent_elmt;
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





function apply_filter()
{
    demo_filter = build_filter_json($('#filters_panel_menu_filter_c > ul > li'));
    console.debug(demo_filter);

    load_variants_array();

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

function toggle_select_sample( id, clean_list=false)
{
    // check if need to add the table
    if (Object.keys(demo_samples).length == 0)
    {
        $('#browser_samples').html("<table id=\"browser_samples_table\" class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"100%\" style=\"margin:0;\"><thead><tr><th style=\"width:30px;\"></th><th>Sample</th></tr></thead><tbody></tbody></table>");
    }

    // check if id already in the list
    checked = false;
    if (id in demo_samples)
    {
        // update check status
        demo_samples[id]["checked"] = !demo_samples[id]["checked"];
        $('#browser_samples_table_'+id+ " input").prop('checked', demo_samples[id]["checked"]);

        // update model & view
        if (!demo_samples[id]["checked"] && clean_list)
        {
            delete(demo_samples[id]);
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
        demo_samples[id] = {"name" : sample["name"], "comments" : sample["comments"], "analyses" : "", "nickname" : "", "attributes" : [], "checked" : true};
        // TODO build row according to existing attributes
        $('#browser_samples_table tbody').append('<tr id="browser_samples_table_{0}"><td><input type=\"checkbox\" value=\"{0}\" checked/></td><td>{1}</td></tr>'.format(id, sample["name"]));
    }
}


function load_variants_array()
{
    // Init the analysis by creating relation between sample, attributes and the analysis
    samples = [];
    $.each(demo_samples, function( key, data ) {
        if (data["checked"])
        {
            samples.push({"id" : key, "attributes" : []});
        }
    });
    $('#variants_list').html('<i class="fa fa-refresh fa-spin fa-3x fa-fw" style="display:block;margin:auto;margin-top:200px;"></i><span class="sr-only">Loading data from database</span>');


    // retrieve list of sample
    $.ajax({ 
        url: rootURL + "/analysis/" + demo_analysis_id + "/filtering", 
        type: "POST",
        data: "{\"mode\" : \"table\", \"filter\" : " + JSON.stringify(demo_filter) + ", \"fields\" : " + JSON.stringify(demo_fields) + "}",
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

    for (var i=0; i<demo_fields.length; i++)
    {
        html += "<th>{0}</th>".format(annotation_fields[demo_fields[i]]["name"]);
    }
    html += "</tr></thead><tbody>";


    var rowhtml = "<tr id=\"variant_{0}\" style=\"cursor: pointer;\"><td><input type=\"checkbox\" value=\"{0}\"/></td>";
    "<td>{1}</td><td>{2}</td><td class=\"pos\">{3}</td><td class=\"seq\">{4}</td><td class=\"seq\">{5}</td></tr>";
    
    $.each(json, function( idx, v ) 
    {

        html += rowhtml.format(v["variant_id"]);
        for (var i=0; i<demo_fields.length; i++)
        {
            fid   = demo_fields[i];
            ftype = annotation_fields[fid]["type"];

            if (fid in annotation_fields_formaters)
            {
                // use special format method to display this field
                html += annotation_fields_formaters[fid](v[demo_fields[i]]);
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
    return "<td>Sample {0}</td>".format(id);
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

        demo_fields.splice(demo_fields.indexOf(f_id),1);
    }
    else
    {
        $(elmt).parent().addClass('check');
        $(elmt).parent().removeClass('uncheck');

        demo_fields.push(f_id);
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

function filter_toggle_condition_group(elmt)
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



function fake_add_sample_attribute()
{
    i=0;
    data = [["<i class=\"fa fa-tag\" aria-hidden=\"true\" style=\"width:20px; text-align:center;\">&nbsp;</i> Control", "<i class=\"fa fa-tag\" aria-hidden=\"true\" style=\"width:20px; text-align:center;\">&nbsp;</i> Sex"],
     ["Yes", "Male"], 
     ["Yes", "Female"], 
     ["No", "Male"]];
    

    $('#browser_samples_table tr').each(function()
    {
        td = (i == 0) ? "th style=\"width:200px\"" : "td";
        $(this).append('<{0}>{1}</{0}><{0}>{2}</{0}>'.format(td, data[i][0], data[i][1]));
        i += 1;
    });

}




function fake_select_variant_submenu(menu_name)
{

    $('#filters_panel_menu_quick').hide();
    $('#filters_panel_menu_info').hide();
    $('#filters_panel_menu_filter').hide();
    $('#filters_panel_menu_' + menu_name ).show();
}

function fake_select_select_submenu(menu_name)
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

function fake_generate_report()
{
    $.ajax({ url: "http://annso.absolumentg.fr/v1/report", type: "GET", async: false}).done(function(report)
    {
        $('#selection_panel_content_report').html(report);
        
    });
}























/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/* Demo browser methods
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */


function display_status_bar(file_id)
{
    var details =  $('#fileEntry-' + file_id + ' td:nth-child(5)').html();
    $('#demo_footer').html((details == "None") ? "&nbsp;" : details);
}


function run_cmd(order)
{
    $.ajax({ url: rootURL + "/run/" + demo_pirus_displayed_run + "/" + order, type: "GET", async: false}).done(function(jsonFile)
    {
        data = jsonFile["data"];
        update_run_header(data);
        
    });
}



function update_run_header(data)
{
    progress = Math.round(parseInt(data["progress"]["value"]) / Math.max(1, (parseInt(data["progress"]["max"]) - parseInt(data["progress"]["min"]))) * 100);

    // Header according the status of the run
    $("#browser_run_name").html("Run : {0}".format(data["name"]));
    $("#browser_run_details").html("Pipeline {0} : <b>{1} % </b>".format(demo_pirus_displayed_run_pipename, progress));
    $("#browser_run_status").html(data["status"]);
    $('#browser_run_monitoring_progress').attr('style', 'right:'+ (100-Math.max(1, progress)) + '%');
    if ($.inArray(data["status"],["PAUSE", "WAITING"]) > -1)$('#browser_run_monitoring_header').attr('class', 'orange');
    if ($.inArray(data["status"], ["ERROR", "CANCELED"]) > -1) $('#browser_run_monitoring_header').attr('class', 'red');
    if ($.inArray(data["status"], ["INITIALIZING", "RUNNING", "FINISHING"]) > -1) $('#browser_run_monitoring_header').attr('class', 'blue');
    if ($.inArray(data["status"],["DONE"]) > -1) $('#browser_run_monitoring_header').attr('class', 'green');

    //  controls according the status of the run
    if ($.inArray(data["status"], ["INITIALIZING", "RUNNING", "WAITING"]) > -1) 
    {
        $('#browser_run_playpause').html('<i class="fa fa-pause" aria-hidden="true"></i>');
        $('#browser_run_playpause').attr('onclick', 'javascript:run_cmd("pause");');
        $('#browser_run_playpause').removeClass('disabled');
        $('#browser_run_stop').removeClass('disabled');
        $('#browser_run_monitoring_refresh').removeClass('collapse');
    }
    else if ($.inArray(data["status"], ["PAUSE"]) > -1) 
    {
        $('#browser_run_playpause').html('<i class="fa fa-play" aria-hidden="true"></i>');
        $('#browser_run_playpause').attr('onclick', 'javascript:run_cmd("play");');
        $('#browser_run_playpause').removeClass('disabled');
        $('#browser_run_stop').removeClass('disabled');
        $('#browser_run_monitoring_refresh').addClass('collapse');
    }
    else // DONE, CANCELED, ERROR
    {
        $('#browser_run_playpause').html('<i class="fa fa-play" aria-hidden="true"></i>');
        $('#browser_run_playpause').attr('onclick', '');
        $('#browser_run_playpause').addClass('disabled');
        $("#browser_run_stop").attr('onclick', '');
        $('#browser_run_stop').addClass('disabled');
        $('#browser_run_monitoring_refresh').addClass('collapse');
    }

    // Logs 
    if (data["vm_info"])
    {
        var html = "<ul>";
        for (k in data["vm"])
        {
            html += "<li><b>{0} :</b> {1}</li>".format(k, data["vm"][k]);
        }
        $("#browser_run_monitoring_vm").html(html);
    }
    else
    {
        $("#browser_run_monitoring_vm").html("<i>{0}</i>".format(data["vm"]));
    }
}


function update_file_header(data)
{
    progress = Math.round(data["upload_offset"] / Math.max(1, data["size"]) * 100);

    // Header style / control according to the status of the file
    if ($.inArray(data["status"],["PAUSE"]) > -1) $('#browser_file_header').attr('class', 'orange');
    if ($.inArray(data["status"], ["ERROR"]) > -1) $('#browser_file_header').attr('class', 'red');
    if ($.inArray(data["status"], ["UPLOADING"]) > -1) $('#browser_file_header').attr('class', 'blue');
    if ($.inArray(data["status"],["UPLOADED", "CHECKED"]) > -1) $('#browser_file_header').attr('class', 'green');
    $('#browser_file_progress').attr('style', 'right:'+ (100-Math.max(1, progress)) + '%');

    
    $("#browser_file_icon").html(get_file_icon(data["type"]));
    $("#browser_file_name").html(data["name"]);
    if ($.inArray(data["status"], ["UPLOADING", "PAUSE", "ERROR"]) > -1)
        $("#browser_file_details").html("Size : {0} / <b>{1}</b>".format(humansize(data["upload_offset"]), humansize(data["size"])));
    else
        $("#browser_file_details").html("Size : <b>{0}</b>".format(humansize(data["size"])));
    if ($.inArray(data["status"],["PAUSE"]) > -1)
        $("#browser_file_status").html(data["status"] + "<br/><span style=\"font-size:12px; font-style:italic; font-weight:100;\">since " + data["status"] + "</span>");
    else
        $("#browser_file_status").html(data["status"]);

    // Infos panel
    html = "<ul>";
    for (var k in data)
    {
        if (typeof data[k] !== 'function') 
        {
            html += "<li><b>{0} : </b>{1}</li>".format(k, data[k]);
        }
    }
    html += "</ul>";
    $("#file_tab_infos").html(html);
}


function show_tab(tab_id, id)
{
    $('#browser_content > div').each( function( index, element )
    {
        $(element).addClass("collapse");
    });
    $('#' + tab_id).removeClass("collapse");
    
    // Manage display of run data
    if (tab_id == 'browser_run')
    {        
        $.ajax({ url: rootURL + "/run/" + id + "/monitoring", type: "GET", async: false}).done(function(jsonFile)
        {

            data = jsonFile["data"];
            demo_pirus_displayed_run = id;
            demo_pirus_displayed_run_pipename = data["pipeline_name"];

            update_run_header(data)
            $("#browser_run_icon").html("<img src=\"{0}\" width=\"50px\" style=\"vertical-align:middle\"/>".format(data["pipeline_icon"]));


            $("#browser_run_monitoring_stdout").text((data["out_tail"] == "") ? "... No log on stdOut ..." : data["out_tail"]);
            $("#browser_run_monitoring_stdout").animate({scrollTop : $("#browser_run_monitoring_stdout")[0].scrollHeight }, 1000 );

            $("#browser_run_monitoring_stderr").text((data["err_tail"] == "") ? "... No log on stdErr ..." : data["err_tail"]);
            $("#browser_run_monitoring_stderr").animate({scrollTop : $("#browser_run_monitoring_stderr")[0].scrollHeight}, 1000 );

            $("#browser_run_monitoring_refresh").attr("onclick", "javascript:monitor_run('"+id+"')");
            $("#browser_run_monitoring_delete").attr("onclick", "javascript:pirus_delete('run', '"+id+"')");
        });


        // Inputs / outputs
        $.ajax({ url: rootURL + "/run/" + id + "/io", type: "GET", async: false}).done(function(jsonFile)
        {
            data = jsonFile["data"];
            if (data["inputs"].length > 0)
            {
                html = "<ul>";
                for (var i=0; i<data["inputs"].length; i++)
                {
                    html += "<li><a href=\"" + rootURL + "/dl/f/" + data["inputs"][i]["id"] + "\" title=\"Download\">" + data["inputs"][i]["name"] + "</a> (" + humansize(data["inputs"][i]["size"]) + ")</li>";
                }
                html += "</ul>";
                $("#monitoring_tab_inputs").html(html);
            }
            else
            {
                $("#monitoring_tab_inputs").html("<i>No input file for this run.</i>");
            }

            if (data["outputs"].length > 0)
            {
                html = "<ul>"
                for (var i=0; i<data["outputs"].length; i++)
                {
                    html += "<li><a href=\"" + rootURL + "/dl/f/" + data["outputs"][i]["id"] + "\" title=\"Download\">" + data["outputs"][i]["name"] + "</a> (" + humansize(data["outputs"][i]["size"]) + ")</li>"
                }
                html += "</ul>"
                $("#monitoring_tab_outputs").html(html)
            }
            else
            {
                $("#monitoring_tab_outputs").html("<i>No ouputs file for this run.</i>");
            }
        });
    }


    // Display of a file
    if (tab_id == "browser_file")
    {
        demo_pirus_displayed_file = id;
        $.ajax({ url: rootURL + "/file/" + id, type: "GET", async: false}).done(function(jsonFile)
        {
            data = jsonFile["data"];
            update_file_header(data);
            $("#browser_file_delete").attr("onclick", "javascript:pirus_delete('file', '"+id+"')");

            // Edit panel
            $("#file_tab_edit_name").val(data["name"]);
            $("#file_tab_edit_type").val(data["type"]);
            $("#file_tab_edit_comments").val(data["comments"]);
            $("#file_tab_edit_tags").val(data["tags"]);

            // Preview panel
            $("#file_tab_preview").html("<i>No preview available.</i>");
        });
    }
}


var status_colorclass_map = {
    "UPLOADING" : "text-primary",
    "PAUSE" : "text-warning",
    "UPLOADED" : "text-success",
    "ERROR" : "text-alert", 
    "CHECKED" : "text-success"
};

function select_file(file_id)
{
    var count = Object.keys(demo_pirus_selection).length;
    var check = !$('#fileEntry-' + file_id + ' input')[0].checked;
    $('#fileEntry-' + file_id + ' input').prop('checked', check);
    var file_name =  $('#fileEntry-' + file_id + ' td:nth-child(2)').text().trim();
    var file_status = $('#fileEntry-' + file_id + ' td:nth-child(7)').text().trim();
    if (check)
    {
        if (count == 0) $('#browserNavSelectionPanel > ul').html('');
        demo_pirus_selection[file_id] = file_name;
        var html = '<li id="browserNavSelectionPanel-' + file_id + "\"><a onclick=\"javascript:show_tab('browser_file','" + file_id + "')\" href=\"#\">";
        html += "<i class=\"fa fa-file " + status_colorclass_map[file_status] + "\" aria-hidden=\"true\"></i> " + file_name + '</a></li>';
        $('#browserNavSelectionPanel ul').append(html);
        count += 1;
    }
    else
    {
        delete demo_pirus_selection[file_id];
        $('#browserNavSelectionPanel-' + file_id).remove();
        if (count == 1) $('#browserNavSelectionPanel > ul').html('<li class="empty_selection">No file selected</li>');
        count -= 1
    }
    
    $('#selection_count').html(count);
}

var activity_inprogress_count = 0
var demo_browser_file_entry =  "<tr id=\"fileEntry-{0}\" onclick=\"javascript:select_file('{0}')\" style=\"cursor: pointer; {1}\">"
demo_browser_file_entry +=  "<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td></tr>";



function add_new_activity_to_demo_browser(type, id)
{
    $('#inprogress_count').html(activity_inprogress_count);
    var name = "name";
    var details = "details";
    var progress = "progress";
    var status = "status";
    // Retrieve data
    activity_inprogress_count += 1;
    if (type == "file")
    {
        // check if entry already exists (resume previous upload)
        elmnt = $('#fileEntry-' + id);
        if (elmnt.length)
        {
            // elmnt exist, so update it
            elmnt[0].replaceWith(demo_browser_file_entry.format(id, name, size, creation, comments, tags , id, status, status_colorclass_map[status]));
        }
        else
        {
            // add new entry into the table
            $('#browser_files_table tbody').append(demo_browser_file_entry.format(id, name, size, creation, comments, tags , id, status, status_colorclass_map[status]));
        }
        
    }
    else if (type == "pipeline")
    {
        $('#browser_inprogress_pipes_table').append(demo_browser_file_entry.format(id, name, size, creation, comments));
    }
    else if (type == "run")
    {
        $('#browser_inprogress_runs_table').append(demo_browser_file_entry.format(id, name, size, creation, comments));
    }

    // Update IHM
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
/* New Run Popup methods
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

var BrutusinForms = brutusin["json-forms"];
var bf, schema;

var runConfigPipeId;
var runConfigPipeName = "{TODO - Pipe Name}";
var runConfigForm;
var runConfigInputs;

function init_run(pipe_id)
{
    // 1- retrieve pipe-config
    $.ajax(
    {
        url: rootURL + "/pipeline/" + pipe_id + "/form.json",
        type: "GET"
    }).fail(function()
    {
        alert( "ERROR" );
    }).done(function(json) 
    {
        var json_db = [];

        if (json.indexOf("__PIRUS_DB_ALL__") != -1)
        {

            // get list of database
            $.ajax({ url: rootURL + "/db", type: "GET", async: false}).done(function(jsonDB)
            {
                json_db = jsonDB["data"];
            })

            json = json.replace(/"__PIRUS_DB_ALL__"/g, JSON.stringify(json_db));
        }
        runConfigForm = json;
        runConfigPipeId = pipe_id;

        $("#inputFilesList tbody").empty();
        for (var key in demo_pirus_selection)
        {
            var size = $('#fileEntry-' + key + " td:nth-child(3)").html();
            var date = $('#fileEntry-' + key + " td:nth-child(4)").html();
            var comments = $('#fileEntry-' + key + " td:nth-child(5)").html();
            $("#inputFilesList > tbody").append("<tr><td>{0}<br/><span class=\"details\">{3}</span></td><td>{1}</td><td>{2}</td></td>".format(demo_pirus_selection[key], size, date, key));
        }


        
        run_config_step_2();
    })
}


function run_config_step_2()
{
    // Retrieve list of selected inputs
    var json_files = []
    var json = runConfigForm
    if (json.indexOf("__PIRUS_INPUT_FILES__") != -1)
    {
        var i = 0;
        for (var key in demo_pirus_selection)
        {
            json_files[i] = demo_pirus_selection[key];
            i++;
        }
        
        json = json.replace(/"__PIRUS_INPUT_FILES__"/g, JSON.stringify(json_files))
    }

    schema = JSON.parse(json);
    schema["properties"]["name"] = {
        "title": "Nom du run",
        "description": "Le nom qui sera affiché pour ce run.",
        "type": "string",
        "required": true
    };
    
    bf = BrutusinForms.create(schema);
    var container = document.getElementById('runConfigContainer');
    container.innerText = ""
    bf.render(container, null);
}

function run_config_step_3()
{
    if (bf.validate())
    {
        config = bf.getData();
        config = JSON.stringify(config, null, 4);


        var html = "<h3>Pipeline : " + runConfigPipeName + "</h3><h4>Inputs</h4>";
        var count = Object.keys(demo_pirus_selection).length;
        if (count > 0)
        {
            html += "<ul>";
            for (var key in demo_pirus_selection)
            {
                html += "<li>{0}</li>".format(demo_pirus_selection[key]);
            }
            html += "</ul>";
        }
        html += "<h4>Config</h4>";
        for (var key in config)
        {
            html += "<li><b>{0}</b> : {1}</li>".format(key, config[key]);
        }
        html += "</ul>";


        $('#runConfirmContainer').html(html);
    }
    else
    {
        // Todo : return on step 2
    }
}
function run_config_step_4()
{
    if (bf.validate())
    {
        config = bf.getData()
        config = JSON.stringify(config, null, 4)
        inputs = []

        var i = 0;
        for (var key in demo_pirus_selection)
        {
            inputs[i] = key;
            config = config.replace(new RegExp(demo_pirus_selection[key], 'g'), key);

            i++;
        }

        inputs = JSON.stringify(inputs, null, 4)

        $.ajax(
        {
            url: rootURL + "/run",
            type: "POST",
            data: "{\"pipeline_id\" : \""+ runConfigPipeId +"\", \"config\" : " + config + ", \"inputs\" : " + inputs + "}"
        }).fail(function()
        {
            alert( "ERROR" );
        }).done(function(txt) 
        {
            alert( "SUCCESS\n" + txt);
        })
    }
}














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









function buildProgressBar(percentage, pbTheme, containerId) {
    var style="progress-bar "

    if  (pbTheme == "ERROR" || pbTheme == "CANCELED")
        { style += "progress-bar-danger"}
    else if (pbTheme == "DONE" || pbTheme == "UPLOADED" || pbTheme == "CHECKED" || pbTheme == 'READY')
        { style += "progress-bar-success"}
    else if (pbTheme == "PAUSE")
        { style += "progress-bar-warning"}
    else if (pbTheme == "RUNNING" || pbTheme == "UPLOADING")
        { style += "progress-bar-striped active"}
    else if (pbTheme == "WAITING") { style += "progress-bar-warning progress-bar-striped active"}



    var html = "<div class='progress'>\
                <div class='" + style + "' role='progressbar' aria-valuenow='" + percentage + "' aria-valuemin='0' aria-valuemax='0' \
                    style='min-width: 2em; width: " + percentage + "%;'>\
                    " + percentage + "% \
                </div>\
            </div>"

    if (containerId !== null)
    {
        $("#" + containerId).html(html)
    }

    return html
}

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