import os


class Config:
    _vals = {}

    @classmethod
    def get(cls, key, default=None):
        if key in cls._vals:
            return cls._vals[key]
        if default is not None:
            return default
        raise KeyError(f'Variable {key} is not set')

    @classmethod
    def setup(cls, **kwargs):
        for key, val in kwargs.items():
            cls._vals[key] = val


Config.setup(
    riot_dev_api_key=os.environ.get('RIOT_DEV_API_KEY')
)
