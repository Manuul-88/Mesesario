const startBtn = document.getElementById("startBtn");
const finalBtn = document.getElementById("finalBtn");

const timeline = document.getElementById("timeline");
const gallery = document.getElementById("gallery");
const letter = document.getElementById("letter");
const surprise = document.getElementById("surprise");
const timeTogether = document.getElementById("timeTogether");

const galleryGrid = document.getElementById("galleryGrid");
const toggleEditBtn = document.getElementById("toggleEditBtn");
const editorPanel = document.getElementById("editorPanel");
const monthForm = document.getElementById("monthForm");
const monthId = document.getElementById("monthId");
const monthLabel = document.getElementById("monthLabel");
const isFeatured = document.getElementById("isFeatured");
const monthDescription1 = document.getElementById("monthDescription1");
const monthDescription2 = document.getElementById("monthDescription2");
const monthImage1 = document.getElementById("monthImage1");
const monthImage2 = document.getElementById("monthImage2");
const keepExistingImage1 = document.getElementById("keepExistingImage1");
const keepExistingImage2 = document.getElementById("keepExistingImage2");
const cancelEditBtn = document.getElementById("cancelEditBtn");
const formTitle = document.getElementById("formTitle");

const startDate = new Date("2025-04-12T14:10:00");

// Local:
// const API_URL = "http://127.0.0.1:8000";
const API_URL =
  window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://mesesario-backend.onrender.com";

let counterStarted = false;
let counterInterval = null;
let editMode = false;
let months = [];

startBtn?.addEventListener("click", () => {
  timeline?.classList.remove("hidden");
  gallery?.classList.remove("hidden");
  letter?.classList.remove("hidden");

  timeline?.scrollIntoView({ behavior: "smooth" });
});

finalBtn?.addEventListener("click", () => {
  surprise?.classList.remove("hidden");
  surprise?.scrollIntoView({ behavior: "smooth" });

  if (!counterStarted) {
    startCounter();
    counterStarted = true;
  }
});

toggleEditBtn?.addEventListener("click", () => {
  editMode = !editMode;

  editorPanel?.classList.toggle("hidden", !editMode);
  toggleEditBtn.textContent = editMode ? "Salir de edición" : "Modo editar";

  if (!editMode) {
    resetForm();
  }

  renderMonths();
});

cancelEditBtn?.addEventListener("click", () => {
  resetForm();
  editorPanel?.classList.add("hidden");
});

monthForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

const formData = new FormData();
formData.append("month_label", monthLabel.value.trim());
formData.append("description_1", monthDescription1.value.trim());
formData.append("description_2", monthDescription2.value.trim());
formData.append("is_featured", isFeatured.checked ? "true" : "false");
formData.append(
  "keep_existing_image_1",
  keepExistingImage1.checked ? "true" : "false"
);
formData.append(
  "keep_existing_image_2",
  keepExistingImage2.checked ? "true" : "false"
);

if (monthImage1.files && monthImage1.files[0]) {
  formData.append("image_1", monthImage1.files[0]);
}

if (monthImage2.files && monthImage2.files[0]) {
  formData.append("image_2", monthImage2.files[0]);
}

  if (monthImage1.files && monthImage1.files[0]) {
  formData.append("image_1", monthImage1.files[0]);
}

if (monthImage2.files && monthImage2.files[0]) {
  formData.append("image_2", monthImage2.files[0]);
}

  const id = monthId.value.trim();

  try {
    let res;

    if (id) {
      res = await fetch(`${API_URL}/api/months/${id}`, {
        method: "PUT",
        body: formData,
      });
    } else {
      res = await fetch(`${API_URL}/api/months`, {
        method: "POST",
        body: formData,
      });
    }

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Error al guardar: ${errorText}`);
    }

    resetForm();
    editorPanel?.classList.add("hidden");
    await loadMonths();
  } catch (error) {
    console.error(error);
    alert("No se pudo guardar el mes.");
  }
});

function startCounter() {
  updateTime();
  counterInterval = setInterval(updateTime, 1000);
}

function updateTime() {
  const now = new Date();
  const diff = now - startDate;

  if (diff < 0) {
    if (timeTogether) {
      timeTogether.innerText = "Nuestro tiempo juntos apenas comienza ❤️";
    }
    return;
  }

  const totalSeconds = Math.floor(diff / 1000);
  const totalMinutes = Math.floor(totalSeconds / 60);
  const totalHours = Math.floor(totalMinutes / 60);
  const totalDays = Math.floor(totalHours / 24);

  const years = Math.floor(totalDays / 365);
  const remainingDaysAfterYears = totalDays % 365;

  const monthsCount = Math.floor(remainingDaysAfterYears / 30);
  const days = remainingDaysAfterYears % 30;

  const hours = totalHours % 24;
  const minutes = totalMinutes % 60;
  const seconds = totalSeconds % 60;

  if (timeTogether) {
    timeTogether.innerText =
      `Llevamos ${years} años, ${monthsCount} meses, ${days} días, ` +
      `${hours} horas, ${minutes} minutos y ${seconds} segundos juntos ❤️`;
  }
}

async function loadMonths() {
  if (!galleryGrid) return;

  try {
    const res = await fetch(`${API_URL}/api/months`);

    if (!res.ok) {
      throw new Error("No se pudieron cargar los meses");
    }

    months = await res.json();
    renderMonths();
  } catch (error) {
    console.error(error);
    galleryGrid.innerHTML = `
      <div class="photo-card future">
        <div class="future-content">
          <h3>Error al cargar</h3>
          <p>No se pudieron obtener los meses desde el servidor.</p>
        </div>
      </div>
    `;
  }
}

function renderMonths() {
  if (!galleryGrid) return;

  galleryGrid.innerHTML = "";

  months.forEach((month) => {
    const card = document.createElement("div");
    card.className = `photo-card ${month.is_featured ? "featured" : ""}`;

    const imageHtml = month.image_path
      ? `<img src="${normalizeImageUrl(month.image_path)}" alt="${escapeHtml(month.month_label)}" />`
      : `<div class="future" style="height:240px;">Sin imagen</div>`;


    const leftImage = month.image_path_1
  ? `<img src="${normalizeImageUrl(month.image_path_1)}" alt="Tu recuerdo" />`
  : `<div class="memory-placeholder">Sin imagen</div>`;

    const rightImage = month.image_path_2
      ? `<img src="${normalizeImageUrl(month.image_path_2)}" alt="Su recuerdo" />`
      : `<div class="memory-placeholder">Sin imagen</div>`;

    card.innerHTML = `
      <div class="month-header">
        <h3>${escapeHtml(month.month_label)}</h3>
        <p>Dos recuerdos, un mismo mes</p>
      </div>

      <div class="memory-pair">
        <div class="memory-box side-one">
          <div class="memory-badge">Manol</div>
          ${leftImage}
          <p>${escapeHtml(month.description_1 || "")}</p>
        </div>

        <div class="memory-center">❤️</div>

        <div class="memory-box side-two">
          <div class="memory-badge">Jess</div>
          ${rightImage}
          <p>${escapeHtml(month.description_2 || "")}</p>
        </div>
      </div>

      ${
        editMode
          ? `
          <div class="card-actions">
            <button type="button" onclick="editMonth(${month.id})">Editar</button>
            <button type="button" onclick="deleteMonth(${month.id})">Eliminar</button>
          </div>
          `
          : ""
      }
    `;  

    galleryGrid.appendChild(card);
  });

  renderFutureCard();
}

function renderFutureCard() {
  if (!galleryGrid) return;

  const futureCard = document.createElement("div");
  futureCard.className = "photo-card future";

  futureCard.innerHTML = `
    <div class="future-content">
      <h3>Por agregar...</h3>
      <p>
        <br />
        Aquí seguirán apareciendo nuestros próximos recuerdos destacados de cada mes
      </p>
      ${
        editMode
          ? `<button type="button" id="addMonthBtn">Agregar mes</button>`
          : ""
      }
    </div>
  `;

  galleryGrid.appendChild(futureCard);

  if (editMode) {
    const addMonthBtn = document.getElementById("addMonthBtn");
    addMonthBtn?.addEventListener("click", () => {
      resetForm();
      formTitle.textContent = "Agregar mes";
      editorPanel?.classList.remove("hidden");
      editorPanel?.scrollIntoView({ behavior: "smooth" });
    });
  }
}

function resetForm() {
  monthForm?.reset();

  if (monthId) monthId.value = "";
  if (keepExistingImage1) keepExistingImage1.checked = true;
  if (keepExistingImage2) keepExistingImage2.checked = true;
  if (formTitle) formTitle.textContent = "Agregar mes";
}

window.editMonth = function (id) {
  const month = months.find((m) => m.id === Number(id));
  if (!month) return;

  monthId.value = month.id;
  monthLabel.value = month.month_label;
  isFeatured.checked = month.is_featured;
  monthDescription1.value = month.description_1 || "";
  monthDescription2.value = month.description_2 || "";
  keepExistingImage1.checked = true;
  keepExistingImage2.checked = true;

  formTitle.textContent = "Editar mes";
  editorPanel?.classList.remove("hidden");
  editorPanel?.scrollIntoView({ behavior: "smooth" });
};

window.deleteMonth = async function (id) {
  const ok = confirm("¿Seguro que quieres eliminar este mes?");
  if (!ok) return;

  try {
    const res = await fetch(`${API_URL}/api/months/${id}`, {
      method: "DELETE",
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Error al eliminar: ${errorText}`);
    }

    await loadMonths();
  } catch (error) {
    console.error(error);
    alert("No se pudo eliminar el mes.");
  }
};

function normalizeImageUrl(path) {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_URL}${path}`;
}

function escapeHtml(text) {
  if (text === null || text === undefined) return "";
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

loadMonths();