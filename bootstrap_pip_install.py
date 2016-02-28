import pip

for package in ["pyyaml", "requests", "jinja2"]:
    pip.main(['install', package])

