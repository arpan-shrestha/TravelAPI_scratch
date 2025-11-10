document.addEventListener("DOMContentLoaded", () => {
  loadBlogs();
  setupAuthLinks();
});

async function loadBlogs() {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role"); // e.g. 'admin', 'editor', 'viewer'

  try {
    const res = await fetch("http://127.0.0.1:8000/blog/", {
      headers: token ? { Authorization: `Token ${token}` } : {},
    });

    if (!res.ok) throw new Error("Failed to fetch blogs");

    const blogs = await res.json();
    const container = document.getElementById("blog-container");
    container.innerHTML = "";

    blogs.forEach((b) => {
      const card = document.createElement("div");
      card.className = "blog-card";

      card.innerHTML = `
        <h3>${b.title}</h3>
        <p>${b.content.slice(0, 150)}...</p>
        <div class="actions"></div>
      `;

      const actions = card.querySelector(".actions");

      // Role-based buttons
      if (role === "admin" || role === "editor") {
        const editBtn = document.createElement("button");
        editBtn.className = "btn-edit";
        editBtn.textContent = "Edit";
        editBtn.onclick = () => editBlog(b.id);
        actions.appendChild(editBtn);
      }

      if (role === "admin") {
        const delBtn = document.createElement("button");
        delBtn.className = "btn-delete";
        delBtn.textContent = "Delete";
        delBtn.onclick = () => deleteBlog(b.id);
        actions.appendChild(delBtn);
      }

      container.appendChild(card);
    });

    // Show add button for admin only
    if (role === "admin") {
      document.getElementById("addBlogBtn").style.display = "block";
    }

  } catch (err) {
    console.error(err);
  }
}

function setupAuthLinks() {
  const token = localStorage.getItem("token");
  const loginLink = document.getElementById("loginLink");
  const logoutLink = document.getElementById("logoutLink");

  if (token) {
    loginLink.style.display = "none";
    logoutLink.style.display = "inline";
  }

  logoutLink.addEventListener("click", () => {
    localStorage.clear();
    window.location.reload();
  });
}

async function deleteBlog(id) {
  if (!confirm("Are you sure you want to delete this blog?")) return;

  const token = localStorage.getItem("token");
  try {
    const res = await fetch(`http://127.0.0.1:8000/blog/${id}/`, {
      method: "DELETE",
      headers: { Authorization: `Token ${token}` },
    });
    if (res.ok) {
      alert("Blog deleted!");
      loadBlogs();
    } else {
      alert("Failed to delete blog.");
    }
  } catch (err) {
    console.error(err);
  }
}

function editBlog(id) {
  alert(`Redirect to blog edit page for ID ${id}`);
  // Later: you can make a modal or redirect to a separate edit.html
}
