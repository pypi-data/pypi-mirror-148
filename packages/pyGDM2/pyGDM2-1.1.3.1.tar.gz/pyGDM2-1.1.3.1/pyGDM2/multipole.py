# encoding: utf-8
#
#Copyright (C) 2017-2022, P. R. Wiecha
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
tools around multipole decomposition and effective polarizabilities

"""
from __future__ import print_function
from __future__ import absolute_import

import warnings
# import math

import numpy as np
import copy
import numba

import time


#==============================================================================
# GLOBAL PARAMETERS
#==============================================================================
DTYPE_C = np.complex64




#==============================================================================
# EXCEPTIONS
#==============================================================================



def multipole_decomposition_exact(sim, field_index, r0=None, epsilon=0.01, 
                                  which_moments=['p', 'm', 'qe', 'qm'],
                                  long_wavelength_approx=False):
    """exact multipole decomposition of the nanostructure optical response
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Multipole decomposition of electromagnetic field inside nanostructure for 
    electric and magnetic dipole and quadrupole moments.


    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r0 : array, default: None
        [x,y,z] position of multipole decomposition development. 
        If `None`, use structure's center of gravity
    
    epsilon : float, default: 0.01
        additional step on r0 (in nm) to avoid numerical divergence of the Bessel terms
        
    which_moments : list of str, default: ['p', 'm', 'qe', 'qm']
        which multipole moments to calculate and return. supported dipole moments: 
            - 'p': electric dipole (full)
            - 'm': magnetic dipole
            - 'qe': electric quadrupole (full)
            - 'qm': magnetic quadrupole
            - 'p1': electric dipole (first order)
            - 'pt': toroidal dipole
            - 'qe1': electric quadrupole (first order)
            - 'qet': toroidal quadrupole
    
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation
            
    
    Returns
    -------
    list of multipole moments. Default:
        
    p : 3-vector
        electric dipole moment
    
    m : 3-vector
        magnetic dipole moment
    
    Qe : 3x3 tensor
        electric quadrupole moment
        
    Qm : 3x3 tensor
        magnetic quadrupole moment
    
    
    Notes
    -----
    For details about the method, see: 
    
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet " +
                         "evaluated. Run `core.scatter` simulation first.")
    
    which_moments = [wm.lower() for wm in which_moments]
    
# =============================================================================
#     preparation
# =============================================================================
    ## structure
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
        sim.r0 = r0
    if np.abs(np.linalg.norm(geo - r0, axis=1)).min() > epsilon:
        epsilon = 0
    r = geo - r0 + epsilon                   # epsilon: avoid divergence of 1/kr when r=0
    norm_r = np.linalg.norm(r, axis=1)
    
    ## illumination properties
    field_params = sim.E[field_index][0]
    wavelength = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, r0[None,:])[0]  # assume structure is fully in one environment
    n_env = eps_env**0.5
    k = 2*np.pi*n_env / wavelength
    kr = k * norm_r
    
    ## electric polarization density of structure
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    E = sim.E[field_index][1]
    P = np.matmul(alpha_tensor, E[...,None])[...,0]
    rP = np.einsum('ij, ij->i', r, P)
    
    ## bessel functions and pre-factors
    if not long_wavelength_approx:
        from scipy.special import spherical_jn as sph_jn
        j0kr = sph_jn(0, kr)
        j1kr = sph_jn(1, kr) / kr
        j2kr = sph_jn(2, kr) / (kr**2)
        j3kr = sph_jn(3, kr) / (kr**3)
        f_pt = 1/2; f_ptA=3; f_ptB=-1
        f_qe = 3; fqe2=2; fqe2A = 5; fqe2B = -1; fqe2C = -1
        f_m = 3/2; f_qm = 15
    else:
        j0kr = j1kr = j2kr = j3kr = np.ones_like(kr)
        f_pt = 1/10; f_ptA=1; f_ptB=-2
        f_qe = 1; fqe2=1/14; fqe2A = 4; fqe2B = -5; fqe2C = 2
        f_m = 1/2; f_qm = 1
    
# =============================================================================
#     multipole calculation
# =============================================================================
    ## ----------- dipole moments
    ## electric dipole
    if 'p' in which_moments or 'p1' in which_moments or 'pt' in which_moments:
        p1 = np.sum(P * j0kr[..., None], axis=0)
        
        ## "toroidal" dipole
        p2 = k**2 * f_pt * np.sum((  f_ptA * rP[...,None]*r 
                                   + f_ptB * norm_r[..., None]**2 * P) * j2kr[..., None], 
                                  axis=0)
        
        p = p1 + p2
    
    ## magnetic dipole
    if 'm' in which_moments:
        m = -1j*k * f_m * np.sum(np.cross(r, P) * j1kr[..., None], axis=0)
    
    ## ----------- quadrupole moments
    ## electric quadrupole
    if 'qe' in which_moments or 'qe1' in which_moments or 'qet' in which_moments:
        Qe1 = np.zeros((3,3), dtype=np.complex64)
        Qe2 = np.zeros((3,3), dtype=np.complex64)
        for i_a in range(3):
            for i_b in range(3):
                
                ## diagonal term
                if i_a==i_b:
                    rP_delta = rP
                else:
                    rP_delta = 0
                
                ## electric quadrupole
                Qe1[i_a, i_b] = np.sum(
                    (
                       3 * (r[:,i_b]*P[...,i_a] + r[:,i_a]*P[...,i_b])
                     - 2*(rP_delta)
                     ) * j1kr)
                
                ## "toroidal" quadrupole
                Qe2[i_a, i_b] = np.sum(
                      (fqe2A*r[:,i_a]*r[:,i_b]*rP 
                      + norm_r**2 * (  fqe2B * (r[:,i_a]*P[:,i_b] + r[:,i_b]*P[:,i_a]) 
                                     + fqe2C * rP_delta)) * j3kr)
                
        Qe1 = f_qe * Qe1
        Qe2 = f_qe * fqe2 * k**2 * Qe2
        Qe = Qe1 + Qe2
    
    ## magnetic quadrupole
    if 'qm' in which_moments:
        Qm = np.zeros((3,3), dtype=np.complex64)
        for i_a in range(3):
            for i_b in range(3):
                Qm[i_a, i_b] = np.sum(
                    (r[:,i_a] * np.cross(r, P)[...,i_b] + 
                     r[:,i_b] * np.cross(r, P)[...,i_a]) * j2kr)
                
        Qm = -1j * k * f_qm * Qm
    
# =============================================================================
#     return results
# =============================================================================
    return_list = []
    for _m in which_moments:
        if _m.lower() == "p1":
            return_list.append(p1)
        if _m.lower() == "pt":
            return_list.append(p2)
        if _m.lower() == "p":
            return_list.append(p)
            
        if _m.lower() == "m":
            return_list.append(m)
            
        if _m.lower() == "qe1":
            return_list.append(Qe1)
        if _m.lower() == "qet":
            return_list.append(Qe2)
        if _m.lower() == "qe":
            return_list.append(Qe)
            
        if _m.lower() in ["qm"]:
            return_list.append(Qm)
    
    return return_list



def extinct(sim, field_index, with_toroidal=True, r0=None, eps_dd=0.001, 
            use_generalized_polarizabilities=False, normalization_E0=True,
            long_wavelength_approx=False):
    """extinction cross sections from multipole decomposition
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns extinction cross sections for electric and magnetic dipole and 
    quadrupole moments of the multipole decomposition.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    with_toroidal : bool, default: True
        whether to add toroidal moments to electric dipole and quadrupole
    
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    eps_dd : float, default: 0.1
        numerical integration step (in nm). Used for e/m quadrupole extinction.
    
    normalization_E0 : bool, default: True
        normalizes sections to max. incident field intensity
        
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation
        
        
    Returns
    -------
    sigma_ext_p : float
        electric dipole extinction cross section (in nm^2)
    
    sigma_ext_m : float
        magnetic dipole extinction cross section (in nm^2)
        
    sigma_ext_q : float
        electric quadrupole extinction cross section (in nm^2)
        
    sigma_ext_mq : float
        magnetic quadrupole extinction cross section (in nm^2)
    
    
    Notes
    -----
    For details about the extinction section of multipole moments, see:
    
    Evlyukhin, A. B. et al. *Multipole analysis of light scattering by 
    arbitrary-shaped nanoparticles on a plane surface.*, 
    JOSA B 30, 2589 (2013)
    
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if sim.E is None and not use_generalized_polarizabilities:
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")

# =============================================================================
#     extinction section calculation
# =============================================================================
    from pyGDM2 import linear
    from pyGDM2 import tools
    
    ## by default, use center of gravity for multimode expansion
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
    
    field_params = tools.get_field_indices(sim)[field_index]
    wavelength   = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    k0 = 2*np.pi / wavelength
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, geo[:1])[0]  # structure must be fully in one environment zone
    n_env = (eps_env**0.5).real
    
    ## incident field and its gradients at multipole position
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(r0[None,:], env_dict, **field_params)
    H0 = sim.efield.field_generator(r0[None,:], env_dict, returnField='H', **field_params)
    
    gradE0, gradH0 = linear.field_gradient(sim, field_index, r0[None,:], 
                                           delta=eps_dd, which_fields=['E0', 'H0'])
    gradE0cj = np.conj(np.array(gradE0)[:,0,3:])
    gradH0cj = np.conj(np.array(gradH0)[:,0,3:])
    
    ## normalization
    if normalization_E0:
        E2in = np.sum(np.abs(E0)**2, axis=1)   # intensity of incident field
    else:
        E2in = 1.0
    prefactor = (4 * np.pi * k0 * 1/n_env * 1/E2in).real
    
    ## get dipole moments
    if not use_generalized_polarizabilities:
        p, p1, m, Qe, Qe1, Qm = multipole_decomposition_exact(
                sim, field_index, r0=r0, 
                long_wavelength_approx=long_wavelength_approx, 
                which_moments=['p', 'p1', 'm', 'qe', 'qe1', 'qm'])
    else:
        if with_toroidal:
            p = eval_generalized_polarizability_p(sim, field_index, which_order='p')
            Qe = eval_generalized_polarizability_qe(sim, field_index, which_order='qe')
        else:
            p1 = eval_generalized_polarizability_p(sim, field_index, which_order='p1')
            Qe1 = eval_generalized_polarizability_qe(sim, field_index, which_order='qe1')
        m = eval_generalized_polarizability_m(sim, field_index)
        Qm = eval_generalized_polarizability_qm(sim, field_index)

    
    
    if with_toroidal:
        ecs_p = prefactor * (np.sum(np.conjugate(E0)*p)).imag
        ecs_Qe = prefactor / 12. * (np.sum(np.tensordot(gradE0cj + gradE0cj.T, Qe) )).imag
    else:
        ecs_p = prefactor * (np.sum(np.conjugate(E0)*p1)).imag
        ecs_Qe = prefactor / 12. * (np.sum(np.tensordot(gradE0cj + gradE0cj.T, Qe1) )).imag
    ecs_m = prefactor / n_env * (np.sum(np.conjugate(H0)*m)).imag
    ecs_Qm = prefactor / n_env / 6 * (np.sum(np.tensordot(gradH0cj.T, Qm) )).imag
    
    return [ecs_p, ecs_m, ecs_Qe, ecs_Qm]
    
    
    


def scs(sim, field_index, with_toroidal=True, 
        use_generalized_polarizabilities=False, r0=None, normalization_E0=True,
        long_wavelength_approx=False):
    """total scattering cross section from multipole decomposition
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns scattering cross sections for electric and magnetic dipole and 
    quadrupole moments of the multipole decomposition.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    with_toroidal : bool, default: True
        whether to add toroidal moments to electric dipole and quadrupole
            
    use_generalized_polarizabilities : bool, default: False
        if True, use generalized polarizabilities
        (does not require evaluation of `core.scatter` for new incident field 
         configurations, first calculation is more expensive)
    
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    normalization_E0 : bool, default: True
        normalizes sections to max. incident field intensity
        
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation
    
    
    Returns
    -------
    sigma_scat_p : float
        electric dipole scattering cross section (in nm^2)
    
    sigma_scat_m : float
        magnetic dipole scattering cross section (in nm^2)
        
    sigma_scat_q : float
        electric quadrupole scattering cross section (in nm^2)
        
    sigma_scat_mq : float
        magnetic quadrupole scattering cross section (in nm^2)
    
    
    Notes
    -----
    For details about the exact multipole formalism and scs calculation, see: 
        
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
    
    """
    from pyGDM2 import tools
# =============================================================================
#     Exception handling
# =============================================================================
    if sim.E is None and not use_generalized_polarizabilities:
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")

# =============================================================================
#     scattering section calculation
# =============================================================================
    ## by default, use center of gravity for multimode expansion
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
    
    field_params = tools.get_field_indices(sim)[field_index]
    wavelength   = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    k0 = 2*np.pi / wavelength
    
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, geo[:1])[0]  # assume structure is fully in one environment
    n_env = (eps_env**0.5).real
    k = k0*n_env
    
    ## normalization: incident field intensity at multipole position
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(r0[None,:], env_dict, **field_params)
    if normalization_E0:
        E2in = np.sum(np.abs(E0)**2, axis=1)   # intensity of incident field
    else:
        E2in = 1.0
    
    ## factor 100: cm --> m (cgs units)
    sc_factor_dp = 100/12*(k0**4 / E2in).real
    sc_factor_Q = 100/1440*(k0**4 / E2in).real
    
    ## the actual scattering sections
    if not use_generalized_polarizabilities:
        p, p1, m, Qe, Qe1, Qm = multipole_decomposition_exact(
                sim, field_index, r0=r0,
                which_moments=['p', 'p1', 'm', 'qe', 'qe1', 'qm'], 
                long_wavelength_approx=long_wavelength_approx)
    else:
        if with_toroidal:
            p = eval_generalized_polarizability_p(sim, field_index, which_order='p', long_wavelength_approx=long_wavelength_approx)
            Qe = eval_generalized_polarizability_qe(sim, field_index, which_order='qe', long_wavelength_approx=long_wavelength_approx)
        else:
            p1 = eval_generalized_polarizability_p(sim, field_index, which_order='p1', long_wavelength_approx=long_wavelength_approx)
            Qe1 = eval_generalized_polarizability_qe(sim, field_index, which_order='qe1', long_wavelength_approx=long_wavelength_approx)
        m = eval_generalized_polarizability_m(sim, field_index, long_wavelength_approx=long_wavelength_approx)
        Qm = eval_generalized_polarizability_qm(sim, field_index, long_wavelength_approx=long_wavelength_approx)
        
    if with_toroidal:
        scs_p = sc_factor_dp * np.sum(np.abs(p)**2)
        scs_Qe = sc_factor_Q * np.sum(np.abs(k*Qe)**2)
    else:
        scs_p = sc_factor_dp * np.sum(np.abs(p1)**2)
        scs_Qe = sc_factor_Q * np.sum(np.abs(k*Qe1)**2)
    scs_m = sc_factor_dp * np.sum(np.abs(m)**2)
    scs_Qm = sc_factor_Q * np.sum(np.abs(k*Qm)**2)
            
    return [scs_p, scs_m, scs_Qe, scs_Qm]
    


def farfield(sim, field_index, 
             r_probe=None,
             r=100000., 
             tetamin=0, tetamax=np.pi/2., Nteta=10, 
             phimin=0, phimax=2*np.pi, Nphi=36, 
             polarizerangle='none', return_value='map', 
             normalization_E0=False, 
             which_moments=['p', 'm', 'qe', 'qm'],
             long_wavelength_approx=False, r0=None):
    """spatially resolved and polarization-filtered far-field scattering 
    
    For a given incident field, calculate the electro-magnetic field 
    (E-component) in the far-field around the nanostructure 
    (on a sphere of radius `r`).
    
    Propagator for scattering into a substrate contributed by C. Majorel
    
    Pure python implementation.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
        
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples. optional. Default: don't use
        defaults to *None*, which means it is not used and a solid angle defined by
        a spherical coordinate range is used instead. If `r_probe` is given, this
        overrides `r`, `tetamin`, `tetamax`, `Nteta`, `Nphi`.
        (list of) coordinate(s) to evaluate farfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        
    r : float, default: 100000.
        radius of integration sphere (distance to coordinate origin in nm)
        
    tetamin, tetamax : float, float; defaults: 0, np.pi/2
        minimum and maximum polar angle in radians 
        (in linear steps from `tetamin` to `tetamax`)
        
    phimin, phimax : float, float; defaults: 0, 2*np.pi
        minimum and maximum azimuth angle in radians, excluding last position
        (in linear steps from `phimin` to `phimax`)
        
    Nteta, Nphi : int, int; defaults: 10, 36
        number of polar and azimuthal angles on sphere to calculate,
        
    polarizerangle : float or 'none', default: 'none'
        optional polarization filter angle **in degrees**(!). If 'none' (default), 
        the total field-intensity is calculated (= no polarization filter)
    
    return_value : str, default: 'map'
        Values to be returned. Either 'map' (default) or 'integrated'.
          - "map" : (default) return spatially resolved farfield intensity at each spherical coordinate (5 lists)
          - "efield" : return spatially resolved E-fields at each spherical coordinate (5 lists)
          - "int_Es" : return the integrated scattered field (as float)
          - "int_E0" : return the integrated fundamental field (as float)
          - "int_Etot" : return the integrated total field (as float)
          
    normalization_E0 : bool, default: False
        has only effect on return_value=="int_Es": Normalizes scattering 
        to peak of incident field intensity inside structure
        
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    which_moments : list of str, default: ['p', 'm', 'qe', 'qm']
        which multipole moments to use for farfield calculations. Supported:
            - 'p': electric dipole (full)
            - 'm': magnetic dipole
            - 'qe': electric quadrupole (full)
            - 'qm': magnetic quadrupole
            - 'p1': electric dipole (first order)
            - 'pt': toroidal dipole
            - 'qe1': electric quadrupole (first order)
            - 'qet': toroidal quadrupole
            
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation
    
    Returns
    -------
    using `r_probe` for position definition:
        3 lists of 6-tuples (x,y,z, Ex,Ey,Ez), complex : 
            - scattered Efield or E-intensity
            - total Efield (inlcuding fundamental field) or total E intensity
            - fundamental Efield (incident field) or E0 intensity
        
    if solid angle is defined via spherical coordinate range:
        - return_value == "map" : 5 arrays of shape (Nteta, Nphi) : 
            - [tetalist : teta angles - if solid angle range input]
            - [philist : phi angles - if solid angle range input]
            - I_sc : intensity of scattered field, 
            - I_tot : intensity of total field (I_tot=|E_sc+E_0|^2), 
            - I0 : intensity of incident field
        
        - return_value == "efield" : float
            - [tetalist : teta angles - if solid angle range input]
            - [philist : phi angles - if solid angle range input]
            - E_sc : complex scattered field at each pos.
            - E_tot : complex total field at each pos. (E_sc+E0)
            - E0 : complex incident field at each pos.
            
        - return_value == "int_XX" : float
            integrated total intensity over specified solid angle
        
    Notes
    -----
    See equation (G1) in
    
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
        
    """
# =============================================================================
#     exception handling
# =============================================================================
    if sim.E is None: 
        raise ValueError("Error: Scattering field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    if str(polarizerangle).lower() == 'none':
        polarizer = 0
    else:
        polarizer = polarizerangle * np.pi/180.
    
    if np.pi < tetamax < 0:
        raise ValueError("`tetamax` out of range, must be in [0, pi]")
    
    if r_probe is not None and return_value in ['int_es', 'int_E0', 'int_Etot']:
        raise ValueError("probing farfield on user-defined positions does not support integration " +
                         "of the intensity since no surface differential can be defined. Use spherical " +
                         "coordinate definition to do the integration.")
    
    which_moments = [wm.lower() for wm in which_moments]
    if ('p' in which_moments and 'p1' in which_moments) or ('p' in which_moments and 'pt' in which_moments):
        raise Exception("Please use one single electric dipole moment for farfield propagation.")
    if ('qe' in which_moments and 'qe1' in which_moments) or ('qe' in which_moments and 'qet' in which_moments):
        raise Exception("Please use one single electric quadrupole moment for farfield propagation.")
        
# =============================================================================
#     preparation
# =============================================================================
    from pyGDM2 import tools
    ## --- spherical probe coordinates
    if r_probe is None:
        tetalist = np.ones((int(Nteta), int(Nphi)))*np.linspace(tetamin, tetamax, int(Nteta))[:,None]
        philist = np.ones((int(Nteta), int(Nphi)))*np.linspace(phimin, phimax, int(Nphi), endpoint=False)[None,:]
        xff = (r * np.sin(tetalist) * np.cos(philist)).flatten()
        yff = (r * np.sin(tetalist) * np.sin(philist)).flatten()
        zff = (r * np.cos(tetalist)).flatten()
        _r_probe = np.transpose([xff, yff, zff])
    else:
        _r_probe = r_probe
        
    ## --- spherical integration steps
    dteta = (tetamax-tetamin) / float(Nteta-1)  # endpoint included
    dphi = (phimax-phimin) / float(Nphi)        # endpoint not included
    
    ## --- incident field config
    field_params    = tools.get_field_indices(sim)[field_index]
    wavelength      = field_params['wavelength']
    
    ## --- structure
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
    n_vec = _r_probe - r0
    R_d = np.linalg.norm(n_vec, axis=1)
    n0_vec = n_vec / R_d[:,None]     # unit vector for direction of scattering
    
    ## --- environment
    sim.struct.setWavelength(wavelength)
    k0 = 2*np.pi / wavelength
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, geo[:1])[0]  # assume structure is fully in one environment
    n_env = (eps_env**0.5).real
    k = k0*n_env
    
#==============================================================================
#     electric polarization of structure, fundamental field
#==============================================================================        
    ## --- fundamental field - use dummy structure with 
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    if return_value == 'int_Es':
        from pyGDM2 import fields
        E0 = fields.nullfield(_r_probe, env_dict, wavelength, returnField='E')
    else:
        E0 = sim.efield.field_generator(_r_probe, env_dict, **field_params)
        
    
    p, p1, pt, m, Qe, Qe1, Qet, Qm = multipole_decomposition_exact(
                sim, field_index, r0=r0,
                which_moments=['p', 'p1', 'pt', 'm', 'qe', 'qe1', 'qet', 'qm'], 
                long_wavelength_approx=long_wavelength_approx)
    
    phase_factor = np.exp(1j*k*R_d)
    prefactor = k0**2 * phase_factor / (R_d)
    
    Es_p1 = prefactor[:,None] * np.cross(n0_vec, np.cross((p1)[None,:], n0_vec))
    Es_pt = prefactor[:,None] * np.cross(n0_vec, np.cross((pt)[None,:], n0_vec))    
    Es_p = Es_p1 + Es_pt
    Es_m = prefactor[:,None] * np.cross(m[None,:], n0_vec)
    
    Es_qe1 = prefactor[:,None] * 1j * k/6 * np.cross(n0_vec, 
                 np.cross(n0_vec, np.tensordot(Qe1, n0_vec, axes=(-1,-1)).T))
    Es_qet = prefactor[:,None] * 1j * k/6 * np.cross(n0_vec, 
                 np.cross(n0_vec, np.tensordot(Qet, n0_vec, axes=(-1,-1)).T))
    Es_qe = Es_qe1 + Es_qet
    Es_qm = prefactor[:,None] * 1j * k/6 * np.cross(n0_vec, 
                                    np.tensordot(Qm, n0_vec, axes=(-1,-1)).T)

    ## sum up all multipole fields
    Escat = np.zeros(shape=(len(_r_probe), 3), dtype=sim.efield.dtypec)
    if ('p1' in which_moments and 'pt' in which_moments) or 'p' in which_moments:
        Escat += Es_p
    elif 'p1' in which_moments:
        Escat += Es_p1
    elif 'pt' in which_moments:
        Escat += Es_pt
    if 'm' in which_moments:
        Escat += Es_m
    if ('qe1' in which_moments and 'qet' in which_moments) or 'qe' in which_moments:
        Escat += Es_qe
    elif 'qe1' in which_moments:
        Escat += Es_qe1
    elif 'qet' in which_moments:
        Escat += Es_qet
    if 'qm' in which_moments:
        Escat += Es_qm
    
    
    Iscat = np.sum((np.abs(Escat)**2), axis=1)


#==============================================================================
#    calc. fields through optional polarization filter
#==============================================================================
    if str(polarizerangle).lower() != 'none':
        ## --- scattered E-field parallel and perpendicular to scattering plane
        Es_par  = ( Escat.T[0] * np.cos(tetalist.flatten()) * np.cos(philist.flatten()) + 
                    Escat.T[1] * np.sin(philist.flatten()) * np.cos(tetalist.flatten()) - 
                    Escat.T[2] * np.sin(tetalist.flatten()) )
        Es_perp = ( Escat.T[0] * np.sin(philist.flatten()) - Escat.T[1] * np.cos(philist.flatten()) )
        ## --- scattered E-field parallel to polarizer
        Es_pol  = ( Es_par * np.cos(polarizer - philist.flatten()) - 
                    Es_perp * np.sin(polarizer - philist.flatten()) )
        
        ## --- fundamental E-field parallel and perpendicular to scattering plane
        E0_par  = ( E0.T[0] * np.cos(tetalist.flatten()) * np.cos(philist.flatten()) + 
                    E0.T[1] * np.sin(philist.flatten()) * np.cos(tetalist.flatten()) - 
                    E0.T[2] * np.sin(tetalist.flatten()) )
        E0_perp = ( E0.T[0] * np.sin(philist.flatten()) - E0.T[1] * np.cos(philist.flatten()) )
        ## --- fundamental E-field parallel to polarizer
        E0_pol  = ( E0_par * np.cos(polarizer - philist.flatten()) - 
                    E0_perp * np.sin(polarizer - philist.flatten()) )

#==============================================================================
#     Intensities with and without fundamental field / polarizer
#==============================================================================
    ## --- total field (no polarizer)
    if r_probe is None:
        out_shape = tetalist.shape
    else:
        out_shape = len(_r_probe)
        
    I_sc  = Iscat.reshape(out_shape)
    I0    = np.sum((np.abs(E0)**2), axis=1).reshape(out_shape)
    I_tot = np.sum((np.abs(E0 + Escat)**2), axis=1).reshape(out_shape)
    
    ## --- optionally: with polarizer
    if str(polarizerangle).lower() != 'none':
        I_sc  = (np.abs(Es_pol)**2).reshape(out_shape)
        I0    = (np.abs(E0_pol)**2).reshape(out_shape)
        I_tot = (np.abs(Es_pol + E0_pol)**2).reshape(out_shape)
    
    
    if return_value.lower() == 'map':
        if r_probe is None:
            return tetalist, philist, I_sc, I_tot, I0
        else:
            return I_sc, I_tot, I0
    elif return_value.lower() in ['efield', 'fields', 'field']:
        if r_probe is None:
            return tetalist, philist, Escat, Escat + E0, E0
        else:
            return Escat, Escat + E0, E0
    else:
        d_solid_surf = r**2 * np.sin(tetalist) * dteta * dphi
        if return_value.lower() == 'int_es':
            if normalization_E0:
                env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
                E0 = sim.efield.field_generator(sim.struct.geometry, 
                                                env_dict, **field_params)
                I0_norm = np.sum(np.abs(E0)**2, axis=1).max()
            else:
                I0_norm = 1
            
            return np.sum(I_sc * d_solid_surf) / I0_norm
        
        elif return_value.lower() == 'int_e0':
            return np.sum(I0 * d_solid_surf)
        
        elif return_value.lower() == 'int_etot':
            return np.sum(I_tot * d_solid_surf)
        
        else:
            raise ValueError("Parameter 'return_value' must be one of ['map', 'int_es', 'int_e0', 'int_etot'].")







def _multipole_farfield(wavelength, eps_env, r0=None, 
                        p=[], m=[], qe=[], qm=[],
                        r_p=None, r_m=None, r_qe=None, r_qm=None,
                        r_probe=None,
                        r=100000., 
                        tetamin=0, tetamax=np.pi/2., Nteta=10, 
                        phimin=0, phimax=2*np.pi, Nphi=36, 
                        return_value='map'):
    """far-field scattering of an explicit list of multipole moments
    
    Radiated electro-magnetic field  (E-field) in the far-field 
    (by default on a sphere of radius `r` around the nanostructure).
    
    
    Parameters
    ----------
    wavelength : float
        radiation wavelength
    
    eps_env : float
        envirnoment permittivity (real part)
        
    r0 : array. optional
        [x,y,z] position of mulipole decomposition development.
        Alternatively the positions of each mutlipole can be specified.
        The default is `None`.
        
    p, m, qe, qm : lists of ndarrays. optional
        lists of dipole and quadrupole moments to propagate to the farfield.
        The default is [].
        
    r_p, r_m, r_qe, r_qm : ndarrays or list of such. optional
        Has effect only if r0 is not specified. Carthesian coordinates of 
        each multipole individually.
    
    r_probe : tuple (x,y,z) or list of 3-lists/-tuples. optional
        defaults to *None*, which means it is not used and a solid angle defined by
        a spherical coordinate range is used instead. If `r_probe` is given, this
        overrides `r`, `tetamin`, `tetamax`, `Nteta`, `Nphi`.
        (list of) coordinate(s) to evaluate farfield on. 
        Format: tuple (x,y,z) or list of 3 lists: [Xmap, Ymap, Zmap] 
        The default is None. (Not used)
        
    r : float, default: 100000.
        radius of integration sphere (distance to coordinate origin in nm)
        
    tetamin, tetamax : float, float; defaults: 0, np.pi/2
        minimum and maximum polar angle in radians 
        (in linear steps from `tetamin` to `tetamax`)
        
    phimin, phimax : float, float; defaults: 0, 2*np.pi
        minimum and maximum azimuth angle in radians, excluding last position
        (in linear steps from `phimin` to `phimax`)
        
    Nteta, Nphi : int, int; defaults: 10, 36
        number of polar and azimuthal angles on sphere to calculate,
    
    return_value : str, default: 'map'
        Values to be returned. Either 'map' (default) or 'integrated'.
          - "map" : (default) return spatially resolved farfield intensity at each spherical coordinate (5 lists)
          - "efield" : return spatially resolved E-fields at each spherical coordinate (5 lists)
          - "int_Es" : return the integrated scattered field (as float)
    
    
    Returns
    -------
    using `r_probe` for position definition:
        3 lists of 6-tuples (x,y,z, Ex,Ey,Ez), complex : 
            - scattered Efield or E-intensity
        
    if solid angle is defined via spherical coordinate range:
        - return_value == "map" : 5 arrays of shape (Nteta, Nphi) : 
            - [tetalist : teta angles - if solid angle range input]
            - [philist : phi angles - if solid angle range input]
            - I_sc : intensity of scattered field, 
        
        - return_value == "efield" : float
            - [tetalist : teta angles - if solid angle range input]
            - [philist : phi angles - if solid angle range input]
            - E_sc : complex scattered field at each pos.
            
        - return_value == "int_XX" : float
            integrated total intensity over specified solid angle
        
    
    Notes
    -----
    See equation (G1) in
    
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
        
    """
# =============================================================================
#     exception handling
# =============================================================================
    if np.pi < tetamax < 0:
        raise ValueError("`tetamax` out of range, must be in [0, pi]")
    
    if r_probe is not None and return_value in ['int_es', 'int_E0', 'int_Etot']:
        raise ValueError("probing farfield on user-defined positions does not support integration " +
                         "of the intensity since no surface differential can be defined. Use spherical " +
                         "coordinate definition to do the integration.")
    
    if r0 is None:
        if r_p is None and r_m is None and r_qe is None and r_qm is None:
            raise Exception("No positions for the multipoles are given.")
        if len(r_p) != len(p):
            raise Exception("Same number of dipole positions and dipole moments required! `p` and `r_p` must be lists of same length.")
        if len(r_m) != len(m):
            raise Exception("Same number of dipole positions and dipole moments required! `m` and `r_m` must be lists of same length.")
        if len(r_qe) != len(qe):
            raise Exception("Same number of quadrupole positions and quadrupole moments required! `qe` and `r_qe` must be lists of same length.")
        if len(r_qm) != len(qm):
            raise Exception("Same number of quadrupole positions and quadrupole moments required! `qm` and `r_qm` must be lists of same length.")
    else:
        r0 = np.array(r0)
        if len(r0) != 3: 
            raise Exception("Multipole position must be carthesian coordinate (array of 3 float)")
        r_p = [r0 for _ in p]
        r_m = [r0 for _ in m]
        r_qe = [r0 for _ in qe]
        r_qm = [r0 for _ in qm]
        
# =============================================================================
#     preparation
# =============================================================================
    ## --- spherical probe coordinates
    if r_probe is None:
        tetalist = np.ones((int(Nteta), int(Nphi)))*np.linspace(tetamin, tetamax, int(Nteta))[:,None]
        philist = np.ones((int(Nteta), int(Nphi)))*np.linspace(phimin, phimax, int(Nphi), endpoint=False)[None,:]
        xff = (r * np.sin(tetalist) * np.cos(philist)).flatten()
        yff = (r * np.sin(tetalist) * np.sin(philist)).flatten()
        zff = (r * np.cos(tetalist)).flatten()
        _r_probe = np.transpose([xff, yff, zff])
    else:
        _r_probe = r_probe
        
    ## --- spherical integration steps
    dteta = (tetamax-tetamin) / float(Nteta-1)  # endpoint included
    dphi = (phimax-phimin) / float(Nphi)        # endpoint not included
    
    ## --- environment
    k0 = 2*np.pi / wavelength
    n_env = (eps_env**0.5).real
    k = k0*n_env
    
#==============================================================================
#     electric polarization of structure, fundamental field
#==============================================================================        
    Escat = np.zeros(shape=(len(_r_probe), 3), dtype=DTYPE_C)
    
    def eval_prefactors(r0, _r_probe, k, k0):
        n_vec = _r_probe - r0
        R_d = np.linalg.norm(n_vec, axis=1)
        n_vec = n_vec / R_d[:,None]     # unit vector along direction of scattering
        
        phase_factor = np.exp(1j*k*R_d)
        prefactor = k0**2 * phase_factor / R_d
        
        return prefactor, n_vec
    
    
    for _r0, _p in zip(r_p, p):
        prefactor, n0_vec = eval_prefactors(_r0, _r_probe, k, k0)
        Es_p = prefactor[:,None] * np.cross(n0_vec, np.cross((_p)[None,:], n0_vec))
        Escat += Es_p     # sum all electric dipole fields
    
    for _r0, _m in zip(r_m, m):
        prefactor, n0_vec = eval_prefactors(_r0, _r_probe, k, k0)
        Es_m = prefactor[:,None] * np.cross(_m[None,:], n0_vec)
        Escat += Es_m     # sum all magnetic dipole fields
    
    for _r0, _qe in zip(r_qe, qe):
        prefactor, n0_vec = eval_prefactors(_r0, _r_probe, k, k0)
        Es_qe = prefactor[:,None] * 1j * k/6 * np.cross(n0_vec, 
                    np.cross(n0_vec, np.tensordot(_qe, n0_vec, axes=(-1,-1)).T))
        Escat += Es_qe     # sum all electric quadrupole fields
    
    for _r0, _qm in zip(r_qm, qm):
        prefactor, n0_vec = eval_prefactors(_r0, _r_probe, k, k0)
        Es_qm = prefactor[:,None] * 1j * k/6 * np.cross(n0_vec, 
                    np.tensordot(_qm, n0_vec, axes=(-1,-1)).T)
        Escat += Es_qm     # sum all magnetic quadrupole fields

    
    Iscat = np.sum((np.abs(Escat)**2), axis=1)



#==============================================================================
#     Intensities with and without fundamental field / polarizer
#==============================================================================
    ## --- total field (no polarizer)
    if r_probe is None:
        out_shape = tetalist.shape
    else:
        out_shape = len(_r_probe)
        
    I_sc  = Iscat.reshape(out_shape)
    
    
    if return_value.lower() == 'map':
        if r_probe is None:
            return tetalist, philist, I_sc
        else:
            return I_sc
    elif return_value.lower() in ['efield', 'fields', 'field']:
        if r_probe is None:
            return tetalist, philist, Escat
        else:
            return Escat
    else:
        d_solid_surf = r**2 * np.sin(tetalist) * dteta * dphi
        if return_value.lower() in ['int_es', 'int']:
            return np.sum(I_sc * d_solid_surf)
        
        else:
            raise ValueError("Parameter 'return_value' must be one of ['map', 'int_es', 'int_e0', 'int_etot'].")











# =============================================================================
# polarizabilities
# =============================================================================
def generalized_polarizability(sim, field_index=None, wavelength=None, 
                               method='lu', epsilon=0.01, r0=None,
                               which_moments=['p1', 'pt', 'qe', 'qt', 'm', 'qm'],
                               long_wavelength_approx=False, verbose=1):
    """generalized electric and magnetic polarizabilities
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns the generalized polarizability tensors that can be used with arbitrary,
    inhomogeneous illumination fields to calculate the effective 
    electric and magnetic multipole moments, induced in the nanostructure.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int, default: None
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`.
        Either `field_index` or `wavelength` must be given.
    
    wavelength : float, default: None
        Optional wavelength (alternative to `field_index`) at which to 
        calculate susceptibility matrix (in nm). 
        Either `field_index` or `wavelength` must be given.
    
    method : string, default: "scipyinv"
        inversion method. One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
         - "scipyinv" scipy default inversion (`scipy.linalg.inv`)
         - "numpyinv" numpy inversion (`np.linalg.inv`, if numpy compiled accordingly: LAPACK's `dgesv`)
         - "cupy" uses CUDA GPU via `cupy`
         - "cuda" (equivalent to "cupy")
         - "lu" LU-decomposition (`scipy.linalg.lu_factor`) - inefficient for `decay_rate`!
    
    epsilon : float, default: 0.01
        additional step on r0 (in nm) to avoid numerical divergence of the Bessel terms
        
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    which_moments : list of str, default: ['p1', 'pt', 'qe1', 'qt', 'm', 'qm']
        which generalized polarizability tensors to calculate and return. supported:
            - 'p1': electric dipole - only first order (rank 2)
            - 'pt': toroidal dipole (rank 3)
            - 'qe1': electric quadrupole - only first order (rank 4)
            - 'qt': toroidal electric quadrupole (rank 4)
            - 'm': magnetic dipole (rank 2)
            - 'qm': magnetic quadrupole (rank 3)
            
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation
        
    verbose : bool default=True
        print runtime info
    
    
    Returns
    -------
    
    by default 6 lists of N tensors, with N the number of discretization cells (see kwarg `which_moments`):
        
    K_P_E, K_T_E, K_QE_E, K_QT_E, K_M_E, K_QM_E
    
    Notes
    -----
    For details , see: 
        
    *PAPER SUBMITTED*
    
    For details about the underlying exact multipole decomposition, see: 
        
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
    
    """
    # =============================================================================
    #     Exception handling
    # =============================================================================
    if field_index is None and wavelength is None:
        raise Exception("Either `field_index` or `wavelength` must be given!")
        
    if field_index is not None and wavelength is not None:
        warnings.warn("`field_index` AND `wavelength` are given! Ignoring `wavelength`.")
        
    
    
    # =============================================================================
    # preparation
    # =============================================================================
    from pyGDM2 import core
    
    which_moments = [wm.lower() for wm in which_moments]
    
    if field_index is not None:
        from pyGDM2 import tools
        wavelength = tools.get_field_indices(sim)[field_index]['wavelength']
    
    if 'p1' in which_moments and not hasattr(sim, 'K_P_E'):
        sim.K_P_E = dict()
    if 'pt' in which_moments and not hasattr(sim, 'K_T_E'):
        sim.K_T_E = dict()
    if 'qe' in which_moments and not hasattr(sim, 'K_QE_E'):
        sim.K_QE_E = dict()
    if 'qt' in which_moments and not hasattr(sim, 'K_QT_E'):
        sim.K_QT_E = dict()
    if 'm' in which_moments and not hasattr(sim, 'K_M_E'):
        sim.K_M_E = dict()
    if 'qm' in which_moments and not hasattr(sim, 'K_QM_E'):
        sim.K_QM_E = dict()
    
    
    
    if verbose:
        t0 = time.time()
        print("wl={}nm. calc. K:".format(np.round(wavelength, 1)), end='')
    
    
    ## structure
    geo = sim.struct.geometry
    alpha = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    if r0 is None:
        r0 = np.average(geo, axis=0)
    sim.r0 = r0
    if np.abs(np.linalg.norm(geo - r0, axis=1)).min() > epsilon:
        epsilon = 0
    Dr = geo - r0  #   = r-r0
    norm_r = np.linalg.norm(Dr + epsilon, axis=1)  # epsilon: avoid divergence of 1/kr at r=0
    norm_r2 = norm_r**2
    
    ## illumination properties
    sim.struct.setWavelength(wavelength)
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, r0[None,:])[0]  # assume structure is fully in one environment
    n_env = eps_env**0.5
    k0 = 2.0*np.pi / wavelength
    k = k0*n_env
    kr = k * norm_r
    
    ## bessel functions and pre-factors
    if not long_wavelength_approx:
        from scipy.special import spherical_jn as sph_jn
        j0kr = sph_jn(0, kr)
        j1kr = sph_jn(1, kr) / kr
        j2kr = sph_jn(2, kr) / (kr**2)
        j3kr = sph_jn(3, kr) / (kr**3)
        f_pt = 1/2; f_ptA=3; f_ptB=-1
        f_qe = 3; fqe2=2; fqe2A = 5; fqe2B = -1; fqe2C = -1
        f_m = 3/2; f_qm = 15
    else:
        j0kr = j1kr = j2kr = j3kr = np.ones_like(kr)
        f_pt = 1/10; f_ptA=1; f_ptB=-2
        f_qe = 1; fqe2=1/14; fqe2A = 4; fqe2B = -5; fqe2C = 2
        f_m = 1/2; f_qm = 1
    
    
    ## ----- gen. propagator
    K = core.get_general_propagator(sim, wavelength, method=method)
    if method.lower() in ['cupy', 'cuda']:
        K = K.get()
    if method.lower() == 'lu':
        import scipy.linalg as la
        K = la.lu_solve(K, np.identity(K[0].shape[0], dtype=K[0].dtype))
        
    if verbose:
        t1 = time.time()
        print(" {:.1f}ms.  electric... ".format((t1-t0)*1000), end='')
    K2 = K.reshape(len(K)//3, 3, -1, 3).swapaxes(1,2).reshape(-1, 3, 3).reshape(len(K)//3,len(K)//3, 3, 3)
    K2a = np.matmul(alpha[:,None,...], K2)
    Ka = np.concatenate(np.concatenate(K2a, axis=1), axis=1)


# =============================================================================
#     electric-electric
# =============================================================================
    ## ----- electric-electric generalized polarizability - dipole
    if 'p1' in which_moments:
        K_P_E = np.sum(K2a * j0kr[:,None,None,None], axis=0)
        sim.K_P_E[wavelength] = K_P_E       # store in simulation object


    ## ----- higher order electric moments
    if 'pt' in which_moments or 'qe' in which_moments or 'qt' in which_moments:
        K_re = np.zeros_like(Ka)
        for i_dp in range(len(Ka)):
            K_re.T[i_dp] = (Dr * Ka.T[i_dp].reshape((len(Ka)//3,3))).reshape((len(Ka),))
        K2_re = K_re.reshape(len(Ka)//3, 3, -1, 3).swapaxes(1,2).reshape(-1, 3, 3).reshape(len(Ka)//3,len(Ka)//3, 3, 3)
            
        
    ## ----- toroidal dipole generalized polarizability 
    if 'pt' in which_moments:
        Qt1 = np.zeros((len(Ka)//3,3,3,3), dtype=np.complex64)
        Qt2 = np.zeros((len(Ka)//3,3,3), dtype=np.complex64)
        for i_a in range(3):
            for i_b in range(3):
                Qt1[:, i_a, i_b] = np.sum(
                    (
                    K2_re[...,i_b,:] * Dr[:,i_a,None,None]
                      ) * j2kr[:, None, None], axis=0)
            Qt2[:, i_a] = np.sum(
                (K2a[...,i_a,:]) * norm_r2[:,None,None]* j2kr[:, None, None], axis=0)
                
        K_T1_E = k**2 * f_pt * f_ptA * Qt1 
        K_T2_E = k**2 * f_pt * f_ptB * Qt2
    
        K_T_E = K_T1_E + K_T2_E[...,None,:]/3
        sim.K_T_E[wavelength] = K_T_E       # store in simulation object


    ## ----- electric quadrupole generalized polarizability 
    krondelta = np.identity(3)
    if 'qe' in which_moments:
        Qe11 = np.zeros((len(Ka)//3,3,3,3), dtype=np.complex64)
        Qe12 = np.zeros((len(Ka)//3,3,3,3,3), dtype=np.complex64)

        for i_a in range(3):
            for i_b in range(3):
                Qe11[:, i_a, i_b] = np.sum(
                    (
                    3*(Dr[:,i_b,None,None] * K2a[...,i_a,:] +
                       Dr[:,i_a,None,None] * K2a[...,i_b,:])
                      ) * j1kr[:, None,None], axis=0)
                
                for i_c in range(3):  # keep separate scalar product elements in last index
                    Qe12[:, i_a, i_b, i_c] = np.sum(
                        (
                        - 2*K2_re[...,i_c,:] * krondelta[i_a,i_b]   # diagonal term
                          ) * j1kr[:, None,None], axis=0)
        
        K_QE_E = f_qe * (Qe12 + Qe11[...,None,:]/3)
        sim.K_QE_E[wavelength] = K_QE_E
    
    
    ## ----- electric toroidal quadrupole generalized polarizability 
    if 'qt' in which_moments:
        Qet1 = np.zeros((len(Ka)//3,3,3,3,3), dtype=np.complex64)
        Qet2 = np.zeros((len(Ka)//3,3,3,3), dtype=np.complex64)
        Qet3 = np.zeros((len(Ka)//3,3,3,3,3), dtype=np.complex64)

        for i_a in range(3):
            for i_b in range(3):
                Qet2[:, i_a, i_b] = np.sum(
                    (
                    fqe2B * (Dr[:,i_a,None,None] * K2a[...,i_b,:] + Dr[:,i_b,None,None] * K2a[...,i_a,:])
                      ) * norm_r2[:,None,None] * j3kr[:, None,None], axis=0)
                
                for i_c in range(3):  # keep separate scalar product elements in last index
                    Qet1[:, i_a, i_b, i_c] = np.sum(
                        (
                         fqe2A * K2_re[...,i_c,:] * Dr[:,i_a,None,None] * Dr[:,i_b,None,None]
                          ) * j3kr[:, None,None], axis=0)
                    Qet3[:, i_a, i_b, i_c] = np.sum(
                        (
                         fqe2C * K2_re[...,i_c,:] * krondelta[i_a,i_b]  # diagonal term
                          ) * norm_r2[:,None,None] * j3kr[:, None,None], axis=0)
        K_QT_E = f_qe * fqe2 * k**2 * (Qet1 + Qet2[...,None,:]/3 + Qet3)
        sim.K_QT_E[wavelength] = K_QT_E



# =============================================================================
#     electric-magnetic
# =============================================================================
    if 'm' in which_moments or 'qm' in which_moments:
        if verbose:
            t2 = time.time()
            print("{:.1f}ms.  magnetic... ".format((t2-t1)*1000), end='')
        K_he = np.zeros_like(Ka)
        for i_dp in range(len(Ka)):
            K_he.T[i_dp] = np.cross(Dr, Ka.T[i_dp].reshape((len(Ka)//3,3))).reshape((len(Ka),))
        K2_he = K_he.reshape(len(Ka)//3, 3, -1, 3).swapaxes(1,2).reshape(-1, 3, 3).reshape(len(Ka)//3,len(Ka)//3, 3, 3)
    
    
    ## ----- electric-magnetic generalized polarizability         
    if 'm' in which_moments:
        K_M_E = np.sum(K2_he * j1kr[:, None, None, None], axis=0)
        K_M_E = -1j*k * f_m * K_M_E
        sim.K_M_E[wavelength] = K_M_E       # store in simulation object


    ## ----- electric-magnetic quadrupole generalized polarizability
    if 'qm' in which_moments:
        Qm = np.zeros((len(Ka)//3,3,3,3), dtype=np.complex64)
        for i_a in range(3):
            for i_b in range(3):
                Qm[:, i_a, i_b] = np.sum(
                    (
                    Dr[:,i_a,None,None] * K2_he[...,i_b,:]  + 
                    Dr[:,i_b,None,None] * K2_he[...,i_a,:] 
                      ) * j2kr[:, None, None], axis=0)
                
        K_QM_E = -1j*k * f_qm * Qm 
        sim.K_QM_E[wavelength] = K_QM_E       # store in simulation object
    
    
    if verbose: 
        print("{:.1f}ms. Done.".format((time.time()-t2)*1000))
    
# =============================================================================
#     return results
# =============================================================================
    return_list = []
    for _m in which_moments:
        if _m.lower() == "p1":
            return_list.append(K_P_E)
        if _m.lower() == "pt":
            return_list.append(K_T_E)
        if _m.lower() in ["qe"]:
            return_list.append(K_QE_E)
        if _m.lower() in ["qt"]:
            return_list.append(K_QT_E)
        if _m.lower() == "m":
            return_list.append(K_M_E)
        if _m.lower() in ["qm"]:
            return_list.append(K_QM_E)
    
    return return_list



def _test_availability_generalized_polarizability(sim, which_moment, wavelength, 
                      method='lu', verbose=False, long_wavelength_approx=False):
    which_moment = which_moment.lower()
    wl = wavelength
    
    calc_gp = False
    if which_moment in ['p1', 'p0', 'p']:
        if not hasattr(sim, 'K_P_E'):
            calc_gp = True
        elif wl not in sim.K_P_E.keys():
            calc_gp = True
            
    if which_moment in ['pt', 'p']:
        if not hasattr(sim, 'K_T_E'):
            calc_gp = True
        elif wl not in sim.K_T_E.keys():
            calc_gp = True
            
    if which_moment == 'm':
        if not hasattr(sim, 'K_M_E'):
            calc_gp = True
        elif wl not in sim.K_M_E.keys():
            calc_gp = True
            
    if which_moment in ['qe1', 'qe0', 'qe']:
        if not hasattr(sim, 'K_QE_E'):
            calc_gp = True
        elif wl not in sim.K_QE_E.keys():
            calc_gp = True
            
    if which_moment in ['qet', 'qe']:
        if not hasattr(sim, 'K_QT_E'):
            calc_gp = True
        elif wl not in sim.K_QT_E.keys():
            calc_gp = True
            
    if which_moment == 'qm':
        if not hasattr(sim, 'K_QM_E'):
            calc_gp = True
        elif wl not in sim.K_QM_E.keys():
            calc_gp = True
    
    if calc_gp:
        if verbose:
            warnings.warn('generalized polarizabilities not available. evaluating...')
        generalized_polarizability(sim, wavelength=wl, method=method, 
                                   long_wavelength_approx=long_wavelength_approx)

        
    


def density_of_multipolar_modes(sim, field_index=None, wavelength=None, return_mode_energy=True, 
                                which_moments=['p', 'm', 'qe', 'qm'], 
                                method='lu', long_wavelength_approx=False):
    """Calculate total density of multipole modes via generalized polarizability
    
    If not yet calculated, will invoke generalize pola. calculation, thus it may
    require some computation time on the first call.
    

    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    energy_density : bool, optional
        whether to return the total mode energy (True) or the accumulated 
        multipole amplitude norm (False). The default is True.
    
    wavelength : float, default: None
        Optional wavelength (alternative to `field_index`) at which to 
        calculate susceptibility matrix (in nm). 
        Either `field_index` or `wavelength` must be given.
    
    which_moments : list of str, default: ['p', 'm', 'qe', 'qm']
        which multipole moments to calculate and return. supported dipole moments: 
            - 'p': electric dipole (full)
            - 'm': magnetic dipole
            - 'qe': electric quadrupole (full)
            - 'qm': magnetic quadrupole
            - 'p1': electric dipole (first order)
            - 'pt': toroidal dipole
            - 'qe1': electric quadrupole (first order)
            - 'qet': toroidal quadrupole
    
    method : string, default: "lu"
        inversion method if generalized pola. not yet calculated. 
        One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
    
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation
    

    Returns
    -------
    out_list : list of float
        total density of modes for each demanded order (= sum of tensor norms 
        of all generalized polarizabilities for each multipole)
    
    
    Notes
    -----
    For details , see: 
        
    *PAPER SUBMITTED*

    """
    # =============================================================================
    #     Exception handling
    # =============================================================================
    if field_index is None and wavelength is None:
        raise Exception("Either `field_index` or `wavelength` must be given!")
        
    if field_index is not None and wavelength is not None:
        warnings.warn("`field_index` AND `wavelength` are given! Ignoring `wavelength`.")
        
    
    # =============================================================================
    # preparation
    # =============================================================================
    if field_index is not None:
        from pyGDM2 import tools
        wavelength = tools.get_field_indices(sim)[field_index]['wavelength']
    
    which_moments = [wm.lower() for wm in which_moments]
    for which_moment in which_moments:
        _test_availability_generalized_polarizability(sim, which_moment, 
                                                      wavelength, method=method, 
                                                      long_wavelength_approx=long_wavelength_approx)
    exp_order = 2 if return_mode_energy else 1
    
    out_list = []
    for wm in which_moments:
        if 'p' == wm:
            out_list.append((np.sum(np.linalg.norm(sim.K_P_E[wavelength], axis=(1,2))) + 
                            np.sum(np.linalg.norm(sim.K_T_E[wavelength], axis=(1,2))))**exp_order)
        if 'p1' == wm:
            out_list.append(np.sum(np.linalg.norm(sim.K_P_E[wavelength], axis=(1,2)))**exp_order)
        if 'pt' == wm:
            out_list.append(np.sum(np.linalg.norm(sim.K_T_E[wavelength], axis=(1,2)))**exp_order)
        if 'qe' == wm:
            out_list.append((np.sum(np.linalg.norm(sim.K_QE_E[wavelength], axis=(1,2))) +
                            np.sum(np.linalg.norm(sim.K_QT_E[wavelength], axis=(1,2))))**exp_order)
        if 'qe1' == wm:
            out_list.append(np.sum(np.linalg.norm(sim.K_QE_E[wavelength], axis=(1,2)))**exp_order)
        if 'qt' == wm:
            out_list.append(np.sum(np.linalg.norm(sim.K_QT_E[wavelength], axis=(1,2)))**exp_order)
        if 'm' == wm:
            out_list.append(np.sum(np.linalg.norm(sim.K_M_E[wavelength], axis=(1,2)))**exp_order)
        if 'qm' == wm:
            out_list.append(np.sum(np.linalg.norm(sim.K_QM_E[wavelength], axis=(1,2)))**exp_order)
    
    return out_list




def eval_generalized_polarizability_p(sim, field_index, which_order='p', method='lu', 
                                      long_wavelength_approx=False):
    """get electric dipole moment via generalized polarizability
    
    will evaluate generalized pola. and store it in simulation, in case it 
    is not yet calculated.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int, default: None
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`.
        Either `field_index` or `wavelength` must be given.
        
    which_order : str, optional
        The default is 'p'. One of:
            - 'p': full dipole moment including toroidal contribution
            - 'p1': only first order dipole
            - 'pt': only toroidal dipole moment
    
    method : string, default: "lu"
        inversion method if generalized pola. not yet calculated. 
        One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
        
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation


    Returns
    -------
    electric dipole moment (complex vector)

    """
    from pyGDM2 import tools
    
    kws_wl = tools.get_field_indices(sim)[field_index]
    wl = kws_wl['wavelength']
    
    for which_moment in ['p1', 'pt']:
        _test_availability_generalized_polarizability(sim, which_moment, 
              wl, method=method, long_wavelength_approx=long_wavelength_approx)
    
        
    K_P_E = sim.K_P_E[wl]
    K_T_E = sim.K_T_E[wl]
    
    ## illuminatin field for 'field_index'
    env_dict = sim.dyads.getConfigDictG(wl, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(sim.struct.geometry, env_dict, **kws_wl)
    
    if which_order.lower() in ['p', 'p0', 'p1']:  # 'p0' equiv. to 'p1'
        p1 = np.sum(np.matmul(K_P_E, E0[...,None]), axis=(0,2))
        if which_order.lower() in ['p0', 'p1']:
            p = p1
        
    if which_order.lower() in ['p', 'pt']:
        pt = np.array([np.sum(np.matmul(K_T_E[...,i,:,:], E0[:,:,None]), axis=(0,2)) for i in range(3)])
        pt = np.sum(pt, axis=1)
        if which_order.lower() == 'p':
            p = p1 + pt
        else:
            p = pt
    return p


def eval_generalized_polarizability_qe(sim, field_index, which_order='qe', method='lu', 
                                      long_wavelength_approx=False):
    """get electric quadrupole moment via generalized polarizability
    
    will evaluate generalized pola. and store it in simulation, in case it 
    is not yet calculated.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int, default: None
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`.
        Either `field_index` or `wavelength` must be given.
        
    which_order : str, optional
        The default is 'qe'. One of:
            - 'qe': full electric quadrupole moment (including toroidal contribution)
            - 'qe1': only first order contribution to quadrupole
            - 'qet': only toroidal quadrupole moment
            
    method : string, default: "lu"
        inversion method if generalized pola. not yet calculated. 
        One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
        
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation

        
    Returns
    -------
    electric quadrupole moment (complex tensor, 3x3)

    """
    from pyGDM2 import tools
    
    kws_wl = tools.get_field_indices(sim)[field_index]
    wl = kws_wl['wavelength']
    
    for which_moment in ['qe', 'qt']:
        _test_availability_generalized_polarizability(sim, which_moment, 
              wl, method=method, long_wavelength_approx=long_wavelength_approx)
    
        
    K_QE_E = sim.K_QE_E[wl]
    K_QT_E = sim.K_QT_E[wl]
    
    ## illumination field for 'field_index'
    env_dict = sim.dyads.getConfigDictG(wl, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(sim.struct.geometry, env_dict, **kws_wl)
    
    
    if which_order.lower() in ['q', 'qe', 'qe0', 'qe1']:  # 'qe0' equiv. to 'qe1'
        qe1 = np.array([
            [np.sum(np.matmul(K_QE_E[...,i,j,:,:], E0[:,:,None]), axis=(0,2)) 
                                         for j in range(3)] for i in range(3)])
        qe1 = np.sum(qe1, axis=-1)
        if which_order.lower() in ['qe0', 'qe1']:
            qe = qe1
        
    if which_order.lower() in ['q', 'qe', 'qet', 'qt']:
        qet = np.array([
            [np.sum(np.matmul(K_QT_E[...,i,j,:,:], E0[:,:,None]), axis=(0,2)) 
                                         for j in range(3)] for i in range(3)])
        qet = np.sum(qet, axis=-1)
        if which_order.lower() in ['q', 'qe']:  # 'q' equiv. to 'qe'
            qe = qe1 + qet
        else:
            qe = qet
    return qe


def eval_generalized_polarizability_m(sim, field_index, method='lu', 
                                      long_wavelength_approx=False):
    """get magnetic dipole moment via generalized polarizability
    
    will evaluate generalized pola. and store it in simulation, in case it 
    is not yet calculated.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int, default: None
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`.
        Either `field_index` or `wavelength` must be given.
            
    method : string, default: "lu"
        inversion method if generalized pola. not yet calculated. 
        One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
        
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation

        
    Returns
    -------
    magnetic quadrupole moment (complex vector)

    """
    from pyGDM2 import tools
    
    kws_wl = tools.get_field_indices(sim)[field_index]
    wl = kws_wl['wavelength']
    
    for which_moment in ['m']:
        _test_availability_generalized_polarizability(sim, which_moment, 
              wl, method=method, long_wavelength_approx=long_wavelength_approx)     
    
    K_M_E = sim.K_M_E[wl]
    
    ## illuminatin field for 'field_index'
    env_dict = sim.dyads.getConfigDictG(wl, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(sim.struct.geometry, env_dict, **kws_wl)
    
    m = np.sum(np.matmul(K_M_E, E0[...,None]), axis=(0,2))
    
    return m


def eval_generalized_polarizability_qm(sim, field_index, method='lu', 
                                      long_wavelength_approx=False):
    """get magnetic quadrupole moment via generalized polarizability
    
    will evaluate generalized pola. and store it in simulation, in case it 
    is not yet calculated.
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int, default: None
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`.
        Either `field_index` or `wavelength` must be given.
            
    method : string, default: "lu"
        inversion method if generalized pola. not yet calculated. 
        One of ["lu", "numpyinv", "scipyinv", "cupy", "cuda"]
        
    long_wavelength_approx : bool, default: False
        if True, use long wavelength approximation

        
    Returns
    -------
    magnetic quadrupole tensor (complex tensor, 3x3)

    """
    from pyGDM2 import tools
    
    kws_wl = tools.get_field_indices(sim)[field_index]
    wl = kws_wl['wavelength']
    
    for which_moment in ['qm']:
        _test_availability_generalized_polarizability(sim, which_moment, 
              wl, method=method, long_wavelength_approx=long_wavelength_approx)
    
    K_QM_E = sim.K_QM_E[wl]
    
    ## illuminatin field for 'field_index'
    env_dict = sim.dyads.getConfigDictG(wl, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(sim.struct.geometry, env_dict, **kws_wl)
    
    qm = np.array([np.sum(np.matmul(K_QM_E[...,i,:,:], E0[:,:,None]), axis=(0,2)) for i in range(3)])
    
    return qm


def extract_effective_polarizability(sim, method='lu',
                                     which_moments=['p1','m'], long_wavelength_approx=True,
                                     illumination_mode='dipole', npoints=25, r_sphere=1000):
    """Extract effective electric and magnetic dipole polarizability for structure
    
    solve inverse problem of adjusting polarizability for different illuminations
    via pseudoinverse
    
    *doc to be completed*
    
    """
    from pyGDM2 import fields
    from pyGDM2 import tools
    from scipy import linalg
    
    def sample_spherical(npoints, ndim=3):
        """random pos. on sphere (R=1). from: https://stackoverflow.com/questions/33976911"""
        vec = np.random.randn(ndim, npoints)
        vec /= np.linalg.norm(vec, axis=0)
        return vec

    ## dipoles of random position and random orientation
    wavelengths = sim.efield.wavelengths
    
    r0 = np.average(sim.struct.geometry, axis=0)
    sim.r0 = r0
    

    if illumination_mode.lower() == 'dipole':
        rnd_pos = sample_spherical(npoints, ndim=3).T * r_sphere
        field_kwargs = [
            dict(x0=rnd_pos[i,0], y0=rnd_pos[i,1], z0=rnd_pos[i,2], 
                 mx=np.random.random()*r_sphere,
                 my=np.random.random()*r_sphere,
                 mz=np.random.random()*r_sphere)
            for i in range(npoints)
            ]
        field_generator = fields.dipole_electric
    else:
    ## -- alternative: plane wave with different polarizations / incident angles
        field_kwargs = [
            dict(inc_angle=0, inc_plane='xz', E_s=0.0, E_p=1.0),
            dict(inc_angle=0, inc_plane='xz', E_s=1.0, E_p=0.0),
            dict(inc_angle=90, inc_plane='xz', E_s=1.0, E_p=0.0),
            dict(inc_angle=90, inc_plane='xz', E_s=0.0, E_p=1.0),
            dict(inc_angle=90, inc_plane='yz', E_s=1.0, E_p=0.0),
            dict(inc_angle=90, inc_plane='yz', E_s=0.0, E_p=1.0),
            ]
        field_generator = fields.plane_wave
    
    n_illum = len(field_kwargs)
    efield = fields.efield(field_generator, wavelengths=wavelengths, kwargs=copy.deepcopy(field_kwargs))
    _sim = sim.copy()
    _sim.efield = efield
    _sim.scatter(method=method)
    
    ahh = []
    aee = []
    for i_wl, wl in enumerate(wavelengths):
        p_eval = np.zeros((3, n_illum), dtype=np.complex64)
        m_eval = np.zeros((3, n_illum), dtype=np.complex64)
        E0_eval = np.zeros((3, n_illum), dtype=np.complex64)
        H0_eval = np.zeros((3, n_illum), dtype=np.complex64)
        for idx, kw  in enumerate(field_kwargs):
            ## illuminatin field for 'field_index'
            env_dict = _sim.dyads.getConfigDictG(wl, _sim.struct, _sim.efield)
            E0 = efield.field_generator([_sim.r0], env_dict, wavelength=wl, **kw)[0]
            # inc. field array shape: (3, n_fields)
            E0_eval[:, idx] = E0
            
            H0 = efield.field_generator([_sim.r0], env_dict, wavelength=wl, returnField='H', **kw)[0]
            H0_eval[:, idx] = H0
            
            kw_wl = kw.copy()
            kw_wl['wavelength'] = wl
            field_index = tools.get_closest_field_index(_sim, kw_wl)
            p, m = multipole_decomposition_exact(_sim, field_index, which_moments=which_moments, 
                                                 long_wavelength_approx=long_wavelength_approx)
            p_eval[...,idx] = p
            m_eval[...,idx] = m
        
        ## pseudo-inverse of all illuminations
        AEinv = linalg.pinv(np.conj(E0_eval).T)
        AHinv = linalg.pinv(np.conj(H0_eval).T)
        
        ## optimum alphas to obtain dipole moments for each illumination
        alpha_pinv = np.conj(np.dot(AEinv, np.conj(p_eval).T)).T
        alpha_minv = np.conj(np.dot(AHinv, np.conj(m_eval).T)).T
        
        aee.append(alpha_pinv.reshape([3,3]))
        ahh.append(alpha_minv.reshape([3,3]))
    
    dict_pola_pseudo = dict(
                sim=sim, r0=sim.r0, r0_MD=sim.r0, r0_ED=sim.r0, 
                alpha_EE=aee, 
                alpha_HH=ahh, 
                wavelengths=sim.efield.wavelengths, 
                k0_spectrum=2 * np.pi / np.array(wavelengths).copy(),
                 )
    
    return dict_pola_pseudo

