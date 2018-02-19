$("#uploadCustomFile").change(function() {
    var fileInput = $(this);
    var selectedFiles = fileInput.prop('files');
    var validFile = true;
    if (selectedFiles.length === 1) {
        var selectedFile = selectedFiles[0];
        if (selectedFile.size > 5242880 || !validFileType(selectedFile)) { // 5 MB
            validFile = false;
        }
    } else {
        validFile = false;
    }
    $("#uploadVideo").prop('disabled', !validFile);
});


var validFileTypes = [
    'video/webm',
    'video/ogg',
    'video/avi',
    'video/mp4'
]

function validFileType(file) {
    for (var i = 0; i < validFileTypes.length; i++) {
        if (file.type === validFileTypes[i]) {
            return true;
        }
    }
    return false;
}

$("#uploadVideoForm").submit(function(event) {
    event.preventDefault(); // avoid to execute the actual submit of the form.

    var uploadVideoForm = $(this);
    console.log("serialized upload form: ", uploadVideoForm.serialize())
    $.post(uploadVideoForm.attr("action"), uploadVideoForm.serialize(), function(data) {
            console.log("after upload post");
//            TODO
        },
        'json'
    );
});
