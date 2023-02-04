const scanner = new Html5QrcodeScanner('scan-reader', {
    qrbox: {
        width: 250,
        height: 250,
    },
    fps: 20,
});
scanner.render(success, error);

function success(result) {
    document.getElementById('result').innerHTML = `<h1 class="text-lg lg:text-2xl uppercase font-bold text-center">Success : ${result}</h1>`;
    document.getElementById('result').value = result;
    scanner.clear();
    // document.getElementById('scan-reader').remove();
    document.getElementById('qr-form').submit();
}

function error(error) {
    console.log(error);
}