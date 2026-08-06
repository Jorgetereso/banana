// Banana Airways — ideas shared store (Cloudflare Worker + KV).
// GET  /  -> returns the stored ideas doc (JSON) or {}
// PUT  /  -> saves the posted JSON as the ideas doc
// No auth: anyone with the URL can read/write (fine for a small team, no sensitive data).

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });

    if (req.method === "GET") {
      const v = await env.IDEAS.get("doc");
      return new Response(v || "{}", { headers: { ...CORS, "Content-Type": "application/json" } });
    }

    if (req.method === "PUT") {
      const body = await req.text();
      // basic guard: must be valid JSON, under 256KB
      if (body.length > 262144) return new Response('{"error":"too big"}', { status: 413, headers: CORS });
      try { JSON.parse(body); } catch (e) { return new Response('{"error":"bad json"}', { status: 400, headers: CORS }); }
      await env.IDEAS.put("doc", body);
      return new Response('{"ok":true}', { headers: { ...CORS, "Content-Type": "application/json" } });
    }

    return new Response("method not allowed", { status: 405, headers: CORS });
  },
};
