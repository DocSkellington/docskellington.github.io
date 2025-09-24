const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

function setup() {
  if (prefersDarkScheme.matches) {
    document.body.classList.toggle("dark-theme");
  } else {
    document.body.classList.toggle("light-theme");
  }
}

function toggleDark() {
  document.body.classList.toggle("light-theme");
  document.body.classList.toggle("dark-theme");
}

function abstract(id) {
  if (id.style.display == "block") {
    id.style.display = "none";
  }
  else {
    id.style.display = "block";
  }
}
