# https://packaging.python.org/en/latest/tutorials/packaging-projects/
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="earthquake-news-indonesia",
    version="0.1",
    author="Warfire-AFF",
    author_email="a.fauzanfarhan@gmail.com",
    description="This package will get the latest detection news of earthquake in indonesia from site bmkg.go.id",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TalentMastery/bundling-package-to-pypi",
    project_urls={
        "Website": "http://code-warfire.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
