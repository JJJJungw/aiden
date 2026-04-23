from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.core.config import settings

router = APIRouter(tags=["Dev Test"])

#ㄴㄴㄴㄴㄴ
@router.get("/dev/google-test", response_class=HTMLResponse)
async def google_test_page() -> str:
    return f"""
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Google Login Test</title>
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <style>
      :root {{
        color-scheme: light;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      body {{
        margin: 0;
        background: linear-gradient(160deg, #f3f7ff 0%, #eef7f1 100%);
        color: #14213d;
      }}
      .wrap {{
        max-width: 760px;
        margin: 48px auto;
        padding: 24px;
      }}
      .card {{
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #d7e3f4;
        border-radius: 20px;
        box-shadow: 0 24px 60px rgba(20, 33, 61, 0.08);
        padding: 28px;
      }}
      h1 {{
        margin: 0 0 12px;
        font-size: 32px;
      }}
      p {{
        margin: 0 0 18px;
        line-height: 1.6;
      }}
      .row {{
        margin: 18px 0;
      }}
      .label {{
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #5c6f91;
        margin-bottom: 8px;
      }}
      pre {{
        white-space: pre-wrap;
        word-break: break-word;
        background: #0f172a;
        color: #e2e8f0;
        padding: 16px;
        border-radius: 14px;
        min-height: 88px;
        margin: 0;
        overflow-x: auto;
      }}
      .pill {{
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: #dff5e8;
        color: #10653a;
        font-weight: 700;
        font-size: 13px;
      }}
      .error {{
        background: #ffe4e6;
        color: #be123c;
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="card">
        <span id="status-pill" class="pill">Ready</span>
        <h1>Google OAuth Test</h1>
        <p>이 페이지에서 Google 로그인 후 HttpOnly 쿠키 발급과 FastAPI <code>/auth/me</code>를 바로 테스트할 수 있습니다.</p>

        <div class="row">
          <div id="g_id_onload"
               data-client_id="{settings.google_client_id}"
               data-callback="handleCredentialResponse"
               data-auto_prompt="false"></div>
          <div class="g_id_signin"
               data-type="standard"
               data-size="large"
               data-theme="outline"
               data-text="continue_with"
               data-shape="pill"></div>
        </div>

        <div class="row">
          <div class="label">Google ID Token</div>
          <pre id="id-token-output">아직 로그인 전입니다.</pre>
        </div>

        <div class="row">
          <div class="label">Backend /auth/google Response</div>
          <pre id="login-output">아직 요청 전입니다.</pre>
        </div>

        <div class="row">
          <div class="label">Backend /auth/me Response</div>
          <pre id="me-output">아직 요청 전입니다.</pre>
        </div>

        <div class="row">
          <button id="logout-button" type="button">Logout</button>
        </div>
      </div>
    </div>

    <script>
      const statusPill = document.getElementById("status-pill");
      const idTokenOutput = document.getElementById("id-token-output");
      const loginOutput = document.getElementById("login-output");
      const meOutput = document.getElementById("me-output");
      const logoutButton = document.getElementById("logout-button");

      function setStatus(text, isError = false) {{
        statusPill.textContent = text;
        statusPill.className = isError ? "pill error" : "pill";
      }}

      function pretty(value) {{
        return JSON.stringify(value, null, 2);
      }}

      async function handleCredentialResponse(response) {{
        try {{
          setStatus("Calling /auth/google");
          idTokenOutput.textContent = response.credential;

          const loginRes = await fetch("/auth/google", {{
            method: "POST",
            credentials: "include",
            headers: {{
              "Content-Type": "application/json"
            }},
            body: JSON.stringify({{ id_token: response.credential }})
          }});

          const loginData = await loginRes.json();
          loginOutput.textContent = pretty(loginData);

          if (!loginRes.ok) {{
            setStatus("Login failed", true);
            meOutput.textContent = "로그인 실패로 /auth/me 호출을 건너뜁니다.";
            return;
          }}

          setStatus("Calling /auth/me");

          const meRes = await fetch("/auth/me", {{
            credentials: "include"
          }});

          const meData = await meRes.json();
          meOutput.textContent = pretty(meData);

          if (!meRes.ok) {{
            setStatus("Authenticated but /auth/me failed", true);
            return;
          }}

          setStatus("Success");
        }} catch (error) {{
          setStatus("Unexpected error", true);
          loginOutput.textContent = String(error);
        }}
      }}

      logoutButton.addEventListener("click", async () => {{
        const response = await fetch("/auth/logout", {{
          method: "POST",
          credentials: "include"
        }});

        if (response.ok) {{
          setStatus("Logged out");
          loginOutput.textContent = "로그아웃 완료";
          meOutput.textContent = "세션이 제거되었습니다.";
        }} else {{
          setStatus("Logout failed", true);
        }}
      }});

      window.handleCredentialResponse = handleCredentialResponse;
    </script>
  </body>
</html>
"""
