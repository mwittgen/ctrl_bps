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

"""Driver for preparing a WMS-specific workflow
"""

import logging

from .bps_utils import dynamically_load, save_qg_subgraph, WhenToSaveQuantumGraphs,\
    create_job_quantum_graph_filename

_LOG = logging.getLogger()


def prepare(config, generic_workflow, out_prefix):
    """Convert generic workflow to a workflow for a particular WMS.

    Parameters
    ----------
    config: `lsst.ctrl.bps.bps_config.BpsConfig`
        Contains configuration for BPS
    generic_workflow: `~lsst.ctrl.bps.generic_workflow.GenericWorkflow`
        Contains generic workflow
    out_prefix: `str`
        Contains directory to which any WMS-specific files should be written.

    Returns
    -------
    `lsst.ctrl.bps.wms_workflow`
        WMS-specific workflow
    """
    wms_service_class = dynamically_load(config["wmsServiceClass"])
    wms_service = wms_service_class(config)
    wms_workflow = wms_service.prepare(config, generic_workflow, out_prefix)

    # Save QuantumGraphs
    # (putting after call to prepare so don't write a bunch of files if prepare fails)
    found, when_to_save_job_qgraph = config.search('when_save_job_qgraph',
                                                   {'default': WhenToSaveQuantumGraphs.TRANSFORM})
    if found and when_to_save_job_qgraph == WhenToSaveQuantumGraphs.PREPARE:
        for job_name in generic_workflow.nodes():
            job = generic_workflow.get_job(job_name)
            save_qg_subgraph(job.quantum_graph, create_job_quantum_graph_filename(config, job, out_prefix))

    return wms_workflow
