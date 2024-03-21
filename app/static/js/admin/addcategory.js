function applyDnDFile(el){
    const beforeUploadEl = el.querySelector(".before-upload");
    const afterUploadEl = el.querySelector(".after-upload");
    const inputUploadEl = el.querySelector("input");
    const imagePreview = el.querySelector(".after-upload img");
    const clearBtn = el.querySelector(".after-upload .clear-btn");


function showImagePreview(img){
    if(img){
        const blobUrl = URL.createObjectURL(img);
        imagePreview.src = blobUrl;
        afterUploadEl.style.display = "block";
        beforeUploadEl.style.display = "none";
    }


}

beforeUploadEl.addEventListener("click", (e) =>{
    e.preventDefault();
    inputUploadEl.click();
});

inputUploadEl.addEventListener("change", (e) =>{
    e.preventDefault();
    showImagePreview(e.target.files[0]);
});


clearBtn.addEventListener("click", (e) =>{
    afterUploadEl.style.display = "none";
    beforeUploadEl.style.display = "flex";
});

beforeUploadEl.addEventListener("dragover", (e) =>{
    e.preventDefault();
    el.classList.add("active");
});

beforeUploadEl.addEventListener("dragleave", (e) =>{
    e.preventDefault();
    el.classList.remove("active");
});

beforeUploadEl.addEventListener("drop", (e) =>{
    e.preventDefault();
    el.classList.remove("active");
    showImagePreview(e.dataTransfer.files[0])
});

}

applyDnDFile(document.querySelector(".file-dnd"));