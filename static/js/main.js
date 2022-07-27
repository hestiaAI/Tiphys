function addTree (name) {
    var li = document.createElement("li");
    li.setAttribute("id", name);
    li.classList.add("nav-item", "nav-link", "d-flex", "justify-content-between");

    var i = document.createElement("i");
    i.classList.add("fa", "fa-trash");
    i.title = "Remove tree";
    li.appendChild(document.createTextNode(name));
    li.appendChild(i);

    var ul = document.getElementById("treesList");
    ul.appendChild(li);
}

function removeTree(name) {
    document.getElementById(name).remove();
}


function showAlert(cat, text) {
    var infobox = document.getElementById('infobox')

    infobox.firstElementChild.classList.add("alert-" + cat)
    infobox.firstElementChild.innerHTML = text

    infobox.hidden = false;

    setTimeout(() => {
        infobox.firstElementChild.classList.remove("alert-" + cat)
      infobox.hidden = true;
    }, 5000); // 👈️ time in milliseconds
}

var dots = window.setInterval( function() {
    var wait = document.getElementById("wait");
    if ( wait.innerHTML.length >= 3 )
        wait.innerHTML = "";
    else
        wait.innerHTML += ".";
    }, 500);

// Function to download data to a file
function downloadFile(data, filename, type) {
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}