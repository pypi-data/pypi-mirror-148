from setuptools import setup

setup(
    name = 'sjm_tools',
    author = 'Jianheng Liu',
    author_email='jhfoxliu@gmail.com',
    url="https://github.com/sysuliujh/Bioinfo-toolkit/tree/master/sjm_tools",
    project_urls={
    },
    description = 'A wraper for SJM',
    version = '1.0',
    packages = ["sjm_tools"],
    license = "MIT",
    scripts=[],
    python_requires=">=2",
    install_requires = [
      "numpy"
    ],
    entry_points={'console_scripts': ['qsjm = sjm_tools.qsjm:main']},
    package_data={"sjm_tools": ["example/*", 'utils/*']},

)