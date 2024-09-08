# cosmic-themes.org
This is the sourcecode for [cosmic-themes.org](https://cosmic-themes.org). No, it is not written in Rust (yet).

## Theme modification requests

If you uploaded a theme but want it removed or changes, please
[open an issue](https://github.com/Fingel/cosmic-themes-org-py/issues).

## Building

This is a very vanilla Django project. I recommend using [uv](https://astral.sh/uv) to
build and run:

```sh
    uv run manage.py migrate && uv run manage.py runserver
```

should be enough to get the site up and running locally. Pull requests welcome!


Note that for now, a binary built from [cosmic-theme-tools](https://github.com/Fingel/cosmic-theme-tools) must be
available somewhere on the $PATH to successfully parse .ron files during theme upload.


