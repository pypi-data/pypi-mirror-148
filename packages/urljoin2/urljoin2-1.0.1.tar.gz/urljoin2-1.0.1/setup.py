from setuptools import setup, find_packages


def main():
    setup(
          name="urljoin2",
          version="1.0.1",
          description="Module for joining strings to form urls.",
          author="Nagy Zoltán",
          author_email="zolika3400@gmail.com",
          packages=find_packages('src'),
          package_dir={'': 'src'}
          )

if __name__ == "__main__":
    main()
