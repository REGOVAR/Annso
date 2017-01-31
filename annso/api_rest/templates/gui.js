


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

function display_error(msg)
{
    $('#modal_error_id').text("");
    $('#modal_error_code').text("");
    $('#modal_error_code').attr('href', "#");
    $('#modal_error_msg').text(msg);
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
            url: "{0}/analysis".format(rootURL),
            type: "POST",
            data: '{"name" : "{0}", "template_id" : {1}}'.format(name, template_id),
            async: false
        }).fail(function() { display_error("TODO : network error"); })
        .done(function(json)
        {
            analysis.load_analysis(json['data']['id']);
        });
    };


    // ------------------------------------------------------------------
    // Load an analysis from server
    this.load_analysis = function (id)
    {
        $.ajax({ url: "{0}/analysis/{1}".format(rootURL, id), type: "GET", async: false}).fail(function() { display_error("TODO : network error"); })
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
        var samples = [];
        $.each(analysis.analysis.samples, function(sid, s) 
        {
            samples.push(s);
        });

        // First build attribute list from the HMI
        var attributes={};
        $('#browser_samples_table th input').each(function (i)
        {
            var value = $(this).val();
            attributes[i+1] = (value == "" || !/^[a-z0-9]+$/i.test(value)) ? null : {'name':value, 'samples_value': {}};
        });

        $('#browser_samples_table tbody tr').each (function (i)
        {
            var sample_id = $(this).attr("id").split('_')[3];
            $(this).find('input').each( function (i)
            {
                // ignore first input as it's for sample's name.
                if (i == 0) return;

                var value = $(this).val();
                if (attributes[i] != null)
                {
                    attributes[i]['samples_value'][sample_id] = (value == "" || !/^[a-z0-9]+$/i.test(value)) ? "" : value;
                }
            });
        });

        analysis.analysis.attributes = [];
        $.each(attributes, function(aid, a) 
        {
            analysis.analysis.attributes.push(a);
        });

        $.ajax({ 
            url: rootURL + "/analysis/" + analysis.analysis.id, 
            type: "PUT", 
            data: JSON.stringify({
                "samples" : samples,
                "attributes" : analysis.analysis.attributes,
                "fields" : analysis.analysis.fields,
                "filter" : analysis.analysis.filter
            }),
            async: false}).fail(function() { display_error("TODO : network error"); })
        .done(function(json)
        {
            if (!json["success"])
            {
                error(json);
            }
        });
    };


    this.add_sample = function (id)
    {
        var sample = null;
        $.ajax({ url: rootURL + "/sample/" + id, type: "GET", async: false}).done(function(json)
        {
            sample = json["data"];
        });
        analysis.analysis.samples[id] = {"id" : id, "name" : sample["name"], "comments" : sample["comments"], "analyses" : "", "nickname" : "", "attributes" : []};
        return sample;
    };

    this.remove_sample = function (id)
    {
        delete(analysis.analysis.samples[id]);
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

        $.ajax({ 
            url: "{0}/analysis/{1}/savefilter".format(rootURL, analysis.analysis.id), 
            type: "POST", 
            data: JSON.stringify({'name': name, 'filter':analysis.analysis.filter}),
            async: false}).fail(function() { display_error("TODO : network error"); })
        .done(function(json)
        {
            if (json["success"])
            {
                analysis.analysis.filters[json.data['id']] = json.data;
            }
            else
            {
                error(json);
            }
        });
    };


    this.add_to_selection = function (id)
    {
        if (analysis.analysis.selection.indexOf(id) == -1)
        {
            analysis.analysis.selection.push(id);
        }
        
    };

    this.remove_to_selection = function (id)
    {
        var idx = analysis.analysis.selection.indexOf(id);
        if (idx != -1)
        {
            analysis.analysis.selection.splice(idx, 1);
        }
    };

    this.export_selection = function ()
    {
        $.ajax({ 
            url: "{0}/analysis/{1}/export/{2}".format(rootURL, analysis.analysis.id, 'csv'), 
            type: "POST", 
            data: JSON.stringify({}),
            async: false}).fail(function() { display_error("TODO : network error"); })
        .done(function(json)
        {
            if (json["success"])
            {
                $('#selection_list').html(json);
            }
            else
            {
                error(json);
            }
        });
    };


    this.report_selection = function ()
    {
        $.ajax({ 
            url: "{0}/analysis/{1}/report/{2}".format(rootURL, analysis.analysis.id, 'dims'),
            type: "POST", 
            data: JSON.stringify({}),
            async: false}).fail(function() { display_error("TODO : network error"); })
        .done(function(report)
        {
            $('#selection_list').html(report);
        });
    };

};

var analysis = new AnnsoControler;






function AnnsoUIControler ()
{

    this.current_tab = "welcom";
    this.tus_uploader = null;

    // ------------------------------------------------------------
    // GLOBAL MENUS / TAB NAVIGATION 

    this.select_tab = function(tab_name)
    {
        this.current_tab = tab_name;
        $('#welcom_toolbar').hide();
        $('#sample_toolbar').hide();
        $('#variant_toolbar').hide();
        $('#' + tab_name + '_toolbar').show();

        if (tab_name == "variant")
        {
            // Save analysis parameters
            analysis.save_analysis();

            // Force refresh of the variant array
            load_variants_array();
        }
    };

    this.select_view = function(view_name)
    {
        if (view_name == null)
        {
            $('#filters_panel_menu_quick').hide();
            $('#filters_panel_menu_info').hide();
            $('#filters_panel_menu_filter').hide();

            $('#variants_list').hide();
            $('#selection_list').show();
        }
        else
        {
            $('#filters_panel_menu_quick').hide();
            $('#filters_panel_menu_info').hide();
            $('#filters_panel_menu_filter').hide();
            $('#filters_panel_menu_' + view_name ).show();

            $('#selection_list').hide();
            $('#variants_list').show();
        }
    };








    // ------------------------------------------------------------
    // DISPLAY method (used to refresh UI according to the model)

    this.display_sample_header = function(flag)
    {
        if (!flag)
        {
            $('#browser_samples').html("<span class=\"maincontent_placeholder\">&#11172; Import and select sample(s) you want to analyse.</span>");
        }
        else
        {
            var html = "";
            $.each(analysis.analysis.attributes, function(id, attr) 
            {
                html += sample_selection_table_attribute.format("th", "Attribute name", attr['name']);
            });
            $('#browser_samples').html(sample_selection_table_header.format(html));
        }
    }

    this.display_saved_filter = function()
    {
        var html = "";
        if (Object.keys(analysis.analysis.filters).length == 0)
        {
            html = filter_save_filter_empty;
        }
        else
        {
            $.each(analysis.analysis.filters, function(fid, f) 
            {
                html += filter_save_filter_row.format(fid, f['name']);
            });
        }

        $('#filters_panel_menu_quick_f > ul').html(html);
        $('#filters_panel_menu_filter_f > ul').html(html);
    }





    this.variant_display = function (display_mode)
    {
        // display_mode = table | list
    };





























    // ------------------------------------------------------------
    // UI ACTIONS

    this.create_analysis = function ()
    {
        var analysis_name = $('#modal_new_analysis_name').val();
        var template_id = -1;

        if (analysis_name != "")
        {
            analysis.new_analysis(analysis_name, template_id);
        }
        else
        {
            alert("Thanks to give a name to your analyse.");
            return;
        }

        if (!analysis.is_valid())
        {
            alert ("TODO : reset whole IHM");
        }  

        $('#modal_new_analysis').modal('hide');
    };


    this.tus_upload = function()
    {
        // Start or continue an upload of file with TUS protocol
        if (this.tus_uploader != null)
        {
            alert("Upload already in progress.");
            return;
        }


        if (!tus.isSupported) 
        {
            $('#modal_import_sample_file .modal-body').html("TUS Not supported ! Upload not available with this browser");
        }

        var file = $("#modal_import_file_tus_localinput").prop('files')[0];
        var chunkSize = parseInt($('#modal_new_file_tus_chunksize').val(), 10);
        console.log("selected file", file);


        if (isNaN(chunkSize)) 
        {
            chunkSize = Infinity;
        }
        var options = {
            endpoint: $('#modal_new_file_tus_endpoint').val(),
            resume: true,
            chunkSize: chunkSize,
            metadata: { 'filename': file.name },
            onError: function(error) 
            {
                $("#modal_import_file_tus_localinput").val("");
                display_error("Failed because: " + error, "alert", "tusFileProgress");
                this.tus_uploader = null;
            },
            onProgress: function(bytesUploaded, bytesTotal) 
            {
                $('#modal_new_file_details').removeClass("hidden");
                var percentage = (bytesUploaded / bytesTotal * 100).toFixed(2);
                console.log(bytesUploaded, bytesTotal, percentage + "%");
                buildProgressBar(percentage, "modal_new_file_progress");
            },
            onSuccess: function() 
            {
                $('#modal_new_file_details').removeClass("hidden");
                $("#modal_import_file_tus_localinput").val("");
                buildProgressBar(100, "modal_new_file_progress");
                this.tus_uploader = null;
            }
        }

        this.tus_uploader = new tus.Upload(file, options);
        this.tus_uploader.start();
    }



    this.reset_filter = function (id)
    {
        if (id == null || !id in analysis.analysis.filters)
        {
            // Empty filter
            $('#filters_panel_menu_filter_c > ul').html(filter_group_template.format('check', 'and', 'checked', '', '', ''));
        }
        else
        {
            // Load the saved filter
            analysis.analysis.filter = analysis.analysis.filters[id]['filter'];
            $('#filters_panel_menu_filter_c > ul').html(build_filter_ui(analysis.analysis.filter));
        }

        ui.apply_filter();
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
        analysis.save_filter(filter_name);

        // Refresh ui
        $('#modal_new_analysis').modal('hide');
        ui.display_saved_filter();

    };



    this.load_sample_database = function ()
    {
        $('#modal_import_sample_db_content').html('<i class="fa fa-refresh fa-spin fa-3x fa-fw" style="margin:200px 250px"></i><span class="sr-only">Loading data from database</span>');
        $.ajax({ url: "{0}/sample".format(rootURL), type: "GET", async: false}).fail(function()
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
                error(json);
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
    };


    this.update_sample_nickname = function (id, elmt)
    {
        var value = $(elmt).val().trim();
        $(elmt).val(value);
        if (value != "" && !/^[a-z0-9 ]+$/i.test(value))
        {
            display_error('Only alphanumeric characters (0...9 and Aa...Zz) are allowed.');
            $(elmt).addClass("error");
        }
        else
        {
            $(elmt).removeClass("error");
        }

        analysis.analysis.samples[id]["nickname"] = value;
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
        var value = $(elmt).val().trim();
        $(elmt).val(value);
        if (value != "" && !/^[a-z0-9]+$/i.test(value))
        {
            display_error('Only alphanumeric characters (0...9 and Aa...Zz) are allowed.');
            $(elmt).addClass("error");
        }
        else
        {
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
        if (Object.keys(analysis.analysis.samples).length == 0)
        {
            this.display_sample_header(false);
        }
        else
        {
            
            // tHeader
            this.display_sample_header(true);

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

                sp.nickname = (sp.nickname == null) ? "" : sp.nickname;
                html += sample_selection_table_row.format(id, sp.name, sp.nickname, attr_html);
            });
            $('#browser_samples_table tbody').append(html);
        }



        // Automaticaly select the Sample section
        $('#nav_project_sample').removeClass("hidden");
        $('#nav_project_variant').removeClass("hidden");
        $('#nav_project_selection').removeClass("hidden");
        $('#nav_project_sample')[0].click(function (e) { e.preventDefault(); $(this).tab('show'); })



        // Reset UI fields
        $('#annotation_fields_list input[type=checkbox]').each(function(idx, elmt) {
            $(elmt).prop('checked', false);
        });
        $.each(analysis.analysis.fields, function(idx, fid) 
        {
            $('#annotation_fields_field_{0}'.format(fid)).prop('checked', true);
        });

        // Reset UI filter
        $('#filters_panel_menu_filter_c > ul').html(build_filter_ui(analysis.analysis.filter));
        // Reset UI saved filters
        ui.display_saved_filter();
        ui.update_selection();
    };









    this.remove_sample = function (elmt)
    {
        id = $(elmt).parent().parent().attr("id").split('_')[3];
        analysis.remove_sample(id);
        $(elmt).parent().parent().remove();
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


    this.check_all_variant = function()
    {
        var checked = $('#checkbox_all_variants').prop('checked');
        $('#variants_list_table input[type=checkbox]').each( function (idx, elmt)
        {
            if (idx == 0) return;
            
            $(elmt).prop('checked', checked);
            ui.check_variant(elmt);
        });
    };
    this.check_variant = function(elmt)
    {
        if ($(elmt).prop('checked'))
        {
            analysis.add_to_selection($(elmt).val());
        }
        else
        {
            analysis.remove_to_selection($(elmt).val());
        }
        ui.update_selection();
    };


    this.update_selection = function()
    {
        if (analysis.analysis.selection.length > 0)
        {
            $('#show_selection').html(toolbar_selection_label.format(" <span class=\"badge\">{0}</span>".format(analysis.analysis.selection.length)));
            $('#show_selection').parent().find("button").each(function(idx, elmt){ $(elmt).attr('disabled', false);});
        }
        else
        {
            $('#show_selection').html(toolbar_selection_label.format(""));
            $('#show_selection').parent().find("button").each(function(idx, elmt){ $(elmt).attr('disabled', true);});
        }
    }



    this.show_selection = function()
    {
        // hide left menu
        ui.select_view(null);

        // Retrieve selected variant data
        $.ajax({ 
        url: "{0}/analysis/{1}/filtering".format(rootURL, analysis.analysis.id), 
        type: "POST",
        data: "{\"mode\" : \"table\", \"filter\" : " + JSON.stringify(analysis.analysis.filter) + ", \"fields\" : " + JSON.stringify(analysis.analysis.fields) + "}",
        async: true}).fail(function()
        {
            display_error("Unknow error in 'load_variants_array' request");
        }).done(function(json)
        {
            if (!json["success"])
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
                count = init_variants_list(json, '#variants_list');
                if (count == 100)
                {
                    // As the server return the max range variants, maybe the total is higher. so, do another request to get total count
                    loading_variants_count();
                }
                else
                {
                    $('#current_filter_count').html(annotation_format_number(count, false));
                    $('#demo_footer').html("{0} variant{1}".format(annotation_format_number(count, false), (count > 1) ? 's' : ''));
                }
                
            }
        });
        
    }

}
var ui = new AnnsoUIControler;












function update_filter_set_map()
{
    html='';
    entry = '<option value="{0}">{1}</option>';
    filter_set_map = {};
    attributes_values = [];
    var idx=0;
    $.each(analysis.analysis.samples, function (id, sample)
    {
        label = "sample " + ((sample["nickname"] != "") ? sample["nickname"] : sample["name"]);
        json  = ["sample", sample["id"]];
        html += entry.format(idx, label);
        filter_set_map[idx] = json;
        idx += 1;
    });
    $.each(analysis.analysis.attributes, function (id, key)
    {
        var k = key['name'];
        $.each(key['samples_value'], function (id, val)
        {
            kv = '{0}:{1}'.format(k, val);
            if (attributes_values.indexOf(kv) == -1)
            {
                attributes_values.push(kv);
                label = "group " + kv;
                json  = ["attribute",  kv];
                html += entry.format(idx, label);
                filter_set_map[idx] = json;
                idx += 1;
            }
        });
    });
    $.each(analysis.analysis.filters, function (id, filter)
    {
        label = "filter " + filter["name"];
        json  = ["filter",  id];
        html += entry.format(idx, label);
        filter_set_map[idx] = json;
        idx += 1;
    });

    $('#modal_filter_variant_set').html(html);
}





var filter_set_map = {};
var filter_operator_display_map = {'==' : '=', '!=' : "&#8800;", '>' : "&gt;", '>=' : "&#8805;", '<' : "&lt;", '<=' : "&#8804;", "IN":"&#8712;", "NOTIN":"&#8713;"};
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
        return filter_set_template.format('check', "{0} {1}".format(json[1], filter_operator_display_map[json[0]]), build_filter_ui_set(json[2]), JSON.stringify(json));
    }
    else
    {
        return "TO BE implemented";
    }
}
function build_filter_ui_set(json)
{
    html = "";

    if (json[0] == "sample")
    {
        s = analysis.analysis.samples[json[1]];
        html = "sample " + (s["nickname"] != "") ? s["nickname"] : s["name"];
    }
    else if (json[0] == "attribute")
    {
        html = "group " + json[1];
    }
    else if (json[0] == "filter")
    {
        f = analysis.analysis.filters[json[1]];
        html = "filter " + f["name"];
    }

    return html;
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

    json = [operator, type, filter_set_map[set]];
    


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






































function toggle_select_sample( id, clean_list=false)
{
    // check if need to add the table
    if (Object.keys(analysis.analysis.samples).length == 0)
    {
        ui.display_sample_header(true);
    }

    // Update check status in the popup
    // TODO : $('#browser_samples_table_'+id+ " input").prop('checked', analysis.analysis.samples[id]["checked"]);

    // update model & view
    if (id in analysis.analysis.samples)
    {
        // remove sample
        analysis.remove_sample(id);
        $('#browser_samples_table_'+id).remove();
    }
    else
    {
        // retrieve sample data and add it
        var sample = analysis.add_sample(id);
        

        var attr_html = "";
        $.each(analysis.analysis.attributes, function(id, attr) 
        {
            attr_html += sample_selection_table_attribute.format("td", "Attribute value", "");
        });
        $('#browser_samples_table tbody').append(sample_selection_table_row.format(id, sample['name'], "", attr_html));
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

    // displaying computing feedback
    $('#current_filter_count').html('<i class="fa fa-refresh fa-spin fa-fw"></i>');
    $('#demo_footer').html('Computing total number of variant filtered <i class="fa fa-refresh fa-spin fa-fw"></i>');
    $('#variants_list').html('<i class="fa fa-refresh fa-spin fa-3x fa-fw" style="display:block;margin:auto;margin-top:200px;"></i><span class="sr-only">Loading data from database</span>');


    // retrieve list of sample
    $.ajax({ 
        url: "{0}/analysis/{1}/filtering".format(rootURL, analysis.analysis.id), 
        type: "POST",
        data: "{\"mode\" : \"table\", \"filter\" : " + JSON.stringify(analysis.analysis.filter) + ", \"fields\" : " + JSON.stringify(analysis.analysis.fields) + "}",
        async: true}).fail(function()
    {
        display_error("Unknow error in 'load_variants_array' request");
    }).done(function(json)
    {
        if (!json["success"])
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
            count = init_variants_list(json, '#variants_list');
            if (count == 100)
            {
                // As the server return the max range variants, maybe the total is higher. so, do another request to get total count
                loading_variants_count();
            }
            else
            {
                $('#current_filter_count').html(annotation_format_number(count, false));
                $('#demo_footer').html("{0} variant{1}".format(annotation_format_number(count, false), (count > 1) ? 's' : ''));
            }
            
        }
    });
}


function loading_variants_count()
{
    // Sending request to get total count
    $.ajax({ 
        url: "{0}/analysis/{1}/filtering/count".format(rootURL, analysis.analysis.id), 
        type: "POST",
        data: "{\"mode\" : \"table\", \"filter\" : " + JSON.stringify(analysis.analysis.filter) + ", \"fields\" : " + JSON.stringify(analysis.analysis.fields) + "}",
        async: true}).fail(function()
    {
        display_error("Unknow error in 'loading_variants_count' request");
    }).done(function(json)
    {
        if (json["success"])
        {
            $('#current_filter_count').html(annotation_format_number(json["data"], false));
            $('#demo_footer').html("{0} variant{1}".format(annotation_format_number(json["data"], false), (json["data"] > 1) ? 's' : ''));
        }
        else
        {
            $('#current_filter_count').html("-");
            $('#demo_footer').html("-");
            display_error(json);
        }
        
    });
}




function init_variants_list(json, container_id)
{
    var count = 0;
    var html = variants_table_header_start;

    for (var i=0; i<analysis.analysis.fields.length; i++)
    {
        html += variants_table_header_cell.format(annotation_fields[analysis.analysis.fields[i]]["name"]);
    }
    html += variants_table_header_end;


    
    $.each(json["data"], function( idx, v ) 
    {
        count += 1;
        selected = (analysis.analysis.selection.indexOf(v["id"].toString()) == -1) ? "" : " checked";
        html += variants_table_row_start.format(v["id"], selected);
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
                    html += variants_table_row_cell.format(v[fid]);
            }
        }
        html += variants_table_row_end;
    });
    $(container_id).html(html + "</tbody></table>");
    return count;
}

function annotation_format_number(value, td=true)
{
    var model = (td) ? "<td class=\"number\">{0}</td>" : "<span class=\"number\">{0}</span>"
    var n = value.toString(), p = n.indexOf('.');
    return model.format(
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
    if (name == null || name == "")
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
















        $('#variants_list_table input[type=checkbox]').each( function (idx, elmt)
        {
            if (idx == 0) return;
            
            $(elmt).prop('checked', checked);
            ui.check_variant(elmt);
        });





 
function filter_toggle_field(elmt, f_id)
{
    var checked = $(elmt).prop('checked');
    if (checked)
    {
        analysis.analysis.fields.push(f_id);
    }
    else
    {
        analysis.analysis.fields.splice(analysis.analysis.fields.indexOf(f_id),1);
    }

    // load_variants_array();
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

function buildProgressBar(percentage, containerId) 
{

    var html = "<div class='progress'>\
                <div class='progress-bar progress-bar-striped active' role='progressbar' aria-valuenow='" + percentage + "' aria-valuemin='0' aria-valuemax='0' \
                    style='min-width: 2em; width: " + percentage + "%;'>\
                    " + percentage + "% \
                </div>\
            </div>";

    if (containerId !== null)
    {
        $("#" + containerId).html(html);
    }
    return html;
}