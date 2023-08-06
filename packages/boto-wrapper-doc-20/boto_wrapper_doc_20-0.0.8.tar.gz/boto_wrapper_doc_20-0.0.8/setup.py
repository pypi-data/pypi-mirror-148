import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boto_wrapper_doc_20",
    # Replace with your own username above
    version="0.0.8",
    author="Rushikesh Darshane",
    author_email="x20231580@student.ncirl.ie",
    description="Simple wrapper over boto3 client for S3, Cognito and SNS clients",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdarshane/boto-wrapper-doc",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=['boto3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)