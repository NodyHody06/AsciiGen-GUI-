import nuitka

nuitka.build(
    module_name='main',
    output_dir='dist',
    standalone=True,
    recurse_all=True,
    entry_point='main.py'
)
