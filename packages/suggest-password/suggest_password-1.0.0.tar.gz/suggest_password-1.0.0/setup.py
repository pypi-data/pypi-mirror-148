import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="suggest_password",
    version="1.0.0",
    author="Prathista Santhosh Kumar Shetty",
    author_email="prathista1995@gmail.com",
    description="Suggests an automatic password for the user",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrathistaS/password_suggestion",
    py_modules=['password_suggestions'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)