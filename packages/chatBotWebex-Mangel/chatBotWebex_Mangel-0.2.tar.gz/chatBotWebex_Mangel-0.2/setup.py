import setuptools


setuptools.setup(
     name='chatBotWebex_Mangel',  
     version='0.2', 
     scripts=['app.py'] , 
     author="Maycol Angel",
     author_email="mangel@alltic.co", 
     description="Un paquete de comandos para comunicarse con webex", 
     url="https://github.com/Viadd/chatboxWebex_mangel.git",
     packages=setuptools.find_packages(), 
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )