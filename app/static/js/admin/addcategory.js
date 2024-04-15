document.getElementById('File').onchange = function(e) {
  let reader = new FileReader();
  reader.readAsDataURL(e.target.files[0]);
  reader.onload = function() {
      let preview = document.getElementById('preview');
      let imagen = document.createElement('img');
      imagen.src = reader.result;
      imagen.className = 'imgC'; // Asignar la clase 'imgC' a la imagen para aplicar estilos CSS
      preview.innerHTML = ""; // Limpiar la imagen actual
      preview.appendChild(imagen); // Agregar la nueva imagen al contenedor preview

      let afterUpload = document.querySelector('.after-upload');
      afterUpload.style.display = "block";
  }
}

document.querySelector('.clear-btn').addEventListener('click', function() {
  let preview = document.getElementById('preview');
  preview.innerHTML = ""; // Limpiar la imagen dentro del contenedor preview

  let afterUpload = document.querySelector('.after-upload');
  afterUpload.style.display = "none"; // Ocultar el contenedor de la imagen después de cargarla
});



