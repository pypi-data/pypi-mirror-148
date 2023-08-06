from setuptools import setup

setup(
    name         = 'pygments-style-kit',
    version      = '0.5',
    maintainer   = "Jakob Jarebica",
    maintainer_email = "jakob.jarebica@student.kit.edu",
    install_requires = ['pygments'],
    packages     = ['pygments_style_kit'],
    url          = "https://kit.edu",
    entry_points = '''
    [pygments.styles]
    kitdark = pygments_style_kit.kitdark:KitdarkStyle
    '''
)
