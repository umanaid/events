var modal = document.getElementById("myModal");
var btn = document.getElementById("openModalBtn");
var span = document.getElementsByClassName("close")[0];
var uploadForm = document.getElementById("uploadForm");
var uploadBtn = document.getElementById("uploadBtn");

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

uploadForm.onsubmit = function(event) {
  event.preventDefault(); // Prevent the default form submission

  var fileInput = document.getElementById('fileToUpload');
  var file = fileInput.files[0];

  if (file) {
    // Here you can handle the file upload using AJAX or other methods
    console.log('File selected:', file.name);
    // For demonstration purpose, you can just hide the modal after selecting a file
    modal.style.display = "none";
  } else {
    alert("Please select a file to upload.");
  }
}
