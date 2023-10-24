const downButton = document.querySelector('#scrolldown');

downButton.addEventListener('click', (e) => {
  let scrollContent = document.querySelector('#hof');
  scrollContent.scrollIntoView({ block: "start", inline: "center" })
})
