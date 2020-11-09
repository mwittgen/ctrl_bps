# This file is part of ctrl_bps.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Misc supporting classes and functions for BPS.
"""

import os
import contextlib
import logging
from enum import Enum

_LOG = logging.getLogger()


class WhenToSaveQuantumGraphs(Enum):
    """Values for when to save the job quantum graphs."""
    QGRAPH = 1   # Must be using single_quantum_clustering algorithm.
    TRANSFORM = 2
    PREPARE = 3
    SUBMIT = 4


@contextlib.contextmanager
def chdir(path):
    """A chdir function that can be used inside a context.

    Parameters
    ----------
    path : `str`
        Path to be made current working directory
    """
    cur_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cur_dir)


def create_job_quantum_graph_filename(job, out_prefix=None):
    """Create a filename to be used when storing the QuantumGraph
    for a job.

    Parameters
    ----------
    job : `~lsst.ctrl.bps.generic_workflow.GenericWorkflowJob`
        Job for which the QuantumGraph file is being saved.
    out_prefix : `str`
        Path prefix for the QuantumGraph filename.

    Returns
    -------
    full_filename : `str`
        The filename for the job's QuantumGraph.
    """
    name_parts = []
    if out_prefix is not None:
        name_parts.append(out_prefix)
    name_parts.append("inputs")
    if job.label is not None:
        name_parts.append(job.label)
    name_parts.append(f"quantum_{job.name}.pickle")
    full_filename = os.path.join("", *name_parts)
    return full_filename


def save_qg_subgraph(qgraph, out_filename):
    """Save subgraph to file.

    Parameters
    ----------
    qgraph : `~lsst.pipe.base.graph.QuantumGraph`
        QuantumGraph to save.
    out_filename : `str`
        Name of the output file.
    """
    if not os.path.exists(out_filename):
        _LOG.debug("Saving QuantumGraph with %d nodes to %s", len(qgraph), out_filename)
        if len(os.path.dirname(out_filename)) > 0:
            os.makedirs(os.path.dirname(out_filename), exist_ok=True)
        with open(out_filename, "wb") as fh:
            qgraph.save(fh)
    else:
        _LOG.debug("Skipping saving QuantumGraph to %s because already exists.", out_filename)
