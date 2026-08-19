from typing import TYPE_CHECKING

from peakrdl.plugins.exporter import ExporterSubcommandPlugin
from peakrdl.process_input import process_input, parse_parameters

from .tidy import run

if TYPE_CHECKING:
    import argparse
    from systemrdl.node import AddrmapNode

import sys
from systemrdl import RDLCompiler, warnings


class Exporter(ExporterSubcommandPlugin):
    short_desc = "Lint and validate a SystemRDL register model"
    long_desc = (
        "Runs additional validation checks on an elaborated SystemRDL "
        "model that the compiler does not catch, such as overlapping "
        "fields within a register."
    )
    generates_output_file = False

    def add_exporter_arguments(self, arg_group: "argparse._ActionsContainer") -> None:
        pass

    def main(self, importers, options):
        # Override to create the compiler with all warnings enabled,
        # which the default ExporterSubcommand.main() does not do.
        rdlc = RDLCompiler(warning_flags=warnings.ALL)

        for udp in self.udp_definitions:
            rdlc.register_udp(udp)

        parameters = parse_parameters(rdlc, options.parameters)
        process_input(rdlc, importers, options.input_files, options)
        root = rdlc.elaborate(
            top_def_name=options.top_def_name,
            inst_name=options.inst_name,
            parameters=parameters,
        )

        exit_code = run(root.top)
        if exit_code:
            sys.exit(exit_code)

    def do_export(self, top_node: "AddrmapNode", options: "argparse.Namespace") -> None:
        exit_code = run(top_node)
        if exit_code:
            sys.exit(exit_code)
