document.getElementById('searchbtn').addEventListener('click', () => {
  document.querySelector('search')
});


document.getElementById('addwaitlist').addEventListener('click',  function (e) {
  e.preventDefault();
  document.getElementById('addwaitlist').style.color = "red";
})


function openNav() {
  document.getElementById('nav-links').style.minHeight = "300px";
  document.getElementById('nav-links').style.display = "block";
  document.getElementById('opennav').style.display = "none";
  document.getElementById('closebtn').style.display = "block";
}


function closeNav() {
  document.getElementById('nav-links').style.minHeight = "0px";
  document.getElementById('nav-links').style.display = "none";
  document.getElementById('opennav').style.display = "block";
  document.getElementById('closebtn').style.display = "none";

}

const menuItem = document.querySelector('.menu-item');
const dropdown = document.querySelector('.dropdown');

menuItem.addEventListener('mouseenter', () => {
  dropdown.style.display = 'block';
});

menuItem.addEventListener('mouseleave', () => {
  dropdown.style.display = 'none';
});



function openFilter() {
  document.getElementById('filters').style.opacity = "1";
}
