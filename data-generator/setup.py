from setuptools import setup, find_packages

setup(name='data-generator',
      version='0.1',
      description='data generator for generating stream based on configured interval ',
      long_description=' generate events to ',
      url='https://github.com/vipinkumar7/mvp.git',
      author='Vipin Kumar',
      author_email='vipinkumar.work@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'google-cloud-dataproc', 'google-cloud-monitoring', 'flask==1.1.1', 'cassandra-driver', 'schedule'
      ],
      include_package_data=True,
      zip_safe=False)
