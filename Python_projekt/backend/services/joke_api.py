import json
from json import JSONDecodeError
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


JOKE_API_BASE_URL = "https://v2.jokeapi.dev/joke/Any"

MOOD_FILTERS: dict[str, dict[str, str]] = {
	"happy": {"blacklistFlags": "nsfw,religious,political,racist,sexist,explicit"},
	"sad": {"blacklistFlags": "nsfw,political,racist,sexist,explicit"},
	"angry": {"blacklistFlags": "nsfw,religious,political,sexist,explicit"},
	"stressed": {"blacklistFlags": "nsfw,political,racist,sexist,explicit"},
	"neutral": {"blacklistFlags": "nsfw,religious,political,racist,sexist,explicit"},
}


class JokeAPIError(RuntimeError):
	pass


def normalize_mood(mood):
	if not mood:
		return "neutral"
	normalized = mood.strip().lower()
	if normalized in MOOD_FILTERS:
		return normalized
	return "neutral"


def build_joke_api_url(mood=None):
	query_params = {"safe-mode": ""}
	query_params.update(MOOD_FILTERS[normalize_mood(mood)])
	return f"{JOKE_API_BASE_URL}?{urlencode(query_params)}"


def _extract_joke_text(payload):
	joke_type = payload.get("type")
	if joke_type == "single":
		return str(payload.get("joke", ""))

	setup = str(payload.get("setup", ""))
	delivery = str(payload.get("delivery", ""))
	if setup and delivery:
		return f"{setup} {delivery}"
	return setup or delivery or ""


def fetch_joke(mood=None):
	try:
		with urlopen(build_joke_api_url(mood), timeout=10) as response:
			raw_payload = response.read().decode("utf-8")
	except URLError as exc:
		raise JokeAPIError("Nie udalo sie pobrac zartu") from exc

	try:
		payload = json.loads(raw_payload)
	except JSONDecodeError as exc:
		raise JokeAPIError("Zly format odpowiedzi z JokeAPI") from exc

	if payload.get("error"):
		raise JokeAPIError("JokeAPI zwrocil blad")

	joke_text = _extract_joke_text(payload).strip()
	if not joke_text:
		raise JokeAPIError("Brak zartu w odpowiedzi")

	return {
		"joke": joke_text,
		"mood": normalize_mood(mood),
		"category": str(payload.get("category") or ""),
	}
