$("#file-input").change(function() {
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
    $("#upload").prop('disabled', !validFile);
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