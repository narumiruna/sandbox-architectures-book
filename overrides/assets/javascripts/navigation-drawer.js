(() => {
  const checkbox = document.querySelector("#__drawer");
  const overlay = document.querySelector('label.md-overlay[for="__drawer"]');
  const label = document.querySelector('.md-header label[for="__drawer"]');
  if (!checkbox || !overlay || !label || typeof document$ === "undefined" || !("inert" in HTMLElement.prototype)) return;

  // Match the drawer layout in Zensical UI 0.0.43, not the search or TOC breakpoint.
  const narrow = matchMedia("screen and (max-width: 76.234375em)");
  const trigger = document.createElement("button");
  trigger.type = "button";
  trigger.className = `${label.className} navigation-drawer__trigger`;
  trigger.hidden = true;
  trigger.addEventListener("click", () => checkbox.click());
  trigger.append(...label.childNodes);
  label.replaceWith(trigger);

  const closeLabels = {
    en: "Close navigation",
    "zh-TW": "關閉導覽列",
  };
  let drawer;
  let navigation;
  let closeButton;
  let groups = new Map();
  let open = false;
  const background = [];

  function sync() {
    const mobile = narrow.matches && Boolean(drawer);
    trigger.hidden = !mobile;
    trigger.setAttribute("aria-expanded", String(mobile && checkbox.checked));
    if (!mobile && checkbox.checked) {
      checkbox.click();
      return;
    }
    if (!drawer) return;

    if (mobile && checkbox.checked) {
      if (open) return;
      open = true;
      drawer.inert = false;
      drawer.setAttribute("role", "dialog");
      drawer.setAttribute("aria-modal", "true");
      drawer.setAttribute("aria-label", navigation.getAttribute("aria-label"));
      closeButton.hidden = false;
      closeButton.focus();

      // Disable the branches outside the drawer without blocking the stock backdrop.
      for (let branch = drawer; branch !== document.body; branch = branch.parentElement) {
        for (const sibling of branch.parentElement.children) {
          if (sibling === branch || sibling === overlay || sibling === checkbox || sibling.inert) continue;
          sibling.inert = true;
          background.push(sibling);
        }
      }
    } else {
      for (const element of background.splice(0)) element.inert = false;
      if (mobile && (open || drawer.contains(document.activeElement))) {
        trigger.focus({ preventScroll: true });
      } else if (!mobile && document.activeElement === closeButton) {
        navigation.querySelector(".md-nav__link[href]")?.focus();
      }
      open = false;
      drawer.inert = mobile;
      drawer.removeAttribute("role");
      drawer.removeAttribute("aria-modal");
      drawer.removeAttribute("aria-label");
      closeButton.hidden = true;
    }
  }

  function syncGroup(label) {
    if (narrow.matches) {
      // The theme uses tabindex="" for section labels that become controls on mobile.
      label.tabIndex = 0;
      label.setAttribute("role", "button");
      label.setAttribute("aria-expanded", String(label.control.checked));
    } else {
      label.setAttribute("tabindex", groups.get(label));
      label.removeAttribute("role");
      label.removeAttribute("aria-expanded");
    }
  }

  checkbox.addEventListener("change", sync);
  narrow.addEventListener("change", () => {
    for (const label of groups.keys()) syncGroup(label);
    sync();
  });
  window.addEventListener("pageshow", (event) => {
    if (event.persisted && checkbox.checked) checkbox.click();
  });

  document.addEventListener("keydown", (event) => {
    if (!open || event.defaultPrevented || event.isComposing) return;
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopPropagation();
      checkbox.click();
    } else if (event.key === "Tab") {
      const items = [...drawer.querySelectorAll("a[href], button, [tabindex]")].filter(
        (item) => item.tabIndex >= 0 && !item.matches(":disabled") && item.getClientRects().length && getComputedStyle(item).visibility === "visible",
      );
      const first = items[0];
      const last = items.at(-1);
      const active = document.activeElement;
      if (!items.includes(active) || active === (event.shiftKey ? first : last)) {
        event.preventDefault();
        (event.shiftKey ? last : first)?.focus();
      }
    } else if (event.key === " " && groups.has(document.activeElement)) {
      event.preventDefault();
      if (!event.repeat) document.activeElement.click();
    } else if (event.key === "/") {
      // The theme's global search shortcut would open a second dialog.
      event.stopPropagation();
    }
  });

  // Instant navigation replaces the sidebar, but keeps the header and checkbox.
  document$.subscribe(() => {
    const nextNavigation = document.querySelector(".md-sidebar--primary:not([hidden]) .md-nav--primary");
    const next = nextNavigation?.closest(".md-sidebar--primary") ?? null;
    if (next === drawer) return;
    if (drawer && checkbox.checked) checkbox.click();
    drawer = next;
    navigation = nextNavigation;
    groups = new Map();
    if (drawer) {
      drawer.id = "book-navigation";
      trigger.setAttribute("aria-controls", drawer.id);
      for (const label of navigation.querySelectorAll("label.md-nav__link[tabindex]")) {
        if (!label.control?.matches(".md-nav__toggle")) continue;
        groups.set(label, label.getAttribute("tabindex"));
        syncGroup(label);
      }
      drawer.addEventListener("change", (event) => {
        for (const label of event.target.labels ?? []) {
          if (groups.has(label)) syncGroup(label);
        }
      });
      closeButton = document.createElement("button");
      closeButton.type = "button";
      closeButton.className = "navigation-drawer__close";
      closeButton.hidden = true;
      closeButton.textContent = "×";
      const language = document.documentElement.lang;
      closeButton.setAttribute("aria-label", closeLabels[language] ?? closeLabels.en);
      if (!Object.hasOwn(closeLabels, language)) closeButton.lang = "en";
      closeButton.addEventListener("click", () => checkbox.click());
      navigation.prepend(closeButton);
      drawer.addEventListener("click", (event) => {
        // Unblock focus for the theme before it follows a link, including same-page sections.
        if (open && event.button === 0 && !event.ctrlKey && !event.metaKey && !event.altKey && !event.shiftKey && event.target.closest("a[href]")) {
          checkbox.click();
        }
      });
    } else {
      trigger.removeAttribute("aria-controls");
    }
    sync();
  });
})();
