from setuptools import setup

setup(
    name         = 'pygments-style-kit',
    version      = '1.0.1',
    maintainer   = "Jakob Jarebica",
    maintainer_email = "jakob.jarebica@student.kit.edu",
    install_requires = ['pygments'],
    packages     = ['pygments_style_kit'],
    url          = "https://gitlab.com/mee02/pygments-style-kit",
    entry_points = '''
    [pygments.styles]
    kitdark = pygments_style_kit.kitdark:KitdarkStyle
    '''
)
