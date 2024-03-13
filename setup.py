from setuptools import setup

VERSION_NUMBER = "1.1.0"

# Load the README file as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="pytest-ai1899",
      version=VERSION_NUMBER,
      description="pytest plugin for connecting to ai1899 smart system stack",
      long_description=long_description,  # Add the long_description field here
      long_description_content_type="text/markdown",  # Specify the content type
      include_package_data=True,
      author="Mor Dabastany",
      url="https://github.com/Formartha/pytest-ai1899",
      packages=["pytest_ai1899"],
      package_data={"pytest_ai1899": ["*"]},
      entry_points={"pytest11": ["dependency = pytest_ai1899.plugin"]},
      install_requires=["requests"],
      license="MIT",
      keywords="pyest-ai1899",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Framework :: Pytest",
          "Intended Audience :: Developers",
          "Operating System :: POSIX",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: MacOS :: MacOS X",
          "Topic :: Software Development :: Quality Assurance",
          "Topic :: Software Development :: Testing",
          "Programming Language :: Python :: 3.11",
      ])
