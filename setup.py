from setuptools import setup, find_packages

setup(
    name="project-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.0",
        "requests==2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'project-analyzer=analyzer:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing project structure and getting architectural insights from Claude AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/project-analyzer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
) 