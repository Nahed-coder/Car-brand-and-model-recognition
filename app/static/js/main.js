
function upload() {
    console.log('clicked on upload button');
    document.getElementById('process_btn').disabled = false;
    document.getElementById('inputFileToLoad').click();
}

function process() {
    console.log('clicked on fake process');
    p_div = document.getElementById('process_div');
    l_div = document.getElementById('loading_div');

    p_div.hidden = true;
    l_div.hidden = false;

    const image_name = 'static/uploads/' + document.getElementById('cache').name;
    upload_to_server().then(
        function (response) {
            if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                    response.status);
                setTimeout(() => {
                    p_div = document.getElementById('process_div');
                    l_div = document.getElementById('loading_div');
                    p_div.hidden = false;
                    l_div.hidden = true;
                    var headline = document.getElementById('headline');
                    headline.innerHTML = `
            <div id="alert_msg" class="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>Error</strong> Please make sure you load an image first
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>`
                }, 1000);
            }
            const formData = new FormData();
            formData.append('image_name', image_name)
            const options = {
                method: 'POST',
                body: formData
            }

            fetch('http://127.0.0.1:5000/process', options)
                .then(
                    function (response) {
                        if (response.status !== 200) {
                            console.log('Looks like there was a problem. Status Code: ' +
                                response.status);
                            return;
                        }
                        response.json().then(function (data) {
                            console.log(data);

                            showResults(data);


                        })
                    }
                )
                .catch(function (err) {
                    document.getElementById('processed_img_card').hidden = false;
                    console.log('Fetch Error :-S', err);
                });
        }
    )
        .catch(function (err) {
            document.getElementById('processed_img_card').hidden = false;
            console.log('Fetch Error :-S', err);
        });;
}


function showResults(data) {
    p_div = document.getElementById('process_div');
    l_div = document.getElementById('loading_div');
    p_div.hidden = false;
    l_div.hidden = true;
    img = document.getElementById('processed_img');

    console.log(data);
    description = document.getElementById('car_description');
    description.innerHTML = "Model :" + data.model + '<br>Brand: ' + data.brand;

    document.getElementById('processed_img_card').hidden = false;
    img.src = document.getElementById('original_img').src;

    var headline = document.getElementById('headline');
    headline.innerHTML = `
    <div id="alert_msg" class="alert alert-dark alert-dismissible fade show" role="alert">
    <strong>Congratuation</strong> Your image is successfuly processed
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>`

}

function upload_to_server() {
    console.log('uploading to server');
    const fileInput = document.querySelector('#inputFileToLoad');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    const options = {
        method: 'POST',
        body: formData
    }
    return fetch('http://127.0.0.1:5000/upload', options);
}


function loadimage() {

    var filesSelected = document.getElementById("inputFileToLoad").files;

    if (filesSelected.length > 0) {
        var fileToLoad = filesSelected[0];
        console.log('file_uploaded: ' + fileToLoad.name);
        if (fileToLoad.type.match("image.*")) {
            var fileReader = new FileReader();
            fileReader.onload = function (fileLoadedEvent) {
                var imageLoaded = document.getElementById("original_img");
                imageLoaded.src = fileLoadedEvent.target.result;
                document.getElementById('cache').name = fileToLoad.name.split(' ').join('_');
            };
            fileReader.readAsDataURL(fileToLoad);
        }
    }

}

