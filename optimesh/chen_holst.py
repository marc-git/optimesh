# -*- coding: utf-8 -*-
#
"""
From

Long Chen, Michael Holst,
Efficient mesh optimization schemes based on Optimal Delaunay
Triangulations,
Comput. Methods Appl. Mech. Engrg. 200 (2011) 967–984,
<https://doi.org/10.1016/j.cma.2010.11.007>.
"""
import numpy
import fastfunc

from .helpers import runner


def get_new_points_volume_averaged(mesh, reference_points):
    scaled_rp = (reference_points.T * mesh.cell_volumes).T

    weighted_rp_average = numpy.zeros(mesh.node_coords.shape)
    for i in mesh.cells["nodes"].T:
        fastfunc.add.at(weighted_rp_average, i, scaled_rp)

    omega = numpy.zeros(len(mesh.node_coords))
    for i in mesh.cells["nodes"].T:
        fastfunc.add.at(omega, i, mesh.cell_volumes)

    idx = mesh.is_interior_node
    new_points = (weighted_rp_average[idx].T / omega[idx]).T
    return new_points


def get_new_points_count_averaged(mesh, reference_points):
    # Estimate the density as 1/|tau|. This leads to some simplifcations: The
    # new point is simply the average of of the reference points
    # (barycenters/cirumcenters) in the star.
    rp_average = numpy.zeros(mesh.node_coords.shape)
    for i in mesh.cells["nodes"].T:
        fastfunc.add.at(rp_average, i, reference_points)

    omega = numpy.zeros(len(mesh.node_coords))
    for i in mesh.cells["nodes"].T:
        fastfunc.add.at(omega, i, numpy.ones(i.shape, dtype=float))

    idx = mesh.is_interior_node
    new_points = (rp_average[idx].T / omega[idx]).T
    return new_points


def odt(*args, uniform_density=False, **kwargs):
    """Optimal Delaunay Triangulation.

    Idea:
    Move interior mesh points into the weighted averages of the circumcenters
    of their adjacent cells. If a triangle cell switches orientation in the
    process, don't move quite so far.
    """
    compute_average = (
        get_new_points_volume_averaged
        if uniform_density
        else get_new_points_count_averaged
    )

    def get_new_points(mesh):
        # Get circumcenters everywhere except at cells adjacent to the boundary;
        # barycenters there.
        cc = mesh.get_cell_circumcenters()
        bc = mesh.get_cell_barycenters()
        # Find all cells with a boundary edge
        boundary_cell_ids = mesh.get_edges_cells()[1][:, 0]
        cc[boundary_cell_ids] = bc[boundary_cell_ids]
        return compute_average(mesh, cc)

    return runner(get_new_points, *args, **kwargs)


def cpt(*args, uniform_density=False, **kwargs):
    """Centroidal Patch Triangulation. Mimics the definition of Centroidal
    Voronoi Tessellations for which the generator and centroid of each Voronoi
    region coincide.

    Idea:
    Move interior mesh points into the weighted averages of the centroids
    (barycenters) of their adjacent cells. If a triangle cell switches
    orientation in the process, don't move quite so far.
    """
    compute_average = (
        get_new_points_volume_averaged
        if uniform_density
        else get_new_points_count_averaged
    )

    def get_new_points(mesh):
        return compute_average(mesh, mesh.get_cell_barycenters())

    return runner(get_new_points, *args, **kwargs)
