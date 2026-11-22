(() => {
    const API = {
        products: "/api/products",
        profile: "/api/profile",
        targets: "/api/profile/targets",
        meals: "/api/meal-entries",
    };

    const MEAL_CATEGORIES = [
        { id: "breakfast", label: "Śniadanie" },
        { id: "lunch", label: "Obiad" },
        { id: "dinner", label: "Kolacja" },
        { id: "snack", label: "Przekąska" },
    ];

    // ---------------- helpers ----------------
    const $ = (sel, root = document) => root.querySelector(sel);
    const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

    const todayIso = () => new Date().toISOString().slice(0, 10);

    const toast = (msg, type = "") => {
        const el = $("#toast");
        el.textContent = msg;
        el.className = `toast show ${type}`;
        setTimeout(() => (el.className = "toast"), 2500);
    };

    async function request(url, options = {}) {
        const response = await fetch(url, {
            headers: { "Content-Type": "application/json" },
            ...options,
        });
        if (response.status === 204) return null;
        const data = await response.json().catch(() => null);
        if (!response.ok) {
            const detail = (data && (data.detail || data.message)) || response.statusText;
            const message = Array.isArray(detail)
                ? detail.map((d) => d.msg || JSON.stringify(d)).join(", ")
                : detail;
            throw new Error(message);
        }
        return data;
    }

    const formToObject = (form) => {
        const data = {};
        new FormData(form).forEach((value, key) => {
            if (value === "" || value === null) return;
            const input = form.elements[key];
            if (input && input.type === "number") {
                data[key] = Number(value);
            } else {
                data[key] = value;
            }
        });
        return data;
    };

    // ---------------- tabs ----------------
    $$(".tab").forEach((tab) => {
        tab.addEventListener("click", () => {
            $$(".tab").forEach((t) => t.classList.remove("active"));
            $$(".tab-panel").forEach((p) => p.classList.remove("active"));
            tab.classList.add("active");
            $(`#tab-${tab.dataset.tab}`).classList.add("active");
            if (tab.dataset.tab === "dashboard") loadDashboard();
            if (tab.dataset.tab === "diary") loadDiary();
            if (tab.dataset.tab === "products") loadProducts();
        });
    });

    // ---------------- profile ----------------
    async function loadProfile() {
        try {
            const profile = await request(API.profile);
            const form = $("#profile-form");
            Object.entries(profile).forEach(([key, value]) => {
                if (form.elements[key]) form.elements[key].value = value;
            });
            await loadTargets();
        } catch {
            // no profile yet – ignore
        }
    }

    async function loadTargets() {
        const box = $("#profile-targets");
        try {
            const t = await request(API.targets);
            box.innerHTML = `
                <div class="target-box"><div class="label">BMR</div><div class="value">${t.bmr_kcal} kcal</div></div>
                <div class="target-box"><div class="label">TDEE</div><div class="value">${t.tdee_kcal} kcal</div></div>
                <div class="target-box"><div class="label">Cel dzienny</div><div class="value">${t.target_kcal} kcal</div></div>
                <div class="target-box"><div class="label">Białko</div><div class="value">${t.protein_g} g</div></div>
                <div class="target-box"><div class="label">Węglowodany</div><div class="value">${t.carbs_g} g</div></div>
                <div class="target-box"><div class="label">Tłuszcze</div><div class="value">${t.fat_g} g</div></div>`;
        } catch {
            box.innerHTML = `<p class="muted">Zapisz profil, aby obliczyć cele.</p>`;
        }
    }

    $("#profile-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = formToObject(event.target);
        try {
            await request(API.profile, { method: "PUT", body: JSON.stringify(payload) });
            toast("Profil zapisany", "success");
            await loadTargets();
        } catch (error) {
            toast(error.message, "error");
        }
    });

    // ---------------- products ----------------
    let productCache = [];

    async function loadProducts(search = "") {
        const url = search ? `${API.products}?search=${encodeURIComponent(search)}` : API.products;
        productCache = await request(url);
        renderProducts(productCache);
        renderProductSelect(productCache);
    }

    function renderProducts(items) {
        const tbody = $("#products-tbody");
        if (!items.length) {
            tbody.innerHTML = `<tr><td colspan="6" class="muted">Brak produktów.</td></tr>`;
            return;
        }
        tbody.innerHTML = items
            .map(
                (p) => `
                <tr>
                    <td>${escapeHtml(p.name)}</td>
                    <td>${p.kcal_per_100g}</td>
                    <td>${p.protein_per_100g}</td>
                    <td>${p.carbs_per_100g}</td>
                    <td>${p.fat_per_100g}</td>
                    <td style="text-align:right">
                        <button class="danger" data-delete-product="${p.id}">Usuń</button>
                    </td>
                </tr>`,
            )
            .join("");
    }

    function renderProductSelect(items) {
        const select = $("#meal-product-select");
        select.innerHTML = items
            .map((p) => `<option value="${p.id}">${escapeHtml(p.name)} (${p.kcal_per_100g} kcal/100g)</option>`)
            .join("");
    }

    $("#products-tbody").addEventListener("click", async (event) => {
        const button = event.target.closest("[data-delete-product]");
        if (!button) return;
        if (!confirm("Usunąć produkt?")) return;
        try {
            await request(`${API.products}/${button.dataset.deleteProduct}`, { method: "DELETE" });
            toast("Produkt usunięty", "success");
            await loadProducts($("#product-search").value.trim());
        } catch (error) {
            toast(error.message, "error");
        }
    });

    $("#product-search").addEventListener("input", (event) => {
        loadProducts(event.target.value.trim());
    });

    $("#product-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = formToObject(event.target);
        try {
            await request(API.products, { method: "POST", body: JSON.stringify(payload) });
            event.target.reset();
            toast("Produkt dodany", "success");
            await loadProducts();
        } catch (error) {
            toast(error.message, "error");
        }
    });

    // ---------------- diary ----------------
    $("#meal-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = formToObject(event.target);
        payload.product_id = Number(payload.product_id);
        try {
            await request(API.meals, { method: "POST", body: JSON.stringify(payload) });
            toast("Dodano wpis", "success");
            event.target.elements.grams.value = "";
            await loadDiary();
            await loadDashboard();
        } catch (error) {
            toast(error.message, "error");
        }
    });

    async function loadDiary() {
        const date = $("#diary-date").value || todayIso();
        $("#diary-date").value = date;
        const summary = await request(`${API.meals}?entry_date=${date}`);
        const container = $("#diary-content");
        if (!summary.entries.length) {
            container.innerHTML = `<p class="muted">Brak wpisów na ${date}.</p>`;
            return;
        }
        container.innerHTML = MEAL_CATEGORIES.map((cat) => {
            const items = summary.entries.filter((e) => e.category === cat.id);
            if (!items.length) return "";
            return `
                <div class="meal-group">
                    <h3>${cat.label}</h3>
                    <table class="data-table">
                        <thead><tr><th>Produkt</th><th>Gramy</th><th>Kcal</th><th>B</th><th>W</th><th>T</th><th></th></tr></thead>
                        <tbody>
                            ${items
                                .map(
                                    (e) => `
                                <tr>
                                    <td>${escapeHtml(e.product.name)}</td>
                                    <td>${e.grams} g</td>
                                    <td>${e.kcal}</td>
                                    <td>${e.protein_g}</td>
                                    <td>${e.carbs_g}</td>
                                    <td>${e.fat_g}</td>
                                    <td style="text-align:right">
                                        <button class="danger" data-delete-entry="${e.id}">Usuń</button>
                                    </td>
                                </tr>`,
                                )
                                .join("")}
                        </tbody>
                    </table>
                </div>`;
        }).join("");
    }

    $("#diary-content").addEventListener("click", async (event) => {
        const button = event.target.closest("[data-delete-entry]");
        if (!button) return;
        try {
            await request(`${API.meals}/${button.dataset.deleteEntry}`, { method: "DELETE" });
            toast("Wpis usunięty", "success");
            await loadDiary();
            await loadDashboard();
        } catch (error) {
            toast(error.message, "error");
        }
    });

    $("#diary-date").addEventListener("change", loadDiary);

    // ---------------- dashboard ----------------
    $("#dashboard-date").addEventListener("change", loadDashboard);

    async function loadDashboard() {
        const date = $("#dashboard-date").value || todayIso();
        $("#dashboard-date").value = date;
        const summary = await request(`${API.meals}?entry_date=${date}`);
        const container = $("#dashboard-content");
        const { totals, targets, remaining_kcal, over_limit } = summary;

        if (!targets) {
            container.innerHTML = `
                <div class="alert info">Ustaw profil, aby zobaczyć cele i bilans.</div>
                <p><strong>Spożyte:</strong> ${totals.kcal} kcal
                    (B ${totals.protein_g} g, W ${totals.carbs_g} g, T ${totals.fat_g} g)</p>`;
            return;
        }

        const alert = over_limit
            ? `<div class="alert danger">Przekroczono dzienny limit kalorii o ${Math.abs(remaining_kcal)} kcal!</div>`
            : remaining_kcal < targets.target_kcal * 0.1
            ? `<div class="alert warning">Zbliżasz się do dziennego limitu. Pozostało ${remaining_kcal} kcal.</div>`
            : `<div class="alert info">Pozostało ${remaining_kcal} kcal do celu.</div>`;

        container.innerHTML = `
            ${alert}
            ${progressRow("Kalorie", totals.kcal, targets.target_kcal, "kcal", over_limit ? "over" : "kcal")}
            ${progressRow("Białko", totals.protein_g, targets.protein_g, "g", "protein")}
            ${progressRow("Węglowodany", totals.carbs_g, targets.carbs_g, "g", "carbs")}
            ${progressRow("Tłuszcze", totals.fat_g, targets.fat_g, "g", "fat")}`;
    }

    function progressRow(label, current, target, unit, cls) {
        const percent = target > 0 ? Math.min(100, (current / target) * 100) : 0;
        return `
            <div class="progress-group">
                <div class="progress-label">
                    <span>${label}</span>
                    <span>${current} / ${target} ${unit}</span>
                </div>
                <div class="progress-track">
                    <div class="progress-bar ${cls}" style="width:${percent}%"></div>
                </div>
            </div>`;
    }

    function escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, (c) => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
        }[c]));
    }

    // ---------------- init ----------------
    const today = todayIso();
    $("#dashboard-date").value = today;
    $("#diary-date").value = today;
    $("#meal-form").elements.entry_date.value = today;

    loadProfile();
    loadProducts();
    loadDashboard();
})();
