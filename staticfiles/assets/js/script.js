document.getElementById('searchbtn').addEventListener('click', ()=> {
    document.querySelector('search')
  });
  

  
  
  function openNav() {
    document.getElementById('nav-links').style.minHeight = "300px";
    document.getElementById('nav-links').style.opacity = "1";
    document.getElementById('opennav').style.opacity = "0";
    document.getElementById('closebtn').style.opacity = "1";
    
  }
  
  
  function closeNav() {
     document.getElementById('nav-links').style.minHeight = "0px";
     document.getElementById('nav-links').style.opacity = "0";
      document.getElementById('opennav').style.opacity = "1";
     document.getElementById('closebtn').style.opacity = "0";

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
