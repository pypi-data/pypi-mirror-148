import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
##with open('requirements.txt') as f:
##    required_package = f.read().splitlines()
    
PROJECT_NAME = "odcommonapp"
USER_NAME = "thangarajdeivasikamani"

setuptools.setup(
    name=f"{PROJECT_NAME}",
    version="0.0.5",
    author=USER_NAME,
    author_email="Thangarajerode@gmail.com",
    description="Object detection common framework application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires= ['Cython==0.29.28', 'Flask==2.0.3', 'Flask-Cors==3.0.10','Keras-Preprocessing==1.1.2', 'matplotlib==3.3.4', 'numpy==1.19.5', 'opencv-python==4.5.5.64', 'Pillow==8.4.0', 'proto-plus==1.20.3', 'protobuf==3.19.4', 'pyarrow==6.0.1', 'tensorflow==2.5.0', 'tensorflow-estimator==2.5.0', 'termcolor==1.1.0','zipp==3.6.0', 'wget==3.2',  'torch==1.10.1', 'torchvision==0.11.2', 'torchaudio==0.10.1', 'cloudpickle', 'omegaconf', 'pycocotools-windows', 'fvcore', 'seaborn>=0.11.0', 'youtube_dl']
)
