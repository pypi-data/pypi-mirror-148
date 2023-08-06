from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = 'ruishi'
AUTHOR = 'Peng1013'
DESCRIPTION = '睿视接口的封装'
URL = 'https://github.com/911061873/ruishi'
EMAIL = 'qinpeng@peng1013.cn'
REQUIRES_PYTHON = '>=3.10.0'

REQUIRED = [
    'httpx', 'pydantic'
]


def get_version() -> str:
    with open(f'./{NAME}/__init__.py') as f:
        for line in f.readlines():
            if line.startswith('version'):
                _version = [i.strip() for i in line.split('=')[1].strip().strip('()').split(',')]
                _version = '.'.join(_version)
        return _version


setup(
    name=NAME,
    version=get_version(),
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={
        "Bug Tracker": f"{URL}/issues",
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages(),
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
)
