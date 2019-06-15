"""Electron-electron repulsion integral."""
from gbasis.base_four_symm import BaseFourIndexSymmetric
from gbasis.contractions import GeneralizedContractionShell
from gbasis.integrals._two_elec_int import (
    _compute_two_elec_integrals,
    _compute_two_elec_integrals_angmom_zero,
)
from gbasis.integrals.point_charge import PointChargeIntegral
import numpy as np


class ElectronRepulsionIntegral(BaseFourIndexSymmetric):
    """Class for constructing electron-electron repulsion integrals.

    The first four axes of the returned array is associated with the given set of contracted
    Gaussian (or a linear combination of a set of Gaussians).

    Attributes
    ----------
    _axes_contractions : tuple of tuple of GeneralizedContractionShell
        Sets of contractions associated with each axis of the array.

    Properties
    ----------
    contractions : tuple of GeneralizedContractionShell
        Contractions that are associated with the first and second indices of the array.

    Methods
    -------
    __init__(self, contractions)
        Initialize.
    construct_array_contraction(self, cont1, cont2, cont3, cont4) :
    np.ndarray(M_1, L_cart_1, M_2, L_cart_2, M_3, L_cart_3, M_4, L_cart_4)
        Return the electron-electron repulsion integrals associated with a
        `GeneralizedContractionShell` instances.
        `M_1` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the first index.
        `L_cart_1` is the number of Cartesian contractions for the given angular momentum associated
        with the first index.
        `M_2` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the second index.
        `L_cart_2` is the number of Cartesian contractions for the given angular momentum associated
        with the second index.
        `M_3` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the third index.
        `L_cart_3` is the number of Cartesian contractions for the given angular momentum associated
        with the third index.
        `M_4` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the fourth index.
        `L_cart_4` is the number of Cartesian contractions for the given angular momentum associated
        with the fourth index.
        Note that the integrals are in Chemists' notation.
    construct_array_cartesian(self) : np.ndarray(K_cart, K_cart, K_cart, K_cart)
        Return the electron-electron repulsion integrals associated with Cartesian Gaussians.
        `K_cart` is the total number of Cartesian contractions within the instance.
        Note that the integrals are in Chemists' notation.
    construct_array_spherical(self) : np.ndarray(K_sph, K_sph, K_sph, K_sph)
        Return the electron-electron repulsion integrals associated with spherical Gaussians (atomic
        orbitals).
        `K_sph` is the total number of spherical contractions within the instance.
        Note that the integrals are in Chemists' notation.
    construct_array_mix(self, coord_types) : np.ndarray(K_cont, K_cont, K_cont, K_cont)
        Return the electron-electron repulsion integrals associated with all of the contraction in
        the given coordinate system.
        `K_cont` is the total number of contractions within the given basis set.
        Note that the integrals are in Chemists' notation.
    construct_array_lincomb(self, transform, coord_type) :
    np.ndarray(K_orbs, K_orbs, K_orbs, K_orbs)
        Return the electron-electron repulsion integrals associated with linear combinations of
        contractions in the given coordinate system.
        `K_orbs` is the number of basis functions produced after the linear combinations.
        Note that the integrals are in Chemists' notation.

    """

    boys_func = PointChargeIntegral.boys_func

    @classmethod
    def construct_array_contraction(cls, cont_one, cont_two, cont_three, cont_four):
        r"""Return electron-electron repulsion interaction integral for the given contractions.

        Parameters
        ----------
        cont_one : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the first index of
            the array.
        cont_two : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the second index of
            the array.
        cont_three : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the third index of
            the array.
        cont_four : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the fourth index of
            the array.

        Returns
        -------
        array_cont : np.ndarray(M_1, L_cart_1, M_2, L_cart_2, M_3, L_cart_3, M_4, L_cart_4)
            Electron-electron repulsion integral associated with the given instances of
            GeneralizedContractionShell.
            First axis corresponds to the segmented contraction within `cont1`. `M_1` is the number
            of segmented contractions with the same exponents (and angular momentum) associated with
            the first index.
            Second axis corresponds to the angular momentum vector of the `cont1`.`L_cart_1` is the
            number of Cartesian contractions for the given angular momentum associated with the
            first index.
            Third axis corresponds to the segmented contraction within `cont2`. `M_2` is the number
            of segmented contractions with the same exponents (and angular momentum) associated with
            the second index.
            Fourth axis corresponds to the angular momentum vector of the `cont2`.`L_cart_2` is the
            number of Cartesian contractions for the given angular momentum associated with the
            second index.
            Fifth axis corresponds to the segmented contraction within `cont3`. `M_3` is the number
            of segmented contractions with the same exponents (and angular momentum) associated with
            the third index.
            Sixth axis corresponds to the angular momentum vector of the `cont3`.`L_cart_3` is the
            number of Cartesian contractions for the given angular momentum associated with the
            third index.
            Seventh axis corresponds to the segmented contraction within `cont4`. `M_4` is the
            number of segmented contractions with the same exponents (and angular momentum)
            associated with the fourth index.
            Eighth axis corresponds to the angular momentum vector of the `cont4`.`L_cart_4` is the
            number of Cartesian contractions for the given angular momentum associated with the
            fourth index.
            Integrals are in Chemists' notation, i.e. `cont1` and `cont2` are associated with the
            coordinate :math:`\mathbf{r}_1` and `cont3` and `cont4` are associated with coordinate
            :math:`\mathbf{r}_2`.

        Raises
        ------
        TypeError
            If `contractions_one` is not a GeneralizedContractionShell instance.
            If `contractions_two` is not a GeneralizedContractionShell instance.
            If `contractions_three` is not a GeneralizedContractionShell instance.
            If `contractions_four` is not a GeneralizedContractionShell instance.

        Notes
        -----
        The integrals are in Chemists' notation. This means that all of `construct_array_cartesian`,
        `construct_array_spherical`, `construct_array_mix`, and `construct_array_lincomb` are in
        Chemists' notation. To use Physicists' notation instead, see `electron_repulsion_cartesian`,
        `electron_repulsion_spherical`, `electron_repulsion_mix`, and `electron_repulsion_lincomb`,
        respectively.

        """
        # pylint: disable=R0914

        if not isinstance(cont_one, GeneralizedContractionShell):
            raise TypeError("`cont_one` must be a GeneralizedContractionShell instance.")
        if not isinstance(cont_two, GeneralizedContractionShell):
            raise TypeError("`cont_two` must be a GeneralizedContractionShell instance.")
        if not isinstance(cont_three, GeneralizedContractionShell):
            raise TypeError("`cont_three` must be a GeneralizedContractionShell instance.")
        if not isinstance(cont_four, GeneralizedContractionShell):
            raise TypeError("`cont_four` must be a GeneralizedContractionShell instance.")

        # TODO: we can probably swap the contractions to get the optimal time or memory usage
        if cont_one.angmom == cont_two.angmom == cont_three.angmom == cont_four.angmom == 0:
            integrals = _compute_two_elec_integrals_angmom_zero(
                cls.boys_func,
                cont_one.coord,
                cont_one.exps,
                cont_one.coeffs,
                cont_two.coord,
                cont_two.exps,
                cont_two.coeffs,
                cont_three.coord,
                cont_three.exps,
                cont_three.coeffs,
                cont_four.coord,
                cont_four.exps,
                cont_four.coeffs,
            )
        else:
            integrals = _compute_two_elec_integrals(
                cls.boys_func,
                cont_one.coord,
                cont_one.angmom,
                cont_one.angmom_components_cart,
                cont_one.exps,
                cont_one.coeffs,
                cont_two.coord,
                cont_two.angmom,
                cont_two.angmom_components_cart,
                cont_two.exps,
                cont_two.coeffs,
                cont_three.coord,
                cont_three.angmom,
                cont_three.angmom_components_cart,
                cont_three.exps,
                cont_three.coeffs,
                cont_four.coord,
                cont_four.angmom,
                cont_four.angmom_components_cart,
                cont_four.exps,
                cont_four.coeffs,
            )
        integrals = np.transpose(integrals, (4, 0, 5, 1, 6, 2, 7, 3))

        # TODO: if we swap the contractions, we need to unswap them here

        return integrals


def electron_repulsion_integral(
    basis, transform=None, coord_type="spherical", notation="physicist"
):
    """Return the electron repulsion integrals fo the given basis set.

    Parameters
    ----------
    basis : list/tuple of GeneralizedContractionShell
        Shells of generalized contractions.
    transform : np.ndarray(K, K_cont)
        Transformation matrix from the basis set in the given coordinate system (e.g. AO) to linear
        combinations of contractions (e.g. MO).
        Transformation is applied to the left, i.e. the sum is over the index 1 of `transform`
        and index 0 of the array for contractions.
        Default is no transformation.
    coord_type : {"cartesian", list/tuple of "cartesian" or "spherical", "spherical"}
        Types of the coordinate system for the contractions.
        If "cartesian", then all of the contractions are treated as Cartesian contractions.
        If "spherical", then all of the contractions are treated as spherical contractions.
        If list/tuple, then each entry must be a "cartesian" or "spherical" to specify the
        coordinate type of each GeneralizedContractionShell instance.
        Default value is "spherical".
    notation : {"physicist", "chemist"}
        Convention with which the integrals are ordered.
        Default is Physicists' notation.

    Returns
    -------
    array : np.ndarray(K, K, K, K)
        Electron-electron repulsion integral of the given basis set.
        If keyword argument `transform` is provided, then the integrals will be transformed
        accordingly.
        Dimensions 0, 1, 2, and 3 of the array are associated with the basis functions in the basis
        set.
        `K` is the total number of basis functions in the basis set.

    Raises
    ------
    ValueError
        If `notation` is not one of "physicist" or "chemist".

    """
    if notation not in ["physicist", "chemist"]:
        raise ValueError("`notation` must be one of 'physicist' or 'chemist'")

    if transform is not None:
        array = ElectronRepulsionIntegral(basis).construct_array_lincomb(transform, coord_type)
    elif coord_type == "cartesian":
        array = ElectronRepulsionIntegral(basis).construct_array_cartesian()
    elif coord_type == "spherical":
        array = ElectronRepulsionIntegral(basis).construct_array_spherical()
    else:
        array = ElectronRepulsionIntegral(basis).construct_array_mix(coord_type)

    if notation == "physicist":
        array = np.transpose(array, (0, 2, 1, 3))
    return array