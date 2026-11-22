// Zensical UI 0.0.43: type 0 initializes the index, type 2 queries it,
// and types 1, 3, and 4 report ready, results, and errors.
(() => {
  const url = new URL(self.location.href);
  // This adapter and the stock worker live in assets/javascripts/workers/.
  const base = new URL("../../../", url);
  const edition = url.searchParams.get("edition");
  const locales = url.searchParams.get("locales");
  const worker = url.searchParams.get("worker");
  if (!edition || !locales || !worker || !/^search\.[a-f0-9]+\.min\.js$/.test(worker)) {
    throw new Error("Invalid edition search worker configuration");
  }
  const translations = new Set(locales.split(","));
  if (edition !== "en" && !translations.has(edition)) {
    throw new Error(`Unknown search edition: ${edition}`);
  }

  importScripts(new URL(worker, url).href);
  const handleMessage = self.onmessage;
  const postMessage = self.postMessage.bind(self);
  let originalIds = [];

  self.onmessage = (event) => {
    const message = event.data;
    if (message.type !== 0) {
      handleMessage.call(self, event);
      return;
    }

    // The page bundle has already resolved each location against the site base.
    const index = message.data;
    originalIds = [];
    const items = index.items.filter(({ location }, id) => {
      const target = new URL(location);
      if (target.origin !== base.origin || !target.pathname.startsWith(base.pathname)) {
        return false;
      }
      const firstSegment = target.pathname.slice(base.pathname.length).split("/", 1)[0];
      const locale = translations.has(firstSegment) ? firstSegment : "en";
      if (locale !== edition) {
        return false;
      }
      originalIds.push(id);
      return true;
    });
    const data = { ...index, config: { ...index.config, lang: [edition] }, items };
    handleMessage.call(self, { data: { ...message, data } });
  };

  // The page still uses the full index to turn result IDs into links. Copy the
  // results before remapping, because the stock worker caches them for pagination.
  self.postMessage = (message) => {
    if (message.type === 3) {
      const items = message.data.items.map((item) => ({ ...item, id: originalIds[item.id] }));
      postMessage({ ...message, data: { ...message.data, items } });
    } else {
      postMessage(message);
    }
  };
})();
