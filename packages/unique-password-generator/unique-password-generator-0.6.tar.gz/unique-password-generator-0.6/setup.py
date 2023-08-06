#
# import setuptools
#
# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
#
# setuptools.setup(
#     name="easy-password-generator",
#     version="0.0.7",
#     author="Sonia Ghongadi",
#     author_email="author@example.com",
#     description="A powerful but simple to use strong password generation library",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/soniaghongadi/password-generator",
#     py_modules=['easy_password_generator'],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )

#---------prathistha----------

import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="suggest_passwords",
#     version="1.0.0",
#     author="Prathista Santhosh Kumar Shetty",
#     author_email="prathista1995@gmail.com",
#     description="Suggests an automatic password for the user",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/PrathistaS/password_suggestion",
#     py_modules=['password_suggestions'],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.7'

from setuptools import setup, find_packages
setup(
    name='unique-password-generator',
    version='0.6',
    license='MIT',
    author="Prathista Santhosh Kumar Shetty",
    author_email='prathista1995@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/PrathistaS/password_suggestion',
    keywords='password genrator',


)