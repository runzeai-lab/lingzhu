"""
灵助 SDK - Python SDK 安装配置（V185.0）
Lingzhu SDK - Python SDK Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lingzhu-sdk",
    version="185.0.0",
    author="灵助 Lingzhu",
    author_email="lingzhu@wuweixin.com",
    description="灵助 SDK - 缓存感知调度器、边缘推理适配器、三进制逻辑仿真",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lingzhu/lingzhu-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status : : 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic : : Software Development :: Libraries :: Python Modules",
        "License : : MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 无外部依赖（纯Python实现）
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    include_package_data=True,
    package_data={
        "lingzhu_sdk": ["py.typed"],
    },
    keywords="lingzhu sdk, cache, edge inference, ternary logic, hexagram",
    project_urls={
        "Bug Reports": "https://github.com/lingzhu/lingzhu-sdk/issues",
        "Source": "https://github.com/lingzhu/lingzhu-sdk",
    },
)