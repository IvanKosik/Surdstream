var selectedVideoFile = null;
var selectedValidFile = false;

$("#upload-custom-file").change(function() {
    selectedVideoFile = null;
    selectedValidFile = false;
    let fileInput = $(this);
    let selectedFiles = fileInput.prop('files');
    if (selectedFiles.length === 1) {
        selectedVideoFile = selectedFiles[0];
        if (selectedVideoFile.size < 5242880 && validFileType(selectedVideoFile)) { // 5 MB
            selectedValidFile = true;
        }
    }
    $("#upload-video").prop('disabled', !selectedValidFile);
});


var validFileTypes = [
    'video/webm',
    'video/ogg',
    'video/avi',
    'video/mp4'
]

function validFileType(file) {
    for (let i = 0; i < validFileTypes.length; i++) {
        if (file.type === validFileTypes[i]) {
            return true;
        }
    }
    return false;
}

$("#upload-video-form").submit(function(event) {
    event.preventDefault(); // avoid to execute the actual submit of the form.

    let uploadVideoForm = $(this);
    let formData = new FormData(this);

    $.ajax({
        method: "POST",
        url: uploadVideoForm.attr("action"),
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log("UPLOADED status: ", data.status_code, "   video_id: ", data.video_id);
//            TODO
        },
        dataType: 'json'
    });
});
