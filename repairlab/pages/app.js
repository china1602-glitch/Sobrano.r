"use strict";

// GitHub Pages preview: this catalogue is a static JSON file, not a Python API.
const grid = document.querySelector("#service-grid");
const selected = document.querySelector("#selected-service");
let services = [];
let category = "Все";

function renderServices() {
  grid.replaceChildren();
  for (const service of services.filter((item) => category === "Все" || item.category === category)) {
    const article = document.createElement("article");
    article.className = "service";
    article.innerHTML = '<div class="service-illustration"><img width="240" height="160" alt=""></div><div class="service-body"><h3></h3><p></p><div class="service-bottom"><b></b><button type="button">→</button></div></div>';
    article.querySelector("img").src = `assets/${service.image}`;
    article.querySelector("h3").textContent = service.title;
    article.querySelector("p").textContent = service.description;
    article.querySelector("b").textContent = `от ${service.price.toLocaleString("ru-RU")} ₽`;
    const button = article.querySelector("button");
    button.setAttribute("aria-label", `Подробнее: ${service.title}`);
    button.addEventListener("click", () => {
      selected.textContent = `Вы выбрали: ${service.title}. Онлайн-заявки в этой демонстрации не принимаются.`;
      selected.focus({ preventScroll: true });
      document.querySelector("#booking").scrollIntoView({
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth",
      });
    });
    grid.append(article);
  }
}

for (const button of document.querySelectorAll(".filter")) {
  button.addEventListener("click", () => {
    category = button.dataset.filter;
    for (const item of document.querySelectorAll(".filter")) {
      item.classList.toggle("active", item === button);
      item.setAttribute("aria-pressed", String(item === button));
    }
    renderServices();
  });
}

async function loadServices() {
  try {
    const response = await fetch("catalog.json");
    if (!response.ok) throw new Error("Catalogue unavailable");
    services = await response.json();
    renderServices();
  } catch {
    grid.textContent = "Не удалось загрузить каталог. Обновите страницу или попробуйте позже.";
  }
}

loadServices();
