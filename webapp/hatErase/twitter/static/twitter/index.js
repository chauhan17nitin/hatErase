const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const links = document.querySelectorAll('.nav-links li');

window.onscroll = function() {myFunction()};

const navbar = document.querySelector('.nav-bar');
var sticky = navbar.offsetTop;


function myFunction() {
    if (window.pageYOffset >= sticky) {
      navbar.classList.add("sticky")
    } else {
      navbar.classList.remove("sticky");
    }
  };



hamburger.addEventListener('click', ()=>{
    navLinks.classList.toggle('open');
    links.forEach(link =>{
        link.classList.toggle("fade");
    });
});