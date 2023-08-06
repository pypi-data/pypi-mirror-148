from setuptools import setup

setup(
    name         = 'pygments-style-kit',
    version      = '0.4',
    maintainer   = "Jakob Jarebica",
    maintainer_email = "jakob.jarebica@student.kit.edu",
    install_requires = ['pygments'],
    packages     = ['pygments-style-kit'],
    url          = "https://kit.edu",
    entry_points = '''
    [pygments.styles]
    kitdark = kitdark:KitdarkStyle
    '''
)
