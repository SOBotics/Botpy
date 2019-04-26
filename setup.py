from distutils.core import setup

setup (
    name = "BotpySE",
    packages = ["BotpySE"],
    version = "0.7.7",
    description = "A python framework to create chatbots on the StackExchange network.",
    author = "Ashish Ahuja",
    author_email = "ashish.ahuja@sobotics.org",
    url = "https://github.com/SOBotics/Botpy",
    install_requires=['chatexchange', 'tabulate', 'jsonpickle', 'pyRedunda']
)
