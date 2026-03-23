from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["frontend"])

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>FastAPI Demo</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 0 16px; }
    h1   { color: #2563eb; }
    h2   { margin-top: 2rem; }
    form { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1rem; }
    input { border: 1px solid #ccc; border-radius: 4px; padding: 6px 10px; }
    button { background: #2563eb; color: #fff; border: none; border-radius: 4px;
             padding: 6px 14px; cursor: pointer; }
    button:hover { background: #1d4ed8; }
    ul { list-style: none; padding: 0; }
    li { background: #f1f5f9; border-radius: 6px; padding: 10px 14px;
         margin: 6px 0; display: flex; justify-content: space-between; align-items: center; }
    .del { background: #ef4444; padding: 4px 10px; font-size: 0.85rem; }
    #status { color: green; min-height: 1.2em; margin-bottom: 0.5rem; }
  </style>
</head>
<body>
  <h1>FastAPI Demo</h1>
  <p id="status"></p>

  <h2>Items</h2>
  <form id="item-form">
    <input id="item-title"  placeholder="Title"       required />
    <input id="item-price"  placeholder="Price"  type="number" step="0.01" required />
    <input id="item-desc"   placeholder="Description (optional)" />
    <button type="submit">Add Item</button>
  </form>
  <ul id="item-list"></ul>

  <h2>Users</h2>
  <form id="user-form">
    <input id="user-name"  placeholder="Username" required />
    <input id="user-email" placeholder="Email"    type="email" required />
    <input id="user-pass"  placeholder="Password" type="password" required />
    <button type="submit">Add User</button>
  </form>
  <ul id="user-list"></ul>

<script>
const status = document.getElementById("status");

function setStatus(msg, ok = true) {
  status.style.color = ok ? "green" : "red";
  status.textContent = msg;
  setTimeout(() => { status.textContent = ""; }, 2500);
}

// --- Items ---
async function loadItems() {
  const res  = await fetch("/items/");
  const data = await res.json();
  const ul   = document.getElementById("item-list");
  ul.innerHTML = data.map(i =>
    `<li data-id="${i.id}">
       <span>${i.title} — $${i.price.toFixed(2)}
         ${i.description ? " · " + i.description : ""}
       </span>
       <button class="del" onclick="deleteItem(${i.id})">Delete</button>
     </li>`
  ).join("") || "<li>No items yet.</li>";
}

async function deleteItem(id) {
  await fetch("/items/" + id, { method: "DELETE" });
  setStatus("Item deleted");
  loadItems();
}

document.getElementById("item-form").addEventListener("submit", async e => {
  e.preventDefault();
  const body = {
    title:       document.getElementById("item-title").value,
    price:       parseFloat(document.getElementById("item-price").value),
    description: document.getElementById("item-desc").value || undefined,
  };
  const res = await fetch("/items/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (res.ok) {
    setStatus("Item added!");
    e.target.reset();
    loadItems();
  } else {
    setStatus("Error: " + (await res.text()), false);
  }
});

// --- Users ---
async function loadUsers() {
  const res  = await fetch("/users/");
  const data = await res.json();
  const ul   = document.getElementById("user-list");
  ul.innerHTML = data.map(u =>
    `<li data-id="${u.id}">
       <span>${u.username} (${u.email})</span>
       <button class="del" onclick="deleteUser(${u.id})">Delete</button>
     </li>`
  ).join("") || "<li>No users yet.</li>";
}

async function deleteUser(id) {
  await fetch("/users/" + id, { method: "DELETE" });
  setStatus("User deleted");
  loadUsers();
}

document.getElementById("user-form").addEventListener("submit", async e => {
  e.preventDefault();
  const body = {
    username: document.getElementById("user-name").value,
    email:    document.getElementById("user-email").value,
    password: document.getElementById("user-pass").value,
  };
  const res = await fetch("/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (res.ok) {
    setStatus("User added!");
    e.target.reset();
    loadUsers();
  } else {
    setStatus("Error: " + (await res.text()), false);
  }
});

loadItems();
loadUsers();
</script>
</body>
</html>"""


@router.get("/ui", response_class=HTMLResponse)
async def frontend():
    return HTML
