# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Setup Configuration
# ═══════════════════════════════════════════════════════════════

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="geo-protection-bot",
    version="1.0.0",
    author="iMumd",
    author_email="iMumd@example.com",
    description="Powerful Telegram protection bot with multi-language support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iMumd/Geo",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "geo-bot=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)