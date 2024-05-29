from pyprojroot import here
import toml

secrets_pth = here(".secrets.toml")
secrets = toml.load(secrets_pth)
APP_TOKEN = secrets["datastax"]["app-token"]



