// options.js
console.log("Hello from Options Page2!");

const name = document.getElementById("name");
const saveBtn = document.getElementById("saveBtn");

saveBtn.addEventListener("click", () => {
     console.log(name.value);
});