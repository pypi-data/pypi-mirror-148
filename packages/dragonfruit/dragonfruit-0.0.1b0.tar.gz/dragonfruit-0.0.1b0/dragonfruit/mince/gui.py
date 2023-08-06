try:
    import mincepy_gui
except ImportError:
    # Protect environments that don't have mincepy gui installed from excepting
    __all__ = tuple()
else:
    from typing import Iterable, Optional

    import ase.visualize
    from ase.io.formats import ioformats
    from ase.io import read as ase_read

    import mincepy

    from dragonfruit import get_visualizable

    __all__ = ("AtomsActioner", "AtomsFileViewer")

    class AtomsActioner(mincepy_gui.Actioner):
        def probe(self, obj, context) -> Optional[Iterable[str]]:
            try:
                visualizable = get_visualizable(obj)
            except TypeError:
                return None

            if isinstance(visualizable, ase.Atoms):  # pylint: disable=no-member
                return ("View Atoms",)
            return ("Visualize",)

        def do(self, action, obj, context):
            ase.visualize.view(get_visualizable(obj))  # pylint: disable=no-member

    class AtomsFileViewer(mincepy_gui.Actioner):

        ase_format = None

        def probe(self, obj, context) -> Optional[Iterable[str]]:
            if isinstance(obj, mincepy.File):
                for fmt in ioformats.values():
                    if fmt.match_name(obj.filename):
                        self.ase_format = fmt.name
                        return ("View File as Atoms",)

            return None

        def do(self, action, obj, context):
            with obj.open() as file:
                images = ase_read(file, format=self.ase_format, index=":")
            if not images:
                # Images is empty, what to do
                msg = "No Atoms objects in file. Is it incomplete?"
                raise ValueError(msg)
            ase.visualize.view(images)  # pylint: disable=no-member

    def get_actioners():
        return (AtomsActioner(), AtomsFileViewer())
