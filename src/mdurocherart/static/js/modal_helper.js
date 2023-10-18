  function openNav(content, background, size) {

    background.style.display = "block";
    content.style.width = `${size}`;
  }

  function closeNav(content, background) {
    content.style.width = "0";
    background.style.display = "none";
  }
