HealthJoy Project
=================


## Steps

- Clone this repo

- Install requirements: `$ pip install -r requirements.txt`

- Update local settings in `settings.py`: 

    `GITHUB_CLIENT_ID` -- From GitHub OAuth. Can be stored in `github_client_id.txt`

    `GITHUB_CLIENT_SECRET` -- From GitHub OAuth. Can be stored in `github_client_secret.txt`

    `GITHUB_REPO_OWNER`

    `GITHUB_REPO_NAME`

- Feel free to disable debug mode.

- Run local server: `python manage.py runserver` (This should run on port 8000)

- Visit the site root `http://localhost:8000/`. Click the `fork` link, login/grant access via github. A success will redirect with a link to the forked repo.


## Running

```bash
(healthjoy) ✔ ~/code/healthjoy/healthjoy [master|●21…8] 
15:39 $ ./manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
June 03, 2021 - 20:41:03
Django version 3.2.3, using settings 'healthjoy.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Sample request logs. In this case the repo being forked is GitHub's Octocat's Hello-World test repo.

```bash
[03/Jun/2021 20:41:56] "GET / HTTP/1.1" 200 307
Not Found: /favicon.ico
[03/Jun/2021 20:42:00] "GET /fork HTTP/1.1" 302 0
[03/Jun/2021 20:42:02] "GET /github/auth/?code=2f7b82188d2535d3e35f HTTP/1.1" 302 0
[03/Jun/2021 20:42:02] "GET /?repo_url=https://github.com/jasonwirth/Hello-World HTTP/1.1" 200 444


```


## Running Tests

Tests can be run with the standard django test runner.

```bash
(healthjoy) ✔ ~/code/healthjoy/healthjoy [master|●21…8] 
15:39 $ ./manage.py test 
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 0.021s

OK
```