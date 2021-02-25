// Salsabil's code from line 3 -46

function readURL(input) {
    if (input.files && input.files[0]) {
  
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
  
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
  
        $('.image-title').html(input.files[0].name);
      };
  
      reader.readAsDataURL(input.files[0]);
  
    } else {
      removeUpload();
    }
  }
  
  function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
  }
  $('.image-upload-wrap').bind('dragover', function () {
      $('.image-upload-wrap').addClass('image-dropping');
    });
    $('.image-upload-wrap').bind('dragleave', function () {
      $('.image-upload-wrap').removeClass('image-dropping');
  });

  function submitUpload() {
    const submitBtn = document.getElementById("submission");
    const customBtn= document.getElementById("custom-Submission-btn");
    customBtn.addEventListener("click", function(){
      submitBtn.click();
    });
  }

  function uploadMessage(file){
    var FileSize = file.files[0].size / 1024 / 1024; // in MiB
        if (FileSize > 1) {
            alert('File size exceeds 2 MB');
           // $(file).val(''); //for clearing with Jquery
        } else {

        }
    alert("File uploaded successfully.")
  }