(() => {
  const key = "sandbox-architectures-book.paper";
  const papers = {
    oat: "Oat",
    sage: "Sage",
    tea: "Tea",
    linen: "Linen",
    original: "Original",
  };
  const root = document.documentElement;

  function applyPaper(value) {
    const paper = Object.hasOwn(papers, value) ? value : "linen";
    root.dataset.paper = paper;
    return paper;
  }

  try {
    applyPaper(localStorage.getItem(key));
  } catch {
    // The CSS default still works if browser storage is blocked.
  }

  document.addEventListener("DOMContentLoaded", () => {
    const palette = document.querySelector('[data-md-component="palette"]');
    if (!palette) return;
    palette.lang = "en";

    const picker = document.createElement("div");
    picker.className = "paper-picker";
    picker.lang = "en";
    const label = document.createElement("label");
    label.className = "md-visually-hidden";
    label.htmlFor = "daytime-paper";
    label.textContent = "Daytime paper";
    const select = document.createElement("select");
    select.id = label.htmlFor;
    for (const [value, name] of Object.entries(papers)) {
      select.add(new Option(name, value));
    }
    select.value = root.dataset.paper ?? "linen";
    picker.append(label, select);
    palette.after(picker);

    select.addEventListener("change", () => {
      const paper = applyPaper(select.value);
      try {
        localStorage.setItem(key, paper);
      } catch {
        // Keep the selection for this page when storage is blocked.
      }
    });

    window.addEventListener("storage", (event) => {
      if (event.key === key || event.key === null) {
        select.value = applyPaper(event.newValue);
      }
    });
  });
})();
