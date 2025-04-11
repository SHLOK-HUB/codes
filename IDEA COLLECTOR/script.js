// script.js
const form = document.getElementById("idea-form");
const titleInput = document.getElementById("idea-title");
const descInput = document.getElementById("idea-desc");
const tagsInput = document.getElementById("idea-tags");
const ideasList = document.getElementById("ideas-list");
const searchBar = document.getElementById("search-bar");
const themeToggle = document.getElementById("toggle-theme");
const exportBtn = document.getElementById("export-btn");

let ideas = JSON.parse(localStorage.getItem("ideas")) || [];

if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark");
}

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
});

searchBar.addEventListener("input", renderIdeas);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const newIdea = {
    title: titleInput.value,
    desc: descInput.value,
    tags: tagsInput.value.split(",").map(tag => tag.trim()).filter(Boolean),
  };
  ideas.push(newIdea);
  localStorage.setItem("ideas", JSON.stringify(ideas));
  titleInput.value = "";
  descInput.value = "";
  tagsInput.value = "";
  renderIdeas();
});

function deleteIdea(index) {
  ideas.splice(index, 1);
  localStorage.setItem("ideas", JSON.stringify(ideas));
  renderIdeas();
}

function renderIdeas() {
  const searchTerm = searchBar.value.toLowerCase();
  ideasList.innerHTML = "";
  ideas
    .filter(idea =>
      idea.title.toLowerCase().includes(searchTerm) ||
      idea.desc.toLowerCase().includes(searchTerm) ||
      (idea.tags && idea.tags.some(tag => tag.toLowerCase().includes(searchTerm)))
    )
    .forEach((idea, index) => {
      const card = document.createElement("div");
      card.className = "idea-card";
      card.innerHTML = `
        <h3>${idea.title}</h3>
        <p>${idea.desc}</p>
        ${idea.tags.length ? `<small>Tags: ${idea.tags.join(", ")}</small>` : ""}
        <button class="delete-btn" onclick="deleteIdea(${index})">X</button>
      `;
      ideasList.appendChild(card);
    });
}

exportBtn.addEventListener("click", () => {
  const fileData = JSON.stringify(ideas, null, 2);
  const blob = new Blob([fileData], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.download = "ideas.json";
  link.href = url;
  link.click();
});

renderIdeas();
