import setuptools

setuptools.setup(name='upbitbox', # 프로젝트 이름
      version='0.0.1', # 프로젝트 버전
      url='https://github.com/DK-Lite/upbitbox.git', # 프로젝트 주소
      author='dk-lite', # 작성자
      author_email='kdk5go@gmail.com', # 작성자 이메일
      description='python wrapper for Upbit', # 간단한 설명
      packages=setuptools.find_packages(),  # 기본 프로젝트 폴더 외에 추가로 입력할 폴더
      long_description=open('README.md').read(), # 프로젝트 설명, 보통 README.md로 관리
      long_description_content_type="text/markdown",
      install_requires=[
            'requests',
            'pandas',
            'PyJWT',
            'PyYAML',
      ], # 설치시 설치할 라이브러리
      python_requires='>=3.6'
)