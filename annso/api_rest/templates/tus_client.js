

// TUS Client for File upload

var annsoFileUpload = null;
var annsoFileInput = document.querySelector("#modal_import_file_tus_localinput");
var annsoFileAlertBox = document.querySelector("#tus_support_alert");
var annsoFileChunkInput = document.querySelector("#modal_new_file_tus_chunksize");
var annsoFileEndpointInput = document.querySelector("#modal_new_file_tus_endpoint");


if (!tus.isSupported) 
{
    annsoFileAlertBox.className = annsoFileAlertBox.className.replace("hidden", "");
}


annsoFileInput.addEventListener("change", function(e) 
{
    var file = e.target.files[0];
    console.log("selected file", file);
    var endpoint = annsoFileEndpointInput.value;
    var chunkSize = parseInt(annsoFileChunkInput.value, 10);


    if (isNaN(chunkSize)) 
    {
        chunkSize = Infinity;
    }
    var options = {
        endpoint: endpoint,
        resume: true,
        chunkSize: chunkSize,
        metadata: { filename: file.name },
        onError: function(error) 
        {
            annsoFileInput.value = "";
            buildPopup("Failed because: " + error, "alert", "tusFileProgress");
        },
        onProgress: function(bytesUploaded, bytesTotal) 
        {
            var percentage = (bytesUploaded / bytesTotal * 100).toFixed(2);
            console.log(bytesUploaded, bytesTotal, percentage + "%");
            buildProgressBar(percentage, "RUN", "modal_new_file_progress");
        },
        onSuccess: function() 
        {
            annsoFileInput.value = "";
            $("#modal_new_file_progress").html("");

        }
    }

    annsoFileUpload = new tus.Upload(file, options);
    annsoFileUpload.start();

    fileId = annsoFileUpload.url.substr(annsoFileUpload.url.lastIndexOf('/') + 1);
    add_new_activity_to_demo_browser("file", fileId);
    // Todo : while the upload of the file start/continue, display a form to edit file information (comments, tags, filename, ...)
})










