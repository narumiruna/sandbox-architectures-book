document$.subscribe(({ body }) => {
  if (typeof katex === "undefined" || typeof renderMathInElement !== "function") return;

  for (const formula of body.querySelectorAll(".arithmatex")) {
    renderMathInElement(formula, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true },
      ],
      ignoredClasses: ["katex", "katex-error"],
    });
  }
});
