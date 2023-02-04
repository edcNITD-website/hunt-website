function searchPage(){
    const searchBar = document.getElementById('key');
    const searchTerm = searchBar.value.toString().toLowerCase();
    // console.log(searchTerm);
    const detailElements = document.getElementsByClassName("searchable");
    for (const detailElement of detailElements) {
        detailElement.parentElement.parentElement.style.display = "none"
    }
    for (const detailElement of detailElements) {
      let display = detailElement.innerText.toLowerCase().includes(searchTerm);
      if(display==true){
        detailElement.parentElement.parentElement.style.display = "grid"
      }
      
    }
  }