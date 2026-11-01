import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const jsonHeaders = { ...corsHeaders, "Content-Type": "application/json" };

function dateDDMMYYYY(value: string): string {
  const [year, month, day] = value.split("-");
  return `${day}/${month}/${year}`;
}
function membershipDates(createdAt: string) {
  const start = new Date(createdAt);
  const startIso = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Kolkata", year: "numeric", month: "2-digit", day: "2-digit",
  }).format(start);
  const [y, m, d] = startIso.split("-").map(Number);
  // 30 calendar days inclusive: 28/10/2026 through 27/11/2026.
  const end = new Date(Date.UTC(y, m - 1, d + 29));
  const endIso = `${end.getUTCFullYear()}-${String(end.getUTCMonth() + 1).padStart(2, "0")}-${String(end.getUTCDate()).padStart(2, "0")}`;
  return { start: dateDDMMYYYY(startIso), end: dateDDMMYYYY(endIso) };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method !== "POST") return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers: jsonHeaders });
  const authHeader = req.headers.get("Authorization") || "";
  const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY") || "";
  const waToken = Deno.env.get("WHATSAPP_ACCESS_TOKEN") || "";
  const phoneNumberId = Deno.env.get("WHATSAPP_PHONE_NUMBER_ID") || "";
  const templateName = Deno.env.get("WHATSAPP_TEMPLATE_NAME") || "seat_confirmation";
  const languageCode = Deno.env.get("WHATSAPP_LANGUAGE_CODE") || "hi";
  if (!authHeader.startsWith("Bearer ") || !supabaseUrl || !anonKey)
    return new Response(JSON.stringify({ error: "Authentication/configuration missing" }), { status: 401, headers: jsonHeaders });

  const client = createClient(supabaseUrl, anonKey, { global: { headers: { Authorization: authHeader } }, auth: { persistSession: false } });
  const { data: userData, error: userError } = await client.auth.getUser();
  if (userError || !userData.user) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401, headers: jsonHeaders });
  const { data: isAdmin, error: adminError } = await client.rpc("is_library_admin");
  if (adminError || isAdmin !== true) return new Response(JSON.stringify({ error: "Library admin access required" }), { status: 403, headers: jsonHeaders });
  if (!waToken || !phoneNumberId) return new Response(JSON.stringify({ error: "WhatsApp Cloud API secrets are not configured" }), { status: 503, headers: jsonHeaders });

  try {
    const body = await req.json();
    const { registration_id, registration_no } = body;
    if (!registration_id || !registration_no) return new Response(JSON.stringify({ error: "Required registration fields missing" }), { status: 400, headers: jsonHeaders });
    const { data: registration, error: recordError } = await client.from("library_registrations")
      .select("id,full_name,mobile,seat_no,status,created_at")
      .eq("id", registration_id).maybeSingle();
    if (recordError || !registration || registration.status !== "active")
      return new Response(JSON.stringify({ error: "Confirmed registration not found" }), { status: 409, headers: jsonHeaders });

    const phone = String(registration.mobile).replace(/[^0-9]/g, "");
    const recipient = phone.length === 10 ? `91${phone}` : phone;
    const dates = membershipDates(registration.created_at);
    const payload = {
      messaging_product: "whatsapp", recipient_type: "individual", to: recipient, type: "template",
      template: { name: templateName, language: { code: languageCode }, components: [{ type: "body", parameters: [
        { type: "text", text: String(registration.full_name).slice(0, 100) },
        { type: "text", text: String(registration.seat_no) },
        { type: "text", text: String(registration_no).slice(0, 40) },
        { type: "text", text: dates.start },
        { type: "text", text: dates.end },
      ] }] },
    };
    const waResponse = await fetch(`https://graph.facebook.com/v22.0/${phoneNumberId}/messages`, {
      method: "POST", headers: { Authorization: `Bearer ${waToken}`, "Content-Type": "application/json" }, body: JSON.stringify(payload),
    });
    const waResult = await waResponse.json().catch(() => ({}));
    if (!waResponse.ok) return new Response(JSON.stringify({ error: "WhatsApp API rejected the message", details: waResult }), { status: 502, headers: jsonHeaders });
    return new Response(JSON.stringify({ success: true, membership_start: dates.start, membership_end: dates.end, whatsapp_message_id: waResult.messages?.[0]?.id || null }), { status: 200, headers: jsonHeaders });
  } catch (error) {
    return new Response(JSON.stringify({ error: error instanceof Error ? error.message : "Unexpected error" }), { status: 500, headers: jsonHeaders });
  }
});
