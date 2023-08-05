"""

This executable will process an ongoing bilby_mcmc analyses to produce a
combined result. The executable is assumed to be run from the submit
directory (e.g., where the .ini file is) and on the submit machine.

Note: if your analysis uses HTCondor file transfer (transfer-files=True), the
resume files required for processing will not exist on the submit machine until
the job has completed. You will need to use bilby_pipe_htcondor_sync to first
sync the files to the submit machine, then run bilby_pipe_process_bilby_mcmc.

"""

import argparse
import copy
import datetime
import glob
import logging
import os
import sys

import dill
import numpy as np

import bilby
from bilby.bilby_mcmc.sampler import Bilby_MCMC
from bilby.bilby_mcmc.utils import ConvergenceInputs
from bilby.core.utils import loaded_modules_dict
from bilby.core.utils import logger as bilby_logger
from bilby_pipe.data_analysis import (
    DataAnalysisInput,
    create_analysis_parser,
    parse_args,
)
from bilby_pipe.utils import logger as bilby_pipe_logger

bilby_pipe_logger.setLevel(logging.WARNING)
bilby_logger.setLevel(logging.WARNING)

RESULT_SUBDIR = "result"


class Dummy:
    pass


class RobustUnpickler(dill.Unpickler):
    def find_class(self, module, name):
        try:
            return super().find_class(module, name)
        except AttributeError as e:
            print(f"WARNING: AttributeError raised: {e}")
            return Dummy


def glob_and_filter_files(args, globpath):
    files = glob.glob(globpath)
    if args.filter_match is not None:
        files = [f for f in files if args.filter_match in f]
    if args.filter_antimatch is not None:
        files = [f for f in files if args.filter_antimatch not in f]
    return files


def read_in_checkpoints(args, label):
    # Identify existing resume files
    path = os.path.join(args.directory, RESULT_SUBDIR, f"{label}*resume.pickle")
    resume_files = glob_and_filter_files(args, path)
    if len(resume_files) > 0:
        print(f"Reading in {len(resume_files)} checkpoint files from {path}")
    else:
        print("No checkpoint files found, exiting")
        sys.exit()

    ptsamplers = []
    for file in resume_files:
        with open(file, "rb") as f:
            ptsampler = RobustUnpickler(f).load()

        # Add the individual label
        ptsampler.label = extract_label_from_filename(file)

        if len(ptsampler.samples) > 0:
            ptsamplers.append(ptsampler)
        else:
            print(f"Resume file {file} contains no usable samples")
    return ptsamplers


def extract_label_from_filename(filename):
    filename = os.path.basename(filename)
    return filename.replace("_resume.pickle", "")


def find_data_dump_file(args):
    path = os.path.join(args.directory, "data", "*dump.pickle")
    dd_files = glob_and_filter_files(args, path)
    if len(dd_files) == 1:
        fname = dd_files[0]
        print(f"Using data dump file {fname}")
        return fname
    else:
        raise ValueError("Multiple data dump files found, aborting")


def find_config(args):
    path = os.path.join(args.directory, "*ini")
    config_files = glob.glob(path)
    if len(config_files) == 1:
        fname = config_files[0]
        print(f"Using config file {fname}")
        return fname
    else:
        raise ValueError("Multiple config files found, aborting")


def get_output_fname(
    outdir_result, ptsamplers, naming_method="datetime", extension="json"
):

    base_labels = {"_".join(pt.label.split("_")[:-1]) for pt in ptsamplers}
    if len(base_labels) > 1:
        raise ValueError("Processing error: resume files mismatch")
    else:
        base_label = list(base_labels)[0]

    if naming_method == "datetime":
        now = datetime.datetime.now().strftime("%y%m%d-%H%M")
        fname = f"{outdir_result}/{base_label}_PRELIM_result{now}.{extension}"
    elif naming_method == "final":
        fname = f"{outdir_result}/{base_label}_merge_result.{extension}"
    else:
        fname = f"{outdir_result}/{base_label}_PRELIM_resultA.{extension}"
        index = "resultA"
        while os.path.isfile(fname):
            new_index = index[:-1] + chr(ord(index[-1]) + 1)
            fname = fname.replace(index, new_index)
            index = new_index
    return fname


def update_convergence_inputs(args, ptsampler):

    # Read in convergence inputs from sampler
    inputs = dict()
    s0 = ptsampler.sampler_list[0]
    for field in ConvergenceInputs._fields:
        if hasattr(s0.chain, field):
            inputs[field] = getattr(s0.chain, field)
        elif hasattr(s0, field):
            inputs[field] = getattr(s0, field)
        elif hasattr(ptsampler, field):
            inputs[field] = getattr(ptsampler, field)
        else:
            raise ValueError(f"Unable to handle {field}")

    # Overwrite convergence inputs
    if args.thin_by_nact:
        inputs["thin_by_nact"] = args.thin_by_nact

    ci = ConvergenceInputs(**inputs)

    ptsampler.set_convergence_inputs(ci)

    return ptsampler


def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        type=str,
        help=(
            'Directory to process: this should be the "outdir" specified in '
            " the configuration file"
        ),
    )
    parser.add_argument("--npool", type=int, default=1, help="Multiprocess using npool")
    parser.add_argument(
        "--thin-by-nact",
        type=float,
        default=None,
        help="Overwrite the thin-by nact used.",
    )
    parser.add_argument(
        "--plot", action="store_true", help="Create plots for each individual sampler."
    )
    parser.add_argument(
        "--diagnostic", action="store_true", help="Create diagnostic plots."
    )
    parser.add_argument(
        "--pt-rejection-sample",
        type=bool,
        default=False,
        help="If True, use pt_rejection_sampling.",
    )
    parser.add_argument(
        "-n",
        "--naming-method",
        type=str,
        default="datetime",
        help=(
            "Naming method for output. If 'datetime', name the file by the"
            "time it was written. If 'final' name it as if it was final."
        ),
    )
    parser.add_argument(
        "--filter-match",
        type=str,
        default=None,
        help=(
            "Filter globbed files against this: anything not containing "
            "filter-match is discarded."
        ),
    )
    parser.add_argument(
        "--filter-antimatch",
        type=str,
        default=None,
        help=(
            "Filter globbed files against this: anything containing "
            "filter-antimatch is discarded."
        ),
    )

    return parser.parse_args()


def process_sampler(ptsampler, analysis, outdir, args):

    # Obtain likelihood and priors
    likelihood, search_priors = analysis.get_likelihood_and_priors()
    priors = analysis.priors

    ind_label = ptsampler.label

    result_kwargs = dict(
        label=ind_label,
        outdir=outdir,
        sampler=analysis.sampler,
        search_parameter_keys=priors.non_fixed_keys,
        fixed_parameter_keys=priors.fixed_keys,
        constraint_parameter_keys=priors.constraint_keys,
        priors=priors,
        meta_data=analysis.meta_data,
        injection_parameters=analysis.meta_data["injection_parameters"],
        sampler_kwargs=analysis.sampler_kwargs,
        use_ratio=True,
    )

    if analysis.result_class is None:
        result = bilby.gw.result.CompactBinaryCoalescenceResult(**result_kwargs)
    else:
        result = analysis.result_class(**result_kwargs)

    ptsampler = update_convergence_inputs(args, ptsampler)

    result = Bilby_MCMC.add_data_to_result(
        result=result,
        ptsampler=ptsampler,
        outdir=outdir,
        label=ind_label,
        make_plots=args.plot,
    )

    result.outdir = outdir
    prior_class = analysis.priors.__class__
    search_priors_copy = copy.deepcopy(prior_class(search_priors))
    likelihood_copy = copy.deepcopy(likelihood)
    if likelihood.jitter_time:
        result.search_parameter_keys.append("time_jitter")

    # Convert sampling time into seconds
    result.sampling_time = result.sampling_time.total_seconds()

    if ptsampler.use_ratio:
        result.log_noise_evidence = likelihood.noise_log_likelihood()
        result.log_bayes_factor = result.log_evidence
        result.log_evidence = result.log_bayes_factor + result.log_noise_evidence
    else:
        result.log_noise_evidence = likelihood.noise_log_likelihood()
        result.log_bayes_factor = result.log_evidence - result.log_noise_evidence

    conversion_function = analysis.parameter_generation
    if None not in [result.injection_parameters, conversion_function]:
        result.injection_parameters = conversion_function(result.injection_parameters)

    result.samples_to_posterior(
        likelihood=likelihood_copy,
        priors=search_priors_copy,
        conversion_function=analysis.parameter_generation,
        npool=args.npool,
    )
    result.meta_data["likelihood"] = likelihood_copy.meta_data
    result.meta_data["loaded_modules"] = loaded_modules_dict()

    result.posterior["log_likelihood"] = ptsampler.samples["logl"]
    result.posterior = result.posterior.drop(columns=["waveform_approximant"])
    result.posterior = result.posterior.astype(np.float64)

    if args.plot:
        Bilby_MCMC.plot_progress(
            ptsampler, result.label, outdir, priors, diagnostic=args.diagnostic
        )

    return result


def main():

    # Setup
    args = get_args()
    config = find_config(args)

    # Get arguments from the config
    config_args, _ = parse_args([config], create_analysis_parser())
    config_args.data_dump_file = find_data_dump_file(args)

    if config_args.sampler != "bilby_mcmc":
        raise ValueError(f"Unable to process samples for sampler {config_args.sampler}")

    # Recreate bilby_pipe analysis object
    analysis = DataAnalysisInput(config_args, [])

    # Use the outdir given at the command line, not the stored outdir
    outdir_result = os.path.join(args.directory, RESULT_SUBDIR)

    label = config_args.label

    ptsamplers = read_in_checkpoints(args, label)

    fname = get_output_fname(
        outdir_result, ptsamplers, args.naming_method, extension=analysis.result_format
    )

    results = []
    for ii, ptsampler in enumerate(ptsamplers):
        print(f"Processing sampler {ii+1}/{len(ptsamplers)}")
        result = process_sampler(ptsampler, analysis, outdir_result, args)
        results.append(result)

    combined_result = bilby.core.result.ResultList(results).combine()
    combined_result.save_to_file(fname, extension=analysis.result_format)
    print(f"Saving results with {len(combined_result.posterior)} samples to {fname}")
