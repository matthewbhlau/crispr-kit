function loadImage(event) {
    var file = event.target.files[0];
    var imageType = /^image\//;

    if (!file || !imageType.test(file.type)) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function() {
        var img = new Image();
        img.onload = function() {
            var container = document.querySelector('.image-container');
            container.style.backgroundImage = 'url(' + this.src + ')';
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
}