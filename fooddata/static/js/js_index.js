
function openform() {
    document.getElementById("myform").style.display = "block";
}

function closeform() {
    document.getElementById("myform").style.display = "none";
}


var slideIndex = 1;
showslide(slideIndex);


function currentslide(n) {
    showslide(slideIndex = n);
}


function plusslide(n) {
    showslide(slideIndex += n);
}


function showslide(n) {
    var slide = document.getElementsByClassName("slide");
    var dot = document.getElementsByClassName("dot");
    if (n > slide.length) { slideIndex = 1 };
    if (n < 1) { slideIndex = slide.length };
    for (i = 0; i < slide.length; i++) {
        slide[i].style.display = "none";
    }
    for (i = 0; i < dot.length; i++) {
        dot[i].className = dot[i].className.replace(" active", "");
    }
    slide[slideIndex - 1].style.display = "block";
    dot[slideIndex - 1].className += " active";
}



document.addEventListener("click", function (event) {

    if (event.target.matches(".cancel") || !event.target.closest(".formpop") && !event.target.closest(".popup") && !event.target.closest(".contact")) {
        closeform()
    }
}, false)