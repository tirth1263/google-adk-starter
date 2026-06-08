const header = document.querySelector(".site-header");

function updateHeaderShadow() {
  if (window.scrollY > 8) {
    header.style.boxShadow = "0 10px 30px rgba(32, 43, 61, 0.08)";
  } else {
    header.style.boxShadow = "none";
  }
}

updateHeaderShadow();
window.addEventListener("scroll", updateHeaderShadow, { passive: true });
