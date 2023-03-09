// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
function ShowHideDel() {
    var confirm = document.getElementById("conf");
    var deleteButton = document.getElementById("deleteButton");
    
    deleteButton.style.display = confirm.checked ? "block" : "none";
}
function ForceUpdate() {
    var force = document.getElementById("force");
    var updateButton = document.getElementById("updateButton");

    updateButton.className = force.checked ? "btn btn-danger" : "btn btn-dark";
}

var deleteButton = document.getElementById("deleteButton");
deleteButton.style.display = "none";

var editModal = document.getElementById('editModal')
editModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever')
    console.log(recipient)
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = editModal.querySelector('.modal-body #id_val')
    modalTitle.value = recipient
})

    var keyModal = document.getElementById('keyModal')
    keyModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget
        
        var apikey = button.getAttribute('data-bs-whatever')
        console.log(apikey)
        
        var modalBox = keyModal.querySelector('.modal-body #api_val')
        modalBox.value = apikey
    });