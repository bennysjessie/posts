const cookieContainer = document.querySelector(".pop-container");
const cookieButton = document.querySelector(".pop-btn");

cookieButton.addEventListener("click",() => {cookieContainer.classList.remove("active");
localStorage.setItem("cookieBannerDisplayed",true);
});

 setTimeout( () => {
  if (!localStorage.getItem("cookieBannerDisplayed"))
    cookieContainer.classList.add("active");



},3000);