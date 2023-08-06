import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="lytorch",
  version="0.0.1",
  author="kamilu",
  author_email="luzhixing12345@163.com",
  description="my implementation of pytorch",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/luzhixing12345/mytorch",
  package_dir={'': 'lytorch'},
  packages=setuptools.find_packages(where='lytorch'),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)