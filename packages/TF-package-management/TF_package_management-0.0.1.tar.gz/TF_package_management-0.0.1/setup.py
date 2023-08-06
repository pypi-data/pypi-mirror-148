import setuptools

setuptools.setup(
    name='TF_package_management',
    version='0.0.1',
    auther='Jesper Thoft Illemann Jæger',
    author_email='jesperjag86@gmail.com',
    description='package manegement system on github',
    url='https://github.com/JesperJager1986/testing_package_management',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
