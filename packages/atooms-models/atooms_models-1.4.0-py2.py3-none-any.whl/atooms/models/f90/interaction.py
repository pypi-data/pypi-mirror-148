import numpy

from atooms.system.interaction import InteractionBase
from .helpers import _merge_source, _normalize_path
import f2py_jit


def _check_polydisperse(species, radius):
    """Check whether system is polydisperse"""
    # Make sure all species are identical
    poly = False
    tolerance = 1e-15
    if numpy.all(species == species[0]):
        delta = abs(radius.min() - radius.max())
        if delta > tolerance * radius.mean():
            poly = True
    return poly


class Interaction(InteractionBase):

    def __init__(self, model, neighbor_list=None,
                 interaction='interaction.f90', helpers='helpers.f90',
                 inline=True, inline_safe=False, debug=False,
                 parallel=False):
        """
        The interaction model can be defined:

        1) Passing a `model` string that matches any of the models
        defined in the atooms-models database (ex. "lennard_jones" or
        "gaussian_core")

        2) Passing a `model` dictionary with "potential" and "cutoff"
        keys and identical layout as the atooms-model database entries
        (ex. https://framagit.org/atooms/models/blob/master/atooms/models/lennard_jones.json)

        The parameters values are provided as dictionaries
        (`potential_parameters` and `cutoff_parameters``) matching the
        intent(in) variables entering the `setup()` routines of the
        fortran modules.
        """
        InteractionBase.__init__(self)
        self.neighbor_list = neighbor_list
        self.order = 'F'
        self.observable.append('gradw')
        self.variables = {'box': 'cell.side:float64',
                          'pos': 'particle.position:float64',
                          'ids': 'particle.species:int32',
                          'rad': 'particle.radius:float64'}

        if not hasattr(model, 'get'):
            # This may be a string, so we look for the model in the
            # atooms-models database and replace the string with the dictionary
            from atooms import models
            model = models.get(model)

        # At this stage we expect a model dictionary
        assert len(model.get('potential')) == 1
        assert len(model.get('cutoff')) == 1
        # Normalize paths
        for entry in model["potential"] + model["cutoff"]:
            if "path" not in entry:
                entry["path"] = _normalize_path(entry.get("type"))

        potential = model.get('potential')[0].get('path')
        potential_parameters = model.get('potential')[0].get('parameters')
        cutoff = model.get('cutoff')[0].get('path')
        cutoff_parameters = model.get('cutoff')[0].get('parameters')

        potential = _normalize_path(potential)
        cutoff = _normalize_path(cutoff)

        self.model = model
        self._module_path = None

        # Merge all sources into a unique source blob
        source = _merge_source(helpers, potential, cutoff, interaction)

        # Inline subroutines
        if inline:
            from f2py_jit.finline import inline_source
            # TODO: depending on f2py-jit version we can inline compute and smooth as well but this should be checked for bacward compatibility
            if inline_safe:
                source = inline_source(source, ignore='compute,smooth,tailor,forces')
            elif inline:
                source = inline_source(source, ignore='tailor,forces')

        # Compile and bundle the module with f2py
        args = ''
        opt_args = '-ffree-form -ffree-line-length-none'
        if debug:
            opt_args += ' -O3 -pg -fbounds-check'
        else:
            opt_args += ' -O3 -ffast-math'
        if parallel:
            opt_args += ' -fopenmp'
            args += ' -lgomp'
        extra_args = '--opt="{}" {}'.format(opt_args, args)

        # Build a unique module.
        # Every model with its own parameter combination corresponds to a unique module
        # and can be safely reused (up to changes in interaction / helpers)
        uid = f2py_jit.build_module(source,
                                    metadata={"interaction": interaction,
                                              "helpers": helpers,
                                              "parallel": parallel,
                                              "potential": [potential, potential_parameters],
                                              "cutoff": [cutoff, cutoff_parameters]},
                                    extra_args=extra_args)

        # Setup potential and cutoff parameters
        _interaction = f2py_jit.import_module(uid)
        _interaction.potential.setup(**potential_parameters)
        _interaction.cutoff.setup(**cutoff_parameters)

        # Store module name (better not store the module itself, else we cannot deepcopy)
        self._uid = uid

        # Cache for polydisperse system
        self._polydisperse = None

    def compute(self, observable, box, pos, ids, rad):
        """
        Compute `observable` from this interaction
        """
        # Check if system is polydisperse (cached)
        if self._polydisperse is None:
            self._polydisperse = _check_polydisperse(ids, rad)
        if self.neighbor_list is None:
            self._compute(observable, box, pos, ids, rad)
        else:
            self._compute_with_neighbors(observable, box, pos, ids)

    def _compute(self, observable, box, pos, ids, rad):
        # One way to refactor these spaghetti is by having interaction.forces() accept radii even if it not used
        # This way we can swap the module because the interface is the same
        _interaction = f2py_jit.import_module(self._uid)
        if observable in ['forces', 'energy', None]:
            if self.forces is None:
                self.forces = numpy.zeros_like(pos, order='F')
            if not self._polydisperse:
                self.energy, self.virial = _interaction.interaction.forces(box, pos, ids, self.forces)
            else:
                self.energy, self.virial = _interaction.interaction_polydisperse.forces(box, pos, ids, rad, self.forces)

        elif observable == 'gradw':
            if not hasattr(self, 'gradw'):
                self.gradw = numpy.zeros_like(pos, order='F')
            if not self._polydisperse:
                _interaction.interaction.gradw(box, pos, ids, self.gradw)
            else:
                _interaction.interaction_polydisperse.gradw(box, pos, ids, rad, self.gradw)

        elif observable == 'hessian':
            ndim, N = pos.shape
            if self.hessian is None:
                self.hessian = numpy.ndarray((ndim, N, ndim, N), order='F')
            if not self._polydisperse:
                _interaction.interaction.hessian(box, pos, ids, self.hessian)
            else:
                _interaction.interaction_polydisperse.hessian(box, pos, ids, rad, self.hessian)

    def _compute_polydisperse(self, observable, box, pos, ids, rad):
        _interaction = f2py_jit.import_module(self._uid)
        if observable in ['forces', 'energy', None]:
            if self.forces is None:
                self.forces = numpy.zeros_like(pos, order='F')
            self.energy, self.virial = _interaction.interaction.forces(box, pos, ids, self.forces)

        elif observable == 'gradw':
            if not hasattr(self, 'gradw'):
                self.gradw = numpy.zeros_like(pos, order='F')
            _interaction.interaction.gradw(box, pos, ids, self.gradw)

        elif observable == 'hessian':
            ndim, N = pos.shape
            if self.hessian is None:
                self.hessian = numpy.ndarray((ndim, N, ndim, N), order='F')
            _interaction.interaction.hessian(box, pos, ids, self.hessian)

    def _compute_with_neighbors(self, observable, box, pos, ids):
        f90 = f2py_jit.import_module(self._uid)
        if observable in ['forces', 'energy', None]:
            if self.forces is None:
                self.forces = numpy.zeros_like(pos, order='F')
            # TODO: rcut
            self.neighbor_list.adjust(box, pos, f90.cutoff.rcut_)
            self.neighbor_list.compute(box, pos, ids)
            self.energy, self.virial = f90.interaction_neighbors.forces(box, pos, ids,
                                                                        self.neighbor_list.neighbors,
                                                                        self.neighbor_list.number_of_neighbors,
                                                                        self.forces)

        elif observable == 'gradw':
            if not hasattr(self, 'gradw'):
                self.gradw = numpy.zeros_like(pos, order='F')
            raise ValueError('gradw not implemented with neighbors')

        elif observable == 'hessian':
            ndim, N = pos.shape
            if self.hessian is None:
                self.hessian = numpy.ndarray((ndim, N, ndim, N), order='F')
            f90.interaction_neighbors.hessian(box, pos, ids,
                                              self.neighbor_list.neighbors,
                                              self.neighbor_list.number_of_neighbors,
                                              self.hessian)
