from botoy import ctx, S, mark_recv
import secrets, re, httpx


def githubasset(owner, repo, type=None, flag=None):
	url = (
		f"https://opengraph.githubassets.com/{secrets.token_urlsafe(16)}/{owner}/{repo}"
	)
	if type:
		return f"{url}/{type}/{flag}"
	return url


async def github():
	if m := ctx.group_msg:
		matched = re.match(
			r"^(?P<owner>[a-zA-Z0-9][a-zA-Z0-9\-]*)/" r"(?P<repo>[a-zA-Z0-9_\-]+).*$",
			m.text,
		)
		found = re.findall(
			r"github\.com/([a-zA-Z0-9][a-zA-Z0-9\-]*)/([a-zA-Z0-9_\-]+)", m.text
		)
		if matched:
			owner, repo = matched["owner"], matched["repo"]
		elif found:
			owner, repo = found[0][0], found[0][1]
		else:
			return

		# process commit/issues/pull
		try:
			type, flag = re.findall(
				r"/(commit|issues|pull)/([a-zA-Z0-9_\-]+)", ctx.Content
			)[0]
		except Exception:
			type = flag = None

		try:
			resp = httpx.get(f"https://api.github.com/repos/{owner}/{repo}", timeout=20)
			resp.raise_for_status()
		except Exception:
			pass
		else:
			await S.image(githubasset(owner, repo, type, flag))


mark_recv(github, author='Lord2333', name="Github缩略图", usage='发送github项目链接自动渲染缩略图')
