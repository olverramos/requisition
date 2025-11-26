//

function downloadFile(fileName, data, fileFormat) {
    const linkSource = 'data:' + fileFormat + ';base64,' + data;
    const downloadLink = document.createElement("a");
    downloadLink.href = linkSource;
    downloadLink.download = fileName;
    downloadLink.click();
}

function dummyFunction() {
    alert("Dummy function called");
}