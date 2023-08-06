import setuptools 

with open("README.md", "r", encoding="utf-8") as fh: 
   long_description = fh.read()

setuptools.setup(
   name = "Datamics-demo-pkg-042022",
   version = "1.1",
   author = "Saumya",
   author_email = "saumya.goyal@datamics.com",
   description = "A small example package",
   long_description = long_description,
   long_description_content_type = "text/markdown",
   url = "https://github.com/saumyagoyal95/OSC_PYPI",
   project_urls = {
      "Bug Tracker": "https://github.com/saumyagoyal95/OSC_PYPI/issues"
   },
   classifiers = [
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   package_dir = {"": "src"},
   packages = setuptools.find_packages(where = "src"),
   python_requires = ">=3.6", 
) 