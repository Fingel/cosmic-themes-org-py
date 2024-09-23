import logging
import subprocess

from django import forms

from .models import Theme

logger = logging.getLogger(__name__)


def ron_to_css(ron: str) -> str:
    try:
        ron_to_css = subprocess.run(
            "cosmic-theme-tools",
            input=ron,
            capture_output=True,
            text=True,
            check=True,
        )
        ron_css = ron_to_css.stdout
        if not ron_css:
            raise ValueError("CSS is empty")
        return ron_css
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to convert RON to JSON: {e}")


class ThemeForm(forms.ModelForm):
    ron = forms.FileField(label="Theme .ron file")
    challenge = forms.IntegerField(label="What is three plus three?")
    css = ""
    ron_text = ""

    def clean_ron(self):
        ron_file = self.cleaned_data["ron"]
        try:
            self.ron_text = ron_file.read().decode("utf-8")
            self.css = ron_to_css(self.ron_text)
        except (ValueError, UnicodeDecodeError) as e:
            logger.warn("Received invalid RON file: %s", ron_file, exc_info=e)
            raise forms.ValidationError(f"{ron_file} is not a valid RON file.")

        return self.ron_text

    def clean_challenge(self):
        answer = self.cleaned_data["challenge"]
        if answer != 6:
            raise forms.ValidationError("Begone bot")
        return answer

    def save(self, *args, **kwargs):
        theme = super().save(commit=False)
        theme.css = self.css
        theme.ron = self.ron_text
        theme.red, theme.green, theme.blue = theme.accent_color(self.css)
        theme.save()
        return theme

    class Meta:
        model = Theme
        fields = ["name", "author", "link"]
