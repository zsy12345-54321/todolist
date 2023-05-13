// Quadrant 1: Important and Urgent
const list1 = document.getElementById("list1");
const input1 = document.getElementById("input1");

// Quadrant 2: Important but Not Urgent
const list2 = document.getElementById("list2");
const input2 = document.getElementById("input2");

// Quadrant 3: Not Important but Urgent
const list3 = document.getElementById("list3");
const input3 = document.getElementById("input3"); 

// Quadrant 4: Not Important and Not Urgent
const list4 = document.getElementById("list4");
const input4 = document.getElementById("input4");

// Function to create a new task
function createTask(task, list) {
  const li = document.createElement("li");
  li.innerHTML = `<span>${task}</span><button class="delete">-</button>`;
  list.appendChild(li);
  li.classList.add("fade-in");
  setTimeout(() => {
    li.classList.remove("fade-in");
  }, 500);
}

// Function to add a task to the list
function addTask(input, list) {
  const task = input.value.trim();
  if (task !== "") {
    createTask(task, list);
    input.value = "";
    document.getElementById("list").submit();
  }
}
// Function to delete a task from the list
function deleteTask(target) {
  const li = target.parentElement;
  li.classList.add("fade-out");
  setTimeout(() => {li.remove();}, 500);
}

// Function to edit a task in the list
function editTask(target) {
  const span = target.querySelector("span");
  const input = document.createElement("input");
  input.type = "text";
  input.value = span.innerText;
  target.replaceChild(input, span);
  input.addEventListener("blur", function(event) {
    span.innerText = input.value;
    target.replaceChild(span, input);
  });
}

// Function to save a task after editing
function saveTask(input) {
  const span = document.createElement("span");
  span.innerText = input.value;
  const li = input.parentElement;
  li.replaceChild(span, input);
  li.classList.add("fade-in");
  setTimeout(() => {
    li.classList.remove("fade-in");
  }, 500);
}

// Event listener to delete or edit a task on button click
document.addEventListener("click", function(event) {
  if (event.target.classList.contains("delete")) {
    deleteTask(event.target);
    showMessage("Task deleted.");}
});
document.addEventListener("dblclick", function(event) {
  if (event.target.tagName === "SPAN") {
    editTask(event.target.parentElement);
  }
});

// Event listener to add a task on enter key press
input1.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    addTask(input1, list1);
    showMessage("Task added.");
  }
});

input2.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    addTask(input2, list2);
    showMessage("Task added.");
  }
});

input3.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    addTask(input3, list3);
    showMessage("Task added.");
  }
});

input4.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    addTask(input4, list4);
    showMessage("Task added.");
  }
});

// Function to show a message to the user
function showMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  messageElement.innerText = message;
  document.body.appendChild(messageElement);
  messageElement.classList.add("fade-in");
  setTimeout(() => {
    messageElement.classList.remove("fade-in");
    messageElement.classList.add("fade-out");
  }, 2000);
  setTimeout(() => {
    messageElement.remove();
  }, 2500);
}
document.addEventListener('DOMContentLoaded', fetchTasks);
