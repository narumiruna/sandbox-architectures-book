// After a strict site build, run: node --test scripts/check_edition_search.mjs
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { createContext, runInContext, runInNewContext } from "node:vm";

const site = new URL("https://example.test/sandbox-architectures-book/");
const webAssembly = "isolation/generated-scripts/webassembly/";
const controlPlanes = "practice/operations/control-planes/";

function readAsset(url) {
  assert.equal(url.origin, site.origin);
  assert.ok(url.pathname.startsWith(site.pathname), `Asset outside the site base: ${url}`);
  return readFileSync(`site/${url.pathname.slice(site.pathname.length)}`, "utf8");
}

function readConfig(page) {
  const html = readAsset(new URL("index.html", page));
  const markup = html.match(/<script\b[^>]*\bid="__config"[^>]*>([\s\S]*?)<\/script>/);
  assert.ok(markup, `Missing theme config on ${page}`);
  const element = { textContent: markup[1] };
  const setup = Array.from(html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g))
    .find(([, body]) => body.includes("edition-search.js"));
  if (setup) {
    const document = {
      baseURI: page.href,
      documentElement: { lang: html.match(/<html\b[^>]*\blang="([^"]+)"/)?.[1] },
      getElementById: (id) => id === "__config" ? element : null,
    };
    runInNewContext(setup[1], { document, URL });
  }
  return JSON.parse(element.textContent);
}

function loadWorker(url) {
  let reply;
  const self = {
    location: { href: url.href },
    postMessage: (data) => reply(structuredClone(data)),
  };
  const context = createContext({
    self,
    URL,
    importScripts: (src) => runInContext(readAsset(new URL(src, url)), context),
  });
  runInContext(readAsset(url), context, { filename: url.pathname });
  return (data) => new Promise((resolve) => {
    reply = resolve;
    self.onmessage({ data: structuredClone(data) });
  });
}

async function search(request, input, index) {
  const locations = new Set();
  let page;
  do {
    const result = await request({
      type: 2,
      data: {
        input,
        page,
        filter: {
          input: { type: "operator", data: { operator: "and", operands: [] } },
          aggregation: { input: [{ type: "term", data: { field: "tags" } }] },
        },
      },
    });
    assert.equal(result.type, 3, `Expected stock worker results for ${input}`);
    const { items, pagination } = result.data;
    for (const { id } of items) {
      // The page turns IDs into links using the unfiltered index.
      assert.ok(index.items[id], `Invalid result ID: ${id}`);
      const location = index.items[id].location;
      assert.ok(!locations.has(location), `Repeated result: ${location}`);
      locations.add(location);
    }
    page = pagination.next;
    if (page) {
      assert.ok(items.length && locations.size < pagination.total, "Invalid next page");
    } else {
      assert.equal(locations.size, pagination.total);
    }
  } while (page);
  return locations;
}

const cases = [
  ["en"],
  ["zh-TW", "資源上限", "practice/operations/resource-limits/"],
];
const translations = cases.slice(1).map(([edition]) => edition);

for (const [edition, phrase, chapter] of cases) {
  test(`stock search stays in ${edition}`, { timeout: 10_000 }, async () => {
    const prefix = edition === "en" ? "" : `${edition}/`;
    const page = new URL(`${prefix}${controlPlanes}`, site);
    const config = readConfig(page);
    const adapter = new URL(config.search, page);
    assert.equal(adapter.pathname, `${site.pathname}assets/javascripts/workers/edition-search.js`);

    const base = new URL(config.base, page);
    if (!base.pathname.endsWith("/")) base.pathname += "/";
    assert.equal(base.href, site.href);
    const index = JSON.parse(readAsset(new URL("search.json", base)));
    for (const item of index.items) {
      // Match the pinned page bundle's absolute location conversion.
      item.location = new URL(`./${item.location}`, base).href;
    }
    const request = loadWorker(adapter);
    assert.deepEqual(await request({ type: 0, data: index }), { type: 1 });

    const queries = [["WebAssembly", webAssembly]];
    if (phrase) queries.push([phrase, chapter]);
    for (const [query, expected] of queries) {
      const locations = await search(request, query, index);
      const target = new URL(`${prefix}${expected}`, base);
      assert.ok(locations.has(target.href), `Search for ${query} missed ${target}`);
      for (const location of locations) {
        const segment = new URL(location).pathname.slice(base.pathname.length).split("/", 1)[0];
        assert.equal(translations.includes(segment) ? segment : "en", edition, location);
      }
    }
  });
}
