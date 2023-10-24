document.addEventListener('DOMContentLoaded', () => {
  const topButton = document.querySelector('#scrolltop');

  topButton.addEventListener('click', (e) => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  })

  document.addEventListener('scroll', () => {
    if (window.scrollY >= 120) {
      topButton.classList.add("visible");
    } else {
      topButton.classList.remove("visible");
    }
  })
})
