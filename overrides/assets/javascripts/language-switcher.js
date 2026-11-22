(() => {
  let pendingSwitch;

  document.addEventListener("click", async (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;

    const link = event.target.closest?.('.language-versions a[href][hreflang][target="_self"]');
    if (!link || link.hasAttribute("download")) return;

    pendingSwitch?.abort();
    const { hash, href: source, origin, protocol } = window.location;
    if (!hash || link.hash || link.getAttribute("aria-current") === "page") return;
    if (link.origin !== origin || link.protocol !== protocol || !["http:", "https:"].includes(protocol)) return;

    let id;
    try {
      id = decodeURIComponent(hash.slice(1));
    } catch {
      return;
    }

    event.preventDefault();
    const destination = new URL(link.href);
    const request = new AbortController();
    pendingSwitch = request;
    try {
      const response = await fetch(destination, { mode: "same-origin", signal: request.signal });
      if (response.ok) {
        // Parse only to check IDs; template content does not load subresources.
        const template = document.createElement("template");
        template.innerHTML = await response.text();
        if (template.content.getElementById(id)) destination.hash = hash;
      }
    } catch {
      // If the check fails, follow the original link.
    }

    if (request.signal.aborted) return;
    pendingSwitch = undefined;
    if (window.location.href === source) window.location.assign(destination);
  });

  if (!("popoverTargetElement" in HTMLButtonElement.prototype) || typeof document$ === "undefined") return;
  let switcher;

  document$.subscribe(({ body }) => {
    switcher?.remove();
    switcher = undefined;

    const template = body.querySelector("#language-switcher-template");
    const versions = body.querySelector(".language-versions");
    const slot = body.querySelector('.md-header__inner > [for="__search"], .md-header__inner > .md-header__source');
    if (!template || !versions || !slot) return;

    switcher = template.content.firstElementChild.cloneNode(true);
    versions.id = "language-versions";
    versions.setAttribute("popover", "auto");
    switcher.append(versions);
    slot.before(switcher);
  });
})();
