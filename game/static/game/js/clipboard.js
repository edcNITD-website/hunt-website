function copyToClipboard() {
    // Get the text field
    var copyText = document.getElementById("share-code");
  
  
     // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.innerText);
  
    // Alert the copied text
    let msgElement = document.getElementById('msg-element');
    if (msgElement) {
        msgElement.style.display = "flex";
    }
    msgElement.innerHTML = '<li class="success">    <div class="text">Copied to clipboard '+copyText.innerText+'</div><div class="my-auto grid place-items-center"><button class="close-msg-btn" onclick="closeMsg(this)"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#fff" class="w-6 h-6 my-auto"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></button></div></li>'
    setTimeout(closeAll, 4500);
  }