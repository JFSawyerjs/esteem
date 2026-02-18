// /* Stato globale degli asset / weights */
// let weightsState = [];


// /* ==========================================================
//    VALIDAZIONE FORM CREAZIONE CONFIG
//    ========================================================== */

// document.addEventListener("DOMContentLoaded", () => {
//     const form = document.querySelector("form");

//     form.addEventListener("submit", (event) => {
//         if (!validateForm()) {
//             event.preventDefault();
//             alert("⚠️ Prima di salvare, completa i campi obbligatori evidenziati.");
//         }
//     });
// });

// document.querySelectorAll("#sec-general input").forEach(input => {
//     input.addEventListener("input", validateGeneral);
// });


// /* ------------------------------------------
//    TOOLS
// -------------------------------------------*/
// function highlightSection(sectionIndex, valid) {
//     const sections = document.querySelectorAll(".section");
//     const sec = sections[sectionIndex];
//     if (!sec) return;

//     sec.style.border = valid ? "2px solid #34c759" : "2px solid #ff9f0a";
// }

// function isNumber(x) {
//     return !isNaN(parseFloat(x)) && isFinite(x);
// }

// /* ==========================================================
//    VALIDAZIONE PER SEZIONE
//    ========================================================== */

// /* ---- 1) GENERAL ---- */
// function validateGeneral() {
//     let ok = true;

//     // Section DOM
//     const section = document.querySelector("#sec-general");

//     // Fields
//     const activeProfile = document.querySelector("#activeProfile");
//     const separator = document.querySelector("#separatorWidth");
//     const migration = document.querySelector("#migrationFactor");
//     const teamSizes = document.querySelector("#teamSizes");

//     // Reset error styles
//     [activeProfile, separator, migration, teamSizes].forEach(el => {
//         el.classList.remove("input-error");
//     });

//     // ---- Validazione Nome Profilo ----
//     if (!activeProfile.value.trim()) {
//         ok = false;
//         activeProfile.classList.add("input-error");
//     }

//     // ---- Separator Width ----
//     if (!isNumber(separator.value) || separator.value <= 0) {
//         ok = false;
//         separator.classList.add("input-error");
//     }

//     // ---- Migration Factor ----
//     if (!isNumber(migration.value) || migration.value < 0) {
//         ok = false;
//         migration.classList.add("input-error");
//     }

//     // ---- Team Sizes ----
//     const rawTeams = teamSizes.value.trim();
//     const teamList = rawTeams
//         .split(",")
//         .map(v => v.trim())
//         .filter(v => v !== "");

//     if (teamList.length === 0 || !teamList.every(isNumber)) {
//         ok = false;
//         teamSizes.classList.add("input-error");
//     }

//     // ---- Section highlight (enterprise style) ----
//     if (ok) {
//         section.classList.remove("invalid");
//         section.classList.add("valid");
//     } else {
//         section.classList.remove("valid");
//         section.classList.add("invalid");
//     }

//     return ok;
// }


// /* ---- 2) APPS ---- */
// function validateApps() {
//     const section = document.querySelector("#sec-apps");
//     let ok = true;

//     const rows = document.querySelectorAll("#appsTable tbody tr");
//     if (rows.length === 0) ok = false;

//     rows.forEach(tr => {
//         const name = tr.querySelector(".app-name").value.trim();
//         const path = tr.querySelector(".app-path").value.trim();

//         if (!name || !path) ok = false;
//     });

//     section.classList.toggle("valid", ok);
//     section.classList.toggle("invalid", !ok);

//     return ok;
// }


// /* ---- 3) DEFAULT INCLUDES ---- */
// function validateIncludes() {
//     const section = document.querySelector("#sec-includes");
//     const rows = document.querySelectorAll("#includesTable tbody tr");

//     const ok = rows.length > 0;

//     if (ok) {
//         section.classList.remove("invalid");
//         section.classList.add("valid");
//     } else {
//         section.classList.remove("valid");
//         section.classList.add("invalid");
//     }

//     return ok;
// }


// /* ---- 4) WEIGHTS ---- */
// function validateWeights() {
//     let ok = true;

//     const section = document.querySelector("#sec-weights");

//     if (!weightsState.length) {
//         ok = false;
//     } else {
//         weightsState.forEach(w => {
//             if (!w.name || !w.label || !["glob","text"].includes(w.mode) || !isNumber(w.value) || w.value <= 0) {
//                 ok = false;
//             }
//         });
//     }

//     if (ok) {
//         section.classList.remove("invalid");
//         section.classList.add("valid");
//     } else {
//         section.classList.remove("valid");
//         section.classList.add("invalid");
//     }

//     return ok;
// }


// /* ---- 5) COMPLEXITY (OPZIONALE) ---- */
// function validateComplexity() {
//     let ok = true;

//     const num = document.querySelector("#complexNum").value;
//     const den = document.querySelector("#complexDen").value;

//     // Se entrambi vuoti → sezione OK
//     if (!num && !den) {
//         highlightSection(4, true);
//         return true;
//     }

//     // se uno solo → errore
//     if (!num || !den) ok = false;

//     // soglie
//     const rows = document.querySelectorAll("#thresholdsTable tbody tr");
//     rows.forEach(tr => {
//         const lbl = tr.querySelector(".th-label").value.trim();
//         const max = tr.querySelector(".th-max").value;

//         if (!lbl) ok = false;
//         if (!isNumber(max)) ok = false;
//     });

//     highlightSection(4, ok);
//     return ok;
// }

// /* ==========================================================
//    VALIDAZIONE COMPLETA
//    ========================================================== */
// function validateForm() {
//     const results = [
//         validateGeneral(),
//         validateApps(),
//         validateIncludes(),
//         validateWeights(),
//         validateComplexity(),
//     ];

//     return results.every(v => v === true);
// }

// /* ==========================================================
//    FUNZIONI ESISTENTI (APP, WEIGHTS, COMPLEXITY)
//    ========================================================== */

// function addAppRow(name = "", path = "") {
//     const tbody = document.querySelector("#appsTable tbody");
//     const tr = document.createElement("tr");

//     tr.innerHTML = `
//         <td><input type="text" class="app-name" value="${name}"></td>
//         <td><input type="text" class="app-path" value="${path}"></td>
//         <td><button type="button" class="btn-small" onclick="this.closest('tr').remove()">X</button></td>
//     `;
//     tbody.appendChild(tr);
// }

// function addAppFromForm() {
//     const nameEl = document.querySelector("#app_name");
//     const pathEl = document.querySelector("#app_path");

//     const name = nameEl.value.trim();
//     const path = pathEl.value.trim();

//     // reset error
//     nameEl.classList.remove("input-error");
//     pathEl.classList.remove("input-error");

//     let valid = true;
//     if (!name) { valid = false; nameEl.classList.add("input-error"); }
//     if (!path) { valid = false; pathEl.classList.add("input-error"); }

//     if (!valid) return;

//     // Aggiungi riga tabella
//     const tbody = document.querySelector("#appsTable tbody");
//     const tr = document.createElement("tr");

//     tr.innerHTML = `
//         <td><input type="text" class="app-name" value="${name}"></td>
//         <td><input type="text" class="app-path" value="${path}"></td>
//         <td><button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateApps();">X</button></td>
//     `;

//     tbody.appendChild(tr);

//     // Pulizia form
//     nameEl.value = "";
//     pathEl.value = "";

//     validateApps();
// }

// function addInclude() {
//     const input = document.querySelector("#includeInput");
//     const value = input.value.trim();
//     const tbody = document.querySelector("#includesTable tbody");

//     if (!value) {
//         input.classList.add("input-error");
//         return;
//     }

//     input.classList.remove("input-error");

//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//         <td>${value}</td>
//         <td>
//             <button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateIncludes();">X</button>
//         </td>
//     `;

//     tbody.appendChild(tr);
//     input.value = "";
//     validateIncludes();
// }




// /* ---- Weights ---- */
// let weightCounter = 0;

// function addWeightCard() {
//     const nameEl     = document.getElementById("w_name");
//     const labelEl    = document.getElementById("w_label");
//     const modeEl     = document.getElementById("w_mode");
//     const valueEl    = document.getElementById("w_value");
//     const patternEl  = document.getElementById("w_pattern");
//     const enabledEl  = document.getElementById("w_enabled");
//     const includeEl  = document.getElementById("w_include");
//     const perEl      = document.getElementById("w_per");
//     const oneIfAnyEl = document.getElementById("w_oneIfAny");

//     // reset grafica errori
//     [nameEl, labelEl, modeEl, valueEl, patternEl, includeEl, perEl].forEach(el => {
//         if (el) el.classList.remove("input-error");
//     });

//     let ok = true;

//     const name     = nameEl.value.trim();
//     const label    = labelEl.value.trim();
//     const mode     = modeEl.value;
//     const value    = valueEl.value;
//     const pattern  = patternEl.value.trim();
//     const enabled  = enabledEl.checked;
//     const per      = perEl.value ? parseInt(perEl.value, 10) : 1;
//     const oneIfAny = oneIfAnyEl.checked;

//     // include: righe -> array
//     const includeLines = includeEl.value
//         .split("\n")
//         .map(x => x.trim())
//         .filter(x => x.length > 0);

//     // VALIDAZIONE BASE
//     if (!name) { nameEl.classList.add("input-error"); ok = false; }
//     if (!label) { labelEl.classList.add("input-error"); ok = false; }
//     if (!["glob","text"].includes(mode)) { modeEl.classList.add("input-error"); ok = false; }
//     if (!isNumber(value) || value <= 0) { valueEl.classList.add("input-error"); ok = false; }
//     if (!pattern) { patternEl.classList.add("input-error"); ok = false; }
//     if (!per || per <= 0) { perEl.classList.add("input-error"); ok = false; }

//     if (!ok) return;

//     // COSTRUZIONE OGGETTO COMPLETO
//     let asset = {
//         enabled,     // boolean
//         name,
//         label,
//         mode,
//         value: parseFloat(value),
//         pattern,
//         include: includeLines,
//         per,
//         oneIfAny
//     };

//     // salva in stato
//     weightsState.push(asset);

//     // aggiorna tabella
//     renderWeightsTable();

//     // svuota form
//     nameEl.value = "";
//     labelEl.value = "";
//     valueEl.value = "";
//     patternEl.value = "";
//     includeEl.value = "";
//     perEl.value = "1";
//     enabledEl.checked = true;
//     oneIfAnyEl.checked = false;

//     // aggiorna complexity selectors
//     refreshComplexitySelectors();

//     validateWeights();
// }

// function renderWeightsTable() {
//     const tbody = document.querySelector("#weightsTable tbody");
//     tbody.innerHTML = "";

//     weightsState.forEach((w, index) => {

//         const tr = document.createElement("tr");

//         tr.innerHTML = `
//             <td>${w.enabled ? "✔️" : "—"}</td>
//             <td>${w.name || ""}</td>
//             <td>${w.label || ""}</td>
//             <td>${w.mode || ""}</td>
//             <td>${w.value ?? ""}</td>
//             <td>${w.pattern || ""}</td>
//             <td>${(w.include && w.include.length) ? w.include.join(", ") : "—"}</td>
//             <td>${w.per ?? 1}</td>
//             <td>${w.oneIfAny ? "✔️" : "—"}</td>
//             <td>
//                 <button type="button" class="btn-small" onclick="removeWeight(${index})">
//                     Rimuovi
//                 </button>
//             </td>
//         `;

//         tbody.appendChild(tr);
//     });
// }





// /* Rimuove un asset */
// function removeWeight(index) {
//     weightsState.splice(index, 1);
//     renderWeightsTable();
//     refreshComplexitySelectors();
//     validateWeights();
// }



// /* Aggiorna select complexity */
// function refreshComplexitySelectors() {
//     const num = document.getElementById("complexNum");
//     const den = document.getElementById("complexDen");

//     if (!num || !den) return;

//     num.innerHTML = "<option value=''>--</option>";
//     den.innerHTML = "<option value=''>--</option>";

//     weightsState.forEach(w => {
//         num.innerHTML += `<option value="${w.name}">${w.name}</option>`;
//         den.innerHTML += `<option value="${w.name}">${w.name}</option>`;
//     });
// }


// /* ---- Thresholds ---- */
// function addThresholdRow() {
//     const tbody = document.querySelector("#thresholdsTable tbody");

//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//         <td><input type="text" class="th-label"></td>
//         <td>
//           <select class="th-op">
//             <option value="<"><</option>
//             <option value=">=">>=</option>
//           </select>
//         </td>
//         <td><input type="number" step="0.1" class="th-max"></td>
//         <td><button type="button" class="btn-small" onclick="this.closest('tr').remove()">X</button></td>
//     `;
//     tbody.appendChild(tr);
// }


// /* ==============================================================  
//    STATO GLOBALE  
// ============================================================== */
// let weightsState = [];


// /* ==============================================================  
//    DOM READY  
// ============================================================== */
// document.addEventListener("DOMContentLoaded", () => {

//     const form = document.querySelector("form");

//     form.addEventListener("submit", (event) => {
//         if (!validateForm()) {
//             event.preventDefault();
//             alert("⚠️ Prima di salvare, completa i campi obbligatori evidenziati.");
//         }
//     });

//     // Attiva validazione real-time per general
//     document.querySelectorAll("#sec-general input").forEach(input => {
//         input.addEventListener("input", () => {
//             validateGeneral();
//             updateSaveButton();
//         });
//     });

//     // Aggiorna pulsante al load
//     updateSaveButton();
// });


// /* ==============================================================  
//    UTILS  
// ============================================================== */
// function highlightSection(sectionIndex, valid) {
//     const sections = document.querySelectorAll(".section");
//     const sec = sections[sectionIndex];
//     if (!sec) return;
//     sec.style.border = valid ? "2px solid #34c759" : "2px solid #ff9f0a";
// }

// function isNumber(x) {
//     return !isNaN(parseFloat(x)) && isFinite(x);
// }

// function updateSaveButton() {
//     const btn = document.getElementById("saveBtn");
//     if (!btn) return;

//     btn.disabled = !validateForm();
// }


// /* ==============================================================  
//    VALIDAZIONI SEZIONALI  
// ============================================================== */

// /* ---- 1) GENERAL ---- */
// function validateGeneral() {
//     let ok = true;
//     const section = document.querySelector("#sec-general");

//     const activeProfile = document.querySelector("#activeProfile");
//     const separator = document.querySelector("#separatorWidth");
//     const migration = document.querySelector("#migrationFactor");
//     const teamSizes = document.querySelector("#teamSizes");

//     [activeProfile, separator, migration, teamSizes].forEach(el => {
//         el.classList.remove("input-error");
//     });

//     if (!activeProfile.value.trim()) {
//         ok = false; activeProfile.classList.add("input-error");
//     }

//     if (!isNumber(separator.value) || separator.value <= 0) {
//         ok = false; separator.classList.add("input-error");
//     }

//     if (!isNumber(migration.value) || migration.value < 0) {
//         ok = false; migration.classList.add("input-error");
//     }

//     const rawTeams = teamSizes.value.trim();
//     const teamList = rawTeams.split(",").map(v => v.trim()).filter(v => v !== "");
//     if (!teamList.length || !teamList.every(isNumber)) {
//         ok = false; teamSizes.classList.add("input-error");
//     }

//     section.classList.toggle("valid", ok);
//     section.classList.toggle("invalid", !ok);

//     return ok;
// }


// /* ---- 2) APPS ---- */
// function validateApps() {
//     const section = document.querySelector("#sec-apps");
//     let ok = true;

//     const rows = document.querySelectorAll("#appsTable tbody tr");
//     if (rows.length === 0) ok = false;

//     rows.forEach(tr => {
//         const name = tr.querySelector(".app-name").value.trim();
//         const path = tr.querySelector(".app-path").value.trim();
//         if (!name || !path) ok = false;
//     });

//     section.classList.toggle("valid", ok);
//     section.classList.toggle("invalid", !ok);

//     return ok;
// }


// /* ---- 3) INCLUDES ---- */
// function validateIncludes() {
//     const section = document.querySelector("#sec-includes");
//     const rows = document.querySelectorAll("#includesTable tbody tr");

//     const ok = rows.length > 0;

//     section.classList.toggle("valid", ok);
//     section.classList.toggle("invalid", !ok);

//     return ok;
// }


// /* ---- 4) WEIGHTS ---- */
// function validateWeights() {
//     const section = document.querySelector("#sec-weights");
//     let ok = true;

//     if (!weightsState.length) ok = false;
//     else {
//         weightsState.forEach(w => {
//             if (!w.name || !w.label || !["glob","text"].includes(w.mode) || !isNumber(w.value) || w.value <= 0) {
//                 ok = false;
//             }
//         });
//     }

//     section.classList.toggle("valid", ok);
//     section.classList.toggle("invalid", !ok);

//     return ok;
// }


// /* ---- 5) COMPLEXITY ---- */
// function validateComplexity() {
//     let ok = true;

//     const num = document.querySelector("#complexNum").value;
//     const den = document.querySelector("#complexDen").value;

//     if (!num && !den) return true;
//     if (!num || !den) ok = false;

//     const rows = document.querySelectorAll("#thresholdsTable tbody tr");
//     rows.forEach(tr => {
//         const lbl = tr.querySelector(".th-label").value.trim();
//         const max = tr.querySelector(".th-max").value;
//         if (!lbl || !isNumber(max)) ok = false;
//     });

//     return ok;
// }


// /* ==============================================================  
//    VALIDAZIONE FINALE  
// ============================================================== */
// function validateForm() {
//     const result = [
//         validateGeneral(),
//         validateApps(),
//         validateIncludes(),
//         validateWeights(),
//         validateComplexity()
//     ].every(v => v === true);

//     return result;
// }


// /* ==============================================================  
//    APPS  
// ============================================================== */

// function addAppRow(name = "", path = "") {
//     const tbody = document.querySelector("#appsTable tbody");
//     const tr = document.createElement("tr");

//     tr.innerHTML = `
//         <td><input type="text" class="app-name" value="${name}"></td>
//         <td><input type="text" class="app-path" value="${path}"></td>
//         <td><button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateApps(); updateSaveButton();">X</button></td>
//     `;
//     tbody.appendChild(tr);

//     validateApps();
//     updateSaveButton();
// }

// function addAppFromForm() {
//     const nameEl = document.querySelector("#app_name");
//     const pathEl = document.querySelector("#app_path");

//     const name = nameEl.value.trim();
//     const path = pathEl.value.trim();

//     nameEl.classList.remove("input-error");
//     pathEl.classList.remove("input-error");

//     if (!name) { nameEl.classList.add("input-error"); return; }
//     if (!path) { pathEl.classList.add("input-error"); return; }

//     addAppRow(name, path);

//     nameEl.value = "";
//     pathEl.value = "";
// }


// /* ==============================================================  
//    INCLUDES  
// ============================================================== */
// function addInclude() {
//     const input = document.querySelector("#includeInput");
//     const value = input.value.trim();
//     const tbody = document.querySelector("#includesTable tbody");

//     if (!value) {
//         input.classList.add("input-error");
//         return;
//     }

//     input.classList.remove("input-error");

//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//         <td>${value}</td>
//         <td><button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateIncludes(); updateSaveButton();">X</button></td>
//     `;

//     tbody.appendChild(tr);
//     input.value = "";

//     validateIncludes();
//     updateSaveButton();
// }


// /* ==============================================================  
//    WEIGHTS (ASSET)  
// ============================================================== */

// function addWeightCard() {
//     const nameEl     = document.getElementById("w_name");
//     const labelEl    = document.getElementById("w_label");
//     const modeEl     = document.getElementById("w_mode");
//     const valueEl    = document.getElementById("w_value");
//     const patternEl  = document.getElementById("w_pattern");
//     const enabledEl  = document.getElementById("w_enabled");
//     const includeEl  = document.getElementById("w_include");
//     const perEl      = document.getElementById("w_per");
//     const oneIfAnyEl = document.getElementById("w_oneIfAny");

//     [nameEl, labelEl, modeEl, valueEl, patternEl, includeEl, perEl].forEach(el => {
//         if (el) el.classList.remove("input-error");
//     });

//     let ok = true;

//     const name     = nameEl.value.trim();
//     const label    = labelEl.value.trim();
//     const mode     = modeEl.value;
//     const value    = valueEl.value;
//     const pattern  = patternEl.value.trim();
//     const enabled  = enabledEl.checked;
//     const per      = perEl.value ? parseInt(perEl.value, 10) : 1;
//     const oneIfAny = oneIfAnyEl.checked;

//     const includeLines = includeEl.value.split("\n").map(x => x.trim()).filter(x => x);

//     if (!name) { nameEl.classList.add("input-error"); ok = false; }
//     if (!label) { labelEl.classList.add("input-error"); ok = false; }
//     if (!["glob","text"].includes(mode)) { modeEl.classList.add("input-error"); ok = false; }
//     if (!isNumber(value) || value <= 0) { valueEl.classList.add("input-error"); ok = false; }
//     if (!pattern) { patternEl.classList.add("input-error"); ok = false; }
//     if (!per || per <= 0) { perEl.classList.add("input-error"); ok = false; }

//     if (!ok) return;

//     const asset = {
//         enabled,
//         name,
//         label,
//         mode,
//         value: parseFloat(value),
//         pattern,
//         include: includeLines,
//         per,
//         oneIfAny
//     };

//     weightsState.push(asset);

//     renderWeightsTable();

//     nameEl.value = "";
//     labelEl.value = "";
//     valueEl.value = "";
//     patternEl.value = "";
//     includeEl.value = "";
//     perEl.value = "1";
//     enabledEl.checked = true;
//     oneIfAnyEl.checked = false;

//     refreshComplexitySelectors();
//     validateWeights();
//     updateSaveButton();
// }

// function renderWeightsTable() {
//     const tbody = document.querySelector("#weightsTable tbody");
//     tbody.innerHTML = "";

//     weightsState.forEach((w, index) => {
//         const tr = document.createElement("tr");
//         tr.innerHTML = `
//             <td>${w.enabled ? "✔️" : "—"}</td>
//             <td>${w.name}</td>
//             <td>${w.label}</td>
//             <td>${w.mode}</td>
//             <td>${w.value}</td>
//             <td>${w.pattern}</td>
//             <td>${w.include.length ? w.include.join(", ") : "—"}</td>
//             <td>${w.per}</td>
//             <td>${w.oneIfAny ? "✔️" : "—"}</td>
//             <td><button type="button" class="btn-small" onclick="removeWeight(${index})">Rimuovi</button></td>
//         `;
//         tbody.appendChild(tr);
//     });
// }

// function removeWeight(index) {
//     weightsState.splice(index, 1);
//     renderWeightsTable();
//     refreshComplexitySelectors();
//     validateWeights();
//     updateSaveButton();
// }


// /* ==============================================================  
//    COMPLEXITY  
// ============================================================== */
// function refreshComplexitySelectors() {
//     const num = document.getElementById("complexNum");
//     const den = document.getElementById("complexDen");

//     if (!num || !den) return;

//     num.innerHTML = "<option value=''>--</option>";
//     den.innerHTML = "<option value=''>--</option>";

//     weightsState.forEach(w => {
//         num.innerHTML += `<option value="${w.name}">${w.name}</option>`;
//         den.innerHTML += `<option value="${w.name}">${w.name}</option>`;
//     });
// }


// /* ==============================================================  
//    THRESHOLDS  
// ============================================================== */
// function addThresholdRow() {
//     const tbody = document.querySelector("#thresholdsTable tbody");

//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//         <td><input type="text" class="th-label"></td>
//         <td>
//             <select class="th-op">
//                 <option value="<"><</option>
//                 <option value=">=">>=</option>
//             </select>
//         </td>
//         <td><input type="number" step="0.1" class="th-max"></td>
//         <td><button type="button" class="btn-small" onclick="this.closest('tr').remove()">X</button></td>
//     `;

//     tbody.appendChild(tr);
// }


/* ==========================================================
   STATO GLOBALE ASSET / WEIGHTS
   ========================================================== */
let weightsState = [];


/* ==========================================================
   BOOTSTRAP DOM
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const saveBtn = document.getElementById("saveBtn");

    // Sblocca il bottone (se era disabled da HTML)
    if (saveBtn) {
        saveBtn.disabled = false;
    }

    // Submit form
    form.addEventListener("submit", (event) => {
        // 1) Validazione
        if (!validateForm()) {
            event.preventDefault();
            alert("⚠️ Prima di salvare, completa i campi obbligatori evidenziati.");
            return;
        }

        // 2) Prepara payload per il backend (apps + weights JSON)
        buildHiddenPayloadFields(form);
        // 3) Lasciamo procedere il submit normalmente
    });

    // Validazione live per la sezione generale
    document.querySelectorAll("#sec-general input").forEach(input => {
        input.addEventListener("input", validateGeneral);
    });
});


/* ==========================================================
   TOOLS
   ========================================================== */

function highlightSection(sectionIndex, valid) {
    const sections = document.querySelectorAll(".section");
    const sec = sections[sectionIndex];
    if (!sec) return;

    sec.style.border = valid ? "2px solid #34c759" : "2px solid #ff9f0a";
}

function isNumber(x) {
    return !isNaN(parseFloat(x)) && isFinite(x);
}

/**
 * Costruisce/aggiorna i campi hidden "apps" e "weights"
 * nel FORM prima dell'invio.
 */
function buildHiddenPayloadFields(form) {
    /* ---- APPS: name|path\n... ---- */
    const appLines = [];
    document.querySelectorAll("#appsTable tbody tr").forEach(tr => {
        const name = tr.querySelector(".app-name")?.value.trim() || "";
        const path = tr.querySelector(".app-path")?.value.trim() || "";
        if (name && path) {
            appLines.push(`${name}|${path}`);
        }
    });
    let appsInput = form.querySelector("input[name='apps']");
    if (!appsInput) {
        appsInput = document.createElement("input");
        appsInput.type = "hidden";
        appsInput.name = "apps";
        form.appendChild(appsInput);
    }
    appsInput.value = appLines.join("\n");

    /* ---- TEAM SIZES ---- */
    const rawTeams = document.querySelector("#teamSizes").value.trim();
    let teamList = [];

    if (rawTeams.length > 0) {
        teamList = rawTeams
            .split(",")
            .map(v => v.trim())
            .filter(v => v !== "" && !isNaN(v))
            .map(Number);
    }

    // crea/aggiorna campo hidden
    let teamInput = form.querySelector("input[name='teamSizes']");
    if (!teamInput) {
        teamInput = document.createElement("input");
        teamInput.type = "hidden";
        teamInput.name = "teamSizes";
        form.appendChild(teamInput);
    }

    teamInput.value = JSON.stringify(teamList);

    /* ---- WEIGHTS: JSON dict { key: { ... } } ---- */
    const weightsPayload = {};

    weightsState.forEach(w => {
        // pattern nel config è un array
        const patternList = w.pattern ? [w.pattern] : [];
        const includeList = Array.isArray(w.include) ? w.include : [];

        weightsPayload[w.name] = {
            enabled: w.enabled,
            label: w.label,
            value: w.value,
            mode: w.mode,
            pattern: patternList,
            include: includeList,
            per: w.per,
            oneIfAny: w.oneIfAny
            // desc opzionale: non lo usiamo, il report fa .get("desc","")
        };
    });

    let weightsInput = form.querySelector("input[name='weights']");
    if (!weightsInput) {
        weightsInput = document.createElement("input");
        weightsInput.type = "hidden";
        weightsInput.name = "weights";
        form.appendChild(weightsInput);
    }
    weightsInput.value = JSON.stringify(weightsPayload);
}


/* ==========================================================
   VALIDAZIONE PER SEZIONE
   ========================================================== */

/* ---- 1) GENERAL ---- */
function validateGeneral() {
    let ok = true;

    const section = document.querySelector("#sec-general");

    const activeProfile = document.querySelector("#activeProfile");
    const separator     = document.querySelector("#separatorWidth");
    const migration     = document.querySelector("#migrationFactor");
    const teamSizes     = document.querySelector("#teamSizes");

    // Reset error styles
    [activeProfile, separator, migration, teamSizes].forEach(el => {
        el.classList.remove("input-error");
    });

    // Nome profilo
    if (!activeProfile.value.trim()) {
        ok = false;
        activeProfile.classList.add("input-error");
    }

    // Separator width
    if (!isNumber(separator.value) || separator.value <= 0) {
        ok = false;
        separator.classList.add("input-error");
    }

    // Migration factor
    if (!isNumber(migration.value) || migration.value < 0) {
        ok = false;
        migration.classList.add("input-error");
    }

    // Team sizes
    const rawTeams = teamSizes.value.trim();
    const teamList = rawTeams
        .split(",")
        .map(v => v.trim())
        .filter(v => v !== "");

    if (teamList.length === 0 || !teamList.every(isNumber)) {
        ok = false;
        teamSizes.classList.add("input-error");
    }

    if (ok) {
        section.classList.remove("invalid");
        section.classList.add("valid");
    } else {
        section.classList.remove("valid");
        section.classList.add("invalid");
    }

    return ok;
}


/* ---- 2) APPS ---- */
function validateApps() {
    const section = document.querySelector("#sec-apps");
    let ok = true;

    const rows = document.querySelectorAll("#appsTable tbody tr");
    if (rows.length === 0) ok = false;

    rows.forEach(tr => {
        const name = tr.querySelector(".app-name").value.trim();
        const path = tr.querySelector(".app-path").value.trim();
        if (!name || !path) ok = false;
    });

    section.classList.toggle("valid", ok);
    section.classList.toggle("invalid", !ok);

    return ok;
}


/* ---- 3) DEFAULT INCLUDES ---- */
function validateIncludes() {
    const section = document.querySelector("#sec-includes");
    const rows = document.querySelectorAll("#includesTable tbody tr");

    const ok = rows.length > 0;

    if (ok) {
        section.classList.remove("invalid");
        section.classList.add("valid");
    } else {
        section.classList.remove("valid");
        section.classList.add("invalid");
    }

    return ok;
}


/* ---- 4) WEIGHTS ---- */
function validateWeights() {
    let ok = true;
    const section = document.querySelector("#sec-weights");

    if (!weightsState.length) {
        ok = false;
    } else {
        weightsState.forEach(w => {
            if (
                !w.name ||
                !w.label ||
                !["glob", "text"].includes(w.mode) ||
                !isNumber(w.value) || w.value <= 0
            ) {
                ok = false;
            }
        });
    }

    if (ok) {
        section.classList.remove("invalid");
        section.classList.add("valid");
    } else {
        section.classList.remove("valid");
        section.classList.add("invalid");
    }

    return ok;
}


/* ---- 5) COMPLEXITY (OPZIONALE) ---- */
function validateComplexity() {
    let ok = true;

    const num = document.querySelector("#complexNum");
    const den = document.querySelector("#complexDen");

    const numVal = num ? num.value : "";
    const denVal = den ? den.value : "";

    // Se entrambi vuoti → sezione OK
    if (!numVal && !denVal) {
        highlightSection(4, true);
        return true;
    }

    if (!numVal || !denVal) ok = false;

    const rows = document.querySelectorAll("#thresholdsTable tbody tr");
    rows.forEach(tr => {
        const lbl = tr.querySelector(".th-label").value.trim();
        const max = tr.querySelector(".th-max").value;

        if (!lbl) ok = false;
        if (!isNumber(max)) ok = false;
    });

    highlightSection(4, ok);
    return ok;
}


/* ==========================================================
   VALIDAZIONE COMPLETA (submit)
   ========================================================== */

function validateForm() {
    const results = [
        validateGeneral(),
        validateApps(),
        validateIncludes(),
        validateWeights(),
        validateComplexity(),
    ];

    return results.every(v => v === true);
}


/* ==========================================================
   FUNZIONI APPS
   ========================================================== */

function addAppRow(name = "", path = "") {
    const tbody = document.querySelector("#appsTable tbody");
    const tr = document.createElement("tr");

    tr.innerHTML = `
        <td><input type="text" class="app-name" value="${name}"></td>
        <td><input type="text" class="app-path" value="${path}"></td>
        <td><button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateApps();">X</button></td>
    `;
    tbody.appendChild(tr);

    validateApps();
}

function addAppFromForm() {
    const nameEl = document.querySelector("#app_name");
    const pathEl = document.querySelector("#app_path");

    const name = nameEl.value.trim();
    const path = pathEl.value.trim();

    nameEl.classList.remove("input-error");
    pathEl.classList.remove("input-error");

    let valid = true;
    if (!name) { valid = false; nameEl.classList.add("input-error"); }
    if (!path) { valid = false; pathEl.classList.add("input-error"); }

    if (!valid) return;

    const tbody = document.querySelector("#appsTable tbody");
    const tr = document.createElement("tr");

    tr.innerHTML = `
        <td><input type="text" class="app-name" value="${name}"></td>
        <td><input type="text" class="app-path" value="${path}"></td>
        <td><button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateApps();">X</button></td>
    `;

    tbody.appendChild(tr);

    nameEl.value = "";
    pathEl.value = "";

    validateApps();
}


/* ==========================================================
   FUNZIONI DEFAULT INCLUDES
   ========================================================== */

function addInclude() {
    // ID aggiornato in base all'HTML: <input id="inc_value">
    const input = document.querySelector("#includeInput");
    const value = input.value.trim();
    const tbody = document.querySelector("#includesTable tbody");

    if (!value) {
        input.classList.add("input-error");
        return;
    }

    input.classList.remove("input-error");

    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td>${value}</td>
        <td>
            <button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateIncludes();">X</button>
        </td>
    `;

    tbody.appendChild(tr);
    input.value = "";
    validateIncludes();
}


/* ==========================================================
   FUNZIONI WEIGHTS / ASSET
   ========================================================== */

let weightCounter = 0; // eventualmente usabile in futuro

function addWeightCard() {
    const nameEl     = document.getElementById("w_name");
    const labelEl    = document.getElementById("w_label");
    const modeEl     = document.getElementById("w_mode");
    const valueEl    = document.getElementById("w_value");
    const patternEl  = document.getElementById("w_pattern");
    const enabledEl  = document.getElementById("w_enabled");
    const includeEl  = document.getElementById("w_include");
    const perEl      = document.getElementById("w_per");
    const oneIfAnyEl = document.getElementById("w_oneIfAny");

    [nameEl, labelEl, modeEl, valueEl, patternEl, includeEl, perEl].forEach(el => {
        if (el) el.classList.remove("input-error");
    });

    let ok = true;

    const name     = nameEl.value.trim();
    const label    = labelEl.value.trim();
    const mode     = modeEl.value;
    const value    = valueEl.value;
    const pattern  = patternEl.value.trim();
    const enabled = enabledEl.value === "true";
    const per      = perEl.value ? parseInt(perEl.value, 10) : 1;
    const oneIfAny = oneIfAnyEl.checked;

    const includeLines = includeEl.value
        .split("\n")
        .map(x => x.trim())
        .filter(x => x.length > 0);

    if (!name) { nameEl.classList.add("input-error"); ok = false; }
    if (!label) { labelEl.classList.add("input-error"); ok = false; }
    if (!["glob","text"].includes(mode)) { modeEl.classList.add("input-error"); ok = false; }
    if (!isNumber(value) || value <= 0) { valueEl.classList.add("input-error"); ok = false; }
    if (!pattern) { patternEl.classList.add("input-error"); ok = false; }
    if (!per || per <= 0) { perEl.classList.add("input-error"); ok = false; }

    if (!ok) return;

    const asset = {
        enabled,
        name,
        label,
        mode,
        value: parseFloat(value),
        pattern,
        include: includeLines,
        per,
        oneIfAny
    };

    weightsState.push(asset);

    renderWeightsTable();

    // reset form
    nameEl.value = "";
    labelEl.value = "";
    valueEl.value = "";
    patternEl.value = "";
    includeEl.value = "";
    perEl.value = "1";
    enabledEl.checked = true;
    oneIfAnyEl.checked = false;

    refreshComplexitySelectors();
    validateWeights();
}


function renderWeightsTable() {
    const tbody = document.querySelector("#weightsTable tbody");
    tbody.innerHTML = "";

    weightsState.forEach((w, index) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${w.enabled ? "✔️" : "—"}</td>
            <td>${w.name || ""}</td>
            <td>${w.label || ""}</td>
            <td>${w.mode || ""}</td>
            <td>${w.value ?? ""}</td>
            <td>${w.pattern || ""}</td>
            <td>${(w.include && w.include.length) ? w.include.join(", ") : "—"}</td>
            <td>${w.per ?? 1}</td>
            <td>${w.oneIfAny ? "✔️" : "—"}</td>
            <td>
                <button type="button" class="btn-small" onclick="removeWeight(${index});">
                    Rimuovi
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}


function removeWeight(index) {
    weightsState.splice(index, 1);
    renderWeightsTable();
    refreshComplexitySelectors();
    validateWeights();
}


/* ==========================================================
   COMPLEXITY: SELECTOR UPDATE & THRESHOLDS
   ========================================================== */

function refreshComplexitySelectors() {
    const num = document.getElementById("complexNum");
    const den = document.getElementById("complexDen");

    if (!num || !den) return;

    num.innerHTML = "<option value=''>--</option>";
    den.innerHTML = "<option value=''>--</option>";

    weightsState.forEach(w => {
        num.innerHTML += `<option value="${w.name}">${w.name}</option>`;
        den.innerHTML += `<option value="${w.name}">${w.name}</option>`;
    });
}

function addThresholdRow() {
    const tbody = document.querySelector("#thresholdsTable tbody");

    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td><input type="text" class="th-label"></td>
        <td>
          <select class="th-op">
            <option value="<"><</option>
            <option value=">=">>=</option>
          </select>
        </td>
        <td><input type="number" step="0.1" class="th-max"></td>
        <td><button type="button" class="btn-small" onclick="this.closest('tr').remove(); validateComplexity();">X</button></td>
    `;
    tbody.appendChild(tr);
}
