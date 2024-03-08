from setuptools import setup

VERSION_NUMBER = "1.0.0"

with open("requirements.txt", "r") as req:
    REQUIREMENTS = req.readlines()


setup(name="pytest-ai1899",
      version=VERSION_NUMBER,
      description="pytest plugin for connecting to ai1899 smart system stack",
      include_package_data=True,
      author="Mor Dabastany",
      url="https://github.com/Formartha/pytest-ai1899",
      packages=["pytest_ai1899"],
      package_data={"pytest_ai1899": ["*"]},
      entry_points={"pytest11": ["dependency = pytest_ai1899.plugin"]},
      install_requires=REQUIREMENTS,
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
