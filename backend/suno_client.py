"""
ONUS PromptLab v2.0 — Suno API Client
Handles authentication and generation requests to Suno's internal REST API.

Auth flow:
  1. User provides their browser cookie (copied from DevTools Network tab)
  2. We extract the session_id from __client cookie
  3. We call Clerk to exchange session_id for a short-lived JWT
  4. We use that JWT as Bearer token for all Suno API calls
  5. JWT is refreshed automatically before expiry (~60s lifetime)
"""

import time
import httpx
import re
from typing import Optional

# ─── Suno / Clerk endpoints ───────────────────────────────────────────────────
CLERK_BASE      = "https://clerk.suno.com"
SUNO_API_BASE   = "https://studio-api.suno.ai"

# Default headers that mimic a real browser request
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer":    "https://suno.com/",
    "Origin":     "https://suno.com",
}


class SunoAuthError(Exception):
    """Raised when the user's cookie is invalid or the session has expired."""
    pass


class SunoGenerationError(Exception):
    """Raised when Suno rejects or fails a generation request."""
    pass


class SunoClient:
    """
    Async client for Suno's internal REST API.
    Each instance is tied to one user's session cookie.
    """

    def __init__(self, cookie: str):
        self.cookie = cookie.strip()
        self._jwt: Optional[str] = None
        self._jwt_expires_at: float = 0.0
        self._session_id: Optional[str] = self._extract_session_id(cookie)

    # ─── Auth helpers ─────────────────────────────────────────────────────────

    def _extract_session_id(self, cookie: str) -> Optional[str]:
        """
        Pull the Clerk session ID out of the raw cookie string.
        Looks for __client_uat or __session patterns used by Clerk.
        """
        # Try __client cookie first — contains the session ID directly
        match = re.search(r'__client=([^;]+)', cookie)
        if match:
            # The __client cookie value is a signed JWT; extract session ID from it
            # Format varies — we'll use it directly as a fallback
            pass

        # The session_id is most reliably pulled from __clerk_db_jwt or via API call
        # We fall back to using the full cookie string for auth
        return None

    async def _refresh_jwt(self) -> str:
        """
        Exchange the browser cookie for a short-lived Clerk JWT.
        Clerk JWTs expire in ~60 seconds — this is called automatically before each request.
        """
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Call Clerk's session endpoint using the cookie for auth
            resp = await client.post(
                f"{CLERK_BASE}/v1/client/sessions/last_active_session/tokens",
                headers={
                    **BROWSER_HEADERS,
                    "Cookie": self.cookie,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"_clerk_js_version": "5.35.1"},
            )

            if resp.status_code == 401:
                raise SunoAuthError(
                    "Cookie is invalid or expired. Please copy a fresh cookie from your browser."
                )
            if resp.status_code != 200:
                raise SunoAuthError(
                    f"Clerk auth failed with status {resp.status_code}: {resp.text[:200]}"
                )

            data = resp.json()
            jwt = data.get("jwt")
            if not jwt:
                raise SunoAuthError("Clerk returned no JWT token. Cookie may be malformed.")

            # Cache the JWT — it expires in ~60s, refresh 10s early
            self._jwt = jwt
            self._jwt_expires_at = time.time() + 50.0
            return jwt

    async def _get_jwt(self) -> str:
        """Return a valid JWT, refreshing if needed."""
        if not self._jwt or time.time() >= self._jwt_expires_at:
            await self._refresh_jwt()
        return self._jwt

    # ─── Core API methods ─────────────────────────────────────────────────────

    async def validate_cookie(self) -> dict:
        """
        Test if the cookie is valid. Returns user info on success.
        Used by the /api/validate-cookie endpoint.
        """
        jwt = await self._get_jwt()
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{SUNO_API_BASE}/api/session/",
                headers={
                    **BROWSER_HEADERS,
                    "Authorization": f"Bearer {jwt}",
                    "Cookie": self.cookie,
                },
            )
            if resp.status_code != 200:
                raise SunoAuthError("Cookie validation failed. Please refresh your cookie.")
            data = resp.json()
            return {
                "valid": True,
                "credits_left": data.get("credits_left", "unknown"),
                "monthly_limit": data.get("monthly_limit", "unknown"),
                "username": data.get("display_name", "unknown"),
            }

    async def generate(
        self,
        title: str,
        lyrics: str,
        style: str,
        model: str = "chirp-v4",
    ) -> list[str]:
        """
        Submit a custom generation request to Suno.
        Returns a list of song IDs (Suno always generates 2 variants).

        Args:
            title:  Song title
            lyrics: Full lyrics with section tags ([Verse], [Chorus], etc.)
            style:  Style descriptor string (e.g. "lo-fi, chill, 85 BPM")
            model:  Suno model version (default: chirp-v4)
        """
        jwt = await self._get_jwt()

        payload = {
            "custom_mode": True,
            "mv": model,
            "input": {
                "prompt": lyrics,
                "tags": style,
                "title": title,
                "make_instrumental": False,
                "infill": False,
                "continue_at": None,
                "continue_clip_id": None,
            },
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{SUNO_API_BASE}/api/generate/v2/",
                headers={
                    **BROWSER_HEADERS,
                    "Authorization": f"Bearer {jwt}",
                    "Cookie": self.cookie,
                    "Content-Type": "application/json",
                },
                json=payload,
            )

            if resp.status_code == 402:
                raise SunoGenerationError(
                    "Insufficient Suno credits. Please top up your account."
                )
            if resp.status_code == 401:
                raise SunoAuthError(
                    "Session expired during generation. Please refresh your cookie."
                )
            if resp.status_code != 200:
                raise SunoGenerationError(
                    f"Suno generation failed ({resp.status_code}): {resp.text[:300]}"
                )

            data = resp.json()
            clips = data.get("clips", [])
            if not clips:
                raise SunoGenerationError("Suno returned no clips. Try again.")

            return [clip["id"] for clip in clips]

    async def get_songs(self, song_ids: list[str]) -> list[dict]:
        """
        Poll Suno for the current status of one or more songs.
        Returns a list of song objects with status, audio_url, etc.

        Poll every 5 seconds until status == 'complete' or 'error'.
        """
        jwt = await self._get_jwt()
        ids_param = ",".join(song_ids)

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{SUNO_API_BASE}/api/feed/",
                params={"ids": ids_param},
                headers={
                    **BROWSER_HEADERS,
                    "Authorization": f"Bearer {jwt}",
                    "Cookie": self.cookie,
                },
            )

            if resp.status_code != 200:
                raise SunoGenerationError(
                    f"Failed to fetch song status ({resp.status_code}): {resp.text[:200]}"
                )

            songs = resp.json()
            return [
                {
                    "id":          s.get("id"),
                    "title":       s.get("title", "Untitled"),
                    "status":      s.get("status", "unknown"),
                    "audio_url":   s.get("audio_url"),
                    "video_url":   s.get("video_url"),
                    "image_url":   s.get("image_url"),
                    "song_url":    f"https://suno.com/song/{s.get('id')}",
                    "duration":    s.get("metadata", {}).get("duration"),
                    "tags":        s.get("metadata", {}).get("tags", ""),
                    "error_msg":   s.get("metadata", {}).get("error_message"),
                }
                for s in songs
            ]
