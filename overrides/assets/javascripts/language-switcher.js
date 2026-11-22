if ("popoverTargetElement" in HTMLButtonElement.prototype && typeof document$ !== "undefined") {
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
}
