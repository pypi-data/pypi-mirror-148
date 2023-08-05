import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="otl",
  version="0.0.2",
  author="waqu",
  author_email="author@example.com",
  description="A ops tools package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)